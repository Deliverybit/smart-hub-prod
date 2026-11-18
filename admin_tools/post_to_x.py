"""Post one update to @TheScoop52.

Keys stay in the repo-root .env file, which git ignores. A post that includes
a link uses about $0.20 of X API credits.

    python admin_tools/post_to_x.py --send --text "TheScoop52 is live. Top 10 NYSE, NASDAQ, Crypto, LSE and TSX. https://thescoop52.com"
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import os
import sys
import time
import urllib.parse
import uuid
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
POST_URL = "https://api.x.com/2/tweets"
MEDIA_URL = "https://api.x.com/2/media/upload"
DEFAULT_LOGO = ROOT / "assets" / "scoop52_logo.png"
CENTRAL = ZoneInfo("America/Chicago")
LIVE_LINE = "TheScoop52 is live. Top 10 NYSE, NASDAQ, Crypto, LSE and TSX. https://thescoop52.com"


def morning_text(moment: datetime | None = None) -> str:
    """One daily post. The greeting uses the Central weekday of the send."""
    when = moment or datetime.now(CENTRAL)
    day = when.astimezone(CENTRAL).strftime("%A")
    return f"Happy {day}. {LIVE_LINE}"


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def require(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value or value.startswith("replace-with-"):
        print(f"Set {name} in {ENV_PATH}", file=sys.stderr)
        raise SystemExit(1)
    return value


def oauth1_header(method: str, url: str) -> str:
    """Sign with the app's user access token. Those keys do not expire."""
    consumer_key = require("X_API_KEY")
    consumer_secret = require("X_API_SECRET")
    token = require("X_ACCESS_TOKEN")
    token_secret = require("X_ACCESS_TOKEN_SECRET")
    oauth = {
        "oauth_consumer_key": consumer_key,
        "oauth_nonce": uuid.uuid4().hex,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": token,
        "oauth_version": "1.0",
    }
    encoded = "&".join(
        f"{urllib.parse.quote(key, safe='')}={urllib.parse.quote(oauth[key], safe='')}"
        for key in sorted(oauth)
    )
    base = "&".join(
        [
            method.upper(),
            urllib.parse.quote(url, safe=""),
            urllib.parse.quote(encoded, safe=""),
        ]
    )
    signing_key = "&".join(
        [
            urllib.parse.quote(consumer_secret, safe=""),
            urllib.parse.quote(token_secret, safe=""),
        ]
    )
    digest = hmac.new(signing_key.encode(), base.encode(), hashlib.sha1).digest()
    oauth["oauth_signature"] = base64.b64encode(digest).decode()
    parts = ", ".join(
        f'{urllib.parse.quote(key, safe="")}="{urllib.parse.quote(oauth[key], safe="")}"'
        for key in sorted(oauth)
    )
    return f"OAuth {parts}"


def upload_logo(path: Path) -> requests.Response:
    with path.open("rb") as image:
        return requests.post(
            MEDIA_URL,
            headers={"Authorization": oauth1_header("POST", MEDIA_URL)},
            data={"media_category": "tweet_image", "media_type": "image/png"},
            files={"media": (path.name, image, "image/png")},
            timeout=60,
        )


def post(text: str, media_id: str = "") -> requests.Response:
    body: dict = {"text": text}
    if media_id:
        body["media"] = {"media_ids": [media_id]}
    return requests.post(
        POST_URL,
        headers={
            "Authorization": oauth1_header("POST", POST_URL),
            "Content-Type": "application/json",
        },
        json=body,
        timeout=30,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Post one update as @TheScoop52.")
    parser.add_argument("--text", default="", help="Post text, up to 280 characters.")
    parser.add_argument(
        "--morning",
        action="store_true",
        help="Use the daily live post, with Happy plus today's weekday.",
    )
    parser.add_argument("--send", action="store_true", help="Publish. Without this, the text is only printed.")
    parser.add_argument("--logo", default="", help="Optional PNG to attach. Omit for a text post.")
    args = parser.parse_args()
    logo = Path(args.logo) if args.logo else None
    if logo is not None and not logo.is_file():
        print(f"Logo not found: {logo}", file=sys.stderr)
        return 1
    if args.morning:
        text = morning_text()
    else:
        text = " ".join(args.text.split())
    if not text:
        print("Post text is empty.", file=sys.stderr)
        return 1
    if len(text) > 280:
        print(f"Post is {len(text)} characters. X allows 280.", file=sys.stderr)
        return 1
    if not args.send:
        print(text)
        if logo is not None:
            print(f"Image: {logo}")
        print("Not sent. Add --send to publish.")
        return 0

    load_env(ENV_PATH)
    media_id = ""
    if logo is not None:
        uploaded = upload_logo(logo)
        if uploaded.status_code not in (200, 201, 202):
            print(uploaded.status_code, uploaded.text, file=sys.stderr)
            return 1
        media_id = str((uploaded.json().get("data") or uploaded.json()).get("id") or "")
        if not media_id:
            print(uploaded.text, file=sys.stderr)
            return 1
    response = post(text, media_id)
    if response.status_code not in (200, 201):
        print(response.status_code, response.text, file=sys.stderr)
        return 1
    post_id = (response.json().get("data") or {}).get("id", "")
    print(f"Posted {post_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
