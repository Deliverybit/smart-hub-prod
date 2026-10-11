"""Ticker → display name lookup from screener page constants."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"


@dataclass(frozen=True)
class _NameSource:
    page_name: str
    deps: tuple[str, ...]
    names_key: str
    kind: str


_NAME_SOURCES: tuple[_NameSource, ...] = (
    _NameSource("1_NYSE_Top_10.py", ("COMPANY_NAMES",), "COMPANY_NAMES", "stock"),
    _NameSource("2_NASDAQ_Top_10.py", ("COMPANY_NAMES",), "COMPANY_NAMES", "stock"),
    _NameSource("3_Crypto_Top_10.py", ("CRYPTO_DATA",), "CRYPTO_NAMES", "crypto"),
    _NameSource("5_CME_Top_10.py", ("COMMODITY_NAMES",), "COMMODITY_NAMES", "commodity"),
    _NameSource("6_ICE_Top_10.py", ("COMMODITY_NAMES",), "COMMODITY_NAMES", "commodity"),
)


def _literal_assignments(path: Path) -> dict[str, object]:
    module = ast.parse(path.read_text(encoding="utf-8"))
    values: dict[str, object] = {}
    for node in module.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        try:
            values[target.id] = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            continue
    return values


def _load_names_env(source: _NameSource) -> dict[str, object]:
    path = PAGES / source.page_name
    env = _literal_assignments(path)
    missing = [name for name in source.deps if name not in env]
    if missing:
        raise RuntimeError(f"{path.name} missing constants: {', '.join(missing)}")

    if source.kind == "crypto" and "CRYPTO_DATA" in env:
        crypto_data = env["CRYPTO_DATA"]
        if isinstance(crypto_data, dict):
            env.setdefault(
                "CRYPTO_NAMES",
                {key: value[0] for key, value in crypto_data.items()},
            )
    return env


@lru_cache(maxsize=1)
def asset_name_lookup() -> dict[str, str]:
    """Map tickers (and common variants) to display names from all screener pages."""
    lookup: dict[str, str] = {}
    for source in _NAME_SOURCES:
        env = _load_names_env(source)
        names = env.get(source.names_key)
        if not isinstance(names, dict):
            continue
        for key, label in names.items():
            key_u = str(key).strip().upper()
            label_s = str(label).strip()
            if not key_u or not label_s:
                continue
            lookup[key_u] = label_s
            if source.kind == "crypto":
                lookup[key_u.replace("-USD", "")] = label_s
            elif source.kind == "commodity":
                lookup[key_u.replace("=F", "")] = label_s
    return lookup


def resolve_asset_display_name(ticker: str) -> str:
    """Return company/crypto/commodity name for a ticker, or the ticker if unknown."""
    normalized = (ticker or "").strip().upper()
    if not normalized:
        return ""
    lookup = asset_name_lookup()
    if normalized in lookup:
        return lookup[normalized]
    if normalized.endswith("-USD"):
        base = normalized[:-4]
        if base in lookup:
            return lookup[base]
    if not normalized.endswith("=F"):
        alt = f"{normalized}=F"
        if alt in lookup:
            return lookup[alt]
    return normalized


_SUMMARY_SOURCES: tuple[_NameSource, ...] = (
    _NameSource("1_NYSE_Top_10.py", ("COMPANY_SUMMARIES",), "COMPANY_SUMMARIES", "stock"),
    _NameSource("2_NASDAQ_Top_10.py", ("COMPANY_SUMMARIES",), "COMPANY_SUMMARIES", "stock"),
    _NameSource("3_Crypto_Top_10.py", ("CRYPTO_SUMMARIES",), "CRYPTO_SUMMARIES", "crypto"),
    _NameSource("5_CME_Top_10.py", ("COMMODITY_SUMMARIES",), "COMMODITY_SUMMARIES", "commodity"),
    _NameSource("6_ICE_Top_10.py", ("COMMODITY_SUMMARIES",), "COMMODITY_SUMMARIES", "commodity"),
)


@lru_cache(maxsize=1)
def asset_summary_lookup() -> dict[str, str]:
    """Map tickers to the same one-line descriptions shown on the saved pages."""
    lookup: dict[str, str] = {}
    for source in _SUMMARY_SOURCES:
        env = _load_names_env(source)
        summaries = env.get(source.names_key)
        if not isinstance(summaries, dict):
            continue
        for key, text in summaries.items():
            key_u = str(key).strip().upper()
            text_s = str(text).strip()
            if not key_u or not text_s:
                continue
            lookup[key_u] = text_s
            if source.kind == "crypto":
                lookup[f"{key_u}-USD"] = text_s
            elif source.kind == "commodity":
                lookup[f"{key_u}=F"] = text_s
    return lookup


def resolve_asset_summary(ticker: str) -> str:
    """Return the saved-page description for a ticker, or blank if unknown."""
    normalized = (ticker or "").strip().upper()
    if not normalized:
        return ""
    lookup = asset_summary_lookup()
    if normalized in lookup:
        return lookup[normalized]
    if normalized.endswith("-USD"):
        base = normalized[:-4]
        if base in lookup:
            return lookup[base]
    if normalized.endswith("=F"):
        base = normalized[:-2]
        if base in lookup:
            return lookup[base]
    if not normalized.endswith("=F"):
        alt = f"{normalized}=F"
        if alt in lookup:
            return lookup[alt]
    return ""
