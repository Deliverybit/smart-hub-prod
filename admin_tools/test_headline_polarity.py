"""Phrase overrides for headline polarity."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sentiment_engine import SentimentEngine, headline_polarity, story_polarity  # noqa: E402


def test_severe_legal_language_scores_minus_one():
    assert headline_polarity("Gildan securities class action lawsuit deadline") == -1.0
    assert headline_polarity("Bank faces criminal probe after fraud fine") == -1.0


def test_target_cut_beats_a_buy_rating():
    title = "B of A Securities maintains Buy on Alamos Gold, lowers target to $39"
    assert headline_polarity(title) == -0.5


def test_strong_and_mild_positive_phrases():
    assert headline_polarity("United Parcel Service earnings beat by $0.06, revenue topped estimates") == 0.5
    assert headline_polarity("Northrop Grumman Price Target Raised to $430") == 0.5
    assert headline_polarity("National Bank lifts target for Emera stock") == 0.5
    assert headline_polarity("Cameco stock rises Tuesday, outperforms market") == 0.5
    assert headline_polarity("Eaton Jumps 4% After Declaring Its Quarterly Dividend") == 0.2
    assert headline_polarity("Eaton declares $1.10 quarterly dividend") == 0.2


def test_phrases_from_other_screens():
    assert headline_polarity("Two workers die after Kinross Gold accidents") == -1.0
    assert headline_polarity("Coinbase shares slide 11% as Binance hack weighs") == -1.0
    assert headline_polarity("Haleon sinks 14.7% after Q3 growth miss") == -0.5
    assert headline_polarity("Zacks downgrades Haleon stock from Hold to Strong Sell") == -0.5
    assert headline_polarity("Take-Two Interactive stock hits 52-week low") == -0.5
    assert headline_polarity("Sterling Capital Sells 6,430 Shares of Take-Two") == -0.5
    assert headline_polarity("Caught Out By Charter Communications' 58% Fall") == -0.5
    assert headline_polarity("T-Mobile US Jumps 5.3% on EPS Beat") == 0.5
    assert headline_polarity("T-Mobile Tops Q3 Estimates") == 0.5
    assert headline_polarity("T-Mobile Raises 2026 Outlook") == 0.5
    assert headline_polarity("GSK Wins FDA Approval For Chronic Hepatitis B Drug") == 0.5
    assert headline_polarity("Lululemon Rallies Over 3%") == 0.2
    assert headline_polarity("Haleon Launches £500m Share Buyback") == 0.2
    assert headline_polarity("GSK to Invest $800M and Create 300 New Jobs") == 0.2


def test_honeywell_project_wins_are_mild_positive():
    assert headline_polarity(
        "Honeywell leaning on physical AI to net $1 billion India revenues"
    ) == 0.2
    assert headline_polarity(
        "Honeywell helping Dangote build world\u2019s largest single-train refinery in Kenya"
    ) == 0.2
    assert headline_polarity(
        "ZBRA vs. HON: Which Industrial Automation Stock is a Better Pick?"
    ) == 0.0
    assert headline_polarity("Revenue declines $1 billion after demand slump") == -0.5


def test_live_headline_gaps():
    assert headline_polarity("T-Mobile price target lowered to $196 from $230") == -0.5
    assert headline_polarity(
        "BofA Adjusts Price Target on Take-Two to $330 From $368, Keeps Buy Rating"
    ) == -0.5
    assert headline_polarity("Disappointing results and guidance cut") == -0.5
    assert headline_polarity("How Raised Earnings Guidance Will Impact the stock") == 0.5
    assert headline_polarity("SoFi Raises Full-Year Guidance") == 0.5
    assert headline_polarity("Can the stock jump 40%?") == 0.2
    assert headline_polarity("Dogecoin drops 4%") == -0.5
    assert headline_polarity("HBAR token pumps 96%") == 0.2
    assert headline_polarity("Buybacks reach 88M shares") == 0.2
    assert headline_polarity("One final sell-off before the correction ends") == -0.5
    assert headline_polarity('Stock rated "reduce" by analysts') == -0.5
    assert headline_polarity("Court revives elder abuse case against the bank") == -1.0
    assert headline_polarity("Potential decline toward 213.5") == -0.5
    assert headline_polarity("The stock has fallen 10%") == -0.5
    assert headline_polarity("Price target raised to $525 from $518") == 0.5


def test_live_screen_headline_gaps():
    assert headline_polarity("Prediction: Dogecoin Will Plunge to Under a Penny in 2026") == -0.5
    assert headline_polarity("Bitcoin Tops $37,000 after a quiet session") < 0.5
    assert headline_polarity("Ethereum Edges Lower; Synthetix Among Top Losers") == -0.5
    assert headline_polarity("Stock Fair Value Edges Lower After Analyst Target Revisions") == -0.5
    assert headline_polarity("Why Cameco (CCJ) Dipped More Than Broader Market Today") == -0.5
    assert headline_polarity("Kinross Gold shares tumble on weaker outlook") == -0.5
    assert headline_polarity("Cameco Has Lost 38% in 6 Months") == -0.5
    assert headline_polarity("Cameco Stock Is Down 36% From Its All-Time High") == -0.5
    assert headline_polarity("Bernstein cuts Charter Communications stock target from USD 150 to USD 120") == -0.5
    assert headline_polarity("How Recent Target Cuts Are Reshaping The Story For ITV") == -0.5
    assert headline_polarity("Upstart Holdings Inc (UPST) PT Lowered to $18 at Citizens") == -0.5
    assert headline_polarity("Baird cuts Eaton target to USD 485.00") == -0.5
    assert headline_polarity("Royal Bank of Canada raised target for Eaton stock to USD 526") == 0.5
    assert headline_polarity("Deutsche Bank raises Eaton stock target from USD 493.00 to USD 521.00") == 0.5
    assert headline_polarity("Goldman Sachs Adjusts Price Target on Northrop Grumman to $525 From $518") == 0.5
    assert headline_polarity("Prudential buys back 3,990,793 shares") == 0.2
    assert headline_polarity("Entain set to axe a fifth of customer care jobs globally") == -0.5
    assert headline_polarity("How Revenue Recognition Lawsuits At Gildan Have Changed Its Story") == -1.0
    assert headline_polarity("Lululemon (LULU) Faces Securities Investigations") == -0.5
    assert headline_polarity("Weekly Recap: UPS job, facility cuts") == -0.5
    assert headline_polarity("A Look At Premium Brands After Recent Share Price Weakness") == -0.5
    assert headline_polarity("Brookfield Pulls Back As Valuation Questions Grow") == -0.5


def test_second_scan_phrases():
    assert headline_polarity("Synthetix to discontinue usage of SNX protocol") == -0.5
    assert headline_polarity("United Parcel Service Inc Stock Warning Signs") == -0.5
    assert headline_polarity("How Low Can Charter Communications Stock Go?") == -0.5
    assert headline_polarity("T-Mobile Shares Lose Signal as SpaceX seeks cell sites") == -0.5
    assert headline_polarity("Dominion Energy combats salt contamination issue") == -0.5
    assert headline_polarity("Entain warn over hit from Brazilian gambling ban") == -0.5
    assert headline_polarity("urge regulators to reject Dominion-NextEra merger") == -0.5
    assert headline_polarity("Gildan Faces Investor Suit Over Alleged Channel Stuffing") == -1.0
    assert headline_polarity("Prudential profit to rise 8%") == 0.2
    assert headline_polarity("Adjusted Earnings, Revenues Rise") == 0.2
    assert headline_polarity("Goldman Sachs raised to Buy at Freedom Broker") == 0.5
    assert headline_polarity("Brings A Third Guidance Raise") == 0.5
    assert headline_polarity("Analysts Boost Their Forecasts Following Upbeat Q3 Earnings") == 0.5
    assert headline_polarity("Plans a shareholder return") == 0.2
    assert headline_polarity("Bullish On Outlook") == 0.2
    assert headline_polarity("Dogecoin Hits 2-Month High") == 0.2
    assert headline_polarity("Securing $200 Million in Funding") == 0.2
    assert headline_polarity("HBAR Foundation to give $155M in grants") == 0.2


def test_third_scan_phrases():
    assert headline_polarity("Lowe's Companies $LOW Shares Bought by Assenagon") == 0.2
    assert headline_polarity("Shares in General Dynamics Purchased by Mirae Asset") == 0.2
    assert headline_polarity("McDonald's Stock Acquired by Sowell Financial") == 0.2
    assert headline_polarity("Boeing Shares Sold by Investment House LLC") == -0.5
    assert headline_polarity("Position Lessened by Fragasso Financial Advisors") == -0.5
    assert headline_polarity("PepsiCo Cut 112 Jobs at a bottling plant") == -0.5
    assert headline_polarity("American Express plans to cut workforce by 5%") == -0.5
    assert headline_polarity("What Telus's Dividend Cut Can Teach Us") == -0.5
    assert headline_polarity("Coinbase downgraded to Sell equivalent at Morgan Stanley") == -0.5
    assert headline_polarity("UBS Reaffirms Their Sell Rating on National Grid") == -0.5
    assert headline_polarity("Bank Decreases Stake in O'Reilly Automotive") == -0.5
    assert headline_polarity("Full-Year Revenue Outlook Lags Consensus") == -0.5
    assert headline_polarity("Morgan Stanley cuts the rating on weaker earnings outlook") == -0.5
    assert headline_polarity("Home Depot Stock Moved Up by 4.07%") == 0.2
    assert headline_polarity("American Tower REIT Is Maintained at Overweight by Barclays") == 0.2
    assert headline_polarity("Home Depot Names Steves & Sons Partner of the Year") == 0.2
    assert headline_polarity("Cameco reports Q3 profit, revenue edges up from year ago") == 0.2
    assert headline_polarity("Southern Company restores power after the hurricane") == 0.2
    assert headline_polarity("Wells Fargo Remains a Buy on Dominion Energy") == 0.2
    assert headline_polarity("National Grid lifts outlook as the stock trades higher") == 0.5
    assert headline_polarity("Idexx Laboratories Beats Q3 Earnings and Revenue Estimates") == 0.5
    assert headline_polarity("American Express is raising its profit forecast") == 0.5
    assert headline_polarity("DA Davidson upgrades The Trade Desk to Hold") == 0.5
    assert headline_polarity("Prologis Raised to Outperform From Market Perform") == 0.5
    assert headline_polarity(
        "American Express profits rise; company plans to cut workforce by 5%"
    ) == -0.5


def test_current_site_headlines():
    assert headline_polarity(
        "CenterBook Partners LP Acquires 68,878 Shares of Bank of America Corporation $BAC"
    ) == 0.2
    assert headline_polarity(
        "Bank of America Corporation $BAC Stake Raised by Alta Advisers Ltd"
    ) == 0.2
    assert headline_polarity(
        "BANK OF AMERICA ALERT: Bragar Eagel & Squire, P.C. Reminds"
    ) == -0.5
    assert headline_polarity(
        "General Dynamics (GD) Lifts Guidance Again, Is The Stock Still Cheap?"
    ) == 0.5
    assert headline_polarity(
        "Associated Banc Corp Purchases New Position in Verizon Communications Inc. $VZ"
    ) == 0.2
    assert headline_polarity(
        "Kestra Advisory Services LLC Increases Holdings"
    ) == 0.2
    assert headline_polarity(
        "On November 3, General Dynamics (GD) counsel sold 12,994 shares"
    ) == -0.5
    assert headline_polarity("UPS Announces Quarterly Dividend") == 0.2
    assert headline_polarity("Waste Management stock slips 1.05% from Friday morning") == -0.5
    assert headline_polarity(
        "Waste Management suspends Indian River County collection Tuesday due to flooding"
    ) == -0.5
    assert headline_polarity("Form 4 Bank of America Corp For: 6 November") == 0.0
    assert headline_polarity("Bank of America Corporation (BAC-PM) Seasonal Returns Chart") == 0.0
    assert headline_polarity(
        "Coinbase has been battered over the past month. Morgan Stanley says steer clear"
    ) == -0.5
    assert headline_polarity(
        "Cadence Design Systems stock breaks below its two hundred day moving average"
    ) == -0.5
    assert headline_polarity(
        "Charter Continues to Lose Internet, Video Customers"
    ) == -0.5
    assert headline_polarity("Emera Incorporated (EMA) Tops Q3 EPS by 16c") == 0.5
    assert headline_polarity(
        "China's bank commission rules cut Prudential's mainland profit outlook"
    ) == -0.5
    assert headline_polarity(
        "Enbridge Reports Strong Third Quarter Results and Reaffirms 2026 Financial Guidance"
    ) == 0.5
    assert headline_polarity("Eaton Reports Record $8.9 Billion in Third-Quarter Sales") == 0.2
    assert headline_polarity("Honeywell Analysis - Is HON Headed Higher?") == 0.2
    assert headline_polarity(
        "Motley Fool: Should You Buy Dogecoin While It's Below $1?"
    ) == 0.0
    assert headline_polarity(
        "Elon Musk's Latest Move Could Send Dogecoin Soaring"
    ) == 0.2
    assert headline_polarity(
        "Algonquin Power & Utilities Corp. Advances +2.01% as shares trade higher"
    ) == 0.2
    assert headline_polarity(
        "Celestica Announces TSX Acceptance of Normal Course Issuer Bid"
    ) == 0.2


def test_finbert_style_financial_phrases():
    assert headline_polarity("Nokia profit rose in the third quarter") == 0.5
    assert headline_polarity("Sales increased and order intake improved") == 0.5
    assert headline_polarity("The company issued a profit warning") == -0.5
    assert headline_polarity("Net income fell after a write-down") == -0.5
    assert headline_polarity("Supplier signed an agreement for a new contract") == 0.2


def test_volatility_surge_is_not_a_boost():
    score = headline_polarity("Implied Volatility Surging for Kinross Gold Stock Options")
    assert score < 0.2


def test_keywords_do_not_fire_on_the_wrong_meaning():
    assert headline_polarity("Results look fine heading into the fall") > -0.5
    assert headline_polarity("The chief executive declined to comment") == 0.0
    assert headline_polarity("Costs rose faster than sales") == -0.5
    assert headline_polarity("Reports net income of $2 billion") != 0.5
    assert headline_polarity("Order intake was steady") != 0.5
    assert headline_polarity("Mirae Asset Purchases 26,029 Shares of Celestica") == 0.2
    assert headline_polarity("Regulators impose a $5 million fine") == -1.0


def test_flat_headline_uses_provider_ticker_score():
    title = "Celestica Inc. (CLS:CA) Analysts Update Stock Forecasts"
    assert headline_polarity(title) == 0.0
    assert story_polarity(title, ticker_sentiment=0.35) == 0.35
    assert story_polarity(
        title,
        "Analysts maintained Buy ratings and set higher price targets.",
        ticker_sentiment=-0.4,
    ) == 0.2
    assert story_polarity("Company faces a securities fraud lawsuit", ticker_sentiment=0.8) == -1.0


def test_summary_cannot_pin_a_clear_or_flat_title_at_minus_one():
    pops = "Coinbase Stock Pops: What's Going On?"
    assert headline_polarity(pops) == 0.0
    assert story_polarity(pops, "Exchange faces a criminal probe after a hack") == 0.0
    assert story_polarity(
        pops,
        "Shares are trading higher after a partnership.",
        ticker_sentiment=-1.0,
    ) == 0.2
    battered = "Coinbase has been battered over the past month. Morgan Stanley says steer clear"
    assert story_polarity(battered, "Regulators open a fraud lawsuit") == headline_polarity(battered)
    assert story_polarity(
        "Morgan Stanley cuts Coinbase stock rating on weaker earnings outlook",
        "The note cites a securities fraud probe.",
    ) == -0.5


def test_gildan_average_is_bearish():
    headlines = [
        "DEADLINE ALERT for Gildan: Securities Fraud Class Actions",
        "Gildan Securities Class Action Deadline",
        "Gildan Securities Class Action Lawsuit",
        "Gildan stock falls Tuesday, underperforms market",
        "Gildan stock price target cut to $64",
    ]
    result = SentimentEngine().analyze_headlines("GIL", headlines)
    assert result["label"] == "bearish"
    assert result["score"] <= -0.5


if __name__ == "__main__":
    test_severe_legal_language_scores_minus_one()
    test_target_cut_beats_a_buy_rating()
    test_strong_and_mild_positive_phrases()
    test_phrases_from_other_screens()
    test_honeywell_project_wins_are_mild_positive()
    test_live_headline_gaps()
    test_live_screen_headline_gaps()
    test_second_scan_phrases()
    test_third_scan_phrases()
    test_current_site_headlines()
    test_finbert_style_financial_phrases()
    test_volatility_surge_is_not_a_boost()
    test_keywords_do_not_fire_on_the_wrong_meaning()
    test_flat_headline_uses_provider_ticker_score()
    test_summary_cannot_pin_a_clear_or_flat_title_at_minus_one()
    test_gildan_average_is_bearish()
    print("ok")
