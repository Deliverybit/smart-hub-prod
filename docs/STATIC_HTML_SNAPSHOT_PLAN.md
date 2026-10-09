# Static HTML pages (implement tomorrow)

Goal: visitors see a finished page immediately. Streamlit builds the page on each visit, so screenshots sent from that build do not make the site faster.

## What to build

Save each page as HTML and CSS, using the same markup and styles the site uses now, so phone, tablet, and desktop still look the same. The browser does the resizing. Do not use picture snapshots.

Rebuild those pages every 15 minutes from the Top 10 lists already stored in the database (the same schedule as the data snapshots). The snapshot API reads those lists. It does not photograph the site.

## What stays frozen until the next rebuild

- Logo, title, and description
- Top 10 rows (prices, range, headlines)

## What stays live

Only these three controls are active:

- Market links, with the current market highlighted the way it is now
- Dark-mode switch (one page, both themes, using the existing CSS)
- Consent checkbox and the terms link (the checkbox still records consent)

## What not to do

- Do not serve landing or market pages as stored screenshots. Fixed images do not match every viewport, and a photo cannot toggle theme, highlight a market, or accept consent.
- Do not embed those images inside the Streamlit run. They arrive only after the page has already started building.

## Bookmark — Oct 7, 2026 (not ready to go live)

Stop here. The live site stays on Streamlit. Saved copies are in `preview/` only. The saved-page behavior is now in the live Streamlit app.

Review copies (local only):

- http://127.0.0.1:8766/index.html
- http://127.0.0.1:8766/nyse.html
- http://127.0.0.1:8766/nasdaq.html
- http://127.0.0.1:8766/crypto.html
- http://127.0.0.1:8766/cme.html
- http://127.0.0.1:8766/ice.html
- http://127.0.0.1:8766/terms.html
- http://127.0.0.1:8766/analyze.html

Files are in `preview/`. Rebuild with `admin_tools/build_consent_snapshot.py` from the saved browser dumps. Streamlit on port 8501 still supplies the logo and index-card images.

Working on those copies: same layout as the app, HTML consent checkbox (results hidden until it is checked), dark mode on desktop, tablet, and phone, last-updated time on the gating page, and tablet/phone tooltip taps.

Working on those copies since Oct 5:

- Market tabs link to the other saved pages, with the current market highlighted. Desktop opens `nyse.html`. Phone and tablet open `index.html`.
- Consent posts to `POST /consent`. The Top 10 stays hidden unless that write succeeds.
- Headline counts open the list, and article links open in a new tab. Opening another tip, or scrolling the page, closes the one that is open.
- Tooltip titles: headlines include the company; company and commodity tips use the row name; other columns use the column name. Desktop header tips use the Streamlit box and still show the column name.
- Desktop tips are hover-only. Dark mode slides, the track turns blue when on, and the choice persists from the landing page through later pages.

Done Oct 7:

- Phone and tablet landing page uses the desktop light and dark colors. Logo has no blue outline. Description and links keep a light blue outline. Dark-mode track turns blue when on. Landing text uses Source Sans.

Done Oct 8:

- Live Streamlit app keeps the landing theme on later pages, closes an open tip when another opens or the page scrolls, shows the column name in the desktop header tip box, and turns the dark-mode track blue when it is on.

Done Oct 8 (saved copies):

- `preview/terms.html` and `preview/analyze.html` exist.

Done Oct 9 (saved copies, commit `1362f05`):

- One Analyze page for every listed stock and commodity. The Analyze control opens `analyze.html?ticker=…` on desktop, tablet, and phone. Data is in `preview/analyze-assets.json`. PEP keeps the long price series; the other symbols have 100 daily bars. The chart is a canvas.
- Selected asset shows the company name and ticker. The longer description is a tooltip on the name (`.scoop-selected-name-tip`), with the same hover, tap, scroll, and outside-click behavior as the other Analyze tips.
- Phone and tablet show Live Price and the four 52-week cards, with a thin green border, a small even gap, and full width under 1366px.
- Landing page on phone and tablet has even spacing and a rounded logo box. Logo, title, and dark-mode toggle were left as they were.
- “I agree to the Disclaimer & Terms” is slightly smaller on desktop and tablet. Phone size is unchanged.
- Consent on the saved market pages posts to local `POST /consent` and stays hidden until that write succeeds. `snapshot_api.serve_preview()` on port 8766 serves `preview/` and that route. Plain `python -m http.server` does not.
- A push does not update production. The live site stays on Streamlit.

Still open before any live switch:

- No 15-minute rebuild from the database. Logo and index-card images still depend on the running app.
- Production consent (`https://data.thescoop52.com/consent`) rejected a write from the local preview. The checkbox only succeeds against the local preview server.
- Market-page dark-mode click handling on the live app still differs from the saved pages.
- Cut over only if the saved pages still match. The live site stays on Streamlit until then.
- Left uncommitted on purpose: `admin_tools/_*.py` scratch scripts and `.wrangler/`.
