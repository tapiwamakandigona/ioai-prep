#!/usr/bin/env python3
"""Build the from-scratch lesson deck: How a Computer Sees (1920x1080, Viktor)."""
import json, html as html_mod
from pathlib import Path

HERE = Path(__file__).parent
A = HERE / "assets"
INK = "#000000"

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
       background:#fff; font-feature-settings:"tnum" 1,"lnum" 1,"ss01" 1; }
.slide { position:relative; width:1920px; height:1080px; padding:80px 120px;
         box-sizing:border-box; overflow:hidden; background:#fff; color:#000;
         page-break-after:always; }
.slide--dark { background:#000; color:#fff; }
.slide--dark .eyebrow { color:rgba(255,255,255,0.55); }
.slide--dark .pagenum { color:rgba(255,255,255,0.35); }
p, .dek, figcaption { text-wrap:pretty; } h1,h2,.title { text-wrap:balance; }
.eyebrow { font-family:var(--font-mono); font-size:13px; letter-spacing:0.16em;
           text-transform:uppercase; color:var(--c-dim); }
.title { font-size:96px; line-height:1.02; font-weight:500; letter-spacing:-0.03em;
         margin:28px 0 0 0; }
.statement { font-size:144px; line-height:1.0; font-weight:500; letter-spacing:-0.03em; margin:0; }
.dek { font-size:34px; line-height:1.3; color:var(--c-dim); margin:0; }
.pagenum { position:absolute; right:120px; top:84px; font-family:var(--font-mono);
           font-size:13px; letter-spacing:0.16em; color:var(--c-faint); }
.bullets { margin:0; padding:0; list-style:none; }
.bullets li { font-size:30px; line-height:1.35; margin-bottom:26px; padding-left:44px;
              position:relative; }
.bullets li:before { content:"\\2192"; position:absolute; left:0; color:var(--c-faint); }
.cap { font-family:var(--font-mono); font-size:13px; letter-spacing:0.16em;
       text-transform:uppercase; color:var(--c-dim); }
.capn { font-size:20px; color:var(--c-dim); line-height:1.35; }
img { image-rendering:auto; }
img.px { image-rendering:pixelated; }
.code { font-family:var(--font-mono); font-size:26px; line-height:1.6;
        background:var(--c-fill-subtle); padding:44px 52px; white-space:pre; }
.code .cm { color:var(--c-dim); }
.interact { position:absolute; left:120px; bottom:80px; font-family:var(--font-mono);
            font-size:13px; letter-spacing:0.16em; text-transform:uppercase; }
.interact b { font-weight:500; background:#000; color:#fff; padding:6px 12px; margin-right:14px; }
"""

# ---------------------------------------------------------------- helpers
def esc(s): return html_mod.escape(s, quote=False)

def slide(body, n, dark=False, eyebrow=None, title=None, interact=None):
    cls = "slide slide--dark" if dark else "slide"
    head = ""
    if eyebrow:
        head += f'<div class="eyebrow">{eyebrow}</div>'
    if title:
        head += f'<h1 class="title" style="font-size:84px">{title}</h1>'
    inter = ""
    if interact:
        inter = f'<div class="interact"><b>LIVE</b>{interact}</div>'
    return (f'<div class="{cls}"><div class="pagenum">{n:02d}</div>'
            f'{head}{body}{inter}</div>')

SLIDES = []

# ---------------------------------------------------------------- 1 cover
SLIDES.append("""
<div class="slide"><div class="eyebrow">A LESSON &middot; COMPUTER VISION &middot; BY A STUDENT, FOR STUDENTS</div>
<h1 class="statement" style="font-size:176px; margin-top:330px;">How a computer<br>sees</h1>
</div>""")

# ---------------------------------------------------------------- 2 the plan
SLIDES.append(slide(f"""
<div style="margin-top:108px; max-width:1240px;">
  <div style="display:grid; grid-template-columns:170px 1fr; row-gap:54px; column-gap:0;">
    <div class="cap" style="padding-top:8px;">ACT 1</div>
    <div style="font-size:34px; line-height:1.35;">How a computer sees &mdash; we compute what a network computes, <span style="white-space:nowrap;">by hand.</span></div>
    <div class="cap" style="padding-top:8px;">ACT 2</div>
    <div style="font-size:34px; line-height:1.35;">How it learns &mdash; nobody programs it; it practices. With my own&nbsp;results.</div>
    <div class="cap" style="padding-top:8px;">ACT 3</div>
    <div style="font-size:34px; line-height:1.35;">What this unlocks &mdash; finding objects, cutting them out, words, generating&nbsp;images.</div>
  </div>
  <p class="dek" style="margin-top:96px; max-width:1100px;">The promise: in one hour you can explain how a photo becomes the word&nbsp;&ldquo;cat.&rdquo;</p>
</div>""", 2, eyebrow="ONE HOUR &middot; ONE STORY", title="The plan"))

# ---------------------------------------------------------------- 3 act 1 divider
SLIDES.append(slide("""
<h1 class="statement" style="margin-top:320px;">A computer has never<br>seen a cat.</h1>
""", 3, dark=True, eyebrow="ACT 1 &middot; HOW A COMPUTER SEES"))

# ---------------------------------------------------------------- 4 pixels
# real 10x10 pixel grid, values from the actual photo
cells = []
for row in pix:
    for v in row:
        # text color flips on dark cells
        tc = "#FFFFFF" if v < 110 else "#000000"
        cells.append(f'<div style="background:rgb({v},{v},{v}); color:{tc}; '
                     f'display:flex; align-items:center; justify-content:center;">{v}</div>')
grid = ('<div style="display:grid; grid-template-columns:repeat(10,52px); '
        'grid-template-rows:repeat(10,52px); font-family:var(--font-mono); '
        'font-size:15px; border:1px solid rgba(0,0,0,0.25);">' + "".join(cells) + "</div>")
SLIDES.append(slide(f"""
<div style="display:flex; gap:90px; margin-top:96px; align-items:flex-start;">
  <div style="width:640px;">
    <img src="assets/chelsea_marked.png" width="640" height="426"/>
    <div class="cap" style="margin-top:18px;">A REAL PHOTO &middot; WHITE BOX = 10&times;10 PIXELS ON HER EYE</div>
    <ul class="bullets" style="margin-top:54px;">
      <li>Each square is a <b>pixel</b>: one brightness number. 0&nbsp;=&nbsp;black, 255&nbsp;=&nbsp;white.</li>
      <li>Color photos: three grids &mdash; red, green, blue.</li>
    </ul>
  </div>
  <div>
    {grid}
    <div class="cap" style="margin-top:18px;">THAT BOX, ZOOMED ALL THE WAY IN &middot; REAL VALUES</div>
    <div class="capn" style="margin-top:10px; max-width:520px;">This grid is ALL the computer gets. No cat, no eye &mdash; just these numbers.</div>
  </div>
</div>""", 4, eyebrow="STEP 1 &middot; WHAT THE COMPUTER ACTUALLY RECEIVES",
     title="A photo is just a grid of numbers",
     interact="ASK THE CHAT: WHICH CORNER HAS THE BIG NUMBERS &mdash; FUR OR PUPIL?"))

# ---------------------------------------------------------------- 5 hand conv
def hgrid(vals, cell=86, fs=30, hl=None):
    n = len(vals[0]); out = []
    for i, row in enumerate(vals):
        for j, v in enumerate(row):
            sty = "background:#fff;"
            if isinstance(v, int) and v == 2: sty = "background:rgba(0,0,0,0.16);"
            out.append(f'<div style="{sty} display:flex; align-items:center; '
                       f'justify-content:center;">{v}</div>')
    w, h = n*cell, len(vals)*cell
    hl_div = ""
    if hl:
        hl_div = (f'<div style="position:absolute; left:{hl[1]*cell}px; top:{hl[0]*cell}px; '
                  f'width:{3*cell-8}px; height:{3*cell-8}px; border:4px solid #000;"></div>')
    return (f'<div style="position:relative; width:{w}px; height:{h}px; '
            f'border:1px solid rgba(0,0,0,0.3); box-sizing:content-box;">'
            f'<div style="display:grid; grid-template-columns:repeat({n},{cell}px); '
            f'grid-template-rows:repeat({len(vals)},{cell}px); gap:0; width:{w}px; '
            f'font-family:var(--font-mono); font-size:{fs}px;">'
            + "".join(out) + f"</div>{hl_div}</div>")

inp = [[2,2,0,0,0]]*5
filt = [[1,0,-1]]*3
SLIDES.append(slide(f"""
<div style="display:flex; gap:56px; margin-top:90px; align-items:flex-start;">
  <div style="flex:0 0 auto;">
    {hgrid(inp, cell=80, hl=(1,0))}
    <div class="cap" style="margin-top:16px;">IMAGE &middot; BRIGHT STRIPE (2s), DARK (0s)</div>
  </div>
  <div style="flex:0 0 auto; font-size:56px; padding-top:150px; color:var(--c-dim);">&times;</div>
  <div style="flex:0 0 auto;">
    {hgrid(filt, cell=80)}
    <div class="cap" style="margin-top:16px;">FILTER &middot; A 3&times;3 STENCIL</div>
  </div>
  <div style="flex:0 0 auto; font-size:56px; padding-top:150px; color:var(--c-dim);">=</div>
  <div style="padding-top:6px; max-width:600px; flex:0 0 600px;">
    <div style="font-family:var(--font-mono); font-size:25px; line-height:1.75;">
      2&middot;1 + 2&middot;0 + 0&middot;(&minus;1)&nbsp;=&nbsp;2<br>
      2&middot;1 + 2&middot;0 + 0&middot;(&minus;1)&nbsp;=&nbsp;2<br>
      2&middot;1 + 2&middot;0 + 0&middot;(&minus;1)&nbsp;=&nbsp;2
    </div>
    <div style="font-size:62px; font-weight:500; margin-top:30px;">sum&nbsp;=&nbsp;6 &nbsp;<span style="font-size:30px; color:var(--c-dim); font-weight:400;">loud &mdash; &ldquo;edge here!&rdquo;</span></div>
    <div style="border-top:1px solid var(--c-line); margin-top:34px; padding-top:30px;
                font-size:28px; color:var(--c-dim); line-height:1.45;">
      Slide the stencil onto the flat dark area: every product is 0.<br>
      <span style="color:#000; font-weight:500;">sum&nbsp;=&nbsp;0</span> &mdash; silent. The filter only shouts on <i>its</i>&nbsp;pattern.</div>
  </div>
</div>""", 5, eyebrow="STEP 2 &middot; THE ONE TRICK BEHIND ALL OF COMPUTER VISION",
     title="Convolution: multiply, add &mdash; done by hand",
     interact="WE COMPUTE THE NINE PRODUCTS TOGETHER, OUT LOUD, BEFORE THE ANSWER"))

# ---------------------------------------------------------------- 6 feature maps
SLIDES.append(slide("""
<div style="display:flex; gap:60px; margin-top:104px;">
  <figure style="margin:0;">
    <img src="assets/chelsea_gray.png" width="500" height="333"/>
    <figcaption class="cap" style="margin-top:16px;">INPUT PHOTO</figcaption>
  </figure>
  <figure style="margin:0;">
    <img src="assets/fmap_vertical.png" width="500" height="333"/>
    <figcaption class="cap" style="margin-top:16px;">OUR FILTER FROM LAST SLIDE &middot; VERTICAL EDGES</figcaption>
  </figure>
  <figure style="margin:0;">
    <img src="assets/fmap_horizontal.png" width="500" height="333"/>
    <figcaption class="cap" style="margin-top:16px;">SAME FILTER, ROTATED &middot; HORIZONTAL EDGES</figcaption>
  </figure>
</div>
<p class="dek" style="margin-top:74px; max-width:1480px;">White = the stencil shouted &ldquo;my pattern is here.&rdquo; Whiskers and eye outlines glow.
Real output &mdash; this exact code ran on this exact photo.</p>
""", 6, eyebrow="STEP 3 &middot; ONE FILTER, RUN EVERYWHERE",
     title="A filter is a pattern detector"))

# ---------------------------------------------------------------- 7 stack layers
SLIDES.append(slide("""
<div style="display:flex; gap:100px; margin-top:96px; align-items:flex-start;">
  <div style="width:560px;">
    <div style="display:grid; grid-template-columns:200px 1fr; row-gap:38px; font-size:29px; line-height:1.3;">
      <div class="cap" style="padding-top:6px;">LAYER 1</div><div>edges &amp; color blobs</div>
      <div class="cap" style="padding-top:6px;">LAYER 2</div><div>textures &mdash; fur, stripes, mesh</div>
      <div class="cap" style="padding-top:6px;">DEEPER</div><div>parts &mdash; ear, eye, wheel</div>
      <div class="cap" style="padding-top:6px;">LAST</div><div>whole objects &mdash; &ldquo;cat&rdquo;</div>
    </div>
    <p class="capn" style="margin-top:52px; max-width:520px;">Each layer looks at the previous layer&rsquo;s maps,
    not the raw photo. This stack is a <b>convolutional neural network</b> &mdash; a&nbsp;CNN.</p>
  </div>
  <div>
    <img src="assets/resnet_filters.png" width="1016" height="248" class="px"/>
    <div class="cap" style="margin-top:18px;">ALL 64 FIRST-LAYER FILTERS OF RESNET18 &middot; LEARNED FROM 1.28M PHOTOS</div>
    <div class="capn" style="margin-top:12px; max-width:980px;">Nobody drew these. The network discovered, by itself,
    that edge and color stencils are the right place to start &mdash; the same idea you just computed by hand.</div>
  </div>
</div>""", 7, eyebrow="STEP 4 &middot; STACKING FILTERS",
     title="Edges &rarr; textures &rarr; parts &rarr; objects"))

# ---------------------------------------------------------------- 8 code card 1
SLIDES.append(slide("""
<div style="margin-top:108px; max-width:1320px;">
<div class="code">import torch.nn as nn

layer = nn.Conv2d(in_channels=3,    <span class="cm"># red, green, blue</span>
                  out_channels=32,  <span class="cm"># learn 32 different stencils</span>
                  kernel_size=3)    <span class="cm"># each stencil is 3&times;3</span></div>
<p class="dek" style="margin-top:60px;">One line of Python = 32 sliding stencils &mdash;
exactly the operation you did by&nbsp;hand.</p>
</div>""", 8, eyebrow="CODE CARD 1 OF 4 &middot; PYTORCH",
     title="The whole &ldquo;eye&rdquo; is one line"))

# ---------------------------------------------------------------- 9 act 2 divider
SLIDES.append(slide("""
<h1 class="statement" style="margin-top:320px;">Nobody programs the filters.<br>The network finds them.</h1>
""", 9, dark=True, eyebrow="ACT 2 &middot; HOW IT LEARNS"))

# ---------------------------------------------------------------- 10 learning loop
loop_svg = f"""
<svg width="1560" height="430" viewBox="0 0 1560 430" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
 orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/></marker></defs>
<image href="assets/aug_original.png" x="0" y="60" width="190" height="190"/>
<text x="95" y="290" font-family="Roboto Mono" font-size="13" letter-spacing="1.5" fill="{INK}" fill-opacity="0.55" text-anchor="middle">PHOTO</text>
<line x1="206" y1="155" x2="280" y2="155" stroke="{INK}" stroke-width="2" marker-end="url(#arr)"/>
<rect x="292" y="105" width="260" height="100" fill="{INK}"/>
<text x="422" y="148" font-family="Satoshi" font-size="26" fill="#FFFFFF" text-anchor="middle">network</text>
<text x="422" y="182" font-family="Roboto Mono" font-size="12" letter-spacing="1.5" fill="#FFFFFF" fill-opacity="0.6" text-anchor="middle">RANDOM STENCILS AT FIRST</text>
<line x1="566" y1="155" x2="640" y2="155" stroke="{INK}" stroke-width="2" marker-end="url(#arr)"/>
<rect x="652" y="105" width="300" height="100" fill="{INK}" fill-opacity="0.05" stroke="{INK}" stroke-opacity="0.4"/>
<text x="802" y="146" font-family="Satoshi" font-size="25" fill="{INK}" text-anchor="middle">guess: &#8220;70% dog&#8221;</text>
<text x="802" y="182" font-family="Roboto Mono" font-size="12" letter-spacing="1.5" fill="{INK}" fill-opacity="0.45" text-anchor="middle">TRUTH: CAT</text>
<line x1="966" y1="155" x2="1040" y2="155" stroke="{INK}" stroke-width="2" marker-end="url(#arr)"/>
<rect x="1052" y="105" width="280" height="100" fill="{INK}" fill-opacity="0.05" stroke="{INK}" stroke-opacity="0.4"/>
<text x="1192" y="146" font-family="Satoshi" font-size="25" fill="{INK}" text-anchor="middle">loss = how wrong</text>
<text x="1192" y="182" font-family="Roboto Mono" font-size="12" letter-spacing="1.5" fill="{INK}" fill-opacity="0.45" text-anchor="middle">ONE NUMBER &middot; BIG = ICE COLD</text>
<path d="M 1192 215 C 1192 380, 422 380, 422 215" fill="none" stroke="{INK}" stroke-width="2.5" stroke-dasharray="8 7" marker-end="url(#arr)"/>
<text x="807" y="358" font-family="Roboto Mono" font-size="13" letter-spacing="1.5" fill="{INK}" text-anchor="middle">NUDGE EVERY STENCIL A TINY STEP THAT SHRINKS THE LOSS &middot; REPEAT A MILLION TIMES</text>
</svg>"""
SLIDES.append(slide(f"""
<div style="margin-top:100px;">{loop_svg}</div>
<p class="dek" style="margin-top:48px; max-width:1500px;">The hot-and-cold game: guess, get told &ldquo;colder,&rdquo; adjust.
After enough rounds, random noise has turned into the edge detectors you&nbsp;saw.</p>
""", 10, eyebrow="STEP 5 &middot; NO EQUATIONS, PROMISE",
     title="Learning = guess, get told how wrong, adjust"))

# ---------------------------------------------------------------- 11 augmentation + code 2
augs = [("aug_original.png","ORIGINAL"),("aug_flip.png","MIRRORED"),("aug_crop.png","RANDOM CROP"),
        ("aug_jitter.png","COLOR SHIFT"),("aug_noise.png","NOISE")]
aug_html = "".join(
    f'<figure style="margin:0;"><img src="assets/{f}" width="280" height="280"/>'
    f'<figcaption class="cap" style="margin-top:14px;">{c}</figcaption></figure>'
    for f, c in augs)
SLIDES.append(slide(f"""
<div style="display:flex; gap:70px; margin-top:88px;">{aug_html}</div>
<div style="display:flex; gap:90px; margin-top:64px; align-items:flex-start;">
  <div class="code" style="font-size:23px; flex:0 0 880px;">train_tf = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
])</div>
  <p style="font-size:28px; line-height:1.45; color:var(--c-dim); max-width:620px; margin:6px 0 0 0;">
  A mirrored cat is still a cat. Every epoch each photo arrives slightly different,
  so the network can&rsquo;t memorize &mdash; it must learn what cats <i>look like</i>.
  <span style="color:#000;">These are the exact lines from my training&nbsp;code.</span></p>
