"""Post one update to @TheScoop52.

Keys stay in the repo-root .env file, which git ignores. A post that includes
a link uses about $0.20 of X API credits.

    python admin_tools/post_to_x.py --send --text "TheScoop52 is live. Top 10 NYSE, NASDAQ, Crypto, LSE and TSX. https://thescoop52.com"
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
POST_URL = "https://api.x.com/2/tweets"
MEDIA_URL = "https://api.x.com/2/media/upload"
REFRESH_URL = "https://api.x.com/2/oauth2/token"
DEFAULT_LOGO = ROOT / "assets" / "scoop52_logo.png"


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


def refresh_access_token() -> str:
    client_id = require("X_CLIENT_ID")
    client_secret = require("X_CLIENT_SECRET")
    refresh_token = require("X_REFRESH_TOKEN")
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    response = requests.post(
        REFRESH_URL,
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "refresh_token", "refresh_token": refresh_token},
        timeout=30,
    )
    if response.status_code != 200:
        print(response.status_code, response.text, file=sys.stderr)
        raise SystemExit(1)
    payload = response.json()
    token = str(payload.get("access_token") or "")
    if not token:
        print("Refresh succeeded but no access token was returned.", file=sys.stderr)
        raise SystemExit(1)
    print("Access token was refreshed. Save the new access token in .env.", file=sys.stderr)
    rotated = payload.get("refresh_token")
    if rotated:
        print("A new refresh token was issued. Save that in .env too.", file=sys.stderr)
    return token


def upload_logo(path: Path, token: str) -> requests.Response:
    with path.open("rb") as image:
        return requests.post(
            MEDIA_URL,
            headers={"Authorization": f"Bearer {token}"},
            data={"media_category": "tweet_image", "media_type": "image/png"},
            files={"media": (path.name, image, "image/png")},
            timeout=60,
        )


def post(text: str, token: str, media_id: str = "") -> requests.Response:
    body: dict = {"text": text}
    if media_id:
        body["media"] = {"media_ids": [media_id]}
    return requests.post(
        POST_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=body,
        timeout=30,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Post one update as @TheScoop52.")
    parser.add_argument("--text", required=True, help="Post text, up to 280 characters.")
    parser.add_argument("--send", action="store_true", help="Publish. Without this, the text is only printed.")
    parser.add_argument("--logo", default="", help="Optional PNG to attach. Omit for a text post.")
    args = parser.parse_args()
    logo = Path(args.logo) if args.logo else None
    if logo is not None and not logo.is_file():
        print(f"Logo not found: {logo}", file=sys.stderr)
        return 1
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
    token = require("X_ACCESS_TOKEN")
    media_id = ""
    if logo is not None:
        uploaded = upload_logo(logo, token)
        if uploaded.status_code == 401 and os.environ.get("X_REFRESH_TOKEN"):
            token = refresh_access_token()
            uploaded = upload_logo(logo, token)
        if uploaded.status_code not in (200, 201, 202):
            print(uploaded.status_code, uploaded.text, file=sys.stderr)
            return 1
        media_id = str((uploaded.json().get("data") or uploaded.json()).get("id") or "")
        if not media_id:
            print(uploaded.text, file=sys.stderr)
            return 1
    response = post(text, token, media_id)
    if response.status_code == 401 and os.environ.get("X_REFRESH_TOKEN"):
        token = refresh_access_token()
        response = post(text, token, media_id)
    if response.status_code not in (200, 201):
        print(response.status_code, response.text, file=sys.stderr)
        return 1
    post_id = (response.json().get("data") or {}).get("id", "")
    print(f"Posted {post_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
