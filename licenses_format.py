"""Turn NOTICE into Terms-style HTML (headings and body copy, not a code block)."""

from __future__ import annotations

import html
import re


def _is_rule(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and set(stripped) <= {"=", "-"}


def _linkify(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(
        r"(https?://[^\s<]+)",
        r'<a href="\1" target="_blank" rel="noopener noreferrer">\1</a>',
        escaped,
    )


def notice_to_html(notice: str) -> str:
    lines = notice.replace("\r\n", "\n").split("\n")
    parts: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        nxt = lines[i + 1] if i + 1 < n else ""
        if _is_rule(line):
            i += 1
            continue
        if line.strip() and _is_rule(nxt):
            tag = "h2" if set(nxt.strip()) <= {"="} else "h3"
            color = "#e2e8f0" if tag == "h2" else "#60a5fa"
            parts.append(
                f'<{tag} style="color:{color};margin:1.4rem 0 0.7rem 0;">'
                f"{html.escape(line.strip())}</{tag}>"
            )
            i += 2
            continue
        if not line.strip():
            i += 1
            continue
        if line.startswith("  ") or (line.strip() and i + 1 < n and lines[i + 1].startswith("  ")):
            title = html.escape(line.strip())
            details: list[str] = []
            i += 1
            while i < n and lines[i].startswith("  "):
                details.append(lines[i].strip())
                i += 1
            items = "".join(f"<li>{_linkify(item)}</li>" for item in details)
            parts.append(
                f'<p style="margin:0.9rem 0 0.25rem 0;"><strong>{title}</strong></p>'
                f'<ul style="margin:0 0 0.8rem 1.2rem;padding:0;">{items}</ul>'
            )
            continue
        chunk = [line.strip()]
        i += 1
        while i < n and lines[i].strip() and not _is_rule(lines[i]) and not (
            i + 1 < n and _is_rule(lines[i + 1])
        ) and not lines[i].startswith("  "):
            chunk.append(lines[i].strip())
            i += 1
        parts.append(f"<p>{_linkify(' '.join(chunk))}</p>")
    return "".join(parts)
