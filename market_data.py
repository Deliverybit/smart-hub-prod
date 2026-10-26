from __future__ import annotations

import re
import time
from datetime import datetime, timezone

import pandas as pd
import requests

from app_config import get_alpha_vantage_api_key

QUOTE_MAX_AGE_DAYS = 14
# Calendar year of split-adjusted daily highs and lows, ending on the scan date.
ROLLING_52W_DAYS = 365
QUOTE_MIN_BARS = 20
# Live quote vs latest daily close. Wide enough for a normal session, tight enough to reject a split-scale mismatch.
QUOTE_CLOSE_BAND = 0.15


def quote_is_usable(dates: list, today: datetime | None = None) -> bool:
    """A screener quote needs a recent bar and enough history to be that company."""
    if len(dates) < QUOTE_MIN_BARS:
        return False
    latest = max(dates)
    if hasattr(latest, "to_pydatetime"):
        latest = latest.to_pydatetime()
    if getattr(latest, "tzinfo", None) is not None:
        latest = latest.astimezone(timezone.utc).replace(tzinfo=None)
    now = today or datetime.now(timezone.utc)
    if now.tzinfo is not None:
        now = now.astimezone(timezone.utc).replace(tzinfo=None)
    return (now - latest).days <= QUOTE_MAX_AGE_DAYS


def _name_tokens(name: str) -> set[str]:
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in name)
    stop = {"inc", "corp", "corporation", "company", "co", "ltd", "plc", "the", "class", "common", "stock", "group"}
    return {token for token in cleaned.split() if token and token not in stop}


def names_agree(saved: str, reported: str) -> bool:
    """True when the saved company name and the vendor name refer to the same firm."""
    left = _name_tokens(saved)
    right = _name_tokens(reported)
    if not left or not right:
        return False
    if left <= right or right <= left:
        return True
    return len(left & right) / min(len(left), len(right)) >= 0.6


def _listing_regions(symbol: str) -> set[str]:
    upper = (symbol or "").strip().upper()
    if upper.endswith(".LON"):
        return {"", "united kingdom"}
    if upper.endswith(".TRT"):
        return {"", "canada", "toronto"}
    return {"", "united states"}


def _symbols_match(reported: str, symbol: str) -> bool:
    """Alpha Vantage sometimes returns the base ticker without the exchange suffix."""
    reported = (reported or "").strip().upper()
    symbol = (symbol or "").strip().upper()
    if not reported or not symbol:
        return False
    if reported == symbol:
        return True
    base, _, suffix = symbol.partition(".")
    return bool(suffix) and reported == base


def symbol_matches_company(ticker: str, matches: list[dict]) -> bool:
    """True when this ticker is a real match for the company, or the search is empty."""
    wanted = (ticker or "").strip().upper()
    scored: list[tuple[float, str]] = []
    for item in matches:
        symbol = str(item.get("1. symbol") or "").strip().upper()
        kind = str(item.get("3. type") or "")
        region = str(item.get("4. region") or "")
        if not symbol or "." in symbol or (kind and kind.lower() != "equity"):
            continue
        if region and region.lower() != "united states":
            continue
        try:
            score = float(item.get("9. matchScore") or 0)
        except (TypeError, ValueError):
            score = 0
        scored.append((score, symbol))
    if not scored:
        return True
    if any(symbol == wanted and score >= 0.5 for score, symbol in scored):
        return True
    best_score, best_symbol = max(scored)
    return not (best_score >= 0.7 and best_symbol != wanted)