</div>""", 11, eyebrow="CODE CARD 2 OF 4 &middot; DATA AUGMENTATION",
     title="Free extra photos: one cat, five lessons"))

# ---------------------------------------------------------------- 12 results chart
def bar(x, pct, label1, label2, dim=False, h_max=440, base=540):
    h = pct / 100 * h_max
    y = base - h
    op = 0.22 if dim else 1.0
    return f"""
<rect x="{x}" y="{y:.0f}" width="210" height="{h:.0f}" fill="{INK}" fill-opacity="{op}"/>
<text x="{x+105}" y="{y-24:.0f}" font-family="Roboto Mono" font-size="38" fill="{INK}" fill-opacity="{0.45 if dim else 1}" text-anchor="middle">{pct}%</text>
<text x="{x+105}" y="{base+46}" font-family="Roboto Mono" font-size="13" letter-spacing="1.5" fill="{INK}" fill-opacity="0.55" text-anchor="middle">{label1}</text>
<text x="{x+105}" y="{base+72}" font-family="Roboto Mono" font-size="13" letter-spacing="1.5" fill="{INK}" fill-opacity="0.35" text-anchor="middle">{label2}</text>"""
chart = f"""
<svg width="1180" height="640" viewBox="0 0 1180 640" xmlns="http://www.w3.org/2000/svg">
{bar(10, 10, "RANDOM GUESSING", "NO MODEL AT ALL", dim=True)}
{bar(320, 50.0, "MY SMALL CNN", "FROM SCRATCH &middot; 4,000 PHOTOS")}
{bar(630, 74.2, "RESNET18, FINETUNED", "ONLY 1,000 PHOTOS")}
{bar(940, 88.5, "CLIP, ZERO-SHOT", "0 TRAINING PHOTOS")}
<line x1="0" y1="540" x2="1180" y2="540" stroke="{INK}" stroke-width="2"/>
</svg>"""
SLIDES.append(slide(f"""
<div style="display:flex; gap:70px; margin-top:80px; align-items:flex-start;">
  <div style="flex:0 0 1180px;">{chart}</div>
  <div style="max-width:400px; padding-top:60px;">
    <p style="font-size:28px; line-height:1.5; margin:0;">Same task: tiny photos, 10 categories (CIFAR-10).
    Accuracy on photos the models never saw.</p>
    <p style="font-size:28px; line-height:1.5; color:var(--c-dim); margin-top:36px;">All three are my runs,
    on an ordinary CPU. The notebooks rerun everything tonight if you&nbsp;want.</p>
    <p style="font-size:28px; line-height:1.5; margin-top:36px;">Lesson: in modern AI you stand on
    giants&rsquo;&nbsp;shoulders.</p>
  </div>
