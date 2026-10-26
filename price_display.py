"""Format LSE and TSX prices for display.

London quotes from Alpha Vantage and Yahoo are in pence (GBp). Toronto quotes
are in Canadian dollars. A USD rate, when supplied, converts the major-unit price.
"""

from __future__ import annotations


def quote_scale(market: str) -> float:
    """Pence to pounds for London. Other markets are already in major units."""
    if (market or "").strip().upper() == "LSE":
        return 0.01
    return 1.0


def local_prefix(market: str) -> str:
    key = (market or "").strip().upper()
    if key == "LSE":
        return "£"
    if key == "TSX":
        return "C$"
    return "$"


def format_listing_price(value, market: str, usd_per_local: float | None = None) -> str:
    amount = float(value) * quote_scale(market)
    if usd_per_local:
        return f"${amount * float(usd_per_local):,.2f}"
    return f"{local_prefix(market)}{amount:,.2f}"


_CURRENCY_NAMES = {
    "GBP": "British Pounds",
    "CAD": "Canadian Dollars",
    "USD": "United States Dollars",
}


CURRENCY_SWITCH_CSS = """
<style>
.st-key-lse_currency,
.st-key-tsx_currency,
.st-key-lse_currency [data-testid="stHorizontalBlock"],
.st-key-tsx_currency [data-testid="stHorizontalBlock"],
.st-key-lse_currency [data-testid="stColumn"],
.st-key-tsx_currency [data-testid="stColumn"],
.st-key-lse_currency [data-testid="stVerticalBlock"],
.st-key-tsx_currency [data-testid="stVerticalBlock"] {
  overflow: visible !important;
}
.st-key-lse_currency [data-testid="stHorizontalBlock"],
.st-key-tsx_currency [data-testid="stHorizontalBlock"] {
  align-items: center !important;
  width: fit-content !important;
  gap: 0.35rem !important;
}
.st-key-lse_currency .currency-abbrev,
.st-key-tsx_currency .currency-abbrev {
  font-size: 1.45rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.04em !important;
  border-bottom: 1px dashed currentColor !important;
  line-height: 1.2 !important;
}
html body .stApp .stMarkdown .tip-wrap.currency-abbrev > .tip-text,
html body .stApp [data-testid="stMarkdownContainer"] .tip-wrap.currency-abbrev > .tip-text {
  min-width: 0 !important;
  width: max-content !important;
  max-width: max-content !important;
  height: auto !important;
  padding: 0.45rem 0.7rem !important;
  font-size: 1.25rem !important;
  font-weight: 500 !important;
  line-height: 1.35 !important;
  white-space: nowrap !important;
  left: 0 !important;
  transform: none !important;
  box-sizing: border-box !important;
}
.st-key-lse_currency [data-testid="stToggle"],
.st-key-tsx_currency [data-testid="stToggle"] {
  margin-top: 0 !important;
}
.st-key-lse_show_usd,
.st-key-tsx_show_usd,
.st-key-lse_show_usd [data-testid="stCheckbox"],
.st-key-tsx_show_usd [data-testid="stCheckbox"] {
  background: transparent !important;
  background-color: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
  outline: none !important;
}
.st-key-lse_show_usd [data-baseweb="checkbox"] > div:first-child,
.st-key-tsx_show_usd [data-baseweb="checkbox"] > div:first-child {
  border-radius: 999px !important;
  width: 3.15rem !important;
  min-width: 3.15rem !important;
  height: 1.7rem !important;
  min-height: 1.7rem !important;
  background: #e2e8f0 !important;
  background-color: #e2e8f0 !important;
}
.st-key-lse_show_usd [data-baseweb="checkbox"] > div:first-child > div,
.st-key-tsx_show_usd [data-baseweb="checkbox"] > div:first-child > div {
  border-radius: 999px !important;
  width: 1.25rem !important;
  height: 1.25rem !important;
  background-color: #2563eb !important;
}
.st-key-lse_show_usd:has(input:checked) [data-baseweb="checkbox"] > div:first-child,
.st-key-tsx_show_usd:has(input:checked) [data-baseweb="checkbox"] > div:first-child {
  background: #22c55e !important;
  background-color: #22c55e !important;
}
.st-key-lse_show_usd:has(input:checked) [data-baseweb="checkbox"] > div:first-child > div,
.st-key-tsx_show_usd:has(input:checked) [data-baseweb="checkbox"] > div:first-child > div {
  background-color: #f8fafc !important;
  transform: translateX(1.7rem) !important;
}
</style>
"""


def currency_abbrev_tip(code: str) -> str:
    """Underlined abbreviation whose hover text is the full currency name."""
    key = (code or "").strip().upper()
    full = _CURRENCY_NAMES.get(key, key)
    return (
        f'<span class="tip-wrap currency-abbrev">{key}'
        f'<span class="tip-text">{full}</span></span>'
    )


_USD_FIELDS = ("Price", "52W Low", "52W High")


def stamp_usd_prices(payload: dict, rate: float | None) -> dict:
    """Store a USD copy of each listing price on the snapshot. No network call."""
    key = str(payload.get("screener_key") or "").upper()
    if key not in {"LSE", "TSX"}:
        return payload
    try:
        factor = quote_scale(key) * float(rate) if rate else None
    except (TypeError, ValueError):
        factor = None
    payload["usd_per_local"] = factor and float(rate)
    rows = list(payload.get("all_results") or []) + list(payload.get("display_results") or [])
    for row in rows:
        if not isinstance(row, dict):
            continue
        for field in _USD_FIELDS:
            value = row.get(field)
            if factor is None or value is None:
                row.pop(f"{field} USD", None)
                continue
            try:
                row[f"{field} USD"] = float(value) * factor
            except (TypeError, ValueError):
                row.pop(f"{field} USD", None)
    for bundle in (payload.get("analyze_bundles") or {}).values():
        if isinstance(bundle, dict):
            bundle["fx"] = float(rate) if factor else None
            bundle["quote_scale"] = quote_scale(key)
    return payload


def usd_per_unit(code: str) -> float | None:
    """Spot units of USD per one unit of ``code`` (GBP or CAD)."""
    from market_data import MarketData

    data = MarketData()._request(
        function="CURRENCY_EXCHANGE_RATE",
        from_currency=code,
        to_currency="USD",
        fail_fast=True,
    )
    rate = (data.get("Realtime Currency Exchange Rate") or {}).get("5. Exchange Rate")
    try:
        value = float(rate)
    except (TypeError, ValueError):
        return None
    return value if value > 0 else None
