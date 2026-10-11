"""Refill saved market-page tables from screener snapshots already in the database."""

from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import quote

PREVIEW = Path(__file__).resolve().parent / "preview"

PAGES = {
    "NYSE": ("nyse.html", "/NYSE_Top_10", "Company"),
    "NASDAQ": ("nasdaq.html", "/NASDAQ_Top_10", "Company"),
    "CRYPTO": ("crypto.html", "/Crypto_Top_10", "Name"),
    "CME": ("cme.html", "/CME_Top_10", "Commodity"),
    "ICE": ("ice.html", "/ICE_Top_10", "Commodity"),
}

COLUMN_TIPS = {
    "Headlines": (
        "Number of recent news headlines found for this stock. "
        "More headlines give a more reliable sentiment reading."
    ),
    "Market Mood": (
        "Proximity to the 52-week low: BELOW LOW = trading under the recorded low, "
        "AT LOW = within 2%, NEAR LOW = above 2% and within 30% of the 52-week low."
    ),
    "% Above Low": (
        "How far the current price is above the 52-week low, expressed as a percentage. "
        "Lower is closer to the floor."
    ),
    "Headline Sentiment": (
        "Average polarity score of recent news headlines (TextBlob). "
        "Ranges from -1.0 (very negative) to +1.0 (very positive). "
        "Stocks below -0.35 are automatically disqualified."
    ),
    "Analyze": (
        "Open a detailed Analyze dashboard for this symbol — price history, "
        "headline sentiment, and related scores."
    ),
}

TBODY = re.compile(r"<tbody>.*?</tbody>", re.S)
ROW = re.compile(r"<tr>(.*?)</tr>", re.S)
TICKER_CELL = re.compile(
    r'data-label="Ticker">(?:(?!</td>).)*<span class="fr-val">([^<]+)',
    re.S,
)
NAME_TIP = re.compile(
    r'scoop-name-tip">(?:[^<]*)<span class="tip-text">([^<]*)',
    re.S,
)


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _tip(text: str, tooltip: str, extra_class: str = "") -> str:
    wrap = "tip-wrap" if not extra_class else f"tip-wrap {extra_class}"
    return (
        f'<span class="{wrap}">{_esc(text)}'
        f'<span class="tip-text">{_esc(tooltip)}</span></span>'
    )


def _td(label: str, inner: str, label_tip: str = "") -> str:
    label_html = _tip(label, label_tip) if label_tip else _esc(label)
    return (
        f'<td data-label="{_esc(label)}">'
        f'<span class="fr-label">{label_html}</span>'
        f'<span class="fr-val">{inner}</span></td>'
    )


def _money(value: object, *, crypto: bool) -> str:
    try:
        price = float(value)
    except (TypeError, ValueError):
        return "N/A"
    if not crypto or abs(price) > 1:
        return f"${price:,.2f}"
    formatted = f"{price:,.8f}"
    whole, _, decimal = formatted.partition(".")
    decimal = decimal.rstrip("0")
    if len(decimal) < 2:
        decimal = decimal.ljust(2, "0")
    return f"${whole}.{decimal}"


def _headlines(count: object, texts: list, urls: list, row_idx: int) -> str:
    aid = f"--hl-r{row_idx}"
    cb_id = f"hl-cb-r{row_idx}"
    lines = []
    for title, url in zip(texts or [], urls or []):
        safe_title = _esc(title)
        if url:
            lines.append(
                f'<div class="hl-tip-line"><a href="{_esc(url)}" target="_blank" '
                f'rel="noopener noreferrer">{safe_title}</a></div>'
            )
        else:
            lines.append(f'<div class="hl-tip-line">{safe_title}</div>')
    return (
        f'<span class="tip-wrap headlines-tip" style="anchor-name: {aid};">'
        f'<input type="checkbox" id="{cb_id}" class="hl-tip-cb" aria-hidden="true">'
        f'<label class="hl-tip-count" for="{cb_id}">{_esc(count)}</label>'
        f'<label class="hl-tip-backdrop" for="{cb_id}" aria-hidden="true"><span>&nbsp;</span></label>'
        f'<span class="tip-text" style="position-anchor: {aid};">'
        f'<span class="hl-tip-heading">Headlines</span>'
        f'<div class="headlines-tip-scroll"><div class="headlines-tip-list">{"".join(lines)}</div></div>'
        f"</span></span>"
    )