</div>""", 12, eyebrow="REAL NUMBERS &middot; MY NOTEBOOKS &middot; CIFAR-10 TEST SET",
     title="I trained this. Here&rsquo;s what happened.",
     interact="BEFORE THE REVEAL: CHAT GUESSES MY FROM-SCRATCH ACCURACY &middot; CLOSEST WINS"))

# ---------------------------------------------------------------- 13 code card 3
SLIDES.append(slide("""
<div style="margin-top:108px; max-width:1500px;">
<div class="code">from torchvision.models import resnet18, ResNet18_Weights

model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
model.fc = nn.Linear(512, 10)  <span class="cm"># swap the last layer: my 10 classes</span></div>
<p class="dek" style="margin-top:60px; max-width:1400px;">Keep every learned filter; replace only the final layer.
This is <b>transfer learning</b> &mdash; the 74.2%&nbsp;recipe.</p>
</div>""", 13, eyebrow="CODE CARD 3 OF 4 &middot; TRANSFER LEARNING",
     title="Borrowing a giant&rsquo;s eyes"))

# ---------------------------------------------------------------- 14 act 3 divider
SLIDES.append(slide("""
<h1 class="statement" style="margin-top:320px;">Same trick.<br>Four superpowers.</h1>
""", 14, dark=True, eyebrow="ACT 3 &middot; WHAT THIS UNLOCKS"))

# ---------------------------------------------------------------- 15 detection
SLIDES.append(slide("""
<div style="display:flex; gap:60px; margin-top:90px; align-items:flex-start;">
  <figure style="margin:0;">
    <img src="assets/det_chelsea.png" width="560" height="373"/>
    <figcaption class="cap" style="margin-top:16px;">REAL OUTPUT &middot; CAT &middot; 97% CONFIDENT</figcaption>
  </figure>
  <figure style="margin:0; margin-top:0;">
    <img src="assets/det_astronaut.png" width="500" height="500"/>
    <figcaption class="cap" style="margin-top:16px;">REAL OUTPUT &middot; PERSON &middot; 91% CONFIDENT</figcaption>
  </figure>
  <div style="max-width:440px; flex:0 0 440px; min-width:0;">
    <ul class="bullets" style="font-size:28px;">
      <li>Classification says &ldquo;there&rsquo;s a cat <i>somewhere</i>.&rdquo; Detection says <b>where</b> &mdash; with a box.</li>
      <li>One pass predicts boxes + labels + confidence &mdash; fast enough for live video.</li>
      <li>Self-driving cameras; your phone finding faces before it focuses.</li>
    </ul>
  </div>
