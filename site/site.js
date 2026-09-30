const DATA_ORIGIN = "https://data.thescoop52.com";
const COLUMNS = [
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
];

function money(value) {
  return `$${Number(value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function cell(row, column) {
  const value = row[column];
  if (value == null || value === "") return "";
  if (column === "Price" || column === "52W Low" || column === "52W High") return money(value);
  if (column === "% Above Low") return `${Number(value).toFixed(2)}%`;
  if (column === "Headline Sentiment") return Number(value).toFixed(3);
  if (column === "Headlines") return headlineList(row);
  return String(value);
}

function headlineList(row) {
  const texts = row._headline_texts || [];
  const urls = row._headline_urls || [];
  if (!texts.length) return String(row.Headlines ?? "");
  const items = texts.map((text, index) => {
    const url = urls[index];
    const label = escapeHtml(text);
    return `<li>${url ? `<a href="${escapeHtml(url)}">${label}</a>` : label}</li>`;
  }).join("");
  return `<ol class="headlines">${items}</ol>`;
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function loadScreener(key) {
  const status = document.querySelector("#status");
  const updated = document.querySelector("#updated");
  const table = document.querySelector("#results");
  status.textContent = "Loading snapshot…";
  const response = await fetch(`${DATA_ORIGIN}/screeners/${key}`);
  if (!response.ok) {
    status.textContent = `Snapshot request failed (${response.status}).`;
    return;
  }
  const payload = await response.json();
  const rows = payload.display_results || [];
  const columns = COLUMNS.filter((column) => rows.some((row) => row[column] != null && row[column] !== ""));
  updated.textContent = payload.last_updated_display
    ? `Last updated ${payload.last_updated_display}`
    : "";
  table.innerHTML = `
    <thead><tr>${columns.map((column) => `<th>${escapeHtml(column)}</th>`).join("")}</tr></thead>
    <tbody>
      ${rows.map((row) => `<tr>${columns.map((column) => `<td>${cell(row, column)}</td>`).join("")}</tr>`).join("")}
    </tbody>`;
  status.textContent = `${rows.length} rows`;
}

const page = document.body.dataset.screener;
if (page) loadScreener(page);