def _analyze(source: str, from_path: str) -> str:
    url = f"/analyze.html?ticker={quote(str(source).strip(), safe='')}"
    if from_path:
        path = from_path if from_path.startswith("/") else f"/{from_path}"
        url = f"{url}&from={quote(path, safe='')}"
    tip = COLUMN_TIPS["Analyze"]
    return (
        '<span class="fr-analyze-cell">'
        f'<a href="{_esc(url)}" target="_self" rel="noopener" class="fr-analyze-link" '
        f'data-ticker="{_esc(source)}">Analyze</a>'
        f'<span class="tip-wrap fr-analyze-mobile-tip" style="display: none;">Analyze'
        f'<span class="tip-text">{_esc(tip)}</span></span></span>'
    )


def _existing_tips(page_html: str) -> dict[str, str]:
    """Keep each symbol's existing company description. New symbols get no description."""
    tips = {}
    for row in ROW.findall(page_html):
        ticker = TICKER_CELL.search(row)
        tip = NAME_TIP.search(row)
        if ticker and tip:
            tips.setdefault(html.unescape(ticker.group(1)), html.unescape(tip.group(1)))
    return tips


def _columns(rows: list[dict], label_field: str) -> list[str]:
    present = set(rows[0])
    ordered = [
        label_field,
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
    ]
    return [name for name in ordered if name == "Analyze" or name in present]


def build_tbody(rows: list[dict], *, label_field: str, from_path: str, tips: dict[str, str], crypto: bool) -> str:
    """Return one tbody using the same cell markup the saved pages already use."""
    columns = [name for name in _columns(rows, label_field) if name != label_field or label_field]
    body = []
    for index, row in enumerate(rows[:10], start=1):
        ticker = str(row.get("Ticker") or "")
        cells = _td("#", str(index))
        for column in columns:
            if column == "Analyze":
                source = str(row.get("_source_ticker") or ticker)
                cells += _td(column, _analyze(source, from_path), COLUMN_TIPS["Analyze"])
                continue
            if column == label_field:
                tip = tips.get(ticker, "")
                name = str(row.get(column) or ticker)
                inner = _tip(name, tip, "scoop-name-tip") if tip else _esc(name)
                cells += _td(column, inner)
                continue
            if column == "Headlines":
                count = row.get("Headlines") or 0
                texts = list(row.get("_headline_texts") or [])[:10]
                urls = list(row.get("_headline_urls") or [])[:10]
                if texts:
                    cells += _td(column, _headlines(count, texts, urls, index - 1), COLUMN_TIPS["Headlines"])
                else:
                    cells += _td(column, _esc(count), COLUMN_TIPS["Headlines"])
                continue
            if column in {"Price", "52W Low", "52W High"}:
                cells += _td(column, _esc(_money(row.get(column), crypto=crypto)))
                continue
            if column == "% Above Low":
                try:
                    cells += _td(column, _esc(f"{float(row.get(column)):.2f}%"), COLUMN_TIPS[column])
                except (TypeError, ValueError):
                    cells += _td(column, "", COLUMN_TIPS[column])
                continue
            if column == "Headline Sentiment":
                try:
                    cells += _td(column, _esc(f"{float(row.get(column)):+.3f}"), COLUMN_TIPS[column])
                except (TypeError, ValueError):
                    cells += _td(column, "", COLUMN_TIPS[column])
                continue
            if column == "Market Mood":
                cells += _td(column, _esc(row.get(column) or ""), COLUMN_TIPS[column])
                continue
            cells += _td(column, _esc(row.get(column) or ""))
        body.append(f"<tr>{cells}</tr>")
    return "<tbody>" + "".join(body) + "</tbody>"


def refill_page(
    page_html: str,
    rows: list[dict],
    *,
    label_field: str,
    from_path: str,
    crypto: bool = False,
    tips: dict[str, str] | None = None,
) -> str:
    """Replace every Full Results tbody. The header, CSS, and surrounding page stay as they are."""
    if not rows or "<tbody>" not in page_html:
        return page_html
    tbody = build_tbody(
        rows,
        label_field=label_field,
        from_path=from_path,
        tips=_existing_tips(page_html) if tips is None else tips,
        crypto=crypto,
    )
    return TBODY.sub(tbody, page_html)


def _bundle_for_row(payload: dict, row: dict) -> dict | None:
    from screener_headlines import _ticker_identity_variants, normalize_screener_ticker

    bundles = payload.get("analyze_bundles") or {}
    ticker = str(row.get("Ticker") or "")
    sym = normalize_screener_ticker(str(row.get("_source_ticker") or ticker))
    for variant in _ticker_identity_variants(sym):
        bundle = bundles.get(variant)
        if bundle:
            return bundle
    return None