</div>""", 15, eyebrow="TRAILER 1 OF 4 &middot; OBJECT DETECTION",
     title="Find it and box it"))

# ---------------------------------------------------------------- 16 segmentation
SLIDES.append(slide("""
<div style="display:flex; gap:56px; margin-top:96px;">
  <figure style="margin:0;"><img src="assets/seg_photo.png" width="500" height="333"/>
    <figcaption class="cap" style="margin-top:16px;">PHOTO</figcaption></figure>
  <figure style="margin:0;"><img src="assets/seg_mask.png" width="500" height="333" style="border:1px solid rgba(0,0,0,0.25); box-sizing:border-box;"/>
    <figcaption class="cap" style="margin-top:16px;">PREDICTED MASK &middot; WHITE = &ldquo;CAT PIXEL&rdquo;</figcaption></figure>
  <figure style="margin:0;"><img src="assets/seg_cutout.png" width="500" height="333" style="border:1px solid rgba(0,0,0,0.12); box-sizing:border-box;"/>
    <figcaption class="cap" style="margin-top:16px;">MASK USED AS SCISSORS</figcaption></figure>
</div>
<p class="dek" style="margin-top:70px; max-width:1560px;">Every single pixel gets a label: cat or not-cat.
Real model output &mdash; and exactly how this video call blurs my background right&nbsp;now.</p>
""", 16, eyebrow="TRAILER 2 OF 4 &middot; SEGMENTATION",
     title="Cut out the exact shape"))

# ---------------------------------------------------------------- 17 CLIP
def clip_bars():
    rows = []
    y = 0
    pairs = sorted(zip(clip["prompts"], clip["probs"]), key=lambda t: -t[1])
    for p, pr in pairs:
        pct = pr * 100
        w = max(pct / 100 * 470, 3)
        rows.append(f"""
