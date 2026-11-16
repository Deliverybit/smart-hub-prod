#!/usr/bin/env python3
"""Daily polarity review for the Render cron scoop52-polarity-review.

Reads the published NYSE, NASDAQ, Crypto, LSE, and TSX boards and prints
headlines the phrase lists did not score. Those are the lines to add on
the next dictionary update. This job does not edit sentiment_engine.py.

Render cron start command:
    python admin_tools/review_headline_polarity.py

Schedule in render.yaml: 30 11 * * * (5:30 AM Central).
"""
from __future__ import annotations

import html
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sentiment_engine import headline_polarity, ruled_polarity  # noqa: E402

BOARDS = ("nyse", "nasdaq", "crypto", "lse", "tsx")
SITE = "https://thescoop52.com"
TITLE_RE = re.compile(
    r'class="hl-tip-line"[^>]*>(?:<a\b[^>]*>)?([^<]+)',
    re.IGNORECASE,
)


def board_headlines(board: str) -> list[str]:
    request = urllib.request.Request(
        f"{SITE}/{board}",
        headers={"User-Agent": "scoop52-polarity-review"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        page = response.read().decode("utf-8", errors="replace")
    titles = []
    seen = set()
    for raw in TITLE_RE.findall(page):
        title = html.unescape(raw).strip()
        if not title or title in seen:
            continue
        seen.add(title)
        titles.append(title)
    return titles


def review() -> int:
    gaps = 0
    for board in BOARDS:
        titles = board_headlines(board)
        unmatched = [title for title in titles if ruled_polarity(title) is None]
        print(f"{board.upper()}: {len(titles)} headlines, {len(unmatched)} outside the phrase lists", flush=True)
        for title in unmatched:
            gaps += 1
            print(f"  {headline_polarity(title):+.2f}  {title}", flush=True)
    print(f"Review complete. {gaps} headlines still use ordinary-English scoring.", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(review())
    except Exception as error:
        print(f"Polarity review failed: {error}", flush=True)
        raise SystemExit(1)
