# Builds teacher_guide.pdf — a slide-by-slide companion in simple English.
# Run from this folder:  uv run --with weasyprint --with pymupdf python build_teacher_guide.py
import html as H
import os
import fitz
from weasyprint import HTML
from guide_content import GUIDE

HERE = os.path.dirname(os.path.abspath(__file__))
DECK_PDF = os.path.join(HERE, "..", "presentation", "how_machines_learn_to_see.pdf")
THUMB_DIR = os.path.join(HERE, "_thumbs")
OUT = os.path.join(HERE, "..", "teacher", "teacher_guide.pdf")

CSS = """
@page { size: 210mm 297mm; margin: 16mm 16mm 18mm 16mm;
        @bottom-right { content: counter(page); font-family: 'Roboto Mono', monospace;
                        font-size: 8pt; color: #999; } }
* { box-sizing: border-box; }
body { font-family: 'Satoshi', 'Helvetica Neue', Arial, sans-serif; color: #000;
       font-size: 10.5pt; line-height: 1.5; margin: 0; }
.cover { page-break-after: always; padding-top: 60mm; }
.cover .kicker { font-family: 'Roboto Mono', monospace; font-size: 9pt; letter-spacing: 0.2em;
                 text-transform: uppercase; color: #666; }
.cover h1 { font-size: 34pt; font-weight: 500; letter-spacing: -0.02em; line-height: 1.1;
            margin: 8mm 0 6mm 0; }
.cover p { font-size: 12pt; color: #333; max-width: 150mm; }
.howto { background: #f4f4f4; padding: 6mm 7mm; margin-top: 10mm; max-width: 160mm; }
.howto p { font-size: 10.5pt; margin: 0 0 2.5mm 0; }
.entry { page-break-inside: avoid; margin-bottom: 9mm; border-top: 1.2pt solid #000;
         padding-top: 4mm; }
.entry .num { font-family: 'Roboto Mono', monospace; font-size: 8.5pt; letter-spacing: 0.18em;
              color: #666; text-transform: uppercase; }
.entry h2 { font-size: 15pt; font-weight: 600; letter-spacing: -0.01em; margin: 1.5mm 0 3.5mm 0; }
.thumb { width: 74mm; float: right; margin: 0 0 3mm 5mm; border: 0.4pt solid #ccc; }
.lbl { font-family: 'Roboto Mono', monospace; font-size: 7.5pt; letter-spacing: 0.18em;
       text-transform: uppercase; color: #888; margin: 3mm 0 1mm 0; }
.mean p { margin: 0 0 2.5mm 0; }
.say { background: #000; color: #fff; padding: 3.5mm 4.5mm; margin-top: 2mm; }
.say p { margin: 0; font-size: 10pt; }
.say .lbl { color: #aaa; margin: 0 0 1mm 0; }
.ask { background: #f4f4f4; padding: 3mm 4.5mm; margin-top: 2.5mm; }
.ask p { margin: 0 0 1.5mm 0; font-size: 9.5pt; }
.ask .lbl { margin: 0 0 1mm 0; }
.clear { clear: both; }
b { font-weight: 600; }
"""


def render_thumbs():
    os.makedirs(THUMB_DIR, exist_ok=True)
    doc = fitz.open(DECK_PDF)
    for i, page in enumerate(doc):
        out = os.path.join(THUMB_DIR, f"s{i+1:02d}.png")
        if not os.path.exists(out):
            page.get_pixmap(dpi=60).save(out)
    return len(doc)


def entry_html(e):
    paras = "".join(f"<p>{p}</p>" for p in e["mean"])
    ask = ""
    if e.get("ask"):
        qa = "".join(f'<p><b>&ldquo;{H.escape(q)}&rdquo;</b> — {H.escape(a)}</p>' for q, a in e["ask"])
        ask = f'<div class="ask"><div class="lbl">If they ask</div>{qa}</div>'
    return f"""
    <div class="entry">
      <div class="num">Slide {e['n']:02d} of 39</div>
      <h2>{e['title']}</h2>
      <img class="thumb" src="_thumbs/s{e['n']:02d}.png"/>
      <div class="lbl">What this actually means</div>
      <div class="mean">{paras}</div>
      <div class="say"><div class="lbl">Say this</div><p>{e['say']}</p></div>
      {ask}
      <div class="clear"></div>
    </div>"""


def main():
    n = render_thumbs()
    assert n == len(GUIDE) == 39, (n, len(GUIDE))
    cover = """
    <div class="cover">
      <div class="kicker">Teacher guide &middot; read me the night before</div>
      <h1>How machines learn to see<br/>— explained simply, slide by slide</h1>
      <p>This guide walks through all 39 slides of the presentation in the simplest English possible.
         For each slide: a small picture of it, what it actually means, the key sentence to say out loud,
         and answers to questions students might ask.</p>
      <div class="howto">
        <p><b>How to use this guide</b></p>
        <p>1. Read it once, start to finish. It takes about 45 minutes.</p>
        <p>2. Any part that makes you pause &mdash; read that section twice. The cheat-sheet slides (36&ndash;38) double as your own revision check.</p>
        <p>3. While presenting, you do not need this guide open &mdash; the &ldquo;say this&rdquo; lines are the backbone, and the slides carry the rest.</p>
        <p>4. Slide 6 is the heart of the whole talk. Practice the nine multiplications once so you can lead them confidently.</p>
      </div>
    </div>"""
    body = cover + "".join(entry_html(e) for e in GUIDE)
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    HTML(string=html, base_url=HERE).write_pdf(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
