"""Post Scoop 52 screens with one shape and one post per market per round.

Central time:

    Weekday morning, one market, tickers in ranks 4–6
        7:00 AM   LSE
        8:00 AM   TSX
        8:30 AM   NYSE
        9:00 AM   NASDAQ
        9:30 AM   Crypto
    Weekday afternoon
        1:00 PM   LSE
        1:30 PM   TSX
        2:00 PM   NYSE
        2:30 PM   NASDAQ
        3:00 PM   Crypto
    Saturday 9:00 AM   one name from each market
    Sunday   4:00 PM   Crypto only

    python admin_tools/post_screen.py --market nyse
    python admin_tools/post_screen.py --market nyse --send
    python admin_tools/post_screen.py --market summary --send
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from html import unescape
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

from post_to_x import ENV_PATH, load_env, post

ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / ".x-posts.json"
SITE = "https://thescoop52.com"
CENTRAL = ZoneInfo("America/Chicago")
ROW = re.compile(r"<tr[\s\S]*?</tr>")
TICKER = re.compile(
    r'data-label="Ticker">(?:(?!</td>).)*<span class="fr-val">([^<]+)',
    re.S,
)
NAME = re.compile(
    r'data-label="(?:Company|Name|Commodity)">(?:(?!</td>).)*?<span class="fr-val">(.*?)</span>\s*</td>',
    re.S,
)
PCT = re.compile(
    r'data-label="% Above Low">(?:(?!</td>).)*<span class="fr-val">([^<]+)',
    re.S,
)
TIP = re.compile(r'<span class="tip-text">[\s\S]*?</span>')
TAG = re.compile(r"<[^>]+>")

MARKETS = {
    "lse": ("LSE", "lse"),
    "tsx": ("TSX", "tsx"),
    "nyse": ("NYSE", "nyse"),
    "nasdaq": ("NASDAQ", "nasdaq"),
    "crypto": ("Crypto", "crypto"),
}
WEEKDAY_MARKETS = ("lse", "tsx", "nyse", "nasdaq", "crypto")
# Weekdays are 0–4, Saturday is 5, Sunday is 6. Each slot stays open 20 minutes.
SLOTS = (
    ((0, 1, 2, 3, 4), 7, 0, "lse"),
    ((0, 1, 2, 3, 4), 8, 0, "tsx"),
    ((0, 1, 2, 3, 4), 8, 30, "nyse"),
    ((0, 1, 2, 3, 4), 9, 0, "nasdaq"),
    ((0, 1, 2, 3, 4), 9, 30, "crypto"),
    ((0, 1, 2, 3, 4), 13, 0, "lse-afternoon"),
    ((0, 1, 2, 3, 4), 13, 30, "tsx-afternoon"),
    ((0, 1, 2, 3, 4), 14, 0, "nyse-afternoon"),
    ((0, 1, 2, 3, 4), 14, 30, "nasdaq-afternoon"),
    ((0, 1, 2, 3, 4), 15, 0, "crypto-afternoon"),
    ((6,), 16, 0, "crypto"),
    ((5,), 9, 0, "summary"),
)


def plain_name(html: str) -> str:
    text = TAG.sub("", TIP.sub("", html))
    return unescape(re.sub(r"\s+", " ", text)).strip()


def fetch_rows(slug: str) -> list[tuple[str, str, float]]:
    response = requests.get(
        f"{SITE}/{slug}",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=40,
    )
    response.raise_for_status()
    rows = []
    for row in ROW.findall(response.text):
        ticker = TICKER.search(row)
        name = NAME.search(row)
        pct = PCT.search(row)
        if not ticker or not name or not pct:
            continue
        number = pct.group(1).replace("%", "").replace(",", "").strip()
        rows.append((plain_name(name.group(1)), unescape(ticker.group(1)).strip(), float(number)))
    return rows


def stamp(moment: datetime) -> str:
    return moment.astimezone(CENTRAL).strftime("%A, %b %-d").replace("%-d", "")


def dated(moment: datetime) -> str:
    local = moment.astimezone(CENTRAL)
    return f"{local.strftime('%A')}, {local.strftime('%b')} {local.day}"


def three_names(slug: str, label: str) -> list[tuple[str, str]]:
    rows = fetch_rows(slug)
    if len(rows) < 3:
        raise RuntimeError(f"{label} did not return three names.")
    return [(name, ticker) for name, ticker, _pct in rows[:3]]


def closest_name(slug: str, label: str) -> str:
    rows = fetch_rows(slug)
    if not rows:
        raise RuntimeError(f"{label} did not return a name.")
    return min(rows, key=lambda item: item[2])[1]


def market_name(key: str) -> str:
    return key.removesuffix("-afternoon")


def rank_tickers(slug: str, label: str, start: int, count: int) -> list[str]:
    rows = fetch_rows(slug)
    end = start + count - 1
    if len(rows) < end:
        raise RuntimeError(f"{label} did not return rank {end}.")
    return [ticker for _name, ticker, _pct in rows[start - 1 : end]]


def morning_post(key: str) -> str:
    """One morning post: ranks 4–6, tickers only, for a single market."""
    label, slug = MARKETS[key]
    tickers = ", ".join(rank_tickers(slug, label, 4, 3))
    return f"{label} {tickers}\n\nSee the Top 3 at The Scoop 52"


def market_post(key: str, moment: datetime) -> str:
    label, slug = MARKETS[market_name(key)]
    names = ", ".join(
        f"({rank}) {name} ({ticker})"
        for rank, (name, ticker) in enumerate(three_names(slug, label), start=1)
    )
    when = "afternoon " if key.endswith("-afternoon") else ""
    return (
        f"{dated(moment)} {when}{label} near 52-week lows\n"
        f"{names}\n"
        f"See the full {label} list at The Scoop 52\n"
        f"{SITE}/{slug}"
    )


def summary_post(moment: datetime) -> str:
    parts = []
    for key in ("nyse", "nasdaq", "crypto", "lse", "tsx"):
        label, slug = MARKETS[key]
        parts.append(f"{label} {closest_name(slug, label)}")
    return f"{dated(moment)} closest to the lows\n{' · '.join(parts)}\n{SITE}"


def allowed(key: str, moment: datetime) -> str:
    weekday = moment.astimezone(CENTRAL).weekday()
    if key.endswith("-afternoon"):
        if weekday > 4:
            return "Afternoon posts are weekdays only."
        key = market_name(key)
    if weekday == 5:
        if key != "summary":
            return "Saturday only sends the summary."
        return ""
    if weekday == 6:
        if key != "crypto":
            return "Sunday only sends Crypto."
        return ""
    if key == "summary":
        return "The summary is Saturday only."
    if key not in MARKETS:
        return "Unknown market."
    return ""


def already_sent(day: str, key: str) -> bool:
    if not LOG_PATH.exists():
        return False
    log = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    return key in log.get(day, [])


def remember(day: str, key: str) -> None:
    log = {}
    if LOG_PATH.exists():
        log = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    log.setdefault(day, [])
    if key not in log[day]:
        log[day].append(key)
    LOG_PATH.write_text(json.dumps(log), encoding="utf-8")


def due_key(moment: datetime) -> str:
    local = moment.astimezone(CENTRAL)
    now = local.hour * 60 + local.minute
    day = local.date().isoformat()
    for days, hour, minute, key in SLOTS:
        start = hour * 60 + minute
        if local.weekday() in days and start <= now < start + 20 and not already_sent(day, key):
            return key
    return ""


def publish(text: str) -> str:
    load_env(ENV_PATH)
    response = post(text)
    if response.status_code not in (200, 201):
        detail = response.text.lower()
        if response.status_code == 403 and "duplicate" in detail:
            print("X rejected this as a duplicate. It was not sent again.", file=sys.stderr)
        else:
            print(response.status_code, response.text, file=sys.stderr)
        raise SystemExit(1)
    return str((response.json().get("data") or {}).get("id", ""))


def main() -> int:
    parser = argparse.ArgumentParser(description="Post one Scoop 52 screen.")
    parser.add_argument(
        "--market",
        choices=(*WEEKDAY_MARKETS, "summary"),
        help="Market to post, or summary for Saturday.",
    )
    parser.add_argument("--send", action="store_true", help="Publish. Without this, the text is only printed.")
    parser.add_argument("--due", action="store_true", help="Post the market scheduled for this time, if one is due.")
    parser.add_argument(
        "--morning",
        action="store_true",
        help="Post ranks 4–6 for one market. This is the morning cron.",
    )
    args = parser.parse_args()
    moment = datetime.now(CENTRAL)
    if args.morning:
        if args.market not in MARKETS:
            print("Name one market with --market.", file=sys.stderr)
            return 1
        text = morning_post(args.market)
        if len(text) > 280:
            print(f"Post is {len(text)} characters. X allows 280.", file=sys.stderr)
            return 1
        if not args.send:
            print(text)
            print("Not sent. Add --send to publish.")
            return 0
        post_id = publish(text)
        print(f"Posted {post_id}")
        return 0
    if args.due:
        args.market = due_key(moment)
        if not args.market:
            print("Nothing is due.")
            return 0
    day = moment.astimezone(CENTRAL).date().isoformat()
    keys = (args.market,) if args.market else (("summary",) if moment.weekday() == 5 else ("crypto",) if moment.weekday() == 6 else WEEKDAY_MARKETS)
    if args.send and not args.market:
        print("Name one market with --market.", file=sys.stderr)
        return 1

    texts = []
    for key in keys:
        reason = allowed(key, moment)
        if reason:
            print(reason, file=sys.stderr)
            return 1
        if already_sent(day, key):
            print(f"{key} was already posted today.", file=sys.stderr)
            return 1
        texts.append(summary_post(moment) if key == "summary" else market_post(key, moment))

    text = "\n\n".join(texts)
    if not args.send:
        print(text)
        print("Not sent. Add --send and --market to publish one.")
        return 0

    post_id = publish(texts[0])
    remember(day, args.market)
    print(f"Posted {post_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