<text x="0" y="{y+24}" font-family="Satoshi" font-size="25" fill="{INK}">&#8220;{p}&#8221;</text>
<rect x="0" y="{y+40}" width="{w:.0f}" height="34" fill="{INK}" fill-opacity="{1 if pct>50 else 0.25}"/>
<text x="{w+16:.0f}" y="{y+65}" font-family="Roboto Mono" font-size="20" fill="{INK}">{pct:.1f}%</text>""")
        y += 104
    return f'<svg width="660" height="{y}" viewBox="0 0 660 {y}" xmlns="http://www.w3.org/2000/svg">{"".join(rows)}</svg>'
SLIDES.append(slide(f"""
<div style="display:flex; gap:64px; margin-top:84px; align-items:flex-start;">
  <figure style="margin:0; flex:0 0 400px;"><img src="assets/chelsea_400.png" width="400" height="266"/>
    <figcaption class="cap" style="margin-top:16px;">I GAVE CLIP THIS PHOTO + 4 SENTENCES</figcaption></figure>
  <div style="flex:0 0 660px;">{clip_bars()}</div>
  <div style="max-width:480px; flex:1; min-width:0;">
    <p style="font-size:27px; line-height:1.45; margin:0;">CLIP learned from <b>400 million</b> internet photos
    with their captions. It scores how well a sentence matches an image &mdash; so you classify with
    <b>sentences</b>, no training. That&rsquo;s &ldquo;zero-shot.&rdquo;</p>
    <div class="code" style="font-size:19px; margin-top:40px; padding:30px 34px;">inputs = processor(
    text=["a cat","a dog","a pizza"],
    images=photo, return_tensors="pt")