class MarketData:
    def __init__(self):
        self.api_key = get_alpha_vantage_api_key(required=True)
        self.base_url = "https://www.alphavantage.co/query"
        self.session = requests.Session()
        self._daily_cache: dict[tuple[str, str], pd.DataFrame] = {}
        self._news_cache: dict[tuple[str, bool], list] = {}
        self._screener_quote_cache: dict[str, dict] = {}
        self._symbol_search_cache: dict[str, list] = {}

    def _new_session(self) -> None:
        try:
            self.session.close()
        except Exception:
            pass
        self.session = requests.Session()

    def _get(self, url: str, *, timeout: int, **kwargs):
        """HTTP GET that cannot stall the scan. A quiet socket is abandoned."""
        import signal
        import threading

        def _alarm(_signum, _frame):
            raise TimeoutError("quote request timed out")

        use_alarm = (
            threading.current_thread() is threading.main_thread()
            and hasattr(signal, "SIGALRM")
        )
        if use_alarm:
            previous = signal.signal(signal.SIGALRM, _alarm)
            signal.alarm(timeout + 5)
        try:
            return self.session.get(url, timeout=timeout, **kwargs)
        except TimeoutError:
            self._new_session()
            raise requests.Timeout("quote request timed out")
        finally:
            if use_alarm:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, previous)

    _CRYPTO_SYMBOLS = {
        "BTC", "ETH", "DOGE", "SOL", "ADA", "SHIB", "XRP", "BNB", "AVAX",
        "LINK", "TRX", "DOT", "MATIC", "LTC", "BCH", "UNI", "ATOM", "ETC",
        "XLM", "FIL", "APT", "ARB", "OP", "NEAR", "INJ", "IMX", "SAND",
        "MANA", "AXS", "ENS", "SNX", "COMP", "SUSHI", "1INCH", "BAT",
        "ZEC", "DASH", "PEPE", "BONK", "WIF", "EIGEN", "SAFE", "AERO",
        "JUP", "SUI", "TIA", "PYTH", "JTO", "SEI", "TAO", "ETHFI", "ONDO",
        "TRUMP", "PENGU", "POPCAT", "PNUT", "MOODENG", "ME", "MOVE", "DRIFT",
        "IO", "REZ", "ZK", "ZRO", "BLUR", "TURBO", "PRIME", "AXL",
        "TON", "WLD", "ENA", "STRK", "PENDLE", "GALA", "FLOW", "CHZ",
        "QNT", "STX", "RUNE", "VET", "THETA", "EOS", "XTZ", "MINA",
        "AR", "KSM", "LPT", "YFI", "ZRX", "SKL", "ANKR", "STORJ",
        "RPL", "FLOKI", "CAKE", "CFX", "W", "ALGO", "ICP", "HBAR",
        "AAVE", "GRT", "MKR", "CRV", "LDO", "FET", "RENDER", "DASH",
    }

    # Alpha Vantage crypto symbols often omit CoinMarketCap numeric suffixes.
    _CRYPTO_ID_ALIASES = {
        "SUI20947": "SUI",
        "JUP29210": "JUP",
        "PEPE24478": "PEPE",
        "APT21794": "APT",
        "UNI7083": "UNI",
        "GRT6719": "GRT",
        "ARB11841": "ARB",
        "IMX10603": "IMX",
        "COMP5692": "COMP",
        "AERO29270": "AERO",
        "AXL17799": "AXL",
        "SAFE21585": "SAFE",
        "TAO22974": "TAO",
        "PRIME23711": "PRIME",
        "PORTAL29555": "PORTAL",
        "MEME28301": "MEME",
    }

    _INDEX_SYMBOLS = {
        "^IXIC": "QQQ",
        "^NYA": "DIA",
        "^GSPC": "SPY",
        "^DJI": "DIA",
    }

    _FUTURES_SYMBOLS = {
        "CL=F": "USO",
        "BZ=F": "BNO",
        "GC=F": "GLD",
        "SI=F": "SLV",
        "PL=F": "PPLT",
        "PA=F": "PALL",
        "HG=F": "CPER",
        "NG=F": "UNG",
        "RB=F": "UGA",
        "HO=F": "UHN",
        "ZC=F": "CORN",
        "ZS=F": "SOYB",
        "ZW=F": "WEAT",
        "ZL=F": "SOYB",
        "ZM=F": "SOYB",
        "ZO=F": "DBA",
        "ZR=F": "DBA",
        "LE=F": "COW",
        "HE=F": "COW",
        "GF=F": "COW",
        "DC=F": "DBA",
        "ES=F": "SPY",
        "NQ=F": "QQQ",
        "YM=F": "DIA",
        "RTY=F": "IWM",
        "6E=F": "FXE",
        "6J=F": "FXY",
        "6B=F": "FXB",
        "6A=F": "FXA",
        "6C=F": "FXC",
        "ZB=F": "TLT",
        "ZN=F": "IEF",
        "ZF=F": "IEI",
        "ZT=F": "SHY",
        "CC=F": "NIB",
        "KC=F": "JO",
        "CT=F": "DBA",
        "SB=F": "CANE",
        "OJ=F": "DBA",
        "DX=F": "UUP",
        "KE=F": "WEAT",
        "LBS=F": "WOOD",
        "LBR=F": "WOOD",
        "BTC=F": "BITO",
        "ETH=F": "ETHA",
        "MBT=F": "BITO",
        "MET=F": "ETHA",
        "MES=F": "SPY",
        "MNQ=F": "QQQ",
        "MYM=F": "DIA",
        "M2K=F": "IWM",
        "EMD=F": "MDY",
        "NKD=F": "EWJ",
        "NIY=F": "EWJ",
        "MME=F": "EEM",
        "SP=F": "SPY",
        "ND=F": "QQQ",
        "MGC=F": "GLD",
        "SIL=F": "SLV",
        "MHG=F": "CPER",
        "MCL=F": "USO",
        "QM=F": "USO",
        "QG=F": "UNG",
        "HH=F": "UNG",
        "NN=F": "UNG",
        "6S=F": "FXF",
        "6N=F": "ENZL",
        "6M=F": "EWW",
        "6L=F": "EWZ",
        "6Z=F": "EZA",
        "6I=F": "INDA",
        "6H=F": "EPOL",
        "E7=F": "FXE",
        "J7=F": "FXY",
        "M6E=F": "FXE",
        "M6A=F": "FXA",
        "M6B=F": "FXB",
        "M6J=F": "FXY",
        "M6C=F": "FXC",
        "M6S=F": "FXF",
        "TN=F": "IEF",
        "UB=F": "TLT",
        "Z3N=F": "IEI",
        "SR3=F": "BIL",
        "SR1=F": "BIL",
        "ZQ=F": "BIL",
        "GE=F": "BIL",
        "FF=F": "BIL",
        "GNF=F": "DBA",
        "CSC=F": "DBA",
        "CB=F": "DBA",
        "GD=F": "DBA",
        "DL=F": "DBA",
        "XC=F": "CORN",
        "XK=F": "SOYB",
        "XW=F": "WEAT",
        "ALI=F": "DBB",
        "HRC=F": "SLX",
        "TIO=F": "PICK",
        "YG=F": "GLD",
        "YI=F": "SLV",
        "QO=F": "GLD",
        "QI=F": "SLV",
        "QC=F": "CPER",
        "SEK=F": "FXS",
        "NOK=F": "NORW",
        "PLN=F": "EPOL",
    }

    # News feed symbol when the London or Toronto code is a different US company, or has no news under the bare ticker.
    _LISTING_NEWS_SYMBOLS = {
        "HSBA.LON": "HSBC",
        "ULVR.LON": "UL",
        "DGE.LON": "DEO",
        "BATS.LON": "BTI",
        "REL.LON": "RELX",
        "NG.LON": "NGG",
        "LLOY.LON": "LYG",
        "BARC.LON": "BCS",
        "TSCO.LON": "TSCDY",
        "GLEN.LON": "GLNCY",
        "AAL.LON": "NGLOY",
        "PRU.LON": "PUK",
        "LSEG.LON": "LNSTY",
        "CPG.LON": "CMPGY",
        "EXPN.LON": "EXPGY",
        "STAN.LON": "SCBFF",
        "BA.LON": "BAESY",
        "RR.LON": "RYCEY",
        "IMB.LON": "IMBBY",
        "ANTO.LON": "ANFGF",
        "SSE.LON": "SSEZY",
        "AV.LON": "AIVAF",
        "LGEN.LON": "LGGNY",
        "RKT.LON": "RBGLY",
        "SN.LON": "SNN",
        "NXT.LON": "NXGPY",
        "AHT.LON": "ASHTY",
        "III.LON": "TGOPY",
        "T.TRT": "TU",
        "ABX.TRT": "GOLD",
        "CNR.TRT": "CNI",
        "MG.TRT": "MGA",
        "PPL.TRT": "PBA",
        "NA.TRT": "NTIOF",
        "L.TRT": "LBLCF",
    }

    def _format_ticker(self, ticker):
        """Normalize user input into an Alpha Vantage compatible symbol."""
        ticker = (ticker or "").strip().upper()
        if ticker in self._INDEX_SYMBOLS:
            return self._INDEX_SYMBOLS[ticker]
        if ticker in self._FUTURES_SYMBOLS:
            return self._FUTURES_SYMBOLS[ticker]
        if ticker.endswith("-USD"):
            base = ticker.replace("-USD", "")
            return self._CRYPTO_ID_ALIASES.get(base, base)
        if ticker in self._CRYPTO_SYMBOLS:
            return ticker
        if ticker.endswith("=F"):
            return ticker.replace("=F", "")
        return ticker

    def _is_crypto(self, ticker: str) -> bool:
        ticker = (ticker or "").strip().upper()
        if ticker.endswith("-USD"):
            return True
        symbol = ticker.replace("-USD", "")
        return symbol in self._CRYPTO_SYMBOLS

    def _request(self, *, fail_fast: bool = False, **params) -> dict:
        max_attempts = 1 if fail_fast else 4
        for attempt in range(max_attempts):
            try:
                response = self._get(
                    self.base_url,
                    params={**params, "apikey": self.api_key},
                    timeout=12 if fail_fast else 20,
                )
                response.raise_for_status()
                data = response.json()
            except (requests.RequestException, ValueError):
                if attempt + 1 < max_attempts:
                    time.sleep(12 * (attempt + 1))
                    continue
                return {}

            if "Error Message" in data:
                return {}

            if "Note" in data or "Information" in data:
                if attempt + 1 < max_attempts:
                    wait = 12 * (attempt + 1)
                    label = params.get("symbol") or params.get("keywords") or ""
                    print(
                        f"Alpha Vantage is busy for {params.get('function')} {label}. Waiting {wait}s.",
                        flush=True,
                    )
                    time.sleep(wait)
                    continue
                return {}

            return data

        return {}

    @staticmethod
    def _to_float(value) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _daily_cache_key(self, ticker: str, outputsize: str) -> tuple:
        symbol = self._format_ticker(ticker)
        if self._is_crypto(ticker):
            return (symbol, "digital", outputsize)
        return (symbol, outputsize)

    @staticmethod
    def _needs_longer_history(df: pd.DataFrame, outputsize: str, max_rows: int | None) -> bool:
        if df is None or df.empty:
            return True
        if outputsize != "full" or max_rows is None:
            return False
        return len(df) < max(int(max_rows) - 20, 1)

    def _history_from_any_cache(
        self,
        ticker: str,
        outputsize: str,
        max_rows: int | None,
    ) -> pd.DataFrame | None:
        """Reuse compact or full cache when it already covers the requested span."""
        keys = [self._daily_cache_key(ticker, outputsize)]
        other = "compact" if outputsize == "full" else "full"
        other_key = self._daily_cache_key(ticker, other)
        if other_key not in keys:
            keys.append(other_key)
        for cache_key in keys:
            cached = self._daily_cache.get(cache_key)
            if cached is None or cached.empty:
                continue
            if self._needs_longer_history(cached, outputsize, max_rows):
                continue
            if max_rows is not None and len(cached) > max_rows:
                return cached.tail(max_rows).copy()
            return cached.copy()
        return None

    def _daily_history_frame(
        self,
        ticker: str,
        outputsize: str = "full",
        max_rows: int | None = None,
        *,
        fail_fast: bool = False,
    ) -> pd.DataFrame:
        symbol = self._format_ticker(ticker)
        cached = self._history_from_any_cache(ticker, outputsize, max_rows)
        if cached is not None:
            return cached

        if self._is_crypto(ticker):
            data = self._request(
                function="DIGITAL_CURRENCY_DAILY",
                symbol=symbol,
                market="USD",
                outputsize=outputsize,
                fail_fast=fail_fast,
            )
            series = data.get("Time Series (Digital Currency Daily)", {})
        else:
            data = self._request(
                function="TIME_SERIES_DAILY_ADJUSTED",
                symbol=symbol,
                outputsize=outputsize,
                fail_fast=fail_fast,
            )
            series = data.get("Time Series (Daily)", {})

        date_keys = sorted(series.keys())
        if max_rows is not None and len(date_keys) > max_rows:
            date_keys = date_keys[-max_rows:]

        rows = []
        for date in date_keys:
            values = series[date]
            close = self._to_float(values.get("4. close"))
            low = self._to_float(values.get("3. low"))
            high = self._to_float(values.get("2. high"))
            if close is None:
                continue
            rows.append({
                "date": pd.to_datetime(date),
                "price": close,
                "low": low,
                "high": high,
                "adj_close": self._to_float(values.get("5. adjusted close")),
                "split": self._to_float(values.get("8. split coefficient")) or 1.0,
            })

        self._apply_share_scale(rows)
        df = pd.DataFrame(rows)
        if not df.empty:
            df = df.sort_values("date").reset_index(drop=True)

        cache_key = self._daily_cache_key(ticker, outputsize)
        self._daily_cache[cache_key] = df
        if max_rows is not None and len(df) > max_rows:
            return df.tail(max_rows).copy()
        return df.copy()

    @staticmethod
    def _apply_share_scale(rows: list[dict]) -> None:
        """Put close, high, and low on the latest share count. Splits inside the series stay aligned."""
        factor = 1.0
        for row in reversed(rows):
            close = row["price"]
            adj = row.pop("adj_close", None)
            split = row.pop("split", 1.0) or 1.0
            if split <= 0:
                split = 1.0
            split_scale = 1.0 / factor
            factor *= split
            traded = float(close) * split_scale
            row["traded_close"] = traded
            if adj is not None and close:
                row["price"] = float(adj)
            else:
                row["price"] = traded
            if row.get("low") is not None:
                row["low"] = float(row["low"]) * split_scale
            if row.get("high") is not None:
                row["high"] = float(row["high"]) * split_scale

    @classmethod
    def _year_window(cls, df: pd.DataFrame, as_of: datetime | None = None) -> pd.DataFrame:
        """Split-adjusted daily bars in the last 365 calendar days."""
        if df.empty or "date" not in df.columns:
            return df
        if as_of is None:
            as_of = datetime.now(timezone.utc)
        if getattr(as_of, "tzinfo", None) is not None:
            as_of = as_of.astimezone(timezone.utc).replace(tzinfo=None)
        end = pd.Timestamp(as_of).normalize()
        start = end - pd.Timedelta(days=ROLLING_52W_DAYS)
        dates = pd.to_datetime(df["date"]).dt.normalize()
        return df.loc[(dates >= start) & (dates <= end)].copy()

    def get_latest_price(self, ticker):
        """Fetch the latest Alpha Vantage price for an asset."""
        symbol = self._format_ticker(ticker)
        if not self._is_crypto(ticker):
            data = self._request(function="GLOBAL_QUOTE", symbol=symbol)
            price = self._to_float(data.get("Global Quote", {}).get("05. price"))
            if price is not None:
                return price

        df = self._daily_history_frame(ticker, outputsize="compact")
        if df.empty:
            return 0.0
        return float(df["price"].iloc[-1])

    def get_price_history(self, ticker, days=30):
        """Fetch historical daily price data. Pass days='max' for all available data."""
        outputsize = "full" if days == "max" else "compact"
        df = self._daily_history_frame(ticker, outputsize=outputsize)
        if df.empty:
            return []

        if days != "max":
            try:
                df = self._span_window(df, int(days))
            except (TypeError, ValueError):
                pass

        df["change_pct"] = df["price"].pct_change()
        history = []
        for _, row in df.iterrows():
            history.append({
                "date": row["date"].strftime("%Y-%m-%d"),
                "price": row["price"],
                "change_pct": row["change_pct"] if not pd.isna(row["change_pct"]) else 0,
            })
        return history

    def get_daily_change(self, ticker):
        """Return latest price and daily percentage change."""
        history = self.get_price_history(ticker, days=5)
        if len(history) < 2:
            return None, None
        previous = history[-2]["price"]
        latest = history[-1]["price"]
        if not previous:
            return latest, 0.0
        return latest, ((latest - previous) / previous) * 100

    def get_analyze_price_bundle(
        self,
        ticker: str,
        days=30,
        *,
        snapshot: dict | None = None,
        fail_fast: bool = True,
    ) -> dict | None:
        """Analyze history from Alpha Vantage. Short ranges use compact; 52w can come from snapshot."""
        chart_max_days = 730
        compact_days = 100
        try:
            chart_days = chart_max_days if days == "max" else min(int(days), chart_max_days)
        except (TypeError, ValueError):
            chart_days = 365

        snap = snapshot or {}
        snap_low = self._to_float(snap.get("year_low") or snap.get("52W Low"))
        snap_high = self._to_float(snap.get("year_high") or snap.get("52W High"))
        snap_price = self._to_float(snap.get("current_price") or snap.get("Price"))
        has_snap_52w = (
            snap_low is not None
            and snap_high is not None
            and snap_low > 0
            and snap_high > 0
        )

        if chart_days <= compact_days:
            outputsize = "full"
            max_rows = 280
        else:
            outputsize = "full"
            max_rows = chart_max_days + 10

        df = self._daily_history_frame(
            ticker,
            outputsize=outputsize,
            max_rows=max_rows,
            fail_fast=fail_fast,
        )
        if df.empty:
            if not has_snap_52w:
                return None
            latest_price = snap_price if snap_price is not None else 0.0
            return {
                "history": [],
                "latest_price": latest_price,
                "week52_low": snap_low,
                "week52_high": snap_high,
                "low_date": None,
                "high_date": None,
            }

        year_df = self._year_window(df)
        low_series = year_df["low"].dropna()
        high_series = year_df["high"].dropna()

        latest_price = float(df["price"].iloc[-1])
        if snap_price is not None and snap_price > 0:
            latest_price = snap_price
        week52_low = float(low_series.min()) if not low_series.empty else snap_low
        week52_high = float(high_series.max()) if not high_series.empty else snap_high

        low_date = high_date = None
        if not low_series.empty:
            low_date = year_df.loc[year_df["low"].idxmin(), "date"].strftime("%b %d, %Y")
        if not high_series.empty:
            high_date = year_df.loc[year_df["high"].idxmax(), "date"].strftime("%b %d, %Y")

        chart_df = self._span_window(df, chart_days)

        chart_df = chart_df.copy()
        chart_df["change_pct"] = chart_df["price"].pct_change().fillna(0)
        history = [
            {
                "date": row["date"].strftime("%Y-%m-%d"),
                "price": float(row["price"]),
                "change_pct": float(row["change_pct"]),
            }
            for row in chart_df.to_dict("records")
        ]

        return {
            "history": history,
            "latest_price": latest_price,
            "week52_low": week52_low,
            "week52_high": week52_high,
            "low_date": low_date,
            "high_date": high_date,
        }

    def get_screener_snapshots(
        self,
        tickers: list[str],
        *,
        av_fallback: bool = True,
    ) -> dict[str, dict]:
        """52-week quotes from Alpha Vantage only."""
        snapshots: dict[str, dict] = {}
        for ticker in tickers:
            cached = self._screener_quote_cache.get(ticker)
            if cached:
                snapshots[ticker] = dict(cached)
                continue
            if not av_fallback:
                continue
            av_row = self.get_market_snapshot(ticker)
            if av_row:
                wrapped = {**av_row, "source": "alpha_vantage", "daily_change_pct": None}
                self._screener_quote_cache[ticker] = dict(wrapped)
                snapshots[ticker] = dict(wrapped)
        return snapshots

    def get_crypto_screener_snapshots(
        self,
        tickers: list[str],
        *,
        av_fallback: bool = True,
    ) -> dict[str, dict]:
        """52-week crypto quotes from Alpha Vantage only."""
        return self.get_screener_snapshots(tickers, av_fallback=av_fallback)

    def get_market_snapshot(self, ticker):
        """Return current price plus 52-week low/high values for screeners."""
        cached = self._screener_quote_cache.get(ticker)
        if cached:
            return {
                "current_price": cached["current_price"],
                "year_low": cached["year_low"],
                "year_high": cached["year_high"],
            }
        symbol = self._format_ticker(ticker)
        quote = self._live_quote(ticker, symbol)
        df = self._year_window(
            self._daily_history_frame(ticker, outputsize="full", fail_fast=True)
        )
        if df.empty or not quote_is_usable(list(df["date"])):
            print(f"Skip {ticker}: price series is stale or too short", flush=True)
            return None

        low_series = df["low"].dropna()
        high_series = df["high"].dropna()
        close_col = "traded_close" if "traded_close" in df.columns else "price"
        last_close = float(df[close_col].iloc[-1])
        if low_series.empty or high_series.empty or last_close <= 0 or quote is None:
            print(f"Skip {ticker}: quote or 52-week range is missing", flush=True)
            return None

        year_low = float(low_series.min())
        year_high = float(high_series.max())
        if year_low <= 0 or year_low > year_high:
            print(f"Skip {ticker}: 52-week range is not usable", flush=True)
            return None
        # Crypto daily bars lag the live rate. The rate is the price to show.
        price = quote if self._is_crypto(ticker) else last_close
        if not self._is_crypto(ticker) and abs(quote - last_close) / last_close > QUOTE_CLOSE_BAND:
            print(f"Skip {ticker}: quote {quote} disagrees with last close {last_close}", flush=True)
            return None
        if price < year_low * (1 - QUOTE_CLOSE_BAND) or price > year_high * (1 + QUOTE_CLOSE_BAND):
            print(f"Skip {ticker}: quote {price} is outside the 52-week range", flush=True)
            return None

        return {
            "current_price": price,
            "year_low": year_low,
            "year_high": year_high,
        }

    def _live_quote(self, ticker: str, symbol: str) -> float | None:
        """Latest Alpha Vantage price for this exact symbol."""
        if self._is_crypto(ticker):
            data = self._request(
                function="CURRENCY_EXCHANGE_RATE",
                from_currency=symbol,
                to_currency="USD",
                fail_fast=True,
            )
            rate = data.get("Realtime Currency Exchange Rate") or {}
            reported = str(rate.get("1. From_Currency Code") or "").strip().upper()
            price = self._to_float(rate.get("5. Exchange Rate"))
        else:
            data = self._request(function="GLOBAL_QUOTE", symbol=symbol, fail_fast=True)
            quote = data.get("Global Quote") or {}
            reported = str(quote.get("01. symbol") or "").strip().upper()
            price = self._to_float(quote.get("05. price"))
        if reported != symbol.upper() or price is None or price <= 0:
            return None
        return price

    def symbol_matches_company(self, ticker: str, company_name: str) -> bool:
        """True when search and company overview both name this ticker."""
        name = (company_name or "").strip()
        symbol = (ticker or "").strip().upper()
        if not name or not symbol:
            return False
        search_key = symbol if "." in symbol else name
        cached = self._symbol_search_cache.get(search_key)
        if cached is None:
            keywords = symbol.split(".", 1)[0] if "." in symbol else name
            data = self._request(function="SYMBOL_SEARCH", keywords=keywords, fail_fast=True)
            cached = list(data.get("bestMatches") or [])
            self._symbol_search_cache[search_key] = cached
        regions = _listing_regions(symbol)
        listed = any(
            str(item.get("1. symbol") or "").strip().upper() == symbol
            and str(item.get("3. type") or "").lower() in {"", "equity"}
            and str(item.get("4. region") or "").lower() in regions
            for item in cached
        )
        if not listed:
            print(f"Skip {symbol}: company {name!r} does not list this ticker", flush=True)
            return False
        if not self._overview_matches(symbol, name):
            print(f"Skip {symbol}: overview does not match {name!r}", flush=True)
            return False
        return True

    def _overview_matches(self, symbol: str, company_name: str) -> bool:
        cached = self._symbol_search_cache.get(f"overview:{symbol}")
        if cached is None:
            data = self._request(function="OVERVIEW", symbol=symbol, fail_fast=True)
            cached = data if isinstance(data, dict) else {}
            self._symbol_search_cache[f"overview:{symbol}"] = cached
        reported_symbol = str(cached.get("Symbol") or "").strip().upper()
        reported_name = str(cached.get("Name") or "")
        if not reported_symbol and not reported_name:
            # London and Toronto overviews often come back empty on this plan.
            return "." in symbol
        return _symbols_match(reported_symbol, symbol) and names_agree(company_name, reported_name)

    def get_52_week_low(self, ticker):
        """Returns the 52-week low price for the asset."""
        snapshot = self.get_market_snapshot(ticker)
        if not snapshot:
            return None
        return snapshot["year_low"]

    def get_52_week_high(self, ticker):
        """Returns the 52-week high price for the asset."""
        snapshot = self.get_market_snapshot(ticker)
        if not snapshot:
            return None
        return snapshot["year_high"]

    def get_52_week_low_high_dates(self, ticker):
        """Returns dates when the 52-week low and high occurred."""
        df = self._year_window(self._daily_history_frame(ticker, outputsize="full"))
        if df.empty or df["low"].dropna().empty or df["high"].dropna().empty:
            return None, None
        low_date = df.loc[df["low"].idxmin(), "date"].strftime("%b %d, %Y")
        high_date = df.loc[df["high"].idxmax(), "date"].strftime("%b %d, %Y")
        return low_date, high_date

    def get_news_headlines(self, ticker):
        """Pulls real-time headlines for the specific asset."""
        items = self.get_news_items(ticker)
        return [item["title"] for item in items]

    def _yahoo_listing_headlines(self, symbol: str) -> list[dict]:
        """Headlines for the London (.L) or Toronto (.TO) listing."""
        import xml.etree.ElementTree as ET
        from html import unescape

        cache_key = (f"YAHOO:{symbol}", False)
        if cache_key in self._news_cache:
            return [dict(item) for item in self._news_cache[cache_key]]

        yahoo_symbol = symbol.replace(".LON", ".L").replace(".TRT", ".TO")
        url = (
            "https://feeds.finance.yahoo.com/rss/2.0/headline"
            f"?s={yahoo_symbol}&region=US&lang=en-US"
        )
        headlines = []
        seen = set()
        try:
            response = self._get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            root = ET.fromstring(response.content)
        except (requests.RequestException, ET.ParseError, ValueError):
            root = None
        if root is not None:
            for item in root.iter("item"):
                title = unescape((item.findtext("title") or "")).strip()
                link = unescape((item.findtext("link") or "")).strip()
                key = (title, link)
                if title and link and key not in seen:
                    seen.add(key)
                    headlines.append({"title": title, "url": link, "source": "Yahoo Finance", "relevance": 0.0})
        result = headlines if headlines else [{"title": f"No current news found for {symbol}", "url": ""}]
        self._news_cache[cache_key] = [dict(item) for item in result]
        return [dict(item) for item in result]

    def get_news_items(self, ticker, *, fail_fast: bool = False):
        """Pulls headline + source URL pairs for the specific asset."""
        symbol = self._format_ticker(ticker)
        is_crypto = self._is_crypto(ticker)
        # NEWS_SENTIMENT has no London or Toronto feed. A mapped US listing is the same company.
        # The bare ticker is often a different US company, so unmapped names use the Yahoo listing feed.
        news_symbol = self._LISTING_NEWS_SYMBOLS.get(symbol)
        if symbol.endswith((".LON", ".TRT")) and not news_symbol:
            return self._yahoo_listing_headlines(symbol)
        if not news_symbol:
            news_symbol = symbol
        cache_key = (news_symbol, is_crypto)
        if cache_key in self._news_cache:
            return [dict(item) for item in self._news_cache[cache_key]]

        params = {"function": "NEWS_SENTIMENT", "limit": 1000}
        if is_crypto:
            params["tickers"] = f"CRYPTO:{symbol}"
        elif news_symbol:
            params["tickers"] = news_symbol

        data = self._request(fail_fast=fail_fast, **params)
        feed = data.get("feed", [])
        if is_crypto:
            expected_ticker = f"CRYPTO:{symbol}"
            base = symbol.replace("-USD", "").lower()

            def _crypto_story(item: dict) -> bool:
                tagged = any(
                    sentiment.get("ticker") == expected_ticker
                    for sentiment in item.get("ticker_sentiment", [])
                )
                if tagged:
                    return True
                folded = re.sub(r"[^a-z0-9]+", " ", str(item.get("title") or "").lower())
                titled = str(item.get("title") or "")
                if re.search(rf"(?<![A-Z0-9]){re.escape(base.upper())}(?![A-Z0-9])", titled):
                    return True
                return f" {base} " in f" {folded} " and base not in {
                    "flow", "turbo", "cash", "rate", "rates", "bank", "dollar", "growth", "market",
                    "price", "prices", "stock", "stocks", "share", "shares", "earnings",
                }

            news = [item for item in feed if _crypto_story(item)]
            source_priority = {
                "Cointelegraph": 0,
                "Decrypt.co": 1,
                "Benzinga": 2,
                "Motley Fool": 3,
            }
            news = sorted(
                enumerate(news),
                key=lambda pair: (
                    source_priority.get(
                        pair[1].get("source") or pair[1].get("source_domain") or "",
                        99,
                    ),
                    pair[0],
                ),
            )
            news = [item for _, item in news]
        else:
            news = feed

        headlines = []
        seen = set()
        for item in news:
            title = item.get("title", "")
            url = item.get("url", "")
            source = item.get("source") or item.get("source_domain") or ""
            if is_crypto and source:
                title = f"{source}: {title}"
            key = (title, url)
            if title and key not in seen:
                seen.add(key)
                relevance = 0.0
                expected = f"CRYPTO:{symbol}" if is_crypto else news_symbol
                for sentiment in item.get("ticker_sentiment") or []:
                    if sentiment.get("ticker") != expected:
                        continue
                    try:
                        relevance = max(relevance, float(sentiment.get("relevance_score") or 0))
                    except (TypeError, ValueError):
                        continue
                headlines.append({
                    "title": title,
                    "url": url,
                    "source": source,
                    "relevance": relevance,
                })

        if is_crypto and not headlines:
            yahoo_symbol = symbol if str(symbol).endswith("-USD") else f"{symbol}-USD"
            yahoo = [
                item for item in self._yahoo_listing_headlines(yahoo_symbol)
                if item.get("url")
            ]
            if yahoo:
                self._news_cache[cache_key] = [dict(item) for item in yahoo]
                return [dict(item) for item in yahoo]
        result = headlines if headlines else [{"title": f"No current news found for {symbol}", "url": ""}]
        self._news_cache[cache_key] = [dict(item) for item in result]
        return [dict(item) for item in result]