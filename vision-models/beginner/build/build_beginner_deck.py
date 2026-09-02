#!/usr/bin/env python3
"""Build 'How Machines Learn to See' — beginner deck for IOAI 2026 Section 3.

Audience: 14-18yo with zero coding/AI background, taught by a fellow student.
1920x1080, Viktor profile, WeasyPrint. Run: uv run python build_beginner_deck.py
"""
import json
import html as html_mod
from pathlib import Path

HERE = Path(__file__).parent
A = HERE.parent / "assets"

pix = json.load(open(A / "pixel_grid.json"))["values"]
clip = json.load(open(A / "clip_results.json"))

# ---------------------------------------------------------------- css
CSS = """
@import url("https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;500&display=swap");

@page { size: 1920px 1080px; margin: 0; }
:root {
  --c-ink: #000000; --c-surface: #FFFFFF;
  --c-dim: rgba(0,0,0,0.55); --c-faint: rgba(0,0,0,0.35);
  --c-line: rgba(0,0,0,0.12); --c-fill-subtle: rgba(0,0,0,0.04);
  --font-display: "Satoshi", sans-serif; --font-mono: "Roboto Mono", monospace;
}
html, body { margin:0; padding:0; }
body { font-family: var(--font-display); font-weight:400; color:var(--c-ink);
       background:#fff; font-feature-settings:"tnum" 1,"lnum" 1; }
.slide { position:relative; width:1920px; height:1080px;
         box-sizing:border-box; background:#fff; color:#000;
         page-break-after:always; }
.inner { position:absolute; top:0; left:0; right:0; bottom:0; padding:72px 120px;
         box-sizing:border-box; overflow:hidden; }
.slide--dark { background:#000; color:#fff; }
.slide--dark .eyebrow { color:rgba(255,255,255,0.55); }
.slide--dark .pagenum { color:rgba(255,255,255,0.35); }
.slide--dark .dek { color:rgba(255,255,255,0.55); }
p, .dek, figcaption, .capn { text-wrap:pretty; } h1,h2,.title { text-wrap:balance; }
.eyebrow { font-family:var(--font-mono); font-size:13px; letter-spacing:0.16em;
           text-transform:uppercase; color:var(--c-dim); }
.title { font-size:72px; line-height:1.05; font-weight:500; letter-spacing:-0.025em;
         margin:20px 0 0 0; }
.statement { font-size:124px; line-height:1.0; font-weight:500; letter-spacing:-0.03em; margin:0; }
.dek { font-size:28px; line-height:1.3; color:var(--c-dim); margin:0; }
.pagenum { position:absolute; right:120px; top:76px; font-family:var(--font-mono);
           font-size:13px; letter-spacing:0.16em; color:var(--c-faint); }
.bullets { margin:0; padding:0; list-style:none; }
.bullets li { font-size:26px; line-height:1.36; margin-bottom:18px; padding-left:44px;
              position:relative; }
.bullets li:before { content:"\\2192"; position:absolute; left:0; color:var(--c-faint); }
.bullets li b { font-weight:500; }
.cap { font-family:var(--font-mono); font-size:13px; letter-spacing:0.16em;
       text-transform:uppercase; color:var(--c-dim); }
.capn { font-size:19px; color:var(--c-dim); line-height:1.35; }
img { image-rendering:auto; }
img.px { image-rendering:pixelated; }
.code { font-family:var(--font-mono); font-size:21px; line-height:1.55;
        background:var(--c-fill-subtle); padding:30px 38px; white-space:pre; }
.code .cm { color:var(--c-dim); }

/* boxes: the recurring teaching furniture */
.tbox { background:var(--c-fill-subtle); padding:24px 32px; box-sizing:border-box; }
.tbox .cap { display:block; margin-bottom:12px; }
.tbox--ink { background:#000; color:#fff; }
.tbox--ink .cap { color:rgba(255,255,255,0.55); }
.tbox p { margin:0; font-size:23px; line-height:1.38; }
.tbox p b { font-weight:500; }
.knob-row { display:grid; grid-template-columns: 1fr 1fr 1fr; }
.knob-row > div { padding:0 28px; }
.knob-row > div:first-child { padding-left:0; }
.knob-row > div:not(:last-child) { border-right:none; }

/* simple data tables */
table.tt { border-collapse:collapse; width:100%; }
table.tt th { font-family:var(--font-mono); font-size:13px; letter-spacing:0.16em;
  text-transform:uppercase; color:var(--c-dim); font-weight:500; text-align:left;
  padding:14px 24px 14px 0; border-bottom:1px solid var(--c-ink); }
table.tt td { font-size:23px; line-height:1.32; padding:13px 24px 13px 0;
  border-bottom:1px solid var(--c-line); vertical-align:top; }
table.tt tr:last-child td { border-bottom:1px solid var(--c-ink); }
table.tt td.term { font-weight:500; white-space:nowrap; }
table.tt td.mono { font-family:var(--font-mono); font-size:20px; }

.interact { position:absolute; left:120px; bottom:56px; font-family:var(--font-mono);
            font-size:13px; letter-spacing:0.16em; text-transform:uppercase; }
.interact b { font-weight:500; background:#000; color:#fff; padding:6px 12px; margin-right:14px; }
.slide--dark .interact b { background:#fff; color:#000; }
"""

# ---------------------------------------------------------------- helpers
SLIDES = []

def slide(body, dark=False, num=True):
    """num=True auto-numbers from position (cover passes num=False)."""
    cls = "slide slide--dark" if dark else "slide"
    n = f'<div class="pagenum">{len(SLIDES)+1:02d}</div>' if num else ""
    SLIDES.append(f'<div class="{cls}"><div class="inner">{n}{body}</div></div>')

def head(eyebrow, title, dek=None, title_size=None):
    ts = f"font-size:{title_size}px;" if title_size else ""
    d = f'<p class="dek" style="margin-top:18px; max-width:1300px;">{dek}</p>' if dek else ""
    return (f'<div class="eyebrow">{eyebrow}</div>'
            f'<h1 class="title" style="{ts} max-width:1480px;">{title}</h1>{d}')

def namebox(terms, width=None, ink=True, label="The proper name"):
    """terms: list of (TERM, plain gloss)."""
    rows = "".join(
        f'<p style="margin:0 0 9px 0;"><b>{t}</b>'
        f'<span style="opacity:0.55;"> — {g}</span></p>' if g else
        f'<p style="margin:0 0 9px 0;"><b>{t}</b></p>'
        for t, g in terms)
    w = f"width:{width}px;" if width else ""
    cls = "tbox tbox--ink" if ink else "tbox"
    return f'<div class="{cls}" style="{w}"><span class="cap">{label}</span>{rows}</div>'

def knobbox(knobs, width=None, label="Turn the knob"):
    """knobs: list of (knob, effect)."""
    rows = "".join(
        f'<p style="margin:0 0 9px 0;"><b>{k}</b>'
        f'<span style="opacity:0.55;"> → {e}</span></p>'
        for k, e in knobs)
    w = f"width:{width}px;" if width else ""
    return f'<div class="tbox" style="{w}"><span class="cap">{label}</span>{rows}</div>'

def bullets(items, size=None, gap=None):
    st = ""
    if size: st += f"font-size:{size}px;"
    if gap: st += f"margin-bottom:{gap}px;"
    lis = "".join(f'<li style="{st}">{i}</li>' for i in items)
    return f'<ul class="bullets">{lis}</ul>'

def code(src, caption=None, size=21):
    esc = html_mod.escape(src).replace("&quot;", '"')
    # gray comments
    out_lines = []
    for ln in esc.split("\n"):
        if "#" in ln:
            i = ln.index("#")
            ln = ln[:i] + f'<span class="cm">{ln[i:]}</span>'
        out_lines.append(ln)
    cap = f'<div class="cap" style="margin-top:20px;">{caption}</div>' if caption else ""
    return f'<div class="code" style="font-size:{size}px;">{chr(10).join(out_lines)}</div>{cap}'

def grid_svg(values, cell=72, fs=26, highlight=None, gray_zero=False):
    """Draw a numeric grid as SVG. highlight: (r0,c0,r1,c1) inclusive box."""
    rows, cols = len(values), len(values[0])
    w, h = cols * cell, rows * cell
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    for r in range(rows):
        for c in range(cols):
            v = values[r][c]
            fill = "#FFFFFF"
            if gray_zero and v == 0:
                fill = "#E8E8E8"
            parts.append(f'<rect x="{c*cell}" y="{r*cell}" width="{cell}" height="{cell}" '
                         f'fill="{fill}" stroke="rgba(0,0,0,0.25)" stroke-width="1"/>')
            parts.append(f'<text x="{c*cell+cell/2}" y="{r*cell+cell/2+fs*0.35}" '
                         f'text-anchor="middle" font-family="Roboto Mono" font-size="{fs}" '
                         f'fill="#000">{v}</text>')
    if highlight:
        r0, c0, r1, c1 = highlight
        parts.append(f'<rect x="{c0*cell}" y="{r0*cell}" width="{(c1-c0+1)*cell}" '
                     f'height="{(r1-r0+1)*cell}" fill="none" stroke="#000" stroke-width="5"/>')
    parts.append("</svg>")
    return "".join(parts)

# ================================================================ PART 0 — SETUP

# ---- S1 cover
slide(num=False, body=f"""
<div class="eyebrow">IOAI 2026 SYLLABUS &middot; SECTION 3 &middot; COMPUTER VISION &middot; TEAM PREP</div>
<h1 class="title" style="font-size:168px; margin-top:280px; max-width:1500px;">How machines<br/>learn to see</h1>
""")

# ---- S2 the promise
slide(head("THE PLAN", "One day, one story",
           "If you can multiply small numbers, you can follow every step today. "
           "New words are only used AFTER we earn them.") + f"""
<div style="margin-top:48px; max-width:1430px;">
{bullets([
 "<b>Part 1 — The trick.</b> How a pile of numbers becomes the word &ldquo;cat&rdquo;. We compute it by hand.",
 "<b>Part 2 — The learning.</b> Nobody programs it. It practices, like the hot-and-cold game.",
 "<b>Part 3 — The shortcut.</b> Borrow a model someone already trained on a million photos.",
 "<b>Part 4 — The superpowers.</b> Find objects, cut them out, talk to images, create images.",
 "<b>Part 5 — The cheat sheets.</b> Every term and every knob, on slides you keep.",
], size=24, gap=30)}
</div>
""")

