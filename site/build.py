#!/usr/bin/env python3
"""Static site generator for the IOAI 2026 / GAITE prep hub.
Renders docs/ (GitHub Pages) from content_*.py task definitions."""
import html
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "docs"


# ---------- authoring helpers (used by content files) ----------
def esc(t: str) -> str:
    return html.escape(t, quote=False)


def bubble(role: str, title: str, body: str) -> str:
    """One chat bubble. role: 'user'|'gemma'|'note'|'divider'. Body is plain text, escaped."""
    if role == "divider":
        return f'<div class="chat-divider"><span>{esc(title)}</span></div>'
    if role == "note":
        return f'<div class="chat-note">{esc(body)}</div>'
    who = "YOU" if role == "user" else "GEMMA 4"
    t = f'<span class="bubble-title">{esc(title)}</span>' if title else ""
    return (
        f'<div class="msg {role}"><div class="msg-who">{who}</div>'
        f'<div class="bubble">{t}<pre>{esc(body)}</pre></div></div>'
    )


def chat(*items) -> str:
    """items: tuples of (role, title, body) or (role, title)."""
    parts = []
    for it in items:
        if len(it) == 2:
            parts.append(bubble(it[0], it[1], ""))
        else:
            parts.append(bubble(it[0], it[1], it[2]))
    return '<div class="chat">' + "".join(parts) + "</div>"


def vs(baseline_html: str, solution_html: str) -> str:
    return (
        '<div class="vs-grid">'
        f'<div class="vs-card vs-base"><div class="vs-label">⚠️ The baseline (what you are given)</div>{baseline_html}</div>'
        f'<div class="vs-card vs-soln"><div class="vs-label">✅ The winning approach</div>{solution_html}</div>'
        "</div>"
    )


# ---------- templates ----------
FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,700;0,9..144,900;1,9..144,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">'
)

YEAR_GROUPS = [
    ("2026", "🚨 2026 Home Tasks — the real ones"),
    ("2025h", "2025 At-Home Round"),
    ("2025c", "2025 Contest Days"),
    ("2025g", "2025 GAITE Extras"),
    ("2024", "2024 (1st edition)"),
]


def sidebar(tasks, active_slug=None, depth=1):
    p = "../" * depth
    items = []
    for gid, gname in YEAR_GROUPS:
        group = [t for t in tasks if t["group"] == gid]
        if not group:
            continue
        items.append(f'<div class="nav-group">{gname}</div>')
        for t in group:
            cls = "nav-item active" if t["slug"] == active_slug else "nav-item"
            items.append(
                f'<a class="{cls}" href="{p}tasks/{t["slug"]}.html">'
                f'<span class="nav-emoji">{t["emoji"]}</span>{esc(t["title"])}</a>'
            )
    extra = (
        f'<div class="nav-group">Guides</div>'
        f'<a class="nav-item{" active" if active_slug=="gemma" else ""}" href="{p}gemma.html"><span class="nav-emoji">💬</span>Gemma 4 Playbook</a>'
        f'<a class="nav-item{" active" if active_slug=="plan" else ""}" href="{p}plan.html"><span class="nav-emoji">🗓️</span>30-Day Plan</a>'
    )
    return (
        f'<nav class="sidebar"><a class="brand" href="{p}index.html">IOAI <b>2026</b>'
        f'<span class="brand-sub">GAITE field manual</span></a>'
        + "".join(items) + extra + "</nav>"
    )


def page(title, body, tasks, active=None, depth=1):
    css = "../" * depth + "style.css"
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · IOAI 2026 Field Manual</title>{FONTS}
<link rel="stylesheet" href="{css}"></head>
<body><div class="layout">
{sidebar(tasks, active, depth)}
<main class="content">{body}</main>
</div></body></html>"""


SECTION_ORDER = [
    ("task", "📜", "The task, in plain English"),
    ("baseline", "🔧", "The baseline you're given"),
    ("solution", "🚀", "Baseline vs. solution"),
    ("beginner", "🧒", "Explain it like I'm brand new"),
    ("gemma", "💬", "The Gemma 4 playthrough (2000-token limit)"),
    ("takeaways", "🎯", "Takeaways & what Day 1 might do with this"),
]


def render_task(t, tasks, prev_t, next_t):
    tags = "".join(f'<span class="tag">{esc(x)}</span>' for x in t["tags"])
    secs = []
    for key, ico, heading in SECTION_ORDER:
        if key in t["sections"]:
            secs.append(
                f'<section class="sec"><h2><span class="sec-ico">{ico}</span>{heading}</h2>'
                f'{t["sections"][key]}</section>'
            )
    nav = '<div class="pager">'
    if prev_t:
        nav += f'<a class="pager-link" href="{prev_t["slug"]}.html">← {prev_t["emoji"]} {esc(prev_t["title"])}</a>'
    else:
        nav += "<span></span>"
    if next_t:
        nav += f'<a class="pager-link next" href="{next_t["slug"]}.html">{next_t["emoji"]} {esc(next_t["title"])} →</a>'
    nav += "</div>"
    body = (
        f'<header class="task-head"><div class="crumb">{esc(dict(YEAR_GROUPS)[t["group"]])}</div>'
        f'<h1>{t["emoji"]} {esc(t["title"])}</h1>'
        f'<p class="tagline">{esc(t["one_liner"])}</p>'
        f'<div class="tags">{tags}<span class="tag diff">{esc(t["difficulty"])}</span></div></header>'
        + "".join(secs) + nav
    )
    return page(t["title"], body, tasks, t["slug"], depth=1)


def build(tasks, index_body, gemma_body, plan_body):
    if OUT.exists():
        for p in OUT.iterdir():
            if p.name == "CNAME":
                continue
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    (OUT / "tasks").mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "style.css", OUT / "style.css")
    (OUT / ".nojekyll").write_text("")
    (OUT / "index.html").write_text(page("Home", index_body, tasks, None, depth=0))
    (OUT / "gemma.html").write_text(page("Gemma 4 Playbook", gemma_body, tasks, "gemma", depth=0))
    (OUT / "plan.html").write_text(page("30-Day Plan", plan_body, tasks, "plan", depth=0))
    for i, t in enumerate(tasks):
        prev_t = tasks[i - 1] if i > 0 else None
        next_t = tasks[i + 1] if i < len(tasks) - 1 else None
        (OUT / "tasks" / f'{t["slug"]}.html').write_text(render_task(t, tasks, prev_t, next_t))
    print(f"Built {2 + 1 + len(tasks)} pages -> {OUT}")


if __name__ == "__main__":
    from content_2026 import TASKS_2026
    from content_2025 import TASKS_2025H, TASKS_2025C, TASKS_2025G
    from content_2024 import TASKS_2024
    from content_pages import index_body, gemma_body, plan_body

    TASKS = TASKS_2026 + TASKS_2025H + TASKS_2025C + TASKS_2025G + TASKS_2024
    build(TASKS, index_body(TASKS), gemma_body(), plan_body())