def _ready_payloads(payloads: list[dict]) -> list[dict]:
    """Keep a market only when every displayed row has an Analyze bundle."""
    ready = []
    for payload in payloads:
        key = str(payload.get("screener_key") or "")
        if key not in PAGES:
            continue
        rows = list(payload.get("display_results") or [])
        missing = [str(row.get("Ticker") or "") for row in rows if _bundle_for_row(payload, row) is None]
        if missing:
            print(f"Skip {key}: Analyze is not ready for {', '.join(missing)}", flush=True)
            continue
        ready.append(payload)
    return ready


def refresh_preview_from_payloads(payloads: list[dict]) -> list[str]:
    """Write market lists and Analyze data together. Skip a market that is missing either."""
    ready = _ready_payloads(payloads)
    written = []
    for payload in ready:
        filename, from_path, label_field = PAGES[str(payload.get("screener_key") or "")]
        path = PREVIEW / filename
        if not path.exists():
            continue
        rows = list(payload.get("display_results") or [])
        updated = refill_page(
            path.read_text(encoding="utf-8"),
            rows,
            label_field=label_field,
            from_path=from_path,
            crypto=payload.get("screener_key") == "CRYPTO",
        )
        updated = stamp_last_updated(updated, str(payload.get("last_updated_display") or ""))
        path.write_text(updated, encoding="utf-8")
        written.append(filename)
    if written:
        refresh_analyze_catalog(ready)
    return written


LAST_UPDATED = re.compile(
    r'(class="scoop-screener-last-updated">Last updated: <b>)[^<]*'
)
ASSETS_PATH = PREVIEW / "analyze-assets.json"
MARKETS = {
    "NYSE": "NYSE Top 10",
    "NASDAQ": "NASDAQ Top 10",
    "CRYPTO": "Crypto 10",
    "CME": "CME Commodities 10",
    "ICE": "ICE Commodities 10",
}


def stamp_last_updated(page_html: str, stamp: str) -> str:
    if not stamp:
        return page_html
    return LAST_UPDATED.sub(lambda match: match.group(1) + stamp, page_html)


def _row_name(row: dict) -> str:
    for key in ("Company", "Name", "Commodity"):
        if row.get(key):
            return str(row[key])
    return str(row.get("Ticker") or "")


def _catalog_asset(payload: dict, row: dict, bundle: dict, previous: dict | None) -> dict:
    from asset_names import resolve_asset_summary

    previous = previous or {}
    ticker = str(row.get("Ticker") or "")
    key = str(payload.get("screener_key") or "")
    filename, from_path, _label = PAGES[key]
    news = list(bundle.get("news_items") or [])
    scores = list((bundle.get("sent_result") or {}).get("headline_scores") or [])
    headlines = []
    for index, item in enumerate(news):
        title = str(item.get("title") or "")
        if not title:
            continue
        score = scores[index][1] if index < len(scores) and len(scores[index]) > 1 else None
        headlines.append({"title": title, "href": str(item.get("url") or ""), "score": score})
    history = list(bundle.get("history") or [])
    series = [{"d": str(point.get("date") or ""), "p": point.get("price")} for point in history]
    return {
        "ticker": ticker,
        "name": _row_name(row),
        "market": MARKETS.get(key, key),
        "page": filename,
        "from": from_path,
        "price": bundle.get("latest_price"),
        "low": bundle.get("week52_low"),
        "high": bundle.get("week52_high"),
        "above": previous.get("above") or COLUMN_TIPS["% Above Low"],
        "mood": previous.get("mood") or COLUMN_TIPS["Market Mood"],
        "sentiment": previous.get("sentiment") or COLUMN_TIPS["Headline Sentiment"],
        "headlines": headlines,
        "series": series,
        "description": previous.get("description") or resolve_asset_summary(ticker),
    }


def refresh_analyze_catalog(payloads: list[dict]) -> int:
    """Refresh Analyze assets from the same bundles that produced the market lists."""
    import json

    catalog = {}
    if ASSETS_PATH.exists():
        catalog = json.loads(ASSETS_PATH.read_text(encoding="utf-8"))
    written = 0
    for payload in payloads:
        key = str(payload.get("screener_key") or "")
        if key not in PAGES:
            continue
        for row in payload.get("display_results") or []:
            ticker = str(row.get("Ticker") or "")
            bundle = _bundle_for_row(payload, row)
            if bundle is None:
                continue
            catalog[ticker] = _catalog_asset(payload, row, bundle, catalog.get(ticker))
            written += 1
    ASSETS_PATH.write_text(json.dumps(catalog, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return written


def refresh_preview_from_database() -> list[str]:
    """Load the stored screener snapshots and refill the saved market tables."""
    from screener_snapshots import _fetch_snapshot_uncached

    payloads = []
    for key in PAGES:
        payload = _fetch_snapshot_uncached(key)
        if payload:
            payloads.append(payload)
    return refresh_preview_from_payloads(payloads)