# ---- S3 base vocabulary
slide(head("BEFORE WE START", "Five words we will use all day",
           "Only these five up front. Every other term gets introduced when you have already understood the idea behind it.") + f"""
<div style="margin-top:28px; max-width:1560px;">
<table class="tt">
<tr><th style="width:330px;">Word</th><th>What it means, in plain words</th></tr>
<tr><td class="term">MODEL</td><td>a machine made of numbers: input goes in, a guess comes out</td></tr>
<tr><td class="term">DATASET</td><td>the pile of examples we teach with — photos plus their correct answers</td></tr>
<tr><td class="term">LABEL</td><td>the correct answer attached to one example: &ldquo;this photo is a cat&rdquo;</td></tr>
<tr><td class="term">TRAINING</td><td>showing the model examples, over and over, until its guesses get good</td></tr>
<tr><td class="term">ACCURACY</td><td>out of 100 tries, how many guesses were right</td></tr>
</table>
</div>
""")

# ---- S4 statement
slide(f"""
<div class="eyebrow">PART 1 &middot; THE TRICK</div>
<p class="statement" style="margin-top:280px; max-width:1600px;">A computer has never<br/>seen a cat.</p>
""", dark=True)

# ---- S5 photo = grid of numbers
pix5 = [row[:7] for row in pix[:5]]
slide(head("PART 1 · THE TRICK", "A photo is just a grid of numbers") + f"""
<div style="display:grid; grid-template-columns: 760px 1fr; column-gap:90px; margin-top:38px;">
  <div>
    {bullets([
      "Zoom far enough into any photo and it falls apart into little squares.",
      "Each square holds <b>one number</b>: 0 means black, 255 means white, in-between means gray.",
      "A color photo is <b>three grids stacked</b> — one for red, one for green, one for blue. That is ALL the computer gets.",
    ], size=26)}
    <div style="margin-top:20px;">
    {namebox([("PIXEL", "one little square of the photo"),
              ("TENSOR", "a grid of numbers (possibly several stacked) — nothing scarier than that")])}
    </div>
  </div>
  <div>
    <figure style="margin:0;">
      <img src="assets/chelsea_marked.png" width="560" height="373"/>
      <figcaption class="capn" style="margin-top:12px; max-width:560px;">Chelsea — a real photo, with a tiny square marked on her eye. Below: the REAL numbers inside that square.</figcaption>
    </figure>
    <div style="margin-top:18px;">{grid_svg(pix5, cell=54, fs=19)}</div>
  </div>
</div>
<div class="interact"><b>ASK THE ROOM</b> Big numbers — in the bright fur or the dark pupil? (255 = white)</div>
""")

# ================================================================ PART 1 — THE TRICK

# ---- S6 hand convolution (centerpiece)
inp = [[2,2,0,0,0],[2,2,0,0,0],[2,2,0,0,0],[2,2,0,0,0],[2,2,0,0,0]]
filt = [[1,0,-1],[1,0,-1],[1,0,-1]]
slide(head("PART 1 · THE TRICK", "The trick, by hand — it is just times tables",
           "The image has a bright stripe (2s) next to a dark area (0s). Where they meet is an edge. Can math FIND that edge?") + f"""
<div style="display:grid; grid-template-columns: 420px 330px 1fr; column-gap:80px; margin-top:20px; align-items:start;">
  <figure style="margin:0;">
    <div class="cap" style="margin-bottom:16px;">1 · A tiny image</div>
    {grid_svg(inp, cell=80, fs=28, highlight=(0,0,2,2), gray_zero=True)}
    <figcaption class="capn" style="margin-top:14px;">Bright stripe of 2s, dark area of 0s. The bold box is where we lay the stencil first.</figcaption>
  </figure>
  <figure style="margin:0;">
    <div class="cap" style="margin-bottom:16px;">2 · A 3&times;3 stencil</div>
    {grid_svg(filt, cell=80, fs=28)}
    <figcaption class="capn" style="margin-top:14px;">Nine chosen numbers. Plus on the left, minus on the right.</figcaption>
  </figure>
  <div>
    <div class="cap" style="margin-bottom:16px;">3 · Multiply matching cells, add all nine</div>
    <div style="font-family:var(--font-mono); font-size:27px; line-height:1.75;">
      2&times;1 + 2&times;0 + 0&times;(&minus;1) &nbsp;=&nbsp; 2<br/>
      2&times;1 + 2&times;0 + 0&times;(&minus;1) &nbsp;=&nbsp; 2<br/>
      2&times;1 + 2&times;0 + 0&times;(&minus;1) &nbsp;=&nbsp; 2<br/>
      <span style="display:inline-block; border-top:1px solid #000; margin-top:10px; padding-top:10px;">total &nbsp;=&nbsp; <b style="font-weight:500; font-size:34px;">6</b> &nbsp;&rarr; &ldquo;my pattern is HERE&rdquo;</span>
    </div>
    <p style="font-size:26px; line-height:1.45; margin:34px 0 0 0; max-width:600px; color:var(--c-dim);">
    Now slide the stencil onto the flat dark area: every cell is 0, every product is 0,
    total = <b style="color:#000; font-weight:500;">0</b> — &ldquo;nothing here.&rdquo; The stencil only speaks on its own pattern.</p>
  </div>
</div>
<div style="margin-top:18px; max-width:1100px;">
{namebox([("CONVOLUTION", "this multiply-and-add operation — the heart of all computer vision"),
          ("FILTER (or KERNEL)", "the little stencil of numbers")])}
</div>
<div class="interact"><b>DO IT TOGETHER</b> Everyone computes the nine products out loud before the reveal</div>
""")

# ---- S7 feature map
slide(head("PART 1 · THE TRICK", "Slide it everywhere — the photo answers back") + f"""
<div style="display:grid; grid-template-columns: 720px 1fr; column-gap:90px; margin-top:38px;">
  <div>
    {bullets([
      "Slide the SAME stencil across the whole photo — thousands of little multiply-and-adds.",
      "Write the answer at every stop. You get a new image that <b>glows where the pattern lives</b>.",
      "Look: the whiskers and eye outlines light up — they are vertical-ish edges.",
      "This is real output — this exact stencil ran on this exact photo.",
    ], size=26)}
    <div style="margin-top:20px;">
    {namebox([("FEATURE MAP", "the glow-map an image produces for one filter: bright = pattern found here")])}
    </div>
  </div>
  <div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:24px;">
      <figure style="margin:0;"><img src="assets/chelsea_gray.png" width="440" height="293"/>
        <figcaption class="capn" style="margin-top:12px;">The photo, in grays</figcaption></figure>
      <figure style="margin:0;"><img src="assets/fmap_vertical.png" width="440" height="293"/>
        <figcaption class="capn" style="margin-top:12px;">Our vertical-edge stencil: whiskers glow</figcaption></figure>
      <figure style="margin:0;"><img src="assets/fmap_horizontal.png" width="440" height="293"/>
        <figcaption class="capn" style="margin-top:12px;">Same stencil rotated 90&deg;: horizontal edges glow</figcaption></figure>
      <div class="tbox" style="align-self:start;">
        <span class="cap">Turn the knob</span>
        <p>Different numbers in the stencil → a different pattern found. Rotate it → horizontal edges. The numbers ARE the pattern.</p>
      </div>
    </div>
  </div>
</div>
""")

# ---- S8 stride & padding
def stride_svg():
    # 6x6 grid, show 3x3 window positions for stride 1 vs stride 2
    cell = 52
    def panel(stride, label):
        w = 6*cell
        parts = [f'<svg width="{w}" height="{w+40}" viewBox="0 0 {w} {w+40}" xmlns="http://www.w3.org/2000/svg">']
        for r in range(6):
            for c in range(6):
                parts.append(f'<rect x="{c*cell}" y="{r*cell}" width="{cell}" height="{cell}" fill="#fff" stroke="rgba(0,0,0,0.2)"/>')
        # first window
        parts.append(f'<rect x="0" y="0" width="{3*cell}" height="{3*cell}" fill="rgba(0,0,0,0.10)" stroke="#000" stroke-width="4"/>')
        # second window at stride
        parts.append(f'<rect x="{stride*cell}" y="0" width="{3*cell}" height="{3*cell}" fill="none" stroke="#000" stroke-width="3" stroke-dasharray="8,7"/>')
        parts.append(f'<text x="0" y="{w+30}" font-family="Roboto Mono" font-size="20" fill="rgba(0,0,0,0.55)">{label}</text>')
        parts.append("</svg>")
        return "".join(parts)
    return panel(1, "STRIDE 1 — step one cell"), panel(2, "STRIDE 2 — step two cells")

def padding_svg():
    cell = 52
    n = 8  # 6 + padding ring
    w = n*cell
    parts = [f'<svg width="{w}" height="{w}" viewBox="0 0 {w} {w}" xmlns="http://www.w3.org/2000/svg">']
    for r in range(n):
        for c in range(n):
            edge = r in (0, n-1) or c in (0, n-1)
            if edge:
                parts.append(f'<rect x="{c*cell}" y="{r*cell}" width="{cell}" height="{cell}" fill="#fff" stroke="rgba(0,0,0,0.35)" stroke-dasharray="5,5"/>')
                parts.append(f'<text x="{c*cell+cell/2}" y="{r*cell+cell/2+7}" text-anchor="middle" font-family="Roboto Mono" font-size="18" fill="rgba(0,0,0,0.35)">0</text>')
            else:
                parts.append(f'<rect x="{c*cell}" y="{r*cell}" width="{cell}" height="{cell}" fill="rgba(0,0,0,0.06)" stroke="rgba(0,0,0,0.2)"/>')
    parts.append("</svg>")
    return "".join(parts)

sv1, sv2 = stride_svg()
slide(head("PART 1 · THE TRICK", "Two sliding rules: stride and padding",
           "Both are just rules about HOW the stencil walks across the photo.") + f"""
<div style="display:grid; grid-template-columns: 1fr 1fr 1fr; column-gap:70px; margin-top:28px; align-items:start;">
  <div>
    <div class="cap" style="margin-bottom:18px;">Stride — the step size</div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">{sv1}{sv2}</div>
    <p class="capn" style="margin-top:18px; font-size:22px;">Stride 1: the stencil visits every position. Stride 2: it skips every other one — the answer map comes out half the size.</p>
  </div>
  <div>
    <div class="cap" style="margin-bottom:18px;">Padding — zeros glued around the border</div>
    {padding_svg()}
    <p class="capn" style="margin-top:18px; font-size:22px;">Without padding the border pixels never sit under the stencil&rsquo;s center, and the map shrinks each layer. The dashed ring of invisible zeros fixes both.</p>
  </div>
  <div>
    {knobbox([
      ("stride 1 → 2", "output map half the size; cheaper, but a blurrier view"),
      ("no padding", "a 3&times;3 stencil shrinks a 7&times;7 photo to 5&times;5 every layer"),
      ("padding 1", "the map stays the same size as the photo"),
      ("kernel 3&times;3 → 7&times;7", "sees bigger patterns at once, but 27 → 147 numbers to learn per filter — slower, needs more data"),
    ])}
  </div>
</div>
""")

