"""Post Scoop 52 screens with one shape and one post per market per day.

Central time:

    Weekdays
        7:00 AM   LSE
        8:00 AM   TSX
        8:30 AM  NYSE
        9:00 AM   NASDAQ
        4:00 PM  Crypto
    Saturday 9:00 AM   one name from each market
    Sunday   4:00 PM   Crypto only

    Catch-up, only when that post was not sent:
        Weekdays 10:00 LSE, 10:20 TSX, 10:40 NYSE, 11:00 NASDAQ
        Saturday 10:00 summary

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
PCT = re.compile(
    r'data-label="% Above Low">(?:(?!</td>).)*<span class="fr-val">([^<]+)',
    re.S,
)

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
    ((0, 1, 2, 3, 4, 6), 16, 0, "crypto"),
    ((5,), 9, 0, "summary"),
)
# Second chance for a morning post the first window missed. Each slot stays open 20 minutes.
CATCHUP = (
    ((0, 1, 2, 3, 4), 10, 0, "lse"),
    ((0, 1, 2, 3, 4), 10, 20, "tsx"),
    ((0, 1, 2, 3, 4), 10, 40, "nyse"),
    ((0, 1, 2, 3, 4), 11, 0, "nasdaq"),
    ((5,), 10, 0, "summary"),
)


def fetch_rows(slug: str) -> list[tuple[str, float]]:
    response = requests.get(
        f"{SITE}/{slug}",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=40,
    )
    response.raise_for_status()
    rows = []
    for row in ROW.findall(response.text):
        ticker = TICKER.search(row)
        pct = PCT.search(row)
        if not ticker or not pct:
            continue
        number = pct.group(1).replace("%", "").replace(",", "").strip()
        rows.append((unescape(ticker.group(1)).strip(), float(number)))
    return rows


def stamp(moment: datetime) -> str:
    return moment.astimezone(CENTRAL).strftime("%A, %b %-d").replace("%-d", "")


def dated(moment: datetime) -> str:
    local = moment.astimezone(CENTRAL)
    return f"{local.strftime('%A')}, {local.strftime('%b')} {local.day}"


def three_names(slug: str, label: str) -> list[str]:
    rows = fetch_rows(slug)
    if len(rows) < 6:
        raise RuntimeError(f"{label} did not return six names.")
    return [ticker for ticker, _pct in rows[3:6]]


def closest_name(slug: str, label: str) -> str:
    rows = fetch_rows(slug)
    if not rows:
        raise RuntimeError(f"{label} did not return a name.")
    return min(rows, key=lambda item: item[1])[0]


def market_post(key: str, moment: datetime) -> str:
    label, slug = MARKETS[key]
    names = ", ".join(
        f"({rank}) {ticker}" for rank, ticker in enumerate(three_names(slug, label), start=4)
    )
    return (
        f"{dated(moment)} {label} near 52-week lows\n"
        f"{names}\n"
        f"See the top 3 {label} at The Scoop 52\n"
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
    for days, hour, minute, key in (*SLOTS, *CATCHUP):
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
    args = parser.parse_args()
    moment = datetime.now(CENTRAL)
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