probs = model(**inputs) \\
    .logits_per_image.softmax(dim=1)</div>
    <div class="cap" style="margin-top:16px;">CODE CARD 4 OF 4 &middot; THE 88.5% MODEL</div>
  </div>
</div>""", 17, eyebrow="TRAILER 3 OF 4 &middot; CLIP",
     title="A model that speaks image and text"))

# ---------------------------------------------------------------- 18 diffusion
frames = "".join(
    f'<img src="assets/diff_{i}.png" width="250" height="250" style="margin-right:{0 if i==4 else 64}px;"/>'
    for i in range(5))
SLIDES.append(slide(f"""
<div style="margin-top:100px;">
  <div class="cap" style="margin-bottom:22px;">TRAINING: RUIN THE PHOTO, STEP BY STEP &nbsp;&rarr;&nbsp; (REAL NOISE, REALLY ADDED)</div>
  <div style="display:flex; align-items:center;">{frames}</div>
  <div class="cap" style="margin-top:22px; text-align:right; width:1506px;">&larr; GENERATION: START FROM PURE STATIC, LEARN TO UNDO ONE STEP AT A TIME</div>
</div>
<p class="dek" style="margin-top:80px; max-width:1500px;">The network practices one humble skill &mdash; remove a little noise.
Apply it over and over to fresh static and an image crystallizes. That&rsquo;s <b>diffusion</b>,
the engine of AI image&nbsp;generators.</p>
""", 18, eyebrow="TRAILER 4 OF 4 &middot; IMAGE GENERATION",
     title="Start from static"))

# ---------------------------------------------------------------- 19 close
SLIDES.append(slide("""
<div style="margin-top:104px; max-width:1340px;">
  <ul class="bullets" style="font-size:33px;">
    <li>Everything today is on the official <b>IOAI 2026 syllabus</b> &mdash; the high-school AI olympiad I&rsquo;m training&nbsp;for.</li>
    <li>My two notebooks rerun it all: the CNN, the 50.0 &rarr; 74.2 &rarr; 88.5 ladder. They&rsquo;re&nbsp;yours.</li>
    <li>You multiplied small numbers and ran a convolution. So yes &mdash; you can do&nbsp;this.</li>
  </ul>
  <p class="dek" style="margin-top:90px;">Questions &mdash; then I&rsquo;ll open the notebooks live.</p>
</div>""", 19, eyebrow="RECAP &middot; PIXELS &rarr; FILTERS &rarr; LEARNING &rarr; SUPERPOWERS",
     title="Not magic. A syllabus."))

# ---------------------------------------------------------------- render
html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{''.join(SLIDES)}</body></html>"""
(HERE / "_lesson_deck.html").write_text(html)

from weasyprint import HTML, default_url_fetcher
def fetcher(url, t=20):
    try: return default_url_fetcher(url, timeout=t)
    except Exception: return {"string": b"", "mime_type": "image/jpeg"}
HTML(string=html, base_url=str(HERE) + "/", url_fetcher=fetcher).write_pdf(
    str(HERE / "vision_from_scratch_deck.pdf"))
print("PDF written:", HERE / "vision_from_scratch_deck.pdf")
