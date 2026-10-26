(function () {
  var face = document.getElementById("scoop-mood-feed-face");
  if (!face) {
    face = document.createElement("style");
    face.id = "scoop-mood-feed-face";
    face.textContent = [
      "html[data-scoop-analyze-active='1'] .scoop-mood-summary { margin-bottom: 0 !important; }",
      "html[data-scoop-analyze-active='1'] [data-testid='stMarkdownContainer']:has(.scoop-mood-summary) { margin-bottom: 0.85rem !important; }",
      "html[data-scoop-analyze-active='1'] [data-testid='stMarkdownContainer']:has(.mood-feed) { margin-bottom: 0.75rem !important; }",
      "html[data-scoop-analyze-active='1'] .mood-feed { margin-top: 0 !important; margin-bottom: 0 !important; overflow-x: hidden !important; overflow-y: auto !important; max-height: none !important; }",
      "@media (min-width: 1367px) { html[data-scoop-analyze-active='1'] [data-testid='stMarkdownContainer']:has(.scoop-mood-summary) { margin-bottom: 20px !important; } html[data-scoop-analyze-active='1'] .mood-feed { margin-top: 0 !important; margin-bottom: 0 !important; overflow-y: auto !important; } }",
      "html[data-scoop-analyze-active='1'] .mood-feed table { border-collapse: separate !important; border-spacing: 0 !important; width: 100% !important; }",
      "html[data-scoop-analyze-active='1'] .mood-feed thead th { position: sticky !important; top: 0 !important; z-index: 4 !important; background: #0f172a !important; color: #f8fafc !important; }"
    ].join("\n");
    document.body.appendChild(face);
  }
  var navFace = document.getElementById("scoop-analyze-market-nav");
  if (!navFace) {
    navFace = document.createElement("style");
    navFace.id = "scoop-analyze-market-nav";
    navFace.textContent = [
      "@media (min-width: 1367px) { html[data-scoop-analyze-active='1'] a.scoop-analyze-back, html[data-scoop-desktop-layout='1'][data-scoop-analyze-active='1'] a.scoop-analyze-back { display: inline-flex !important; font-size: 1.85rem !important; font-weight: 800 !important; line-height: 1.2 !important; padding: 0.95rem 1.45rem !important; min-height: 3.6rem !important; gap: 0.45rem !important; } }",
      "html[data-scoop-analyze-active='1'] [data-testid='stElementContainer']:has(a.scoop-analyze-back),",
      "html[data-scoop-analyze-active='1'] [data-testid='element-container']:has(a.scoop-analyze-back) { display: block !important; }",
      "@media (min-width: 1367px) {",
      "html[data-scoop-analyze-active='1'] [data-testid='stSidebar'] [data-testid='stPageLink'][data-scoop-nav-active] { background: transparent !important; border-color: transparent !important; box-shadow: none !important; }",
      "html[data-scoop-analyze-active='1'] [data-testid='stSidebar'] [data-testid='stPageLink'][data-scoop-nav-active] a { background-color: rgba(151, 166, 195, 0.15) !important; border-radius: 0.5rem !important; box-shadow: none !important; }",
      "html[data-scoop-analyze-active='1'] [data-testid='stSidebar'] [data-testid='stPageLink'][data-scoop-nav-active] a:hover { background-color: rgba(151, 166, 195, 0.25) !important; }",
      "html:not([data-scoop-theme='dark'])[data-scoop-analyze-active='1'] [data-testid='stSidebar'] [data-testid='stPageLink'][data-scoop-nav-active] a p,",
      "html:not([data-scoop-theme='dark'])[data-scoop-analyze-active='1'] [data-testid='stSidebar'] [data-testid='stPageLink'][data-scoop-nav-active] span { background: transparent !important; color: rgb(49, 51, 63) !important; }",
      "html:not([data-scoop-theme='dark'])[data-scoop-analyze-active='1'] [data-testid='stSidebar'] [data-testid='stPageLink'][data-scoop-nav-active] a { color: rgb(49, 51, 63) !important; background-color: rgba(151, 166, 195, 0.15) !important; }",
      "html[data-scoop-theme='dark'][data-scoop-analyze-active='1'] [data-testid='stSidebar'] [data-testid='stPageLink'][data-scoop-nav-active] a p,",
      "html[data-scoop-theme='dark'][data-scoop-analyze-active='1'] [data-testid='stSidebar'] [data-testid='stPageLink'][data-scoop-nav-active] span { background: transparent !important; color: rgb(250, 250, 250) !important; }",
      "html[data-scoop-theme='dark'][data-scoop-analyze-active='1'] [data-testid='stSidebar'] [data-testid='stPageLink'][data-scoop-nav-active] a { color: rgb(250, 250, 250) !important; background-color: rgba(151, 166, 195, 0.15) !important; }",
      "}"
    ].join("\n");
    document.body.appendChild(navFace);
  }
  var LABELS = ["7 days", "30 days", "90 days", "180 days", "1 year", "2 years"];
  var DAYS = [7, 30, 90, 180, 365, 730];
  var series = [];
  var currentAsset = null;
  var showUsd = false;

  function usdStorageKey(asset) {
    if (!asset) return "";
    var market = String(asset.market || "");
    if (asset.currency === "GBP" || market.indexOf("LSE") !== -1) return "scoop-usd-LSE";
    if (asset.currency === "CAD" || market.indexOf("TSX") !== -1) return "scoop-usd-TSX";
    return "";
  }

  function readShowUsd(asset) {
    var key = usdStorageKey(asset);
    if (!key) return false;
    try {
      var value = sessionStorage.getItem(key);
      return value === "usd" || value === "1";
    } catch (err) { return false; }
  }

  function writeShowUsd(asset, on) {
    var key = usdStorageKey(asset);
    if (!key) return;
    try { sessionStorage.setItem(key, on ? "usd" : "local"); } catch (err) {}
  }

  function sliderRoot() {
    return document.querySelector('[data-testid="stSlider"]');
  }

  function draw(days) {
    var host = document.querySelector(".js-plotly-plot .svg-container");
    if (!host || !series.length) return;
    var svg = host.querySelector("svg.main-svg");
    if (svg) svg.style.display = "none";
    var canvas = host.querySelector("canvas.scoop-price-canvas");
    if (!canvas) {
      canvas = document.createElement("canvas");
      canvas.className = "scoop-price-canvas";
      canvas.style.display = "block";
      canvas.style.width = "100%";
      canvas.style.height = (window.innerWidth >= 1367 ? "500px" : "500px");
      host.style.width = "100%";
      host.style.height = canvas.style.height;
      host.appendChild(canvas);
    }
    canvas.style.height = "500px";
    host.style.height = "500px";
    var slice = series.slice(-Math.min(days, series.length));
    var dpr = window.devicePixelRatio || 1;
    var w = host.clientWidth || 640;
    var h = 500;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    var ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var dark = document.documentElement.getAttribute("data-scoop-theme") === "dark";
    var bg = dark ? "#0f172a" : "#ffffff";
    var grid = dark ? "rgba(148,163,184,0.25)" : "rgba(51,65,85,0.18)";
    var text = dark ? "#e2e8f0" : "#334155";
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, w, h);
    var tickPx = window.innerWidth >= 1367 ? 40 : 26;
    var narrow = window.innerWidth < 1367;
    var datePx = narrow ? 24 : 28;
    var prices = slice.map(function (row) { return shownPrice(row.p); });
    var min = Math.min.apply(null, prices);
    var max = Math.max.apply(null, prices);
    if (min === max) { min -= 1; max += 1; }
    var span = max - min;
    var head = narrow ? 0.22 : 0.08;
    min -= span * head;
    max += span * head;
    ctx.font = tickPx + "px \"Source Sans 3\", \"Source Sans Pro\", sans-serif";
    var labelW = 0;
    for (var probe = 0; probe <= 4; probe++) {
      var sample = min + ((max - min) * probe) / 4;
      labelW = Math.max(labelW, ctx.measureText(formatMoney(sample)).width);
    }
    var padL = Math.ceil(labelW + (narrow ? 18 : 28));
    var padR = narrow ? 18 : 28;
    var padT = narrow ? Math.ceil(tickPx + 36) : 48;
    var padB = narrow ? 56 : 72;
    var plotW = Math.max(10, w - padL - padR);
    var plotH = h - padT - padB;
    function xAt(i) { return padL + (slice.length === 1 ? plotW / 2 : (i / (slice.length - 1)) * plotW); }
    function yAt(p) { return padT + (1 - (p - min) / (max - min)) * plotH; }
    ctx.strokeStyle = grid;
    ctx.lineWidth = 1;
    ctx.fillStyle = text;
    ctx.textAlign = "right";
    ctx.textBaseline = "middle";
    for (var g = 0; g <= 4; g++) {
      var val = min + ((max - min) * g) / 4;
      var y = yAt(val);
      ctx.beginPath();
      ctx.moveTo(padL, y);
      ctx.lineTo(padL + plotW, y);
      ctx.stroke();
      ctx.fillText(formatMoney(val), padL - 8, y);
    }
    ctx.font = datePx + "px \"Source Sans 3\", \"Source Sans Pro\", sans-serif";
    ctx.textBaseline = "top";
    var tickCount = Math.min(narrow ? 2 : 3, slice.length);
    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    for (var t = 0; t < tickCount; t++) {
      var idx = tickCount === 1 ? 0 : Math.round((t / (tickCount - 1)) * (slice.length - 1));
      var x = xAt(idx);
      var raw = slice[idx].d.slice(0, 10);
      var label = raw;
      if (narrow) {
        var parts = raw.split("-");
        label = months[Number(parts[1]) - 1] + " " + parts[0];
      }
      ctx.textAlign = "center";
      if (t === 0) { ctx.textAlign = "left"; x = padL; }
      if (t === tickCount - 1) { ctx.textAlign = "right"; x = padL + plotW; }
      ctx.fillText(label, x, padT + plotH + 10);
    }
    ctx.beginPath();
    slice.forEach(function (row, i) {
      var x = xAt(i), y = yAt(shownPrice(row.p));
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.strokeStyle = "#4ade80";
    ctx.lineWidth = 2;
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.stroke();
    var last = slice[slice.length - 1];
    ctx.fillStyle = "#4ade80";
    ctx.beginPath();
    ctx.arc(xAt(slice.length - 1), yAt(shownPrice(last.p)), slice.length < 2 ? 7 : 4, 0, Math.PI * 2);
    ctx.fill();
    canvas._slice = slice;
    canvas._map = { padL: padL, plotW: plotW, xAt: xAt };
    fitHeadlines();
  }

  function fitHeadlines() {
    var feed = document.querySelector(".mood-feed");
    if (window.innerWidth >= 1367) {
      if (!feed) return;
      var mood = document.querySelector(".scoop-mood-summary");
      var chart = document.querySelector("canvas.scoop-price-canvas") || document.querySelector('[data-testid="stPlotlyChart"]');
      if (!mood || !chart) return;
      feed.style.setProperty("margin-top", "0px", "important");
      feed.style.setProperty("margin-bottom", "0px", "important");
      var gapNow = feed.getBoundingClientRect().top - mood.getBoundingClientRect().bottom;
      feed.style.setProperty("margin-top", (20 - gapNow) + "px", "important");
      var top = mood.getBoundingClientRect().bottom + 20;
      var h = Math.round(chart.getBoundingClientRect().bottom - top);
      if (h < 220) h = 220;
      var px = h + "px";
      feed.style.setProperty("height", px, "important");
      feed.style.setProperty("max-height", px, "important");
      feed.style.setProperty("overflow-y", "auto", "important");
      return;
    }
    var foot = document.querySelector(".disclaimer-footer");
    if (!feed || !foot) return;
    var gap = 16;
    var rect = feed.getBoundingClientRect();
    var footRect = foot.getBoundingClientRect();
    var padNow = footRect.top - rect.bottom;
    if (padNow > gap - 4 && padNow < gap + 28 && rect.height > 200) return;
    var footH = footRect.height || 72;
    var anchor = rect.top < 8 ? 8 : rect.top;
    var h = window.innerHeight - footH - gap - anchor;
    if (h < 220) h = 220;
    var slack = footRect.top - rect.bottom - gap;
    if (feed.dataset.scoopSlack !== "skip" && slack > 12) {
      var trial = rect.height + slack;
      var before = footRect.top;
      feed.style.setProperty("height", Math.round(trial) + "px", "important");
      feed.style.setProperty("max-height", Math.round(trial) + "px", "important");
      if (foot.getBoundingClientRect().top - before > 4) {
        feed.dataset.scoopSlack = "skip";
      } else {
        h = trial;
      }
    }
    var px = Math.round(h) + "px";
    if (feed.style.height === px) return;
    feed.style.setProperty("height", px, "important");
    feed.style.setProperty("max-height", px, "important");
    feed.style.setProperty("overflow-y", "auto", "important");
  }

  function setIndex(i) {
    var root = sliderRoot();
    if (!root) return;
    i = Math.max(0, Math.min(LABELS.length - 1, i));
    var input = root.querySelector('input[type="range"]');
    var thumb = root.querySelector('[data-testid="stSliderThumbValue"]');
    var wrap = thumb && thumb.parentElement;
    if (input) {
      input.value = String(i);
      input.setAttribute("aria-valuetext", LABELS[i]);
    }
    if (wrap) wrap.style.left = (i / (LABELS.length - 1)) * 100 + "%";
    if (thumb) {
      var p = thumb.querySelector("p");
      if (p) p.textContent = LABELS[i];
    }
    placeRangeLabel(LABELS[i]);
    root.querySelectorAll(".scoop-range-dot").forEach(function (dot, n) {
      dot.classList.toggle("scoop-range-dot-on", n === i);
    });
    draw(DAYS[i]);
  }

  function placeRangeLabel(text) {
    var heading = document.querySelector("h3.search-price-chart-heading");
    if (!heading) return;
    var label = document.getElementById("scoop-range-end-label");
    if (!label) {
      label = document.createElement("div");
      label.id = "scoop-range-end-label";
      heading.parentElement.insertBefore(label, heading);
    }
    label.textContent = text;
  }

  function bindSlider() {
    var root = sliderRoot();
    if (!root || root.dataset.scoopBound) return;
    root.dataset.scoopBound = "1";
    var track = root.querySelector('[data-orientation="horizontal"]');
    if (!track) return;
    LABELS.forEach(function (label, i) {
      var dot = document.createElement("button");
      dot.type = "button";
      dot.className = "scoop-range-dot";
      dot.style.left = (i / (LABELS.length - 1)) * 100 + "%";
      dot.setAttribute("aria-label", label);
      dot.addEventListener("pointerdown", function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        setIndex(i);
      });
      track.appendChild(dot);
    });
    function fromEvent(ev) {
      var rect = track.getBoundingClientRect();
      var ratio = rect.width ? (ev.clientX - rect.left) / rect.width : 0;
      setIndex(Math.round(Math.max(0, Math.min(1, ratio)) * (LABELS.length - 1)));
    }
    track.addEventListener("pointerdown", function (ev) {
      track.setPointerCapture(ev.pointerId);
      fromEvent(ev);
    });
    track.addEventListener("pointermove", function (ev) {
      if (ev.buttons) fromEvent(ev);
    });
    var input = root.querySelector('input[type="range"]');
    if (input) {
      input.addEventListener("input", function () { setIndex(Number(input.value)); });
      input.addEventListener("change", function () { setIndex(Number(input.value)); });
    }
  }

  var snapshotUpdated = "";

  function noteLastUpdate() {
    var caps = document.querySelectorAll('[data-testid="stMain"] [data-testid="stCaptionContainer"] p');
    if (!caps.length || !snapshotUpdated) return;
    var dark = document.documentElement.getAttribute("data-scoop-theme") === "dark";
    caps.forEach(function (cap) {
      if (!cap.dataset.scoopOriginal) cap.dataset.scoopOriginal = cap.textContent;
      if (cap.dataset.scoopOriginal.indexOf("Last updated") !== 0) return;
      cap.innerHTML = "Last updated: <b>" + snapshotUpdated + "</b>";
      cap.style.textAlign = "right";
      cap.style.display = "block";
      cap.style.width = "100%";
      cap.style.fontWeight = "400";
      cap.style.fontSize = "1.6rem";
      cap.style.lineHeight = "1.75";
      cap.style.margin = "0.4rem 0 0.9rem";
      cap.style.color = dark ? "#e2e8f0" : "#64748b";
      var box = cap.closest('[data-testid="stCaptionContainer"]');
      if (box) box.style.textAlign = "right";
    });
  }

  function assetTicker() {
    var params = new URLSearchParams(window.location.search);
    var ticker = params.get("ticker") || "PEP";
    try { ticker = decodeURIComponent(ticker.replace(/\+/g, " ")); } catch (err) {}
    return ticker;
  }

  function lookupAsset(catalog, ticker) {
    var upper = String(ticker || "").toUpperCase();
    var exact = catalog[ticker] || catalog[upper];
    if (exact) return exact;
    var bare = upper.replace(/-USD$/, "").replace(/=F$/, "");
    var keys = [bare, bare + "-USD", bare + "=F"];
    var best = null;
    keys.forEach(function (key) {
      var asset = key && catalog[key];
      if (!asset) return;
      if (!best || String(asset.updated || "") > String(best.updated || "")) best = asset;
    });
    return best || catalog.PEP;
  }

  function shownPrice(value) {
    var amount = Number(value);
    if (!currentAsset || !currentAsset.currency) return amount;
    var local = amount * (Number(currentAsset.scale) || 1);
    if (showUsd) return local * (Number(currentAsset.fx) || 1);
    return local;
  }

  function formatMoney(value) {
    if (value == null || isNaN(Number(value))) return "—";
    var prefix = "$";
    if (currentAsset && currentAsset.currency && !showUsd) {
      prefix = currentAsset.currency === "GBP" ? "£" : "C$";
    }
    return prefix + Number(value).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function money(value) {
    return formatMoney(shownPrice(value));
  }

  function currencyStorageKey(code) {
    if (code === "GBP") return "scoop-usd-LSE";
    if (code === "CAD") return "scoop-usd-TSX";
    return "";
  }

  function readShowUsd(code) {
    var key = currencyStorageKey(code);
    if (!key) return false;
    try { return localStorage.getItem(key) === "usd"; } catch (err) { return false; }
  }

  function writeShowUsd(code, usd) {
    var key = currencyStorageKey(code);
    if (!key) return;
    try { localStorage.setItem(key, usd ? "usd" : "local"); } catch (err) {}
  }

  function chooseCurrency(usd) {
    showUsd = usd;
    writeShowUsd(currentAsset && currentAsset.currency, usd);
    var button = document.querySelector(".scoop-currency-switch");
    if (button) {
      button.setAttribute("aria-pressed", usd ? "true" : "false");
      button.setAttribute("aria-label", usd ? "Show prices in local currency" : "Show prices in USD");
    }
    applyAsset(currentAsset);
    var input = sliderRoot() && sliderRoot().querySelector('input[type="range"]');
    draw(DAYS[input ? Number(input.value) : 0]);
  }

  function mountCurrencySwitch() {
    if (!document.getElementById("scoop-currency-switch")) {
      var style = document.createElement("style");
      style.id = "scoop-currency-switch";
      style.textContent = ".scoop-currency{display:flex;align-items:center;gap:.45rem;width:fit-content;margin:.4rem 0 .8rem}.scoop-currency .currency-abbrev{position:relative !important;font-size:1.45rem;font-weight:700;letter-spacing:.04em;border-bottom:1px dashed currentColor;line-height:1.2;cursor:help}.scoop-currency .currency-abbrev>.tip-text{display:none !important;visibility:hidden !important;opacity:0 !important;position:absolute !important;left:0 !important;right:auto !important;bottom:calc(100% + 10px) !important;top:auto !important;transform:none !important;z-index:100002 !important;width:max-content !important;min-width:0 !important;max-width:16rem !important;height:auto !important;padding:14px 18px !important;font-family:Source Sans,sans-serif !important;font-size:1.08rem !important;font-weight:400 !important;line-height:1.42 !important;white-space:normal !important;text-align:left !important;color:#e2e8f0 !important;background:#1e1e2f !important;border:2px solid #22c55e !important;outline:none !important;border-radius:8px !important;box-shadow:0 4px 16px rgba(0,0,0,.45) !important;box-sizing:border-box !important}.scoop-currency .currency-abbrev>.tip-text::before,.scoop-currency .currency-abbrev>.tip-text::after{content:none !important;display:none !important}.scoop-currency .currency-abbrev>.tip-text>.scoop-tip-title{display:block !important;font-weight:700 !important;font-size:1.12rem !important;line-height:1.25 !important;margin:0 0 .45rem !important;padding:0 0 .4rem !important;border-bottom:1px solid rgba(148,163,184,.45) !important;color:#f8fafc !important}.scoop-currency .currency-abbrev:hover>.tip-text,.scoop-currency .currency-abbrev:focus>.tip-text,.scoop-currency .currency-abbrev:focus-within>.tip-text{display:block !important;visibility:visible !important;opacity:1 !important}html[data-scoop-theme=dark] .scoop-currency .currency-abbrev>.tip-text{border-color:#fff !important}.scoop-currency-switch{width:3.15rem;height:1.7rem;border:0;border-radius:999px;background:#e2e8f0;padding:0;position:relative;cursor:pointer}.scoop-currency-switch::after{content:\"\";position:absolute;top:.22rem;left:.22rem;width:1.25rem;height:1.25rem;border-radius:999px;background:#2563eb}.scoop-currency-switch[aria-pressed=true]{background:#22c55e}.scoop-currency-switch[aria-pressed=true]::after{background:#f8fafc;transform:translateX(1.45rem)}";
      document.body.appendChild(style);
    }
    var existing = document.querySelector(".scoop-currency");
    if (!currentAsset || !currentAsset.currency) {
      if (existing) existing.remove();
      showUsd = false;
      return;
    }
    showUsd = readShowUsd(currentAsset.currency);
    if (existing) {
      var held = existing.querySelector(".scoop-currency-switch");
      if (held) held.setAttribute("aria-pressed", showUsd ? "true" : "false");
      return;
    }
    var heading = document.querySelector("h1");
    if (!heading) return;
    var host = heading.closest('[data-testid="stElementContainer"]') || heading.parentElement;
    var code = currentAsset.currency;
    var names = { GBP: "British Pounds", CAD: "Canadian Dollars", USD: "United States Dollars" };
    var box = document.createElement("div");
    box.className = "scoop-currency";
    box.innerHTML = '<span class="tip-wrap currency-abbrev" tabindex="0">' + code + '<span class="tip-text"><div class="scoop-tip-title">' + code + '</div>' + names[code] + '</span></span>'
      + '<button type="button" class="scoop-currency-switch" aria-pressed="' + (showUsd ? "true" : "false") + '" aria-label="' + (showUsd ? "Show prices in local currency" : "Show prices in USD") + '"></button>'
      + '<span class="tip-wrap currency-abbrev" tabindex="0">USD<span class="tip-text"><div class="scoop-tip-title">USD</div>' + names.USD + '</span></span>';
    host.insertAdjacentElement("afterend", box);
    var button = box.querySelector("button");
    button.addEventListener("click", function () {
      chooseCurrency(button.getAttribute("aria-pressed") !== "true");
    });
    var labels = box.querySelectorAll(".currency-abbrev");
    if (labels[0]) labels[0].addEventListener("click", function () { chooseCurrency(false); });
    if (labels[1]) labels[1].addEventListener("click", function () { chooseCurrency(true); });
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"]/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" }[ch];
    });
  }

  function setMetric(label, value, delta) {
    var metrics = document.querySelectorAll('[data-testid="stMetric"]');
    for (var i = 0; i < metrics.length; i++) {
      var name = metrics[i].querySelector('[data-testid="stMetricLabel"] p');
      if (!name || name.textContent.trim() !== label) continue;
      var amount = metrics[i].querySelector('[data-testid="stMetricValue"] p');
      if (amount) amount.textContent = value;
      if (delta != null) {
        var pill = metrics[i].querySelector('[data-testid="stMetricDelta"] div');
        if (pill) pill.textContent = delta;
      }
    }
  }

  function applyAsset(asset) {
    if (!asset) return;
    currentAsset = asset;
    showUsd = readShowUsd(asset);
    mountCurrencySwitch();
    document.title = asset.ticker + " — Analyze";
    var heading = document.querySelector("h1 [data-heading-text]") || document.querySelector("h1");
    if (heading) heading.textContent = asset.ticker + " — Analyze";
    document.querySelectorAll(".scoop-subtitle-text").forEach(function (el) {
      el.textContent = "Ticker: " + asset.ticker;
      var nameEl = el.previousElementSibling;
      if (!nameEl) return;
      nameEl.textContent = "";
      var tip = document.createElement("span");
      tip.className = "scoop-analyze-desktop-tip scoop-selected-name-tip";
      tip.tabIndex = 0;
      tip.appendChild(document.createTextNode(asset.name || asset.ticker));
      if (asset.description) {
        var box = document.createElement("span");
        box.className = "tip-text";
        var label = document.createElement("span");
        label.className = "scoop-analyze-tip-label";
        label.textContent = asset.name || asset.ticker;
        box.appendChild(label);
        box.appendChild(document.createTextNode(asset.description));
        tip.appendChild(box);
      }
      nameEl.appendChild(tip);
    });
    document.querySelectorAll("p, div, span").forEach(function (el) {
      if ((el.textContent || "").trim().indexOf("Analyzing:") !== 0) return;
      if (el.querySelector("p, div")) return;
      el.textContent = "Analyzing: " + asset.ticker;
    });
    var snapshot = String(asset.page || "").split("?")[0].split("/").pop();
    if (snapshot.indexOf(".html") === -1) {
      var marketName = String(asset.market || "");
      if (marketName.indexOf("NASDAQ") !== -1) snapshot = "nasdaq.html";
      else if (marketName.indexOf("LSE") !== -1) snapshot = "lse.html";
      else if (marketName.indexOf("TSX") !== -1) snapshot = "tsx.html";
      else if (marketName.indexOf("Crypto") !== -1) snapshot = "crypto.html";
      else snapshot = "nyse.html";
    }
    var backHref = snapshot + "?scoop_from_analyze=1";
    var backLabel = "← Back to " + (asset.market || "market");
    document.querySelectorAll("a.scoop-analyze-back, a.scoop-mobile-back-home").forEach(function (back) {
      back.setAttribute("href", backHref);
      back.textContent = backLabel;
    });
    var pageFile = String(asset.page || "").split("?")[0].split("/").pop();
    document.querySelectorAll('[data-testid="stSidebar"] [data-testid="stPageLink"]').forEach(function (box) {
      var link = box.querySelector("a");
      var href = link ? String(link.getAttribute("href") || "") : "";
      var file = href.split("?")[0].split("/").pop();
      if (pageFile && file === pageFile) box.setAttribute("data-scoop-nav-active", "");
      else box.removeAttribute("data-scoop-nav-active");
    });
    var change = "—";
    if (asset.series && asset.series.length > 1) {
      var prev = asset.series[asset.series.length - 2].p;
      var last = asset.series[asset.series.length - 1].p;
      if (prev) change = ((last - prev) / prev * 100 >= 0 ? "+" : "") + ((last - prev) / prev * 100).toFixed(2) + "% (24h)";
    }
    var priceLabel = currentAsset && currentAsset.currency && !showUsd
      ? "Live Price (" + currentAsset.currency + ")"
      : "Live Price (USD)";
    document.querySelectorAll('[data-testid="stMetricLabel"] p').forEach(function (name) {
      if (/^Live Price \(/.test(name.textContent.trim())) name.textContent = priceLabel;
    });
    setMetric(priceLabel, money(asset.price), change);
    setMetric("52-Week Low", money(asset.low));
    setMetric("52-Week High", money(asset.high));
    if (asset.price != null && asset.low != null) {
      var abovePct = asset.low ? ((asset.price - asset.low) / asset.low * 100) : 0;
      setMetric("Above 52-Week Low", money(asset.price - asset.low), (abovePct >= 0 ? "+" : "") + abovePct.toFixed(1) + "%");
    }
    if (asset.price != null && asset.high != null) {
      var belowPct = asset.high ? ((asset.price - asset.high) / asset.high * 100) : 0;
      setMetric("Below 52-Week High", money(asset.high - asset.price), belowPct.toFixed(1) + "%");
    }
    if (asset.ticker !== "PEP") {
      document.querySelectorAll("div, p, span").forEach(function (el) {
        if (el.children.length === 0 && /^Hit on /.test((el.textContent || "").trim())) el.textContent = "";
      });
    }
    var body = document.querySelector(".mood-feed tbody");
    if (body && asset.headlines) {
      body.innerHTML = asset.headlines.map(function (item) {
        var score = item.score == null ? "—" : (Number(item.score) > 0 ? "+" : "") + Number(item.score).toFixed(2);
        return "<tr><td>" + escapeHtml(item.title) + "</td><td style=\"text-align:right\">" + score + "</td><td style=\"text-align:center\"><a href=\"" + escapeHtml(item.href) + "\" target=\"_blank\" rel=\"noopener\">Source</a></td></tr>";
      }).join("");
      var values = asset.headlines.map(function (item) { return Number(item.score); }).filter(function (n) { return !isNaN(n); });
      if (values.length) {
        var avg = values.reduce(function (sum, n) { return sum + n; }, 0) / values.length;
        var mood = avg > 0.05 ? "Bullish" : avg < -0.05 ? "Bearish" : "Neutral";
        var signed = (avg > 0 ? "+" : "") + avg.toFixed(4);
        document.querySelectorAll("b").forEach(function (el) {
          var parent = el.parentElement ? el.parentElement.textContent : "";
          if (parent.indexOf("Current Mood") >= 0 && /Neutral|Bullish|Bearish/i.test(el.textContent)) el.textContent = mood;
          if (parent.indexOf("Score:") >= 0 && /^[+-]?\d+\.\d+$/.test(el.textContent.trim())) el.textContent = signed;
        });
      }
    }
    series = asset.series || [];
  }

  function stampSortKey(text) {
    var months = { Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5, Jul: 6, Aug: 7, Sep: 8, Oct: 9, Nov: 10, Dec: 11 };
    var match = String(text || "").trim().match(/^([A-Za-z]{3}) (\d{1,2}), (\d{4})\s+(\d{1,2}):(\d{2}) (AM|PM) CT$/);
    if (!match || months[match[1]] == null) return 0;
    var hour = Number(match[4]) % 12;
    if (match[6] === "PM") hour += 12;
    return Date.UTC(Number(match[3]), months[match[1]], Number(match[2]), hour, Number(match[5]));
  }

  function newestScanStamp(catalog) {
    var best = "";
    var bestKey = 0;
    Object.keys(catalog || {}).forEach(function (key) {
      var asset = catalog[key];
      var stamp = asset && asset.updated;
      var sortKey = stampSortKey(stamp);
      if (sortKey >= bestKey && stamp) {
        best = stamp;
        bestKey = sortKey;
      }
    });
    return best;
  }

  fetch("analyze-assets.json?v=" + Date.now())
    .then(function (res) { return res.json(); })
    .then(function (catalog) {
      snapshotUpdated = newestScanStamp(catalog);
      var ticker = assetTicker();
      applyAsset(lookupAsset(catalog, ticker));
      bindSlider();
      noteLastUpdate();
      var input = sliderRoot() && sliderRoot().querySelector('input[type="range"]');
      setIndex(input ? Number(input.value) : 0);
      window.addEventListener("resize", function () {
        noteLastUpdate();
        var input = sliderRoot() && sliderRoot().querySelector('input[type="range"]');
        draw(DAYS[input ? Number(input.value) : 0]);
        fitHeadlines();
      });
      window.addEventListener("scroll", fitHeadlines, true);
      fitHeadlines();
      new MutationObserver(function () {
        noteLastUpdate();
        var input = sliderRoot() && sliderRoot().querySelector('input[type="range"]');
        draw(DAYS[input ? Number(input.value) : 0]);
      }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-scoop-theme"] });
    });
})();