# ---- S9 pooling
def pool_svg():
    cell = 88
    vals = [[1,3,2,1],[4,8,1,0],[2,1,9,5],[0,3,2,6]]
    quads = [(0,0,8),(0,2,2),(2,0,4),(2,2,9)]
    w = 4*cell
    parts = [f'<svg width="{w+340}" height="{w}" viewBox="0 0 {w+340} {w}" xmlns="http://www.w3.org/2000/svg">']
    for r in range(4):
        for c in range(4):
            v = vals[r][c]
            mx = max(vals[(r//2)*2][(c//2)*2], vals[(r//2)*2][(c//2)*2+1], vals[(r//2)*2+1][(c//2)*2], vals[(r//2)*2+1][(c//2)*2+1])
            fill = "rgba(0,0,0,0.10)" if v == mx else "#fff"
            parts.append(f'<rect x="{c*cell}" y="{r*cell}" width="{cell}" height="{cell}" fill="{fill}" stroke="rgba(0,0,0,0.25)"/>')
            parts.append(f'<text x="{c*cell+cell/2}" y="{r*cell+cell/2+10}" text-anchor="middle" font-family="Roboto Mono" font-size="30" fill="#000">{v}</text>')
    # quad borders
    parts.append(f'<rect x="0" y="0" width="{2*cell}" height="{2*cell}" fill="none" stroke="#000" stroke-width="4"/>')
    parts.append(f'<rect x="{2*cell}" y="0" width="{2*cell}" height="{2*cell}" fill="none" stroke="#000" stroke-width="4"/>')
    parts.append(f'<rect x="0" y="{2*cell}" width="{2*cell}" height="{2*cell}" fill="none" stroke="#000" stroke-width="4"/>')
    parts.append(f'<rect x="{2*cell}" y="{2*cell}" width="{2*cell}" height="{2*cell}" fill="none" stroke="#000" stroke-width="4"/>')
    # arrow
    ax = 4*cell + 40
    parts.append(f'<line x1="{ax}" y1="{2*cell}" x2="{ax+80}" y2="{2*cell}" stroke="#000" stroke-width="3"/>')
    parts.append(f'<polygon points="{ax+80},{2*cell} {ax+62},{2*cell-9} {ax+62},{2*cell+9}" fill="#000"/>')
    # output 2x2
    ox = ax + 120
    out = [[8,2],[3,9]]
    for r in range(2):
        for c in range(2):
            parts.append(f'<rect x="{ox+c*cell}" y="{cell+r*cell}" width="{cell}" height="{cell}" fill="rgba(0,0,0,0.06)" stroke="#000" stroke-width="2"/>')
            parts.append(f'<text x="{ox+c*cell+cell/2}" y="{cell+r*cell+cell/2+10}" text-anchor="middle" font-family="Roboto Mono" font-size="30" fill="#000">{out[r][c]}</text>')
    parts.append("</svg>")
    return "".join(parts)

slide(head("PART 1 · THE TRICK", "Pooling — shrink the map, forgive small shifts") + f"""
<div style="display:grid; grid-template-columns: 780px 1fr; column-gap:90px; margin-top:38px;">
  <div>
    {bullets([
      "Look at each little 2&times;2 window and <b>keep only the biggest number</b>: &ldquo;was the pattern here at all?&rdquo;",
      "The map shrinks to half size → everything after it is 4&times; cheaper.",
      "If the pattern moves by one pixel, the biggest number in the window usually does not change → <b>small shifts stop mattering</b>.",
      "Cousin: <b>average pooling</b> takes the mean instead. At the very end, averaging each whole map down to ONE number gives a short summary list of the photo.",
    ], size=25)}
  </div>
  <div>
    <div class="cap" style="margin-bottom:22px;">Max pooling, 2&times;2 — keep each quadrant&rsquo;s winner</div>
    {pool_svg()}
    <div style="margin-top:22px;">
    {namebox([("MAX / AVERAGE POOLING", "keep the max (or the mean) of each small window"),
              ("GLOBAL AVERAGE POOLING", "average each whole map to one number — the final summary step")])}
    </div>
  </div>
</div>
""")

# ---- S10 ReLU
def relu_svg():
    w, h = 560, 360
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    cx, cy = w/2, h/2
    parts.append(f'<line x1="30" y1="{cy}" x2="{w-30}" y2="{cy}" stroke="rgba(0,0,0,0.25)" stroke-width="2"/>')
    parts.append(f'<line x1="{cx}" y1="30" x2="{cx}" y2="{h-30}" stroke="rgba(0,0,0,0.25)" stroke-width="2"/>')
    parts.append(f'<line x1="40" y1="{cy}" x2="{cx}" y2="{cy}" stroke="#000" stroke-width="5"/>')
    parts.append(f'<line x1="{cx}" y1="{cy}" x2="{w-50}" y2="50" stroke="#000" stroke-width="5"/>')
    parts.append(f'<text x="{cx-180}" y="{cy+40}" font-family="Roboto Mono" font-size="20" fill="rgba(0,0,0,0.55)">negative → 0</text>')
    parts.append(f'<text x="{cx+40}" y="{cy-90}" font-family="Roboto Mono" font-size="20" fill="rgba(0,0,0,0.55)">positive → kept</text>')
    parts.append("</svg>")
    return "".join(parts)

slide(head("PART 1 · THE TRICK", "ReLU — the &ldquo;keep the good news&rdquo; switch") + f"""
<div style="display:grid; grid-template-columns: 800px 1fr; column-gap:90px; margin-top:38px;">
  <div>
    {bullets([
      "After each convolution, walk over the map and <b>replace every negative number with 0</b>. Positives pass through untouched. That is the entire rule.",
      "Why bother? Stacking plain multiply-and-add layers is like stacking rulers — <b>a stack of rulers is still a ruler</b>. One bend between layers lets each layer build something NEW on top of the last.",
      "Without it, a 50-layer network computes nothing more than a 1-layer one.",
    ], size=25)}
    <div style="margin-top:28px;">
    {namebox([("ACTIVATION FUNCTION", "the bend between layers; ReLU is the standard one"),
              ("RELU", "max(0, x) — negatives become 0, positives stay"),
              ("SIGMOID / TANH", "older bends that squash numbers into 0&ndash;1 or &minus;1&ndash;1 — you will see the names")])}
    </div>
  </div>
  <div style="padding-top:50px;">{relu_svg()}</div>
</div>
""")

# ---- S11 the full CNN
def pipeline_svg():
    w, h = 1640, 250
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    stages = [("PHOTO", "224×224×3"), ("FILTERS + RELU", "many glow-maps"), ("POOL", "half size"),
              ("FILTERS + RELU", "deeper patterns"), ("POOL", "half again"),
              ("GLOBAL AVERAGE", "short list = embedding"), ("SCORES", "cat 92%")]
    n = len(stages); bw = 200; gap = (w - n*bw) / (n-1)
    for i, (t, s) in enumerate(stages):
        x = i*(bw+gap)
        fill = "#000" if i == n-1 else "#fff"
        tcol = "#fff" if i == n-1 else "#000"
        scol = "rgba(255,255,255,0.55)" if i == n-1 else "rgba(0,0,0,0.55)"
        parts.append(f'<rect x="{x}" y="60" width="{bw}" height="130" fill="{fill}" stroke="#000" stroke-width="2.5"/>')
        parts.append(f'<text x="{x+bw/2}" y="115" text-anchor="middle" font-family="Roboto Mono" font-size="17" letter-spacing="1.5" fill="{tcol}">{t}</text>')
        parts.append(f'<text x="{x+bw/2}" y="152" text-anchor="middle" font-family="Roboto Mono" font-size="15" fill="{scol}">{s}</text>')
        if i < n-1:
            ax = x + bw
            parts.append(f'<line x1="{ax+6}" y1="125" x2="{ax+gap-10}" y2="125" stroke="#000" stroke-width="2.5"/>')
            parts.append(f'<polygon points="{ax+gap-6},125 {ax+gap-20},118 {ax+gap-20},132" fill="#000"/>')
    parts.append("</svg>")
    return "".join(parts)

slide(head("PART 1 · THE TRICK", "Stack it all — the complete seeing machine",
           "Filters find edges. The next layer looks at the GLOW-MAPS and finds combinations: textures, then parts, then objects.") + f"""
<div style="margin-top:22px;">{pipeline_svg()}</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; column-gap:80px; margin-top:22px;">
  {namebox([("CONVOLUTIONAL NEURAL NETWORK — CNN", "the whole stack of filter layers"),
            ("EMBEDDING", "the short list of numbers that summarizes the photo"),
            ("IMAGE CLASSIFICATION", "one label for the whole photo — what this machine does")])}
  {namebox([("SOFTMAX", "turns final scores into percentages that add to 100"),
            ("EDGES → TEXTURES → PARTS → OBJECTS", "what layers 1, 2, 3&hellip; learn to find, in that order")], label="And the ladder it climbs")}
</div>
""")

# ---- S12 code card 1
slide(head("PART 1 · CODE", "The whole &ldquo;eye&rdquo; is a few honest lines",
           "Every line below is something you already understand. Read the comments, not the syntax.") + f"""
<div style="display:grid; grid-template-columns: 980px 1fr; column-gap:80px; margin-top:20px;">
  <div>
{code('''import torch.nn as nn

model = nn.Sequential(
    nn.Conv2d(3, 32, kernel_size=3, padding=1),  # 32 stencils, 3x3, on R,G,B
    nn.ReLU(),                                   # keep the good news
    nn.MaxPool2d(2),                             # shrink, forgive shifts
    nn.Conv2d(32, 64, kernel_size=3, padding=1), # 64 deeper stencils
    nn.ReLU(),
    nn.AdaptiveAvgPool2d(1),                     # global average -> summary
    nn.Flatten(),
    nn.Linear(64, 10),                           # 10 class scores
)''', caption="A real, complete image classifier — this shape scores ~50% on a 10-class photo task (chance = 10%)")}
  </div>
  <div>
    {knobbox([
      ("out_channels 32 → 64", "more patterns spotted per layer; slower, more to learn"),
      ("kernel_size 3 → 7", "each stencil sees a bigger patch; weights jump 27 → 147 per filter"),
      ("delete the ReLU lines", "the stack collapses into one big ruler — accuracy tanks"),
      ("add more conv blocks", "deeper ladder: textures → parts → objects; needs more data and time"),
    ])}
  </div>
</div>
""")

# ---- quick check 1
def quiz(part, qa, myth=None):
    rows = "".join(
        f'<div style="margin-bottom:44px;"><p style="font-size:30px; font-weight:500; margin:0 0 9px 0;">{q}</p>'
        f'<p style="font-size:25px; color:var(--c-dim); margin:0;">{a}</p></div>'
        for q, a in qa)
    m = ""
    if myth:
        m = (f'<div class="tbox tbox--ink" style="margin-top:10px;"><span class="cap">Myth vs reality</span>'
             f'<p><b>Myth:</b> {myth[0]}</p><p style="margin-top:10px;"><b>Reality:</b> {myth[1]}</p></div>')
    slide(head(f"{part} · QUICK CHECK", "Close the laptop lids — quick check",
               "Answers out loud, no grades. If the room can answer these, we have earned the next part.") + f"""
<div style="display:grid; grid-template-columns: 1fr 760px; column-gap:90px; margin-top:22px;">
  <div>{rows}</div>
  <div>{m}</div>
</div>
""")

quiz("PART 1", [
  ("A friend says &ldquo;the computer looks at the photo.&rdquo; What does it ACTUALLY get?",
   "A grid of numbers, 0&ndash;255 — three grids for a color photo. Nothing else."),
  ("What does a filter do, in one sentence?",
   "It slides over the photo, multiplies and adds, and writes a big number wherever its pattern appears."),
  ("Why does a CNN need ReLU between layers?",
   "Without the bend, the whole stack collapses into one layer — stacked rulers are still a ruler."),
  ("What does pooling buy us?",
   "Smaller maps (cheaper) and forgiveness for small shifts of the pattern."),
], myth=("AI sees the way we do — it just &ldquo;recognizes&rdquo; the cat.",
         "It has no eyes and no idea what a cat is. It does millions of multiply-and-adds on a number grid, and the numbers it multiplies by were learned, not programmed."))

# ================================================================ PART 2 — THE LEARNING

# ---- S13 statement
slide(f"""
<div class="eyebrow">PART 2 &middot; THE LEARNING</div>
<p class="statement" style="margin-top:280px; max-width:1700px;">Nobody programs the filters.<br/>The network finds them.</p>
<p class="dek" style="margin-top:38px; max-width:1200px;">On slide 6, WE chose the nine stencil numbers. In a real network, all the stencils — millions of numbers — start as random noise. Then they learn.</p>
""", dark=True)

# ---- S14 learning loop
def loop_svg():
    w, h = 700, 560
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    boxes = [("PHOTO", 60, 40), ("MODEL GUESSES", 60, 170), ("COMPARE WITH LABEL", 60, 300), ("LOSS = HOW WRONG", 60, 430)]
    for t, x, y in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="420" height="80" fill="#fff" stroke="#000" stroke-width="2.5"/>')
        parts.append(f'<text x="{x+210}" y="{y+48}" text-anchor="middle" font-family="Roboto Mono" font-size="18" letter-spacing="1.5" fill="#000">{t}</text>')
        if y < 430:
            parts.append(f'<line x1="{x+210}" y1="{y+80}" x2="{x+210}" y2="{y+126}" stroke="#000" stroke-width="2.5"/>')
            parts.append(f'<polygon points="{x+210},{y+130} {x+203},{y+114} {x+217},{y+114}" fill="#000"/>')
    # feedback arrow
    parts.append(f'<path d="M 480 470 L 600 470 L 600 210 L 484 210" fill="none" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<polygon points="480,210 496,203 496,217" fill="#000"/>')
    parts.append(f'<text x="652" y="345" text-anchor="middle" font-family="Roboto Mono" font-size="16" fill="rgba(0,0,0,0.55)" transform="rotate(-90 652 345)">NUDGE EVERY NUMBER</text>')
    parts.append("</svg>")
    return "".join(parts)

slide(head("PART 2 · THE LEARNING", "Learning is the hot-and-cold game") + f"""
<div style="display:grid; grid-template-columns: 850px 1fr; column-gap:90px; margin-top:20px;">
  <div>
    {bullets([
      "Show the network a photo. It guesses: &ldquo;70% dog, 20% cat&hellip;&rdquo; — badly, because its stencils are random.",
      "We know the label is &ldquo;cat&rdquo;, so we hand it one number — <b>how wrong it was</b>. Big number = ice cold.",
      "A recipe then tells <b>every stencil number which direction to nudge</b> to be slightly less wrong.",
      "One photo, one tiny nudge. A million photos later, the random stencils have become the edge detectors you saw earlier. Nobody put them there.",
    ], size=25)}
    <div style="margin-top:38px;">
    {namebox([("LOSS", "the wrongness score — that is the entire meaning of the word"),
              ("BACKPROPAGATION", "the recipe that works out each number&rsquo;s nudge direction"),
              ("EPOCH", "one full pass through the whole dataset")])}
    </div>
  </div>
  <div style="padding-top:20px;">{loop_svg()}</div>
</div>
""")

# ---- S15 gradient descent
def hill_svg():
    w, h = 640, 420
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    # valley curve
    parts.append(f'<path d="M 40 60 Q 200 80 300 300 Q 340 380 380 300 Q 480 80 600 50" fill="none" stroke="#000" stroke-width="3.5"/>')
    # ball positions stepping down
    pts = [(110, 88), (180, 130), (240, 210), (290, 285), (335, 340)]
    for i, (x, y) in enumerate(pts):
        r = 13 if i == len(pts)-1 else 10
        fill = "#000" if i == len(pts)-1 else "rgba(0,0,0,0.3)"
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')
    parts.append(f'<text x="60" y="395" font-family="Roboto Mono" font-size="17" fill="rgba(0,0,0,0.55)">downhill, step by step</text>')
    return "".join(parts) + "</svg>"

def bounce_svg():
    w, h = 640, 420
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    parts.append(f'<path d="M 40 60 Q 200 80 300 300 Q 340 380 380 300 Q 480 80 600 50" fill="none" stroke="#000" stroke-width="3.5"/>')
    pts = [(120, 95), (520, 75), (170, 122), (470, 95)]
    for i, (x, y) in enumerate(pts):
        parts.append(f'<circle cx="{x}" cy="{y}" r="10" fill="rgba(0,0,0,0.35)"/>')
        if i < len(pts)-1:
            nx, ny = pts[i+1]
            parts.append(f'<line x1="{x}" y1="{y}" x2="{nx}" y2="{ny}" stroke="rgba(0,0,0,0.35)" stroke-width="2" stroke-dasharray="6,6"/>')
    parts.append(f'<text x="60" y="395" font-family="Roboto Mono" font-size="17" fill="rgba(0,0,0,0.55)">steps too big — bouncing across the valley</text>')
    return "".join(parts) + "</svg>"

slide(head("PART 2 · THE LEARNING", "Wrongness is a landscape. Training rolls downhill.",
           "Imagine every possible setting of the stencil numbers as a point in a hilly landscape — height = loss. Training = rolling the ball to a low spot.") + f"""
<div style="display:grid; grid-template-columns: 1fr 1fr; column-gap:80px; margin-top:38px;">
  <div>
    <div class="cap" style="margin-bottom:18px;">Good step size</div>
    {hill_svg()}
  </div>
  <div>
    <div class="cap" style="margin-bottom:18px;">Step size 10&times; too big</div>
    {bounce_svg()}
  </div>
</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; column-gap:80px; margin-top:18px;">
  {namebox([("GRADIENT DESCENT", "the rolling-downhill procedure"),
            ("LEARNING RATE", "the step size — the single most important knob in training"),
            ("ADAM", "gradient descent with momentum and self-adjusting steps; the sensible default")])}
  {knobbox([
    ("learning rate too small", "the ball crawls; training takes forever"),
    ("learning rate 10&times; too big", "loss bounces or explodes; it never settles"),
    ("a good default", "Adam with learning rate 0.001, then let it shrink during training"),
  ])}
</div>
""")

# ---- S16 overfitting
def overfit_svg():
    w, h = 760, 460
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    # axes
    parts.append(f'<line x1="70" y1="380" x2="710" y2="380" stroke="rgba(0,0,0,0.3)" stroke-width="2"/>')
    parts.append(f'<line x1="70" y1="40" x2="70" y2="380" stroke="rgba(0,0,0,0.3)" stroke-width="2"/>')
    # train curve: rises steadily
    parts.append(f'<path d="M 70 360 Q 220 140 420 90 Q 560 60 700 50" fill="none" stroke="#000" stroke-width="4"/>')
    # test curve: rises then falls
    parts.append(f'<path d="M 70 365 Q 230 200 400 170 Q 520 160 700 260" fill="none" stroke="rgba(0,0,0,0.45)" stroke-width="4" stroke-dasharray="10,8"/>')
    # stop marker
    parts.append(f'<line x1="430" y1="60" x2="430" y2="380" stroke="#000" stroke-width="2" stroke-dasharray="4,6"/>')
    parts.append(f'<text x="445" y="84" font-family="Roboto Mono" font-size="17" fill="#000">STOP HERE</text>')
    parts.append(f'<text x="540" y="110" font-family="Roboto Mono" font-size="17" fill="#000">train ↑</text>')
    parts.append(f'<text x="540" y="320" font-family="Roboto Mono" font-size="17" fill="rgba(0,0,0,0.55)">test ↓ = memorizing</text>')
    parts.append(f'<text x="330" y="420" font-family="Roboto Mono" font-size="17" fill="rgba(0,0,0,0.55)">TIME (EPOCHS) →</text>')
    parts.append(f'<text x="30" y="210" font-family="Roboto Mono" font-size="17" fill="rgba(0,0,0,0.55)" transform="rotate(-90 30 210)">ACCURACY →</text>')
    return "".join(parts) + "</svg>"

slide(head("PART 2 · THE LEARNING", "Overfitting — memorizing is not understanding") + f"""
<div style="display:grid; grid-template-columns: 820px 1fr; column-gap:90px; margin-top:20px;">
  <div>
    {bullets([
      "A student who memorizes past papers aces every practice test — and fails the real exam. Networks do exactly this.",
      "So we <b>split the dataset</b>: TRAIN photos (study material) and TEST photos (the real exam — the network NEVER studies these).",
      "Watch both scores. Train accuracy climbs forever. Test accuracy rises&hellip; then <b>falls</b>. The fall is the moment memorizing started.",
      "Fixes: stop at the peak, get more varied data, or use the &ldquo;forget a little on purpose&rdquo; brakes below.",
    ], size=25)}
    <div style="margin-top:20px;">
    {namebox([("OVERFITTING", "scoring high on study material, low on the real exam"),
              ("TRAIN / TEST SPLIT", "study material vs the never-seen exam"),
              ("EARLY STOPPING · DROPOUT · WEIGHT DECAY", "the standard anti-memorizing brakes")])}
    </div>
  </div>
  <div style="padding-top:30px;">
    {overfit_svg()}
    <div style="margin-top:28px;">
    {knobbox([("more epochs", "train accuracy up forever; test accuracy up, then down"),
              ("more varied data", "memorizing starts later or never")])}
    </div>
  </div>
</div>
""")

# ---- S17 augmentation
slide(head("PART 2 · THE LEARNING", "Augmentation — free extra photos",
           "A flipped cat is still a cat. So every time a photo is used, change it a little — the network can never just memorize it.") + f"""
<div style="display:grid; grid-template-columns: repeat(5, 1fr); column-gap:28px; margin-top:38px;">
  <figure style="margin:0;"><img src="assets/aug_original.png" width="280" height="280"/><figcaption class="cap" style="margin-top:14px;">ORIGINAL</figcaption></figure>
  <figure style="margin:0;"><img src="assets/aug_flip.png" width="280" height="280"/><figcaption class="cap" style="margin-top:14px;">FLIPPED</figcaption></figure>
  <figure style="margin:0;"><img src="assets/aug_crop.png" width="280" height="280"/><figcaption class="cap" style="margin-top:14px;">CROPPED</figcaption></figure>
  <figure style="margin:0;"><img src="assets/aug_jitter.png" width="280" height="280"/><figcaption class="cap" style="margin-top:14px;">RECOLORED</figcaption></figure>
  <figure style="margin:0;"><img src="assets/aug_noise.png" width="280" height="280"/><figcaption class="cap" style="margin-top:14px;">NOISY</figcaption></figure>
</div>
<div style="display:grid; grid-template-columns: 980px 1fr; column-gap:80px; margin-top:38px;">
  <div>
{code('''train_tf = transforms.Compose([
    transforms.RandomCrop(32, padding=4),   # random framing
    transforms.RandomHorizontalFlip(),      # mirror half the time
    transforms.ToTensor(),
])''', caption="Real lines from the training code that produced the numbers on slide 19")}
  </div>
  {knobbox([
    ("apply to TEST photos", "never — the exam must stay fixed"),
    ("too strong (crop 90% away)", "the label itself is destroyed; accuracy drops"),
    ("the classic trap", "flipping digits turns 6 into 9 — every change must keep the label true"),
  ])}
</div>
""")

# ---- S18 learned filters
slide(head("PART 2 · THE LEARNING", "What the network actually taught itself") + f"""
<div style="display:grid; grid-template-columns: 1fr 1100px; column-gap:80px; margin-top:38px;">
  <div>
    {bullets([
      "These are the REAL first-layer stencils of ResNet18, a famous network trained on 1.28 million photos.",
      "<b>Nobody drew these.</b> They started as random noise.",
      "They became edge and color detectors — the network <b>discovered</b> that edges are the right place to start seeing.",
      "Layer 2 looks at edge-maps and finds textures: fur, stripes, mesh. Higher layers: ear, eye, wheel — then &ldquo;cat&rdquo;.",
    ], size=25)}
  </div>
  <div>
    <img src="assets/resnet_filters.png" width="1016" height="248" class="px"/>
    <p class="capn" style="margin-top:18px;">All 64 first-layer filters of ResNet18, enlarged. Compare with the stencil you computed by hand on slide 6.</p>
    <div style="margin-top:18px; font-family:var(--font-mono); font-size:22px; letter-spacing:0.06em;">
      EDGES &nbsp;→&nbsp; TEXTURES &nbsp;→&nbsp; PARTS &nbsp;→&nbsp; OBJECTS
    </div>
    <p class="capn" style="margin-top:14px;">the ladder every trained CNN climbs, layer by layer</p>
  </div>
</div>
""")

# ---- S19 receipts
def bars_svg():
    w, h = 1500, 520
    data = [("50.0%", "SMALL CNN, FROM SCRATCH", "4,000 training photos · 3 epochs", 50.0),
            ("74.2%", "PRETRAINED RESNET18, FINETUNED", "only 1,000 training photos", 74.2),
            ("88.5%", "CLIP, ZERO-SHOT", "0 training photos", 88.5)]
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    bw = 330; gap = (w - 3*bw) / 2
    maxh = 360
    for i, (v, t, s, pct) in enumerate(data):
        x = i*(bw+gap); bh = maxh * pct/100; y = 430 - bh
        parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="#000"/>')
        parts.append(f'<text x="{x}" y="{y-22}" font-family="Satoshi" font-weight="500" font-size="58" fill="#000">{v}</text>')
        parts.append(f'<text x="{x}" y="{470}" font-family="Roboto Mono" font-size="17" letter-spacing="1.5" fill="#000">{t}</text>')
        parts.append(f'<text x="{x}" y="{500}" font-family="Roboto Mono" font-size="15" fill="rgba(0,0,0,0.55)">{s}</text>')
    # chance line
    cy = 430 - maxh*0.10
    parts.append(f'<line x1="0" y1="{cy}" x2="{w-90}" y2="{cy}" stroke="rgba(0,0,0,0.35)" stroke-width="2" stroke-dasharray="8,8"/>')
    parts.append(f'<text x="{w-80}" y="{cy+6}" font-family="Roboto Mono" font-size="15" fill="rgba(0,0,0,0.55)">CHANCE 10%</text>')
    return "".join(parts) + "</svg>"

slide(head("PART 2 · RECEIPTS", "Real numbers, run on an ordinary laptop CPU",
           "Task: 10 kinds of small photos (CIFAR-10) — cat, ship, truck&hellip; Random guessing scores 10%. Every number below is reproducible from the notebooks in this repo.") + f"""
<div style="margin-top:48px;">{bars_svg()}</div>
<p class="dek" style="margin-top:18px; max-width:1400px;">The two bigger bars are Part 3 and Part 4 of this talk: borrowing trained eyes, and models that learned from the whole internet.</p>
<div class="interact"><b>ASK THE ROOM</b> Before revealing: guess what the from-scratch CNN scored. Closest wins.</div>
""")

# ================================================================ PART 3 — THE SHORTCUT

# ---- statement
slide(dark=True, body=f"""
<div class="eyebrow">PART 3 &middot; THE SHORTCUT</div>
<p class="statement" style="margin-top:280px; max-width:1700px;">Never start<br/>from scratch.</p>
<p class="dek" style="margin-top:38px; max-width:1300px;">Someone already spent weeks of computer time teaching a network to see, on 1.28 million photos. Those trained eyes are free to download.</p>
""")

# ---- pretrained + transfer learning
def transfer_svg():
    w, h = 700, 480
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    # backbone
    parts.append(f'<rect x="40" y="60" width="380" height="300" fill="rgba(0,0,0,0.06)" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<text x="230" y="140" text-anchor="middle" font-family="Roboto Mono" font-size="18" letter-spacing="1.5" fill="#000">TRAINED EYES</text>')
    parts.append(f'<text x="230" y="178" text-anchor="middle" font-family="Roboto Mono" font-size="15" fill="rgba(0,0,0,0.55)">all the filter layers</text>')
    parts.append(f'<text x="230" y="206" text-anchor="middle" font-family="Roboto Mono" font-size="15" fill="rgba(0,0,0,0.55)">edges → textures → parts</text>')
    parts.append(f'<text x="230" y="252" text-anchor="middle" font-family="Roboto Mono" font-size="16" fill="#000">🔒 FROZEN — keep as-is</text>')
    # old head crossed out
    parts.append(f'<rect x="470" y="60" width="190" height="120" fill="#fff" stroke="rgba(0,0,0,0.35)" stroke-width="2" stroke-dasharray="7,6"/>')
    parts.append(f'<text x="565" y="110" text-anchor="middle" font-family="Roboto Mono" font-size="15" fill="rgba(0,0,0,0.45)">OLD DECISION</text>')
    parts.append(f'<text x="565" y="136" text-anchor="middle" font-family="Roboto Mono" font-size="15" fill="rgba(0,0,0,0.45)">1000 classes</text>')
    parts.append(f'<line x1="480" y1="70" x2="650" y2="170" stroke="#000" stroke-width="3"/>')
    parts.append(f'<line x1="650" y1="70" x2="480" y2="170" stroke="#000" stroke-width="3"/>')
    # new head
    parts.append(f'<rect x="470" y="240" width="190" height="120" fill="#000"/>')
    parts.append(f'<text x="565" y="290" text-anchor="middle" font-family="Roboto Mono" font-size="15" fill="#fff">NEW DECISION</text>')
    parts.append(f'<text x="565" y="316" text-anchor="middle" font-family="Roboto Mono" font-size="15" fill="rgba(255,255,255,0.6)">YOUR 10 classes</text>')
    parts.append(f'<line x1="420" y1="300" x2="462" y2="300" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<polygon points="466,300 450,293 450,307" fill="#000"/>')
    parts.append(f'<text x="350" y="430" font-family="Roboto Mono" font-size="16" fill="rgba(0,0,0,0.55)">swap only the last piece, retrain that</text>')
    return "".join(parts) + "</svg>"

slide(head("PART 3 · THE SHORTCUT", "Borrow trained eyes, swap the final decision",
           "A chef who switches from Italian to Japanese food does not relearn chopping and seasoning — only the new recipes. Networks transfer the same way.") + f"""
<div style="display:grid; grid-template-columns: 820px 1fr; column-gap:90px; margin-top:20px;">
  <div>
    {bullets([
      "Networks trained on ImageNet (1.28M photos, 1000 classes) already know edges, textures, fur, wheels — skills useful for ANY photo task.",
      "Chop off only the final decision layer, bolt on a fresh one for YOUR classes, train mostly that.",
      "That is how 1,000 photos beat 4,000 on slide 20: <b>74.2% vs 50.0%</b> — the eyes came pre-trained.",
      "Rule of thumb: with a pretrained start, 100&ndash;1,000 photos per class is often enough.",
    ], size=25)}
    <div style="margin-top:20px;">
    {namebox([("PRETRAINED MODEL / BACKBONE", "a network someone already trained; the part you keep"),
              ("TRANSFER LEARNING", "reusing trained eyes on a new task"),
              ("FINETUNING", "the gentle retraining on your own photos"),
              ("FREEZING", "locking layers so training cannot change them")])}
    </div>
  </div>
  <div style="padding-top:30px;">{transfer_svg()}</div>
</div>
""")

# ---- ResNet skip connections
def skip_svg():
    w, h = 660, 430
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    # main path
    parts.append(f'<rect x="60" y="40" width="180" height="70" fill="#fff" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<text x="150" y="83" text-anchor="middle" font-family="Roboto Mono" font-size="16" fill="#000">INPUT x</text>')
    parts.append(f'<rect x="60" y="170" width="180" height="70" fill="rgba(0,0,0,0.06)" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<text x="150" y="200" text-anchor="middle" font-family="Roboto Mono" font-size="15" fill="#000">FILTER LAYERS</text>')
    parts.append(f'<text x="150" y="224" text-anchor="middle" font-family="Roboto Mono" font-size="14" fill="rgba(0,0,0,0.55)">learn the CHANGE</text>')
    parts.append(f'<circle cx="150" cy="330" r="30" fill="#fff" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<text x="150" y="341" text-anchor="middle" font-family="Satoshi" font-size="32" fill="#000">+</text>')
    parts.append(f'<line x1="150" y1="110" x2="150" y2="164" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<polygon points="150,168 143,153 157,153" fill="#000"/>')
    parts.append(f'<line x1="150" y1="240" x2="150" y2="294" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<polygon points="150,298 143,283 157,283" fill="#000"/>')
    # skip arrow
    parts.append(f'<path d="M 240 75 L 420 75 L 420 330 L 186 330" fill="none" stroke="#000" stroke-width="2.5" stroke-dasharray="9,7"/>')
    parts.append(f'<polygon points="182,330 198,323 198,337" fill="#000"/>')
    parts.append(f'<text x="440" y="200" font-family="Roboto Mono" font-size="16" fill="rgba(0,0,0,0.55)">SKIP CONNECTION</text>')
    parts.append(f'<text x="440" y="228" font-family="Roboto Mono" font-size="15" fill="rgba(0,0,0,0.55)">the express lane:</text>')
    parts.append(f'<text x="440" y="252" font-family="Roboto Mono" font-size="15" fill="rgba(0,0,0,0.55)">x rides through untouched</text>')
    parts.append(f'<line x1="150" y1="360" x2="150" y2="404" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<polygon points="150,408 143,393 157,393" fill="#000"/>')
    parts.append(f'<text x="220" y="395" font-family="Roboto Mono" font-size="16" fill="#000">OUTPUT = change + x</text>')
    return "".join(parts) + "</svg>"

slide(head("PART 3 · THE SHORTCUT", "ResNet — why &ldquo;deeper&rdquo; suddenly worked",
           "Surprise from 2015: a 56-layer network scored WORSE than a 20-layer one. Deeper should never be worse — a deep net could just copy the shallow one. The fix was one humble arrow.") + f"""
<div style="display:grid; grid-template-columns: 820px 1fr; column-gap:90px; margin-top:18px;">
  <div>
    {bullets([
      "In a deep stack, the learning signal must travel back through every layer — like a message whispered down a 50-person line, it <b>fades to nothing</b>.",
      "ResNet adds an express lane around every block: the input <b>skips ahead and is added back</b> at the end.",
      "Each block now only learns the small CHANGE it wants to make. Doing nothing is easy: change = 0.",
      "The learning signal rides the express lanes backwards too — 50, 100, 152 layers suddenly train fine.",
    ], size=25)}
    <div style="margin-top:18px;">
    {namebox([("SKIP / RESIDUAL CONNECTION", "the express lane: output = input + learned change"),
              ("RESNET-18 / -50", "the standard pretrained backbones; the number counts the layers")])}
    </div>
  </div>
  <div style="padding-top:24px;">{skip_svg()}</div>
</div>
""")

# ---- code card 2: transfer learning
slide(head("PART 3 · CODE", "Transfer learning is four honest lines",
           "This is the exact recipe behind the 74.2% bar — borrow, freeze, swap, train.") + f"""
<div style="display:grid; grid-template-columns: 1060px 1fr; column-gap:80px; margin-top:20px;">
  <div>
{code('''from torchvision import models

model = models.resnet18(weights="IMAGENET1K_V1")  # 1. borrow trained eyes

for p in model.parameters():
    p.requires_grad = False                       # 2. freeze them

model.fc = nn.Linear(512, 10)                     # 3. swap the decision layer

# 4. train as usual -- only the new layer learns''', caption="Result on our laptop: 74.2% with 1,000 photos — vs 50.0% from scratch with 4,000")}
  </div>
  <div>
    {knobbox([
      ("unfreeze everything", "more flexible, but with few photos it overfits — and a high learning rate DESTROYS the pretrained eyes"),
      ("tiny dataset (&lt;500 photos)", "keep frozen — frozen usually WINS here"),
      ("plenty of photos", "unfreeze with a small learning rate (0.0001) for the backbone"),
      ("weights=None", "random start — you are back to the 50% bar"),
    ])}
  </div>
</div>
""")

# ================================================================ PART 4 — SUPERPOWERS

# ---- statement
slide(dark=True, body=f"""
<div class="eyebrow">PART 4 &middot; THE SUPERPOWERS</div>
<p class="statement" style="margin-top:280px; max-width:1700px;">One label per photo<br/>was just the beginning.</p>
<p class="dek" style="margin-top:38px; max-width:1300px;">Same trained eyes, different heads bolted on: find every object, cut them out pixel by pixel, talk to images in plain English, create images from nothing.</p>
""")

# ---- detection
slide(head("PART 4 · SUPERPOWERS", "Object detection — WHERE, not just what") + f"""
<div style="display:grid; grid-template-columns: 640px 1fr; column-gap:80px; margin-top:18px;">
  <div>
    <figure style="margin:0;"><img src="assets/det_chelsea.png" width="600" height="400"/>
      <figcaption class="capn" style="margin-top:12px;">Real output of a detector (SSDLite) on our cat: <b>cat 97%</b></figcaption></figure>
    <figure style="margin:24px 0 0 0;"><img src="assets/det_astronaut.png" width="440" height="440"/>
      <figcaption class="capn" style="margin-top:12px;">Same model, busier photo: <b>person 91%</b> — many objects, one pass</figcaption></figure>
  </div>
  <div>
    {bullets([
      "The model outputs a list: <b>box + label + confidence</b> for every object it can find — all in one pass over the photo.",
      "Messy detail: the raw model proposes MANY overlapping boxes per object. A cleanup step keeps each cluster&rsquo;s most confident box and deletes the rest.",
      "How do we grade a box? Overlap with the true box: <b>area of overlap &divide; area of union</b>. 1.0 = perfect, &ge;0.5 traditionally counts as a hit.",
    ], size=24)}
    <div style="margin-top:22px;">
    {namebox([("BOUNDING BOX", "the rectangle around an object"),
              ("CONFIDENCE", "how sure the model is about that box"),
              ("IoU — INTERSECTION OVER UNION", "the overlap score for grading boxes"),
              ("NMS — NON-MAXIMUM SUPPRESSION", "the duplicate-box cleanup step")])}
    </div>
    <div style="margin-top:20px;">
    {knobbox([("confidence cutoff 0.5 → 0.8", "fewer boxes, fewer false alarms — but real objects get missed"),
              ("NMS overlap limit down", "stricter cleanup; two cats sitting together may merge into one box")])}
    </div>
  </div>
</div>
""")

# ---- detector families
slide(head("PART 4 · SUPERPOWERS", "Three detector families you should recognize",
           "All reuse a pretrained backbone as their eyes — the difference is the head and the speed/accuracy trade.") + f"""
<div style="margin-top:28px; max-width:1680px;">
<table class="tt">
<tr><th style="width:260px;">Family</th><th style="width:560px;">The idea, in plain words</th><th style="width:420px;">Character</th><th>Pick it when</th></tr>
<tr><td class="term">YOLO<br/><span style="font-weight:400; font-size:19px; color:var(--c-dim);">&ldquo;You Only Look Once&rdquo;</span></td>
    <td>cut the photo into a grid; every cell predicts boxes for objects centered in it — one single pass</td>
    <td>the speed king — 150+ photos/second on a GPU</td><td>live video, robots, drones</td></tr>
<tr><td class="term">SSD</td>
    <td>same one-pass idea, but predicts from several map sizes at once — big maps catch small objects</td>
    <td>fast and light — it produced the cat slide</td><td>phones and small devices</td></tr>
<tr><td class="term">DETR</td>
    <td>a transformer head asks ~100 learned questions: &ldquo;is there an object like X anywhere?&rdquo; — no grid, no NMS cleanup needed</td>
    <td>elegant, accurate, slower to train</td><td>accuracy over speed, modern stacks</td></tr>
</table>
</div>
<p class="dek" style="margin-top:18px; max-width:1400px;">For the exam: know the names, the one-pass idea, and that YOLO = real-time. You do not need their internals.</p>
""")

# ---- segmentation
slide(head("PART 4 · SUPERPOWERS", "Segmentation — a label for every pixel") + f"""
<div style="display:grid; grid-template-columns: repeat(3, 1fr); column-gap:36px; margin-top:38px;">
  <figure style="margin:0;"><img src="assets/seg_photo.png" width="460" height="306"/><figcaption class="cap" style="margin-top:14px;">PHOTO</figcaption></figure>
  <figure style="margin:0;"><img src="assets/seg_mask.png" width="460" height="306"/><figcaption class="cap" style="margin-top:14px;">MASK — EVERY PIXEL: CAT OR NOT</figcaption></figure>
  <figure style="margin:0;"><img src="assets/seg_cutout.png" width="460" height="306"/><figcaption class="cap" style="margin-top:14px;">CUTOUT = PHOTO &times; MASK</figcaption></figure>
</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; column-gap:80px; margin-top:20px;">
  <div>
    {bullets([
      "Boxes are rectangles; cats are not. Segmentation answers <b>per pixel</b>: which class does this pixel belong to?",
      "The classic shape is a letter <b>U</b>: shrink the photo to understand WHAT is there, then grow it back to full size to say WHERE, pixel-perfect.",
      "Shrinking loses fine detail — so express lanes copy crisp edges from the shrinking side straight to the growing side. Skip connections again!",
    ], size=24)}
  </div>
  <div>
    {namebox([("SEGMENTATION MASK", "the per-pixel answer sheet"),
              ("SEMANTIC vs INSTANCE", "&ldquo;all cat pixels&rdquo; vs &ldquo;cat #1 vs cat #2&rdquo;"),
              ("U-NET / ENCODER-DECODER", "the shrink-then-grow architecture with skip connections"),
              ("WHERE YOU MET IT", "background blur on video calls, medical scans, self-driving")])}
  </div>
</div>
""")

# ---- quick check 2
quiz("PARTS 3–4A", [
  ("Why did 1,000 photos beat 4,000 photos in our experiment?",
   "The 1,000-photo model started with pretrained eyes (transfer learning); the 4,000-photo model started from random noise."),
  ("What does a skip connection let a block do?",
   "Learn only the small CHANGE to its input — and let the learning signal travel deep without fading."),
  ("Detection vs segmentation, one sentence each?",
   "Detection: a box + label + confidence per object. Segmentation: a class for every single pixel."),
  ("What does NMS throw away?",
   "Duplicate overlapping boxes around the same object — keeps the most confident one."),
], myth=("To use deep learning you need millions of photos and a giant computer.",
         "With a pretrained backbone, 100&ndash;1,000 photos per class and a laptop is often enough. Our 74.2% ran on a CPU."))

# ---- self-supervised
def contrastive_svg():
    w, h = 700, 460
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    # photo to two views
    parts.append(f'<rect x="40" y="40" width="170" height="110" fill="rgba(0,0,0,0.06)" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<text x="125" y="100" text-anchor="middle" font-family="Roboto Mono" font-size="15" fill="#000">ONE PHOTO</text>')
    for dy, lbl in [(0, "VIEW A: crop+recolor"), (140, "VIEW B: flip+blur")]:
        parts.append(f'<rect x="330" y="{30+dy}" width="240" height="80" fill="#fff" stroke="#000" stroke-width="2"/>')
        parts.append(f'<text x="450" y="{77+dy}" text-anchor="middle" font-family="Roboto Mono" font-size="14" fill="#000">{lbl}</text>')
        parts.append(f'<line x1="210" y1="95" x2="322" y2="{70+dy}" stroke="#000" stroke-width="2"/>')
    # embedding space
    parts.append(f'<rect x="60" y="250" width="580" height="180" fill="#fff" stroke="rgba(0,0,0,0.25)" stroke-width="1.5" stroke-dasharray="6,6"/>')
    parts.append(f'<text x="80" y="282" font-family="Roboto Mono" font-size="14" fill="rgba(0,0,0,0.45)">EMBEDDING SPACE</text>')
    parts.append(f'<circle cx="290" cy="350" r="13" fill="#000"/>')
    parts.append(f'<circle cx="350" cy="370" r="13" fill="#000"/>')
    parts.append(f'<text x="320" y="412" text-anchor="middle" font-family="Roboto Mono" font-size="14" fill="#000">pull together</text>')
    parts.append(f'<circle cx="540" cy="320" r="13" fill="#fff" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<line x1="370" y1="362" x2="520" y2="328" stroke="rgba(0,0,0,0.4)" stroke-width="2" stroke-dasharray="5,6"/>')
    parts.append(f'<text x="520" y="290" text-anchor="middle" font-family="Roboto Mono" font-size="14" fill="rgba(0,0,0,0.55)">other photos: push apart</text>')
    return "".join(parts) + "</svg>"

slide(head("PART 4 · SUPERPOWERS", "Self-supervised — learning without any labels",
           "Labels are the expensive part: humans must tag every photo. The internet has billions of photos with no tags. Trick: make the photo its own label.") + f"""
<div style="display:grid; grid-template-columns: 820px 1fr; column-gap:90px; margin-top:18px;">
  <div>
    {bullets([
      "Take a photo. Make <b>two different augmented views</b> of it (crop one, flip and blur the other) — slide 18&rsquo;s tricks, reused.",
      "Rule for the network: views of the SAME photo must land close together in embedding space; different photos far apart.",
      "To pull this off it must learn what MATTERS in an image — real seeing skills, no human labels anywhere.",
      "Then add a small decision layer with just a few labeled photos on top. Nearly free trained eyes.",
    ], size=24)}
    <div style="margin-top:18px;">
    {namebox([("SELF-SUPERVISED LEARNING", "the data provides its own training signal — no human labels"),
              ("CONTRASTIVE LEARNING", "the pull-together / push-apart recipe")])}
    </div>
  </div>
  <div style="padding-top:20px;">{contrastive_svg()}</div>
</div>
""")

# ---- CLIP
clip_rows = "".join(
    f'<div style="display:grid; grid-template-columns:240px 1fr 110px; align-items:center; margin-bottom:18px;">'
    f'<span style="font-family:var(--font-mono); font-size:21px;">{lbl}</span>'
    f'<div style="background:rgba(0,0,0,0.08); height:34px;"><div style="background:#000; height:34px; width:{max(pct*5.6,3):.0f}px;"></div></div>'
    f'<span style="font-family:var(--font-mono); font-size:21px; text-align:right;">{pct:.1f}%</span></div>'
    for lbl, pct in sorted(zip(clip["prompts"], [p * 100 for p in clip["probs"]]),
                           key=lambda x: -x[1])
)

slide(head("PART 4 · SUPERPOWERS", "CLIP — the model you can talk to",
           "Don&rsquo;t teach it classes at all. Describe them in English and let the model pick the closest description.") + f"""
<div style="display:grid; grid-template-columns: 860px 1fr; column-gap:90px; margin-top:18px;">
  <div>
    {bullets([
      "CLIP is TWO encoders: one turns photos into embeddings, one turns <b>sentences</b> into embeddings — in the SAME space.",
      "Trained on 400 million internet (photo, caption) pairs with the contrastive recipe from the last slide: photo and its caption pull together.",
      "To classify: embed the photo, embed each candidate sentence, pick the closest. <b>New classes = new sentences.</b> Zero retraining.",
      "That is the 88.5% bar from slide 20 — zero training photos.",
    ], size=24)}
    <div style="margin-top:22px;">
    {namebox([("CLIP", "contrastive language–image pretraining — a shared space for photos and text"),
              ("ZERO-SHOT", "solving a task with no task-specific training examples"),
              ("PROMPT", "the sentence you classify with — wording matters")])}
    </div>
  </div>
  <div>
    <div class="cap" style="margin-bottom:24px;">Real CLIP output on our cat photo</div>
    {clip_rows}
    <div style="margin-top:20px;">
    {knobbox([("rephrase the prompt", "&ldquo;a photo of a {{class}}&rdquo; beats the bare word — a few % for free"),
              ("add classes", "just add sentences — no retraining"),
              ("bigger CLIP (ViT-L/14)", "~63% → ~75% zero-shot on the 1000-class benchmark, ~3&times; slower")])}
    </div>
  </div>
</div>
""")

# ---- code card 3: CLIP
slide(head("PART 4 · CODE", "Zero-shot classification, complete and honest") + f"""
<div style="display:grid; grid-template-columns: 1080px 1fr; column-gap:80px; margin-top:20px;">
  <div>
{code('''import clip, torch

model, preprocess = clip.load("ViT-B/32")          # trained eyes + text eyes
labels = ["a photo of a cat", "a photo of a dog",
          "a photo of a tiger", "a photo of a pizza"]

image = preprocess(my_photo).unsqueeze(0)          # photo -> tensor
text  = clip.tokenize(labels)                      # sentences -> tokens

img_emb  = model.encode_image(image)               # both into the SAME space
txt_emb  = model.encode_text(text)

sims = (img_emb @ txt_emb.T).softmax(dim=-1)       # closeness -> percentages''', caption="Output on our cat: cat 97.9% · tiger 1.6% · dog 0.5% · pizza 0.0%")}
  </div>
  <div>
    {knobbox([
      ("swap the labels list", "an entirely new classifier, instantly"),
      ("&ldquo;cat&rdquo; → &ldquo;a photo of a cat&rdquo;", "matches how captions looked in training — accuracy up"),
      ("ask something weird", "&ldquo;a photo of a grumpy cat&rdquo; works too — it is just a sentence"),
    ])}
  </div>
</div>
""")

# ---- GANs
def gan_svg():
    w, h = 720, 420
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">']
    parts.append(f'<rect x="40" y="60" width="260" height="100" fill="#000"/>')
    parts.append(f'<text x="170" y="103" text-anchor="middle" font-family="Roboto Mono" font-size="16" fill="#fff">GENERATOR</text>')
    parts.append(f'<text x="170" y="130" text-anchor="middle" font-family="Roboto Mono" font-size="13" fill="rgba(255,255,255,0.6)">noise → fake photo</text>')
    parts.append(f'<rect x="420" y="60" width="260" height="100" fill="#fff" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<text x="550" y="103" text-anchor="middle" font-family="Roboto Mono" font-size="16" fill="#000">DISCRIMINATOR</text>')
    parts.append(f'<text x="550" y="130" text-anchor="middle" font-family="Roboto Mono" font-size="13" fill="rgba(0,0,0,0.55)">real or fake?</text>')
    parts.append(f'<line x1="300" y1="110" x2="412" y2="110" stroke="#000" stroke-width="2.5"/>')
    parts.append(f'<polygon points="416,110 400,103 400,117" fill="#000"/>')
    parts.append(f'<text x="358" y="95" text-anchor="middle" font-family="Roboto Mono" font-size="13" fill="rgba(0,0,0,0.55)">fakes</text>')
    parts.append(f'<line x1="550" y1="20" x2="550" y2="52" stroke="#000" stroke-width="2"/>')
    parts.append(f'<polygon points="550,56 543,42 557,42" fill="#000"/>')
    parts.append(f'<text x="640" y="30" text-anchor="middle" font-family="Roboto Mono" font-size="13" fill="rgba(0,0,0,0.55)">real photos</text>')
    parts.append(f'<path d="M 550 160 L 550 260 L 170 260 L 170 166" fill="none" stroke="#000" stroke-width="2.5" stroke-dasharray="9,7"/>')
    parts.append(f'<polygon points="170,162 163,177 177,177" fill="#000"/>')
    parts.append(f'<text x="360" y="290" text-anchor="middle" font-family="Roboto Mono" font-size="14" fill="rgba(0,0,0,0.55)">&ldquo;caught you&rdquo; — feedback the generator learns from</text>')
    parts.append(f'<text x="360" y="370" text-anchor="middle" font-family="Roboto Mono" font-size="15" fill="#000">both get better every round — until fakes pass inspection</text>')
    return "".join(parts) + "</svg>"

slide(head("PART 4 · SUPERPOWERS", "GANs — a counterfeiter and a detective",
           "Now the other direction: not understanding images — CREATING them.") + f"""
<div style="display:grid; grid-template-columns: 820px 1fr; column-gap:90px; margin-top:18px;">
  <div>
    {bullets([
      "Two networks train against each other. The <b>counterfeiter</b> turns random noise into fake photos. The <b>detective</b> sees real photos and fakes, and calls real-or-fake.",
      "Every round the detective gets sharper, so the counterfeiter must get better — an arms race that ends in photorealistic fakes.",
      "Honest subtlety: <b>the counterfeiter NEVER sees a real photo.</b> It learns only from the detective&rsquo;s feedback.",
      "Famous, fast, but moody to train — sometimes the counterfeiter finds ONE face that always works and prints it forever.",
    ], size=24)}
    <div style="margin-top:22px;">
    {namebox([("GAN — GENERATIVE ADVERSARIAL NETWORK", "the two-player forgery game"),
              ("GENERATOR / DISCRIMINATOR", "the counterfeiter / the detective"),
              ("MODE COLLAPSE", "the one-trick-forger failure mode")])}
    </div>
  </div>
  <div style="padding-top:30px;">{gan_svg()}</div>
</div>
""")

# ---- diffusion
slide(head("PART 4 · SUPERPOWERS", "Diffusion — the idea behind modern image generators",
           "DALL·E, Stable Diffusion, Midjourney — under the hood it is this. And you already know every ingredient.") + f"""
<div style="margin-top:20px;">
  <div class="cap" style="margin-bottom:20px;">Generation runs RIGHT to LEFT: start from pure noise, remove a little at each step</div>
  <div style="display:grid; grid-template-columns: repeat(5, 250px); column-gap:36px;">
    <figure style="margin:0;"><img src="assets/diff_0.png" width="250" height="250"/><figcaption class="cap" style="margin-top:12px;">CLEAN</figcaption></figure>
    <figure style="margin:0;"><img src="assets/diff_1.png" width="250" height="250"/><figcaption class="cap" style="margin-top:12px;">STEP 250</figcaption></figure>
    <figure style="margin:0;"><img src="assets/diff_2.png" width="250" height="250"/><figcaption class="cap" style="margin-top:12px;">STEP 500</figcaption></figure>
    <figure style="margin:0;"><img src="assets/diff_3.png" width="250" height="250"/><figcaption class="cap" style="margin-top:12px;">STEP 750</figcaption></figure>
    <figure style="margin:0;"><img src="assets/diff_4.png" width="250" height="250"/><figcaption class="cap" style="margin-top:12px;">PURE NOISE</figcaption></figure>
  </div>
</div>
<div style="display:grid; grid-template-columns: 1fr 1fr; column-gap:80px; margin-top:18px;">
  <div>
    {bullets([
      "<b>Training:</b> take a photo, add a random amount of noise, ask a network to predict the noise. Easy, stable homework — no arms race.",
      "<b>Generating:</b> start from pure noise, remove a little ~50 times. A text prompt (via CLIP-style text understanding) steers every step.",
    ], size=24)}
  </div>
  <div>
    {namebox([("DIFFUSION MODEL", "learns to remove noise; generates by denoising step by step"),
              ("GUIDANCE SCALE", "how hard the prompt steers — ~7.5 is typical; too high looks burnt"),
              ("STEPS", "more = better and slower; 20–50 is common")])}
  </div>
</div>
""")

# ================================================================ PART 5 — CHEAT SHEETS

# ---- quick check 3
quiz("PART 4B", [
  ("How does CLIP classify a photo of a thing it was never explicitly taught?",
   "It embeds the photo and your candidate sentences into the same space and picks the closest sentence."),
  ("In a GAN, which network never sees a real photo?",
   "The generator — it learns only from the discriminator&rsquo;s feedback."),
  ("What is a diffusion model&rsquo;s only skill?",
   "Removing a little noise. Generation = applying that skill ~50 times starting from pure noise."),
  ("Self-supervised learning has no labels. What replaces them?",
   "The photo itself: two augmented views must land close together in embedding space."),
])

# ---- syllabus map
slide(head("PART 5 · CHEAT SHEET", "The IOAI syllabus map — where we covered what",
           "Every Section 3 topic, the slide where it lives, and the one line to remember.") + f"""
<div style="margin-top:18px; max-width:1700px;">
<table class="tt" style="font-size:22px;">
<tr><th style="width:430px;">Syllabus topic</th><th style="width:130px;">Slides</th><th>One line to remember</th></tr>
<tr><td class="term" style="font-size:23px;">Images as tensors, pixels</td><td class="mono">05</td><td style="font-size:23px;">a photo is 3 stacked grids of numbers 0&ndash;255</td></tr>
<tr><td class="term" style="font-size:23px;">Convolution, filters, stride, padding</td><td class="mono">06&ndash;08</td><td style="font-size:23px;">slide a stencil, multiply &amp; add; stride = step size, padding = zero border</td></tr>
<tr><td class="term" style="font-size:23px;">Pooling (max/avg/global)</td><td class="mono">09</td><td style="font-size:23px;">keep each window&rsquo;s winner — smaller map, shift-forgiving</td></tr>
<tr><td class="term" style="font-size:23px;">Activations (ReLU)</td><td class="mono">10</td><td style="font-size:23px;">zero the negatives — without the bend, depth is fake</td></tr>
<tr><td class="term" style="font-size:23px;">CNNs &amp; classification</td><td class="mono">11&ndash;12</td><td style="font-size:23px;">stacked filters climb edges → textures → parts → objects</td></tr>
<tr><td class="term" style="font-size:23px;">Loss, gradient descent, overfitting, augmentation</td><td class="mono">14&ndash;18</td><td style="font-size:23px;">roll downhill on the wrongness landscape; never grade on the study set</td></tr>
<tr><td class="term" style="font-size:23px;">Pretrained encoders, ResNet, transfer learning</td><td class="mono">21&ndash;23</td><td style="font-size:23px;">borrow trained eyes, swap the decision layer; skips let depth train</td></tr>
<tr><td class="term" style="font-size:23px;">Detection (YOLO/SSD/DETR), IoU, NMS</td><td class="mono">25&ndash;26</td><td style="font-size:23px;">box + label + confidence in one pass; IoU grades, NMS dedupes</td></tr>
<tr><td class="term" style="font-size:23px;">Segmentation, U-Net</td><td class="mono">27</td><td style="font-size:23px;">a class per pixel; shrink to understand, grow back to localize</td></tr>
<tr><td class="term" style="font-size:23px;">Self-supervised / contrastive</td><td class="mono">29</td><td style="font-size:23px;">two views of one photo pull together — the data labels itself</td></tr>
<tr><td class="term" style="font-size:23px;">CLIP &amp; zero-shot</td><td class="mono">30&ndash;31</td><td style="font-size:23px;">photos and sentences share one space; new classes = new sentences</td></tr>
<tr><td class="term" style="font-size:23px;">Generative: GANs, diffusion</td><td class="mono">32&ndash;33</td><td style="font-size:23px;">forgery arms race vs learn-to-denoise — diffusion won the quality war</td></tr>
</table>
</div>
""")

# ---- glossary
gloss = [
  ("pixel", "one square of a photo, holding a number 0–255"),
  ("tensor", "a grid (or stack of grids) of numbers"),
  ("model", "a machine made of numbers: input → guess"),
  ("label", "the correct answer attached to an example"),
  ("convolution", "slide a stencil, multiply matching cells, add"),
  ("filter / kernel", "the stencil of numbers"),
  ("feature map", "the glow-map: bright = pattern found here"),
  ("stride", "how far the stencil steps each move"),
  ("padding", "zeros glued around the border"),
  ("pooling", "keep each window's max (or mean) — shrink the map"),
  ("ReLU", "negatives → 0; the bend that makes depth real"),
  ("CNN", "the full stack of filter layers"),
  ("embedding", "the short number-list summary of an input"),
  ("softmax", "scores → percentages that sum to 100"),
  ("loss", "the wrongness score"),
  ("gradient descent", "nudge every number downhill on the loss"),
  ("learning rate", "the step size of those nudges"),
  ("epoch", "one full pass through the dataset"),
  ("overfitting", "memorizing the study set, failing the exam"),
  ("augmentation", "flip/crop/recolor — free extra photos"),
  ("pretrained / backbone", "a network someone already trained"),
  ("transfer learning", "reuse trained eyes on a new task"),
  ("finetuning", "gentle retraining on your own data"),
  ("skip connection", "express lane: output = input + change"),
  ("bounding box / IoU / NMS", "detection's rectangle, grade, and dedupe"),
  ("segmentation mask", "a class for every pixel"),
  ("self-supervised", "the data provides its own training signal"),
  ("CLIP / zero-shot", "shared photo-text space; classify by sentence"),
  ("GAN", "counterfeiter vs detective"),
  ("diffusion", "generate by removing noise, step by step"),
]
half = (len(gloss) + 1) // 2
def gcol(items):
    return "".join(
        f'<p style="font-size:22.5px; line-height:1.32; margin:0 0 15px 0;"><b style="font-weight:500;">{t}</b>'
        f'<span style="color:var(--c-dim);"> — {d}</span></p>' for t, d in items)
slide(head("PART 5 · CHEAT SHEET", "Every word we earned today — all 30") + f"""
<div style="display:grid; grid-template-columns: 1fr 1fr; column-gap:100px; margin-top:18px; max-width:1700px;">
  <div>{gcol(gloss[:half])}</div>
  <div>{gcol(gloss[half:])}</div>
</div>
""")

# ---- knob cheat sheet
slide(head("PART 5 · CHEAT SHEET", "The knob table — change this, get that",
           "The practical round usually asks exactly this: predict what a change does before you run it.") + f"""
<div style="margin-top:18px; max-width:1700px;">
<table class="tt" style="font-size:22px;">
<tr><th style="width:480px;">Turn this knob</th><th>What happens</th></tr>
<tr><td class="term" style="font-size:23px;">more filters per layer (32 → 128)</td><td style="font-size:23px;">richer patterns spotted; ~4&times; the numbers to learn and compute</td></tr>
<tr><td class="term" style="font-size:23px;">bigger kernel (3&times;3 → 7&times;7)</td><td style="font-size:23px;">sees wider patterns; 9 → 49 multiplies per stop</td></tr>
<tr><td class="term" style="font-size:23px;">stride 1 → 2</td><td style="font-size:23px;">output map halves; faster, blurrier view</td></tr>
<tr><td class="term" style="font-size:23px;">remove ReLU</td><td style="font-size:23px;">depth collapses to one layer; accuracy tanks</td></tr>
<tr><td class="term" style="font-size:23px;">learning rate &times;100</td><td style="font-size:23px;">loss bounces or explodes — never settles</td></tr>
<tr><td class="term" style="font-size:23px;">learning rate &divide;100</td><td style="font-size:23px;">crawls; may never arrive in time</td></tr>
<tr><td class="term" style="font-size:23px;">train far past the test-accuracy peak</td><td style="font-size:23px;">overfitting — train score up, exam score down</td></tr>
<tr><td class="term" style="font-size:23px;">add flip/crop augmentation</td><td style="font-size:23px;">typically +3&ndash;8% test accuracy on small datasets</td></tr>
<tr><td class="term" style="font-size:23px;">pretrained start vs random start</td><td style="font-size:23px;">our receipts: 74.2% with 1,000 photos vs 50.0% with 4,000</td></tr>
<tr><td class="term" style="font-size:23px;">detector confidence cutoff up</td><td style="font-size:23px;">fewer false alarms, more missed objects</td></tr>
<tr><td class="term" style="font-size:23px;">better CLIP prompt wording</td><td style="font-size:23px;">a few % accuracy for free — no retraining</td></tr>
<tr><td class="term" style="font-size:23px;">diffusion guidance scale up (7.5 → 20)</td><td style="font-size:23px;">obeys the prompt harder; colors go burnt, variety drops</td></tr>
</table>
</div>
""")

# ---- close
slide(dark=True, body=f"""
<div class="eyebrow">THE END &middot; GO WIN</div>
<p class="statement" style="margin-top:280px; max-width:1750px;">It was never magic.<br/>It was multiply, add,<br/>and practice.</p>
<p class="dek" style="margin-top:28px; max-width:1300px;">Everything today ran on an ordinary laptop, and every number on these slides is real. The notebooks to re-run them are in our repo.</p>
""")

# ================================================================ render
def main():
    html = ("<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<style>{CSS}</style></head><body>" + "".join(SLIDES) + "</body></html>")
    out_html = HERE / "beginner_deck.html"
    out_html.write_text(html)
    print(f"slides: {len(SLIDES)}")
    from weasyprint import HTML
    HTML(str(out_html), base_url=str(HERE.parent)).write_pdf(str(HERE.parent / "presentation" / "how_machines_learn_to_see.pdf"))
    print("PDF written")

if __name__ == "__main__":
    main()
