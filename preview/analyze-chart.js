(function () {
  var LABELS = ["7 days", "30 days", "90 days", "180 days", "1 year", "2 years"];
  var DAYS = [7, 30, 90, 180, 365, 730];
  var series = [];

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
    var datePx = narrow ? 16 : 28;
    var padL = tickPx >= 40 ? 210 : 108, padR = narrow ? 8 : 28, padT = 36, padB = narrow ? 48 : 72;
    var plotW = Math.max(10, w - padL - padR);
    var plotH = h - padT - padB;
    var prices = slice.map(function (r) { return r.p; });
    var min = Math.min.apply(null, prices);
    var max = Math.max.apply(null, prices);
    if (min === max) { min -= 1; max += 1; }
    var span = max - min;
    min -= span * 0.06;
    max += span * 0.06;
    function xAt(i) { return padL + (slice.length === 1 ? plotW / 2 : (i / (slice.length - 1)) * plotW); }
    function yAt(p) { return padT + (1 - (p - min) / (max - min)) * plotH; }
    ctx.strokeStyle = grid;
    ctx.lineWidth = 1;
    ctx.font = tickPx + "px \"Source Sans 3\", \"Source Sans Pro\", sans-serif";
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
      ctx.fillText("$" + val.toFixed(2), padL - 8, y);
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
      var x = xAt(i), y = yAt(row.p);
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.strokeStyle = "#4ade80";
    ctx.lineWidth = 2;
    ctx.stroke();
    var last = slice[slice.length - 1];
    ctx.fillStyle = "#4ade80";
    ctx.beginPath();
    ctx.arc(xAt(slice.length - 1), yAt(last.p), slice.length < 2 ? 7 : 4, 0, Math.PI * 2);
    ctx.fill();
    canvas._slice = slice;
    canvas._map = { padL: padL, plotW: plotW, xAt: xAt };
    fitHeadlines();
  }

  function fitHeadlines() {
    var feed = document.querySelector(".mood-feed");
    var chart = document.querySelector("canvas.scoop-price-canvas");
    if (!feed) return;
    if (window.innerWidth < 1367 || !chart) {
      feed.style.height = "";
      feed.style.maxHeight = "";
      return;
    }
    var gap = chart.getBoundingClientRect().bottom - feed.getBoundingClientRect().top;
    if (gap < 240) return;
    feed.style.setProperty("height", Math.round(gap) + "px", "important");
    feed.style.setProperty("max-height", Math.round(gap) + "px", "important");
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

  function noteLastUpdate() {
    var caps = document.querySelectorAll('[data-testid="stCaptionContainer"] p');
    if (!caps.length || !series.length) return;
    var parts = series[series.length - 1].d.slice(0, 10).split("-");
    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var stamp = "Last updated " + months[Number(parts[1]) - 1] + " " + Number(parts[2]) + ", " + parts[0] + ", 4:00 PM ET";
    caps.forEach(function (cap) {
      if (!cap.dataset.scoopOriginal) cap.dataset.scoopOriginal = cap.textContent;
      cap.textContent = window.innerWidth >= 1367 ? cap.dataset.scoopOriginal : stamp;
    });
  }

  function assetTicker() {
    var params = new URLSearchParams(window.location.search);
    var ticker = params.get("ticker") || "PEP";
    try { ticker = decodeURIComponent(ticker.replace(/\+/g, " ")); } catch (err) {}
    return ticker;
  }

  function money(value) {
    if (value == null || isNaN(Number(value))) return "—";
    return "$" + Number(value).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
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
        box.textContent = asset.description;
        tip.appendChild(box);
      }
      nameEl.appendChild(tip);
    });
    document.querySelectorAll("p, div, span").forEach(function (el) {
      if ((el.textContent || "").trim().indexOf("Analyzing:") !== 0) return;
      if (el.querySelector("p, div")) return;
      el.textContent = "Analyzing: " + asset.ticker;
    });
    var back = document.querySelector("a.scoop-analyze-back");
    if (back && asset.page) {
      back.setAttribute("href", asset.page + "?scoop_from_analyze=1");
      back.textContent = "← Back to " + asset.market;
    }
    var change = "—";
    if (asset.series && asset.series.length > 1) {
      var prev = asset.series[asset.series.length - 2].p;
      var last = asset.series[asset.series.length - 1].p;
      if (prev) change = ((last - prev) / prev * 100 >= 0 ? "+" : "") + ((last - prev) / prev * 100).toFixed(2) + "% (24h)";
    }
    setMetric("Live Price (USD)", money(asset.price), change);
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

  fetch("analyze-assets.json?v=4")
    .then(function (res) { return res.json(); })
    .then(function (catalog) {
      var ticker = assetTicker();
      applyAsset(catalog[ticker] || catalog.PEP);
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
      new MutationObserver(function () {
        var input = sliderRoot() && sliderRoot().querySelector('input[type="range"]');
        draw(DAYS[input ? Number(input.value) : 0]);
      }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-scoop-theme"] });
    });
})();
