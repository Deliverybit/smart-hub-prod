"""Shared proximity selection for Top 10 screeners."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

INTERNAL_THRESHOLD_PCT = 15
MAX_PAD_CAP_PCT = 30
TARGET_COUNT = 10

MARKET_MOOD_TIP = (
    "Proximity to the 52-week low: BELOW LOW = trading under the recorded low, "
    "AT LOW = within 2%, NEAR LOW = above 2% and within 30% of the 52-week low."
)


@dataclass(frozen=True)
class ProximitySelection:
    results: list[dict[str, Any]]
    mode: str
    strict_count: int
    padded_count: int
    eligible_count: int


def select_proximity_results(
    all_results: list[dict[str, Any]],
    *,
    target: int = TARGET_COUNT,
    internal_threshold: float = INTERNAL_THRESHOLD_PCT,
    max_pad_cap: float = MAX_PAD_CAP_PCT,
) -> ProximitySelection:
    """Select up to ``target`` rows using 15% strict / 30% cap proximity rules."""
    if not all_results:
        return ProximitySelection([], "empty", 0, 0, 0)

    def pct(row: dict[str, Any]) -> float:
        return float(row["% Above Low"])

    eligible = [row for row in all_results if pct(row) <= max_pad_cap]
    strict = sorted(
        [row for row in eligible if pct(row) <= internal_threshold],
        key=pct,
    )

    if len(strict) >= target:
        final = strict[:target]
        return ProximitySelection(
            final,
            "all_strict",
            len(final),
            0,
            len(eligible),
        )

    if strict:
        strict_tickers = {row["Ticker"] for row in strict}
        padded_pool = sorted(
            [row for row in eligible if row["Ticker"] not in strict_tickers],
            key=pct,
        )
        need = target - len(strict)
        padded = padded_pool[:need]
        final = strict + padded
        return ProximitySelection(
            final,
            "padded",
            len(strict),
            len(padded),
            len(eligible),
        )

    if eligible:
        final = sorted(eligible, key=pct)[:target]
        return ProximitySelection(
            final,
            "closest_only",
            0,
            len(final),
            len(eligible),
        )

    return ProximitySelection([], "empty", 0, 0, 0)


def selection_status_message(
    selection: ProximitySelection,
    *,
    asset_noun: str,
    scanned_count: int,
    universe_size: int,
) -> tuple[str, str]:
    """Return a Streamlit status helper name and markdown message."""
    count = len(selection.results)
    shortfall = ""
    if count < TARGET_COUNT:
        shortfall = f" (only **{count}** within **{MAX_PAD_CAP_PCT}%** right now)"

    if selection.mode == "all_strict":
        return (
            "success",
            f"Found **{count}** candidates{shortfall} from {scanned_count} of "
            f"{universe_size} {asset_noun} scanned.",
        )

    if selection.mode == "padded":
        return (
            "info",
            f"**{selection.strict_count}** {asset_noun} within "
            f"**{INTERNAL_THRESHOLD_PCT}%** of their 52-week low; "
            f"**{selection.padded_count}** additional closest names shown "
            f"(up to **{MAX_PAD_CAP_PCT}%**).{shortfall}",
        )

    if selection.mode == "closest_only":
        return (
            "info",
            f"No {asset_noun} within **{INTERNAL_THRESHOLD_PCT}%** of their 52-week low; "
            f"showing the **{count}** closest available (within "
            f"**{MAX_PAD_CAP_PCT}%**).{shortfall}",
        )

    return (
        "warning",
        f"No {asset_noun} within **{MAX_PAD_CAP_PCT}%** of their 52-week low right now.",
    )


def proximity_how_it_works(asset_label: str = "asset") -> str:
    """Standard info-box copy for proximity screeners."""
    return (
        f"**How it works:** Each {asset_label} is checked for proximity to its 52-week low, "
        f"ranked by closeness, and filtered to within **{MAX_PAD_CAP_PCT}%** of the low. "
        f"Names within **{INTERNAL_THRESHOLD_PCT}%** are preferred; if fewer than 10 qualify, "
        f"the closest names up to **{MAX_PAD_CAP_PCT}%** fill the table."
    )


_SENTIMENT_KEYWORD_PHRASES = {
    "stock": "scandal, bankruptcy, fraud, lawsuits, and delisting",
    "crypto": "scandal, bankruptcy, fraud, scams, rug-pulls, and hacks",
    "commodity": "scandal, bankruptcy, manipulation, sanctions, and contamination",
}


def sentiment_negative_keyword_notice(profile: str = "stock") -> str:
    """Disclosure shown on market screeners: negative headline keywords are filtered out."""
    keywords = _SENTIMENT_KEYWORD_PHRASES.get(profile, _SENTIMENT_KEYWORD_PHRASES["stock"])
    return (
        "**Sentiment screening:** Headline sentiment scans recent news for negative keywords "
        f"(including {keywords}). Names whose headlines match scandal, bankruptcy, or related "
        "red-flag terms are **not** included in the Top 10 results."
    )


def proximity_how_it_works_compact(asset_label: str = "asset") -> str:
    """Short mobile/tablet copy for proximity screener info."""
    return (
        f"**How it works:** Ranks {asset_label}s nearest the 52-week low; "
        f"shows up to 10 within **{MAX_PAD_CAP_PCT}%** of the low."
    )


def sentiment_negative_keyword_notice_compact(profile: str = "stock") -> str:
    """Short mobile/tablet sentiment disclosure (profile kept for API parity)."""
    _ = profile
    return (
        "**Sentiment:** Excludes names with scandal, bankruptcy, or similar red-flag headlines."
    )


def _landing_markdown_html(text: str) -> str:
    """Convert **bold** markers to HTML for landing intro blocks."""
    import html
    import re

    parts: list[str] = []
    last = 0
    for match in re.finditer(r"\*\*(.+?)\*\*", text):
        if match.start() > last:
            parts.append(html.escape(text[last : match.start()]))
        parts.append(f"<strong>{html.escape(match.group(1))}</strong>")
        last = match.end()
    if last < len(text):
        parts.append(html.escape(text[last:]))
    return "".join(parts)


_SCREENER_LANDING_SUMMARY_FULL: dict[str, str] = {
    "NYSE": (
        "Screens a curated watchlist of **{n}** well-known U.S. stocks—mostly "
        "financials, healthcare, industrials, energy, and consumer names—for those trading "
        "**at or near their 52-week low** using Alpha Vantage daily market data. "
        "This is a selected sample, not the Dow Jones Industrial Average, not every NYSE listing, "
        "and not a large-cap or official exchange universe. "
        "Headline sentiment is fetched for the final displayed rows."
    ),
    "NASDAQ": (
        "Screens a curated watchlist of **{n}** well-known U.S. stocks—mostly "
        "technology, consumer, biotech, and growth names—for those trading **at or near "
        "their 52-week low** using Alpha Vantage daily market data. "
        "This is a selected sample, not the Nasdaq-100, not every Nasdaq listing, "
        "and not a large-cap or official exchange universe. "
        "Headline sentiment is fetched for the final displayed rows."
    ),
    "CRYPTO": (
        "Screens a curated watchlist of **{n}** well-known cryptocurrencies "
        "for those trading **closest to their 52-week low**. "
        "This is a selected sample, not every listed coin and not an official "
        "exchange or market-cap ranking. "
        "Proximity uses a batched market quote (last price and 52-week range); "
        "Alpha Vantage remains available on Analyze. "
        "Many names trade on large venues (Coinbase, Binance, Kraken, KuCoin, Gemini), "
        "but listing coverage varies. "
        "Headline sentiment is fetched for the final displayed rows."
    ),
    "CME": (
        "Screens a curated watchlist of **{n}** well-known CME Group futures "
        "(CME, CBOT, NYMEX, COMEX) for those trading **closest to their 52-week low**. "
        "This is a selected sample, not every listed contract and not an official "
        "CME product universe. "
        "Proximity uses a batched market quote (last price and 52-week range); "
        "Alpha Vantage and ETF proxies remain available on Analyze. "
        "Headline sentiment is fetched for the final displayed rows."
    ),
    "ICE": (
        "Screens a curated watchlist of **{n}** well-known ICE-linked commodity "
        "futures and commodity ETFs for those trading **closest to their 52-week low**. "
        "This is a selected sample, not every ICE listing and not an official "
        "exchange or index universe. "
        "Proximity uses a batched market quote (last price and 52-week range); "
        "Alpha Vantage remains available on Analyze. "
        "Headline sentiment is fetched for the final displayed rows."
    ),
}

_SCREENER_LANDING_SUMMARY_COMPACT: dict[str, str] = {
    "NYSE": "**{n}** curated well-known stocks near **52-week lows** (selected sample, not an official NYSE universe). Headline sentiment on shown rows.",
    "NASDAQ": "**{n}** curated well-known stocks near **52-week lows** (selected sample, not an official Nasdaq universe). Headline sentiment on shown rows.",
    "CRYPTO": "**{n}** well-known cryptocurrencies near **52-week lows** (selected sample, not an official market universe). Headline sentiment on shown rows.",
    "CME": "**{n}** well-known CME Group futures near **52-week lows** (selected sample, not an official CME universe). Tap **Analyze** for deeper sentiment.",
    "ICE": "**{n}** well-known ICE-linked futures and commodity ETFs near **52-week lows** (selected sample, not an official ICE universe). Tap **Analyze** for deeper sentiment.",
}

_SCREENER_LANDING_INTRO_CSS = """
<style id="scoop-landing-intro-css">
    .scoop-landing-full { display: none; }
    .scoop-landing-compact { display: block; }
    .scoop-landing-gate-note { display: none; }
    .scoop-landing-summary,
    .scoop-landing-sentiment {
        margin: 0 0 0.65rem 0;
        line-height: 1.55;
    }
    .scoop-landing-info {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 0.5rem;
        padding: 0.85rem 1rem;
        margin: 0 0 0.65rem 0;
        line-height: 1.55;
    }
    html[data-scoop-theme="dark"] .scoop-landing-info {
        background: rgba(30, 58, 138, 0.22);
        border-color: #1e40af;
        color: #e2e8f0;
    }
    .scoop-landing-divider {
        border: none;
        border-top: 1px solid rgba(49, 51, 63, 0.2);
        margin: 0.65rem 0;
    }
    html[data-scoop-theme="dark"] .scoop-landing-divider {
        border-top-color: rgba(148, 163, 184, 0.35);
    }
    @media (max-width: 1366px) {
        .scoop-landing-full { display: none !important; }
        .scoop-landing-compact { display: block !important; }
        .scoop-landing-summary,
        .scoop-landing-sentiment {
            margin-bottom: 0.8rem;
            line-height: 1.5;
        }
        .scoop-landing-info {
            padding: 0.75rem 0.85rem;
            margin-bottom: 0.8rem;
            line-height: 1.5;
        }
        .scoop-landing-divider {
            margin: 0.6rem 0;
        }
        .scoop-landing-compact:last-of-type .scoop-landing-sentiment {
            margin-bottom: 1rem;
        }
        html:not([data-scoop-screener-gated="1"]) .scoop-landing-info,
        html:not([data-scoop-screener-gated="1"]) .scoop-landing-sentiment,
        html:not([data-scoop-screener-gated="1"]) .scoop-landing-divider {
            display: none !important;
        }
        html[data-scoop-screener-gated="1"] .scoop-landing-gate-note {
            display: block !important;
            margin: 0 0 0.55rem 0;
            padding: 0.55rem 0.7rem;
            line-height: 1.4;
            border-radius: 0.5rem;
        }
        .scoop-screener-last-updated {
            margin-top: 0.35rem !important;
            margin-bottom: 0.85rem !important;
        }
        html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stAlert"] {
            margin-top: 0.35rem !important;
            margin-bottom: 0.85rem !important;
        }
    }
    @media (min-width: 1367px) {
        .scoop-landing-gate-note { display: none !important; }
        .scoop-landing-summary,
        .scoop-landing-sentiment {
            margin-bottom: 0.9rem;
        }
        .scoop-landing-info {
            padding: 0.9rem 1.05rem;
            margin-bottom: 0.9rem;
        }
        .scoop-landing-divider {
            margin: 0.85rem 0;
        }
        .scoop-landing-compact:last-of-type .scoop-landing-sentiment {
            margin-bottom: 1.1rem;
        }
        .scoop-screener-last-updated {
            margin-top: 0.4rem !important;
            margin-bottom: 0.9rem !important;
        }
        html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stAlert"] {
            margin-top: 0.4rem !important;
            margin-bottom: 0.9rem !important;
        }
        html:not([data-scoop-screener-gated="1"]) .scoop-landing-compact .scoop-landing-info,
        html:not([data-scoop-screener-gated="1"]) .scoop-landing-compact .scoop-landing-sentiment,
        html:not([data-scoop-screener-gated="1"]) .scoop-landing-divider {
            display: block !important;
        }
    }
    .scoop-screener-last-updated {
        text-align: right;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    html[data-scoop-theme="dark"] .scoop-screener-last-updated {
        color: #94a3b8;
    }
</style>
"""


def screener_landing_summary(market: str, universe_size: int, *, compact: bool = False) -> str:
    """Return summary copy for a market screener landing page."""
    templates = _SCREENER_LANDING_SUMMARY_COMPACT if compact else _SCREENER_LANDING_SUMMARY_FULL
    template = templates.get(market)
    if template is None:
        raise ValueError(f"Unknown screener market: {market}")
    return template.format(n=universe_size)


def render_screener_landing_intro(
    st_module,
    *,
    market: str,
    universe_size: int,
    asset_label: str,
    sentiment_profile: str,
    crypto_affiliate_caption: bool = False,
) -> None:
    """Render desktop + mobile/tablet landing copy before the terms gate."""
    summary_full = screener_landing_summary(market, universe_size, compact=False)
    summary_compact = screener_landing_summary(market, universe_size, compact=True)
    how_full = proximity_how_it_works(asset_label)
    how_compact = proximity_how_it_works_compact(asset_label)
    sentiment_full = sentiment_negative_keyword_notice(sentiment_profile)
    sentiment_compact = sentiment_negative_keyword_notice_compact(sentiment_profile)

    affiliate_block = ""
    if crypto_affiliate_caption:
        affiliate_block = (
            '<p class="scoop-landing-affiliate scoop-landing-full">'
            "Some exchange links may be affiliate links. "
            'See our <a href="/Terms_of_Service" target="_self">Terms of Service</a> for details.'
            "</p>"
        )

    st_module.markdown(
        _SCREENER_LANDING_INTRO_CSS
        + f'<div class="scoop-landing-full"><p class="scoop-landing-summary">{_landing_markdown_html(summary_full)}</p></div>'
        + f'<div class="scoop-landing-compact"><p class="scoop-landing-summary">{_landing_markdown_html(summary_compact)}</p></div>'
        + affiliate_block
        + '<hr class="scoop-landing-divider" />'
        + f'<div class="scoop-landing-full"><div class="scoop-landing-info">{_landing_markdown_html(how_full)}</div></div>'
        + f'<div class="scoop-landing-compact"><div class="scoop-landing-info">{_landing_markdown_html(how_compact)}</div></div>'
        + f'<div class="scoop-landing-full"><p class="scoop-landing-sentiment">{_landing_markdown_html(sentiment_full)}</p></div>'
        + f'<div class="scoop-landing-compact"><p class="scoop-landing-sentiment">{_landing_markdown_html(sentiment_compact)}</p></div>',
        unsafe_allow_html=True,
    )


def sync_screener_gating_layout(st_module, *, gated: bool) -> None:
    """Toggle desktop full-width layout while the terms gate is showing."""
    if gated:
        from admin_tools.tablet_mobile_layout_css import DESKTOP_SCREENER_GATING_LAYOUT

        st_module.markdown(
            f'<style id="scoop-screener-gating-page-css">{DESKTOP_SCREENER_GATING_LAYOUT}</style>',
            unsafe_allow_html=True,
        )
        from landing_page import _landing_view_100_script

        st_module.html(
            '<script>document.documentElement.setAttribute("data-scoop-screener-gated","1");</script>'
            + _landing_view_100_script(),
            unsafe_allow_javascript=True,
        )
    else:
        st_module.html(
            '<script>document.documentElement.removeAttribute("data-scoop-screener-gated");</script>',
            unsafe_allow_javascript=True,
        )


def render_screener_last_updated(st_module, last_updated: str) -> None:
    """Render the screener refresh timestamp row."""
    st_module.markdown(
        f'<div class="scoop-screener-last-updated">'
        f"Last updated: <b>{last_updated}</b></div>",
        unsafe_allow_html=True,
    )


# Desktop table column order — mirrors mobile card layout (tablet_mobile_layout_css.py).
_FULL_RESULTS_COLUMN_ORDER = (
    "Company",
    "Commodity",
    "Name",
    "Ticker",
    "Price",
    "52W Low",
    "% Above Low",
    "52W High",
    "Exchanges",
    "Headlines",
    "Market Mood",
    "Headline Sentiment",
    "Analyze",
)


def order_full_results_columns(columns) -> list[str]:
    """Reorder Full Results table columns to match mobile card field order."""
    cols = list(columns)
    ordered = [c for c in _FULL_RESULTS_COLUMN_ORDER if c in cols]
    return ordered + [c for c in cols if c not in ordered]
