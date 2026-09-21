from __future__ import annotations

from pathlib import Path


def logo_path_str() -> str:
    """
    Return the app logo path as a string for Streamlit page_icon/sidebar usage.
    """

    root = Path(__file__).resolve().parent
    # Prefer a top-level logo if present, otherwise fall back to assets.
    preferred = root / "The Scoop 52 Logo.png"
    fallback = root / "assets" / "scoop52_logo.png"
    return str(preferred if preferred.exists() else fallback)


def render_environment_banner(st_module) -> None:
    """Production clone: no environment banner."""
    return

