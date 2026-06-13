#!/usr/bin/env python3
"""Build the Vision Models deck PDF (1920x1080, Viktor profile, WeasyPrint)."""
import random

random.seed(42)

INK = "#000000"

# ---------------------------------------------------------------- svg helpers

def svg(w, h, content):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg">{content}</svg>')

def rect(x, y, w, h, fill="none", opacity=None, stroke=None, sw=1, so=None, dash=None):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'
    if opacity is not None: s += f' fill-opacity="{opacity}"'
    if stroke: s += f' stroke="{stroke}" stroke-width="{sw}"'
    if so is not None: s += f' stroke-opacity="{so}"'
    if dash: s += f' stroke-dasharray="{dash}"'
    return s + '/>'

def line(x1, y1, x2, y2, sw=2, so=1.0, dash=None, marker=False):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="{sw}" stroke-opacity="{so}"'
    if dash: s += f' stroke-dasharray="{dash}"'
    if marker: s += ' marker-end="url(#arr)"'
    return s + '/>'

def txt(x, y, t, size=15, mono=True, anchor="start", op=1.0, weight=400):
    fam = "Roboto Mono" if mono else "Satoshi"
    sp = ' letter-spacing="1.5"' if mono and size <= 14 else ''
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{INK}" fill-opacity="{op}" '
            f'text-anchor="{anchor}"{sp}>{t}</text>')

ARROW_DEF = ('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
             'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
             f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/></marker></defs>')

def noise_dots(x, y, w, h, n, seed):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        out.append(f'<rect x="{x + r.uniform(0, w-4):.0f}" y="{y + r.uniform(0, h-4):.0f}" '
                   f'width="4" height="4" fill="{INK}" fill-opacity="{r.uniform(0.25,0.95):.2f}"/>')
    return "".join(out)

def scene(x, y, s, opacity=1.0, flipped=False, frame=True):
    """A tiny 'photo': sun circle + mountain triangle inside an s×s square."""
    g = []
    if frame:
        g.append(rect(x, y, s, s, fill="#FFFFFF", stroke=INK, sw=2))
    cx = x + (0.72 if not flipped else 0.28) * s
    g.append(f'<circle cx="{cx:.0f}" cy="{y+0.26*s:.0f}" r="{0.11*s:.0f}" fill="{INK}" fill-opacity="{0.85*opacity:.2f}"/>')
    if not flipped:
        pts = f"{x+0.08*s:.0f},{y+0.92*s:.0f} {x+0.45*s:.0f},{y+0.38*s:.0f} {x+0.82*s:.0f},{y+0.92*s:.0f}"
    else:
        pts = f"{x+0.92*s:.0f},{y+0.92*s:.0f} {x+0.55*s:.0f},{y+0.38*s:.0f} {x+0.18*s:.0f},{y+0.92*s:.0f}"
    g.append(f'<polygon points="{pts}" fill="{INK}" fill-opacity="{0.55*opacity:.2f}"/>')
    g.append(line(x+3, y+0.92*s, x+s-3, y+0.92*s, sw=2, so=0.35*opacity))
    return "".join(g)

# ---------------------------------------------------------------- diagrams

def d2_tensor():
    g = [ARROW_DEF]
    g.append(scene(0, 60, 190))
    g.append(txt(0, 286, "WHAT WE SEE", 13, op=0.55))
    g.append(line(220, 155, 286, 155, sw=2, marker=True))
    # numeric pixel grid 6x6
    gx, gy, c = 306, 40, 42
    r = random.Random(3)
    for i in range(6):
        for j in range(6):
            v = r.randint(8, 250)
            g.append(rect(gx+j*c, gy+i*c, c, c, fill=INK, opacity=round(v/255*0.16,3), stroke=INK, sw=1, so=0.18))
            g.append(txt(gx+j*c+c/2, gy+i*c+c/2+5, str(v), 12, anchor="middle", op=0.8))
    g.append(txt(gx, gy+6*c+34, "WHAT THE COMPUTER SEES", 13, op=0.55))
    g.append(txt(gx, gy+6*c+56, "H &#215; W &#215; 3 &#183; VALUES 0&#8211;255", 13, op=0.35))
    g.append(line(gx+6*c+26, 155, gx+6*c+92, 155, sw=2, marker=True))
    # embedding vector
    vx, vy = gx+6*c+112, 50
    vals = [0.12, -0.87, 0.45, 0.03, 0.91, -0.33]
    for i, v in enumerate(vals):
        g.append(rect(vx, vy+i*36, 96, 36, fill=INK, opacity=round(abs(v)*0.55+0.05,2), stroke=INK, sw=1, so=0.25))
    g.append(txt(vx+48, vy+6*36+34, "EMBEDDING", 13, anchor="middle", op=0.55))
    g.append(txt(vx+48, vy+6*36+56, "512 numbers", 14, anchor="middle", op=0.35))
    return svg(880, 360, "".join(g))

def d3_conv():
    g = [ARROW_DEF]
    c = 48
    gx, gy = 0, 70
    # input 7x7
    r = random.Random(11)
    for i in range(7):
        for j in range(7):
            g.append(rect(gx+j*c, gy+i*c, c, c, fill=INK, opacity=round(r.uniform(0,0.10),3), stroke=INK, sw=1, so=0.15))
    # highlighted 3x3 window at (1,1)
    g.append(rect(gx+1*c, gy+1*c, 3*c, 3*c, fill=INK, opacity=0.10, stroke=INK, sw=3))
    # dashed next position
    g.append(rect(gx+2*c, gy+1*c, 3*c, 3*c, fill="none", stroke=INK, sw=2, so=0.35, dash="6 6"))
    g.append(txt(gx+2*c+3*c-8, gy+1*c-10, "next step &#8594;", 13, op=0.45, anchor="end"))
    g.append(txt(gx, gy+7*c+34, "INPUT 7&#215;7", 13, op=0.55))
    # kernel
    kx, ky = gx+7*c+56, gy+40
    kw = [["-1","0","1"],["-2","0","2"],["-1","0","1"]]
    for i in range(3):
        for j in range(3):
            g.append(rect(kx+j*c, ky+i*c, c, c, fill=INK, opacity=0.05, stroke=INK, sw=1.5, so=0.55))
            g.append(txt(kx+j*c+c/2, ky+i*c+c/2+6, kw[i][j], 17, anchor="middle", op=0.85))
    g.append(txt(kx+1.5*c, ky-18, "FILTER 3&#215;3 (LEARNED)", 13, anchor="middle", op=0.55))
    g.append(txt(kx+1.5*c, ky+3*c+38, "&#215; multiply, &#931; sum", 15, anchor="middle", op=0.7))
    g.append(line(gx+4*c+14, gy+2.5*c, kx-16, gy+2.5*c, sw=2, marker=True))
    # output 5x5
    ox, oy = kx+3*c+60, gy+c
    for i in range(5):
        for j in range(5):
            g.append(rect(ox+j*c, oy+i*c, c, c, fill=INK, opacity=0.03, stroke=INK, sw=1, so=0.15))
    g.append(rect(ox, oy, c, c, fill=INK, opacity=0.9))
    g.append(line(kx+3*c+12, gy+2.5*c, ox-16, gy+2.5*c, sw=2, marker=True))
    g.append(txt(ox, oy+5*c+34, "FEATURE MAP 5&#215;5", 13, op=0.55))
    g.append(txt(ox, oy+5*c+58, "one number per position", 14, mono=False, op=0.45))
    return svg(900, 520, "".join(g))

def d4_pool():
    g = [ARROW_DEF]
    c = 62
    gx, gy = 0, 40
    vals = [[1,3,2,1],[5,8,1,2],[2,1,9,4],[1,3,2,6]]
    maxes = [[8,2],[3,9]]
    quad_op = [[0.04,0.10],[0.10,0.04]]
    for i in range(4):
        for j in range(4):
            qo = quad_op[i//2][j//2]
            g.append(rect(gx+j*c, gy+i*c, c, c, fill=INK, opacity=qo, stroke=INK, sw=1, so=0.2))
            bold = vals[i][j] == maxes[i//2][j//2]
            g.append(txt(gx+j*c+c/2, gy+i*c+c/2+6, str(vals[i][j]), 19 if bold else 16,
                         anchor="middle", op=1.0 if bold else 0.4, weight=500 if bold else 400))
    g.append(rect(gx, gy, 4*c, 4*c, fill="none", stroke=INK, sw=2, so=0.6))
    g.append(line(gx+2*c, gy, gx+2*c, gy+4*c, sw=2, so=0.6))
    g.append(line(gx, gy+2*c, gx+4*c, gy+2*c, sw=2, so=0.6))
    g.append(txt(gx, gy+4*c+32, "2&#215;2 MAX POOL", 13, op=0.55))
    g.append(line(gx+4*c+18, gy+2*c, gx+4*c+76, gy+2*c, sw=2, marker=True))
    ox = gx+4*c+96
    for i in range(2):
        for j in range(2):
            g.append(rect(ox+j*c, gy+c+ (i-1)*c + c, c, c, fill=INK, opacity=0.10, stroke=INK, sw=1.5, so=0.6))
            g.append(txt(ox+j*c+c/2, gy+c+(i-1)*c+c+c/2+7, str(maxes[i][j]), 20, anchor="middle", weight=500))
    g.append(txt(ox, gy+3*c+32, "STRONGEST", 13, op=0.55))
    g.append(txt(ox, gy+3*c+52, "SIGNAL KEPT", 13, op=0.55))
    return svg(560, 360, "".join(g))

def d4_pipeline():
    g = [ARROW_DEF]
    stages = ["image", "conv + ReLU", "pool", "conv + ReLU", "pool", "avg pool", "linear"]
    x = 0; y = 16; h = 64
    widths = [78, 118, 66, 118, 66, 94, 76]
    for i, (s, w) in enumerate(zip(stages, widths)):
        fill_op = 0.05 if i % 2 == 0 else 0.12
        g.append(rect(x, y, w, h, fill=INK, opacity=fill_op, stroke=INK, sw=1.5, so=0.5))
        g.append(txt(x+w/2, y+h/2+5, s, 13, anchor="middle", mono=False, op=0.85))
        x += w
        if i < len(stages)-1:
            g.append(line(x+3, y+h/2, x+19, y+h/2, sw=2, marker=True)); x += 24
    g.append(line(x+3, y+h/2, x+21, y+h/2, sw=2, marker=True))
    g.append(txt(x+30, y+h/2-6, "cat&#160;0.92", 15, weight=500))
    g.append(txt(x+30, y+h/2+18, "dog&#160;0.08", 15, op=0.4))
    return svg(920, 110, "".join(g))

def d5_aug():
    g = [ARROW_DEF]
    s = 150
    # source
    g.append(scene(0, 140, s+20))
    g.append(txt(0, 140+s+50, "ORIGINAL &#183; LABEL: CAT", 13, op=0.55))
    vx = 330
    variants = [("FLIP", 0), ("RANDOM CROP", 1), ("NOISE", 2), ("PATCH CUT-OUT", 3)]
    pos = [(vx, 20), (vx+250, 20), (vx, 250), (vx+250, 250)]
    for (name, kind), (px, py) in zip(variants, pos):
        if kind == 0:
            g.append(scene(px, py, s, flipped=True))
        elif kind == 1:
            g.append(rect(px, py, s, s, fill="#FFFFFF", stroke=INK, sw=2))
            # zoomed-in: big triangle portion
            g.append(f'<polygon points="{px-30},{py+s} {px+s*0.55:.0f},{py-40} {px+s+40},{py+s}" fill="{INK}" fill-opacity="0.55" clip-path="url(#c{px})"/>')
            g.append(f'<clipPath id="c{px}"><rect x="{px+2}" y="{py+2}" width="{s-4}" height="{s-4}"/></clipPath>')
        elif kind == 2:
            g.append(scene(px, py, s))
            g.append(noise_dots(px+4, py+4, s-8, s-8, 90, seed=5))
        else:
            g.append(scene(px, py, s))
            g.append(rect(px+s*0.42, py+s*0.30, s*0.42, s*0.42, fill=INK, opacity=0.18, stroke=INK, sw=1.5, so=0.5))
        g.append(txt(px, py+s+28, name, 13, op=0.55))
        g.append(txt(px, py+s+50, "label: cat &#10003;", 14, op=0.85))
    # arrows from source to each
    for (px, py) in pos:
        g.append(line(196, 215, px-18, py+s/2, sw=1.5, so=0.5, marker=True))
    return svg(800, 470, "".join(g))

def d6_resnet():
    g = [ARROW_DEF]
    cx = 230
    g.append(txt(cx, 24, "input  x", 17, anchor="middle", mono=False, op=0.85))
    g.append(line(cx, 36, cx, 86, sw=2, marker=True))
    # split point
    g.append(f'<circle cx="{cx}" cy="92" r="4" fill="{INK}"/>')
    # main path
    g.append(line(cx, 96, cx, 130, sw=2, marker=True))
    g.append(rect(cx-110, 136, 220, 62, fill=INK, opacity=0.08, stroke=INK, sw=1.5, so=0.6))
    g.append(txt(cx, 174, "conv 3&#215;3 + ReLU", 16, anchor="middle", mono=False, op=0.85))
    g.append(line(cx, 202, cx, 236, sw=2, marker=True))
    g.append(rect(cx-110, 242, 220, 62, fill=INK, opacity=0.08, stroke=INK, sw=1.5, so=0.6))
    g.append(txt(cx, 280, "conv 3&#215;3", 16, anchor="middle", mono=False, op=0.85))
    g.append(txt(cx+130, 224, "F(x)", 16, op=0.55))
    g.append(line(cx, 308, cx, 348, sw=2, marker=True))
    # skip path
    g.append(f'<path d="M {cx} 92 C {cx+260} 110, {cx+260} 330, {cx+22} 362" fill="none" stroke="{INK}" stroke-width="2" marker-end="url(#arr)"/>')
    g.append(txt(cx+218, 226, "skip connection", 13, op=0.55))
    g.append(txt(cx+218, 246, "(identity)", 13, op=0.35))
    # plus node
    g.append(f'<circle cx="{cx}" cy="366" r="20" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>')
    g.append(txt(cx, 374, "+", 24, anchor="middle", weight=500))
    g.append(line(cx, 388, cx, 428, sw=2, marker=True))
    g.append(txt(cx, 454, "output  =  x + F(x)", 18, anchor="middle", mono=False, weight=500))
    g.append(txt(cx, 482, '"keep the input, learn only the correction"', 14, anchor="middle", mono=False, op=0.45))
    return svg(560, 500, "".join(g))

def d7_finetune():
    g = [ARROW_DEF]
    bw, bh = 250, 56
    # Panel A
    ax = 30
    g.append(txt(ax, 18, "A &#183; FREEZE + NEW HEAD", 13, op=0.55))
    layers = ["conv block 1", "conv block 2", "conv block 3", "conv block 4"]
    y = 40
    for nm in layers:
        g.append(rect(ax, y, bw, bh, fill=INK, opacity=0.05, stroke=INK, sw=1.5, so=0.4))
        g.append(txt(ax+18, y+bh/2+5, "&#10052; " + nm, 15, mono=False, op=0.5))
        y += bh + 10
    g.append(rect(ax, y, bw, bh, fill=INK, opacity=0.9))
    g.append(f'<text x="{ax+18}" y="{y+bh/2+5}" font-family="Satoshi" font-size="15" fill="#FFFFFF">new head &#8212; trained</text>')
    g.append(txt(ax, y+bh+30, "&#10052; = FROZEN WEIGHTS", 13, op=0.45))
    # Panel B
    bx = ax + bw + 120
    g.append(txt(bx, 18, "B &#183; PARAMETER-EFFICIENT (ADAPTERS)", 13, op=0.55))
    y = 40
    for i, nm in enumerate(layers):
        g.append(rect(bx, y, bw, bh, fill=INK, opacity=0.05, stroke=INK, sw=1.5, so=0.4))
        g.append(txt(bx+18, y+bh/2+5, "&#10052; " + nm, 15, mono=False, op=0.5))
        y += bh
        if i < 3:
            g.append(rect(bx+40, y, bw-80, 18, fill=INK, opacity=0.9))
            g.append(f'<text x="{bx+bw/2}" y="{y+13}" font-family="Roboto Mono" font-size="11" fill="#FFFFFF" text-anchor="middle" letter-spacing="1">ADAPTER &#8212; TRAINED</text>')
            y += 18 + 8
    g.append(rect(bx, y, bw, bh, fill=INK, opacity=0.9))
    g.append(f'<text x="{bx+18}" y="{y+bh/2+5}" font-family="Satoshi" font-size="15" fill="#FFFFFF">new head &#8212; trained</text>')
    g.append(txt(bx, y+bh+30, "~1&#8211;5% OF WEIGHTS UPDATED", 13, op=0.45))
    return svg(720, 460, "".join(g))

def d8_detect():
    g = [ARROW_DEF]
    pw = 270; s = 168
    panels = ["YOLO &#183; GRID, ONE PASS", "SSD &#183; MULTI-SCALE, ONE PASS", "DETR &#183; TRANSFORMER SET"]
    for p, name in enumerate(panels):
        px = p * (pw + 60)
        g.append(txt(px, 16, name, 13, op=0.55))
        if p == 0:
            g.append(scene(px, 40, s))
            for k in range(1, 4):
                g.append(line(px+k*s/4, 40, px+k*s/4, 40+s, sw=1, so=0.3))
                g.append(line(px, 40+k*s/4, px+s, 40+k*s/4, sw=1, so=0.3))
            g.append(rect(px+s*0.50, 40+s*0.10, s*0.42, s*0.38, fill="none", stroke=INK, sw=3))
            g.append(rect(px+s*0.06, 40+s*0.34, s*0.66, s*0.60, fill="none", stroke=INK, sw=3))
            g.append(txt(px+s*0.5, 40+s+30, "boxes from grid cells", 13, anchor="middle", mono=False, op=0.5))
            g.append(txt(px+s*0.5, 40+s+52, "built for real time", 13, anchor="middle", mono=False, op=0.5))
        elif p == 1:
            sizes = [s, int(s*0.62), int(s*0.36)]
            yy = 40
            for i, sz in enumerate(sizes):
                g.append(rect(px, yy, sz, sz*0.5, fill=INK, opacity=0.05+0.05*i, stroke=INK, sw=1.5, so=0.5))
                g.append(rect(px+sz*0.2, yy+sz*0.12, sz*0.26, sz*0.26, fill="none", stroke=INK, sw=2.5))
                g.append(txt(px+sz+14, yy+sz*0.25+5, ["small objects","medium","large"][i], 12, mono=False, op=0.45))
                yy += int(sz*0.5) + 14
            g.append(txt(px+s*0.5, 40+s+52, "boxes at several scales", 13, anchor="middle", mono=False, op=0.5))
        else:
            g.append(scene(px, 40, int(s*0.55)))
            g.append(line(px+int(s*0.55)+8, 40+s*0.28, px+int(s*0.55)+34, 40+s*0.28, sw=2, marker=True))
            tx = px+int(s*0.55)+44
            g.append(rect(tx, 40+s*0.10, 120, s*0.36, fill=INK, opacity=0.9))
            g.append(f'<text x="{tx+60}" y="{40+s*0.31}" font-family="Satoshi" font-size="14" fill="#FFFFFF" text-anchor="middle">transformer</text>')
            # object slots
            yy = 40 + int(s*0.62)
            labels = ["dog", "ball", "&#8709;", "&#8709;"]
            for i, lb in enumerate(labels):
                op = 0.9 if lb not in ("&#8709;",) else 0.06
                g.append(rect(px+i*62, yy, 54, 40, fill=INK, opacity=op, stroke=INK, sw=1, so=0.3))
                col = "#FFFFFF" if op > 0.5 else INK
                fop = 1.0 if op > 0.5 else 0.4
                g.append(f'<text x="{px+i*62+27}" y="{yy+25}" font-family="Roboto Mono" font-size="13" fill="{col}" fill-opacity="{fop}" text-anchor="middle">{lb}</text>')
            g.append(txt(px+s*0.5+30, yy+70, "direct set of predictions,", 13, anchor="middle", mono=False, op=0.5))
            g.append(txt(px+s*0.5+30, yy+92, "no anchors, no NMS", 13, anchor="middle", mono=False, op=0.5))
    return svg(940, 320, "".join(g))

def d9_unet():
    g = [ARROW_DEF]
    bw0, bh = 150, 52
    levels = 4
    xL, xR = 60, 660
    ys = [30, 110, 190, 270]
    for i in range(levels):
        w = bw0 - i*22
        # encoder block
        g.append(rect(xL + i*40, ys[i], w, bh, fill=INK, opacity=0.06+0.04*i, stroke=INK, sw=1.5, so=0.5))
        # decoder block
        g.append(rect(xR - i*40 - w, ys[i], w, bh, fill=INK, opacity=0.06+0.04*i, stroke=INK, sw=1.5, so=0.5))
        # skip arrow
        g.append(line(xL + i*40 + w + 10, ys[i]+bh/2, xR - i*40 - w - 12, ys[i]+bh/2, sw=2, so=0.55, dash="8 7", marker=True))
        if i < levels-1:
            g.append(line(xL + i*40 + (w)/2, ys[i]+bh+2, xL + (i+1)*40 + (w-22)/2, ys[i+1]-4, sw=2, marker=True))
            g.append(line(xR - i*40 - w/2, ys[i+1]-4, xR - i*40 - w/2, ys[i+1]-4, sw=2))
            g.append(line(xR - (i+1)*40 - (w-22)/2, ys[i+1]+ -4, xR - i*40 - w/2, ys[i]+bh+2, sw=2, marker=True))
    # bottleneck
    bnw = 120
    g.append(rect((xL+xR)/2 - bnw/2 + 10, 350, bnw, bh, fill=INK, opacity=0.22, stroke=INK, sw=1.5, so=0.6))
    g.append(line(xL + 3*40 + (bw0-66)/2, ys[3]+bh+2, (xL+xR)/2 - 10, 348, sw=2, marker=True))
    g.append(line((xL+xR)/2 + 30, 348, xR - 3*40 - (bw0-66)/2, ys[3]+bh+2, sw=2, marker=True))
    g.append(txt((xL+xR)/2+10, 350+bh+26, "BOTTLENECK", 13, anchor="middle", op=0.45))
    # input / output
    g.append(scene(xL-58, ys[0]-24, 46, frame=True))
    g.append(line(xL-6, ys[0]+2, xL+12, ys[0]+12, sw=2, marker=True))
    mx = xR + 16
    g.append(rect(mx, ys[0]-24, 46, 46, fill="#FFFFFF", stroke=INK, sw=2))
    g.append(f'<polygon points="{mx+6},{mx and ys[0]+16} {mx+24},{ys[0]-16} {mx+42},{ys[0]+16}" fill="{INK}" fill-opacity="0.85"/>')
    g.append(txt(mx+23, ys[0]+40, "MASK", 11, anchor="middle", op=0.45))
    # labels
    g.append(txt(xL+10, 450, "ENCODER &#183; WHAT", 13, op=0.55))
    g.append(txt(xR-10, 450, "DECODER &#183; WHERE", 13, op=0.55, anchor="end"))
    g.append(txt((xL+xR)/2+10, 18, "SKIP CONNECTIONS CARRY FINE DETAIL", 13, anchor="middle", op=0.45))
    return svg(780, 470, "".join(g))

def d10_vit():
    g = [ARROW_DEF]
    s = 200
    g.append(scene(0, 60, s, frame=True))
    # patch grid lines
    for k in range(1, 4):
        g.append(line(k*s/4, 60, k*s/4, 60+s, sw=2, so=0.7))
        g.append(line(0, 60+k*s/4, s, 60+k*s/4, sw=2, so=0.7))
    g.append(txt(0, 60+s+30, "IMAGE &#8594; 16 PATCHES", 13, op=0.55))
    g.append(line(s+18, 160, s+58, 160, sw=2, marker=True))
    # token row
    tx, ty, tc = s+76, 138, 44
    for i in range(8):
        g.append(rect(tx+i*(tc+8), ty, tc, tc, fill=INK, opacity=0.06+0.025*(i%4), stroke=INK, sw=1.5, so=0.5))
        g.append(txt(tx+i*(tc+8)+tc/2, ty+tc+20, str(i+1), 12, anchor="middle", op=0.4))
    g.append(txt(tx+4*(tc+8), ty+tc+44, "+ POSITION EMBEDDING", 13, anchor="middle", op=0.45))
    # highlight token 2, attention arcs to others
    hi = 1
    hx = tx+hi*(tc+8)+tc/2
    g.append(rect(tx+hi*(tc+8), ty, tc, tc, fill=INK, opacity=0.85))
    weights = [0.9, 0, 0.25, 0.5, 0.15, 0.7, 0.2, 0.35]
    for i, w in enumerate(weights):
        if i == hi or w == 0: continue
        ox = tx+i*(tc+8)+tc/2
        mid = (hx+ox)/2
        h = 50 + abs(ox-hx)*0.10
        g.append(f'<path d="M {hx} {ty} Q {mid} {ty-h} {ox} {ty}" fill="none" stroke="{INK}" stroke-width="{1+w*3:.1f}" stroke-opacity="{0.25+w*0.6:.2f}"/>')
    g.append(txt(tx+4*(tc+8), ty-86, "ATTENTION &#183; EVERY PATCH SEES EVERY PATCH", 13, anchor="middle", op=0.45))
    # transformer box
    bx, by = tx+30, ty+96
    g.append(line(hx, ty+tc+54, hx, by-6, sw=0, so=0))
    g.append(rect(bx, by, 8*(tc+8)-8-60, 54, fill=INK, opacity=0.9))
    g.append(f'<text x="{bx + (8*(tc+8)-68)/2}" y="{by+33}" font-family="Satoshi" font-size="17" fill="#FFFFFF" text-anchor="middle">transformer encoder</text>')
    g.append(line(tx+4*(tc+8), ty+tc+50, tx+4*(tc+8), by-8, sw=2, marker=True))
    return svg(780, 330, "".join(g))

def d11_ssl():
    g = [ARROW_DEF]
    g.append(scene(0, 120, 130))
    g.append(txt(0, 290, "ONE IMAGE", 13, op=0.55))
    # two views
    g.append(line(140, 160, 196, 92, sw=1.5, so=0.5, marker=True))
    g.append(line(140, 220, 196, 270, sw=1.5, so=0.5, marker=True))
    g.append(scene(208, 50, 100, flipped=True))
    g.append(noise_dots(212, 54, 92, 92, 30, seed=9))
    g.append(txt(208, 178, "VIEW A", 13, op=0.55))
    g.append(scene(208, 226, 100))
    g.append(rect(208+38, 226+30, 40, 40, fill=INK, opacity=0.15))
    g.append(txt(208, 354, "VIEW B", 13, op=0.55))
    # shared encoder
    ex, ey = 370, 150
    g.append(line(316, 100, ex-8, ey+30, sw=2, marker=True))
    g.append(line(316, 276, ex-8, ey+70, sw=2, marker=True))
    g.append(rect(ex, ey, 150, 100, fill=INK, opacity=0.9))
    g.append(f'<text x="{ex+75}" y="{ey+45}" font-family="Satoshi" font-size="16" fill="#FFFFFF" text-anchor="middle">shared</text>')
    g.append(f'<text x="{ex+75}" y="{ey+68}" font-family="Satoshi" font-size="16" fill="#FFFFFF" text-anchor="middle">encoder</text>')
    # embedding space
    sx, sy, ss = 590, 40, 330
    g.append(line(ex+158, ey+50, sx-12, ey+50, sw=2, marker=True))
    g.append(rect(sx, sy, ss, ss, fill=INK, opacity=0.025, stroke=INK, sw=1.5, so=0.3))
    g.append(txt(sx, sy+ss+28, "EMBEDDING SPACE", 13, op=0.55))
    ax_, ay_ = sx+150, sy+150
    bx_, by_ = sx+205, sy+185
    g.append(f'<circle cx="{ax_}" cy="{ay_}" r="11" fill="{INK}"/>')
    g.append(f'<circle cx="{bx_}" cy="{by_}" r="11" fill="{INK}" fill-opacity="0.55"/>')
    g.append(txt(ax_-18, ay_-18, "A", 14, anchor="end"))
    g.append(txt(bx_+18, by_+30, "B", 14))
    g.append(line(ax_+34, ay_+22, ax_+14, ay_+9, sw=2.5, marker=True))
    g.append(line(bx_-34, by_-22, bx_-14, by_-9, sw=2.5, marker=True))
    g.append(txt(ax_+30, ay_+105, "PULL TOGETHER", 12, anchor="middle"))
    ox_, oy_ = sx+62, sy+62
    g.append(f'<circle cx="{ox_}" cy="{oy_}" r="11" fill="none" stroke="{INK}" stroke-width="2"/>')
    g.append(line(ox_+16, oy_+12, ox_+52, oy_+38, sw=2.5, dash="5 5", marker=True))
    g.append(txt(ox_-12, oy_-22, "OTHER IMAGE &#8212; PUSH AWAY", 12))
    return svg(940, 410, "".join(g))

def d12_clip():
    g = [ARROW_DEF]
    # image side
    g.append(scene(0, 30, 90))
    g.append(scene(16, 46, 90))
    g.append(line(118, 90, 158, 90, sw=2, marker=True))
    g.append(rect(166, 56, 160, 70, fill=INK, opacity=0.9))
    g.append(f'<text x="246" y="97" font-family="Satoshi" font-size="16" fill="#FFFFFF" text-anchor="middle">image encoder</text>')
    # text side
    g.append(rect(0, 250, 130, 34, fill=INK, opacity=0.05, stroke=INK, sw=1, so=0.3))
    g.append(txt(10, 272, '"a photo of', 13, mono=False, op=0.7))
    g.append(rect(0, 292, 130, 34, fill=INK, opacity=0.05, stroke=INK, sw=1, so=0.3))
    g.append(txt(10, 314, ' a dog"', 13, mono=False, op=0.7))
    g.append(line(138, 290, 158, 290, sw=2, marker=True))
    g.append(rect(166, 255, 160, 70, fill=INK, opacity=0.9))
    g.append(f'<text x="246" y="296" font-family="Satoshi" font-size="16" fill="#FFFFFF" text-anchor="middle">text encoder</text>')
    # shared space
    sx, sy, ss = 420, 60, 270
    g.append(line(334, 91, sx-12, sy+90, sw=2, marker=True))
    g.append(line(334, 290, sx-12, sy+190, sw=2, marker=True))
    g.append(rect(sx, sy, ss, ss, fill=INK, opacity=0.025, stroke=INK, sw=1.5, so=0.3))
    g.append(txt(sx+ss/2, sy+ss+28, "ONE SHARED EMBEDDING SPACE", 13, anchor="middle", op=0.55))
    g.append(f'<circle cx="{sx+150}" cy="{sy+120}" r="10" fill="{INK}"/>')
    g.append(txt(sx+150, sy+96, "dog photo", 13, mono=False, anchor="middle", op=0.7))
    g.append(f'<rect x="{sx+178}" y="{sy+138}" width="16" height="16" fill="{INK}" fill-opacity="0.55"/>')
    g.append(txt(sx+186, sy+182, '"a photo of a dog"', 13, mono=False, anchor="middle", op=0.7))
    g.append(f'<circle cx="{sx+58}" cy="{sy+212}" r="10" fill="none" stroke="{INK}" stroke-width="2"/>')
    g.append(txt(sx+58, sy+244, "car photo", 13, mono=False, anchor="middle", op=0.45))
    # similarity matrix
    mx, my, mc = 770, 80, 44
    g.append(txt(mx+2*mc, my-22, "SIMILARITY MATRIX", 13, anchor="middle", op=0.55))
    for i in range(4):
        for j in range(4):
            op = 0.9 if i == j else 0.06
            g.append(rect(mx+j*mc, my+i*mc, mc, mc, fill=INK, opacity=op, stroke=INK, sw=1, so=0.2))
    g.append(txt(mx-12, my+2*mc, "IMAGES", 11, anchor="end", op=0.4))
    g.append(txt(mx+2*mc, my+4*mc+24, "CAPTIONS", 11, anchor="middle", op=0.4))
    g.append(txt(mx+2*mc, my+4*mc+62, "TRAIN: BRIGHT DIAGONAL", 12, anchor="middle", op=0.55))
    g.append(txt(mx+2*mc, my+4*mc+84, "= MATCHED PAIRS", 12, anchor="middle", op=0.55))
    return svg(960, 410, "".join(g))

def d13_gan():
    g = [ARROW_DEF]
    # noise z
    g.append(rect(0, 120, 100, 100, fill="#FFFFFF", stroke=INK, sw=2))
    g.append(noise_dots(4, 124, 92, 92, 110, seed=21))
    g.append(txt(50, 250, "NOISE z", 13, anchor="middle", op=0.55))
    g.append(line(108, 170, 152, 170, sw=2, marker=True))
    # generator
    g.append(rect(160, 130, 170, 80, fill=INK, opacity=0.9))
    g.append(f'<text x="245" y="164" font-family="Satoshi" font-size="17" fill="#FFFFFF" text-anchor="middle">generator</text>')
    g.append(f'<text x="245" y="188" font-family="Roboto Mono" font-size="11" fill="#FFFFFF" fill-opacity="0.6" text-anchor="middle" letter-spacing="1">THE FORGER</text>')
    g.append(line(338, 170, 382, 170, sw=2, marker=True))
    # fake image
    g.append(scene(390, 120, 100))
    g.append(noise_dots(394, 124, 92, 92, 18, seed=4))
    g.append(txt(440, 250, "FAKE IMAGE", 13, anchor="middle", op=0.55))
    g.append(line(498, 170, 542, 170, sw=2, marker=True))
    # discriminator
    g.append(rect(550, 130, 190, 80, fill=INK, opacity=0.08, stroke=INK, sw=2, so=0.8))
    g.append(txt(645, 164, "discriminator", 17, mono=False, anchor="middle", op=0.9))
    g.append(txt(645, 188, "THE DETECTIVE", 11, anchor="middle", op=0.45))
    # real images feeding in
    g.append(scene(600, 0, 76))
    g.append(scene(616, 12, 76))
    g.append(txt(700, 50, "REAL", 12, op=0.45))
    g.append(line(655, 96, 648, 124, sw=2, marker=True))
    # verdict
    g.append(line(748, 170, 792, 170, sw=2, marker=True))
    g.append(txt(802, 162, "real?", 17, mono=False, weight=500))
    g.append(txt(802, 188, "fake?", 17, mono=False, weight=500, op=0.45))
    # feedback arrows
    g.append(f'<path d="M 645 218 C 645 300, 245 300, 245 218" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="7 6" marker-end="url(#arr)"/>')
    g.append(txt(445, 318, "FEEDBACK: HOW WAS I CAUGHT? &#8594; FORGE BETTER", 13, anchor="middle", op=0.55))
    return svg(900, 350, "".join(g))

def d14_diffusion():
    g = [ARROW_DEF]
    s = 130
    n_frames = 5
    gap = 50
    noise_counts = [0, 45, 110, 200, 330]
    opac = [1.0, 0.8, 0.5, 0.25, 0.0]
    for i in range(n_frames):
        x = i*(s+gap)
        g.append(rect(x, 90, s, s, fill="#FFFFFF", stroke=INK, sw=2))
        if opac[i] > 0:
            g.append(scene(x, 90, s, opacity=opac[i], frame=False))
        g.append(noise_dots(x+4, 94, s-8, s-8, noise_counts[i], seed=30+i))
        if i < n_frames-1:
            # forward arrow above
            g.append(line(x+s+6, 70, x+s+gap-6, 70, sw=2, so=0.45, marker=True))
            # reverse arrow below
            g.append(line(x+s+gap-6, 250, x+s+6, 250, sw=2.5, marker=True))
    g.append(txt(0, 40, "FORWARD &#183; ADD NOISE &#183; FIXED, NO LEARNING &#8594;", 13, op=0.45))
    g.append(txt(n_frames*(s+gap)-gap, 322, "&#8592; REVERSE &#183; REMOVE NOISE &#183; LEARNED &#8212; THIS IS GENERATION", 13, anchor="end"))
    g.append(txt(0, 250+ -6, "", 13))
    g.append(txt(0, 105+s+ 36, "IMAGE", 12, op=0.45))
    g.append(txt((n_frames-1)*(s+gap)+s/2, 105+s+36, "PURE NOISE", 12, anchor="middle", op=0.45))
    g.append(txt((n_frames-1)*(s+gap)+s/2, 105+s+58, "(START HERE TO GENERATE)", 11, anchor="middle", op=0.35))
    return svg(950, 345, "".join(g))

def d16_journey():
    g = [ARROW_DEF]
    nodes = ["pixels", "conv", "ResNet", "detect / segment", "ViT", "self-supervised", "CLIP", "GAN / diffusion"]
    y = 60
    g.append(line(10, y, 1620, y, sw=2, so=0.25))
    total_w = 1610
    step = total_w / (len(nodes)-1)
    for i, nm in enumerate(nodes):
        cx = 10 + i*step
        filled = i in (1, 4, 7)
        if filled:
            g.append(f'<circle cx="{cx:.0f}" cy="{y}" r="13" fill="{INK}"/>')
        else:
            g.append(f'<circle cx="{cx:.0f}" cy="{y}" r="13" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/>')
        anchor = "start" if i == 0 else ("end" if i == len(nodes)-1 else "middle")
        g.append(txt(cx if anchor!="start" else cx-12, y+50, nm, 17, mono=False, anchor=anchor, op=0.85, weight=500))
        sub = ["a tensor", "local patterns", "deep + reusable", "what is where", "global attention", "no labels needed", "vision &#8596; text", "create images"][i]
        g.append(txt(cx if anchor!="start" else cx-12, y+78, sub, 13, mono=False, anchor=anchor, op=0.4))
    return svg(1680, 170, "".join(g))

# ---------------------------------------------------------------- html build

CSS_EXTRA = """
.s-eyebrow { position: absolute; top: 80px; left: 120px; }
.s-num { position: absolute; bottom: 44px; left: 120px; font-family: var(--font-mono);
         font-size: 13px; letter-spacing: 0.16em; color: var(--c-faint); }
.s-title { font-family: var(--font-display); font-weight: 500; font-size: 66px;
           line-height: 1.05; letter-spacing: -0.02em; margin: 0; max-width: 1500px; }
.s-head { margin-top: 41px; }
.content { display: flex; gap: 90px; margin-top: 66px; height: 690px; }
.col-text { width: 640px; flex: none; display: flex; flex-direction: column; justify-content: flex-start; }
.col-fig  { flex: 1; min-width: 0; display: flex; align-items: center; justify-content: center; }
.bullet { padding: 24px 0; font-family: var(--font-body); font-size: 23px; line-height: 1.42;
          color: rgba(0,0,0,0.78); border-bottom: 1px solid var(--c-line); }
.bullet:first-child { padding-top: 0; }
.bullet:last-child { border-bottom: none; }
.bullet b { font-weight: 500; color: #000; }
.theory-tag { display: inline-block; font-family: var(--font-mono); font-size: 13px;
              letter-spacing: 0.16em; text-transform: uppercase; background: #000; color: #FFF;
              padding: 7px 14px; margin-left: 24px; vertical-align: middle; }
table.syl { border-collapse: collapse; width: 100%; margin-top: 70px; }
table.syl th { font-family: var(--font-mono); font-size: 13px; letter-spacing: 0.16em;
               text-transform: uppercase; color: var(--c-dim); text-align: left;
               padding: 0 0 16px 0; border-bottom: 1px solid #000; font-weight: 400; }
table.syl td { font-family: var(--font-body); font-size: 21.5px; padding: 13.5px 40px 13.5px 0;
               border-bottom: 1px solid var(--c-line); color: rgba(0,0,0,0.8); }
table.syl td.lvl { font-family: var(--font-mono); font-size: 15px; letter-spacing: 0.08em; }
table.syl td.num { text-align: right; padding-right: 0; font-family: var(--font-mono); font-size: 15px; color: rgba(0,0,0,0.45); }
table.syl tr.theory td { color: #000; font-weight: 500; }
"""

def slide_html(num, eyebrow, title, bullets, figure, theory=False, fig_caption=None):
    btxt = "".join(f'<div class="bullet">{b}</div>' for b in bullets)
    tag = '<span class="theory-tag">Theory</span>' if theory else ''
    cap = f'<div style="font-family: var(--font-mono); font-size:13px; letter-spacing:0.16em; text-transform:uppercase; color: var(--c-faint); margin-top: 24px;">{fig_caption}</div>' if fig_caption else ''
    return f'''
<div class="slide">
  <div class="s-eyebrow eyebrow">{eyebrow}</div>
  <div class="s-head"><h1 class="s-title">{title}{tag}</h1></div>
  <div class="content">
    <div class="col-text">{btxt}</div>
    <div class="col-fig"><div>{figure}{cap}</div></div>
  </div>
  <div class="s-num">{num:02d}</div>
</div>'''

slides = []

# 1 — cover
slides.append(f'''
<div class="slide">
  <div class="s-eyebrow eyebrow">IOAI 2026 &#183; SYLLABUS SECTION 3 &#183; COMPUTER VISION</div>
  <div style="margin-top: 270px;">
    <h1 class="title" style="font-size: 158px;">Vision Models:<br/>From Pixels<br/>to Diffusion</h1>
  </div>
</div>''')

# 2
slides.append(slide_html(2, "THE PROBLEM", "An image is just a tensor of numbers", [
  "A color image is a grid of pixels: <b>height &#215; width &#215; 3 channels</b> (R, G, B), each value 0&#8211;255",
  "A small 224&#215;224 photo is already ~150,000 numbers &#8212; meaning lives in <b>patterns</b>, not pixels",
  "The same object shifts, scales, rotates, changes lighting &#8212; the model must learn <b>invariance</b>",
  "Goal: compress raw pixels into a short, meaningful vector &#8212; an <b>embedding</b>",
], d2_tensor()))

# 3
slides.append(slide_html(3, "CONVOLUTIONAL LAYERS", "Convolution: a small filter slides over the image", [
  "A <b>filter (kernel)</b> is a tiny grid of learned weights &#8212; e.g. 3&#215;3 &#8212; slid across the image",
  "At each position: multiply weights by pixels underneath, sum &#8594; <b>one output number</b>",
  "The output grid is a <b>feature map</b> &#8212; it lights up wherever the filter&#8217;s pattern appears",
  "<b>Weight sharing</b>: same filter everywhere &#8594; few parameters; pattern found at any location",
  "Stack layers: edges &#8594; textures &#8594; object parts &#8594; objects",
], d3_conv(), theory=True))

# 4
fig4 = d4_pool() + '<div style="height: 60px;"></div>' + d4_pipeline()
slides.append(slide_html(4, "IMAGE CLASSIFICATION", "Pooling + stacking = a CNN classifier", [
  "<b>Max pooling</b>: keep the largest value in each 2&#215;2 window &#8212; halve resolution, keep the strongest signal",
  "<b>Average pooling</b>: take the mean &#8212; used globally at the very end of most CNNs",
  "Pooling adds tolerance to small shifts and makes deeper layers cheaper",
  "Recipe: [conv &#8594; ReLU &#8594; pool] &#215; N, then a linear layer &#8594; class probabilities",
  "In code: <b>nn.Conv2d, nn.MaxPool2d, nn.Linear</b> &#8212; that&#8217;s a full classifier",
], fig4))

# 5
slides.append(slide_html(5, "IMAGE AUGMENTATION", "Augmentation: free data from the data you have", [
  "Apply label-preserving changes during training: <b>flip, random crop, noise</b>, rotation, color jitter",
  "Model sees a &#8220;new&#8221; image every epoch &#8594; less overfitting, better generalization",
  "<b>Patch cut-out</b>: hide random patches so the model can&#8217;t rely on one local cue",
  "One line per transform (torchvision.transforms) &#8212; often the best accuracy boost in competitions",
  "Rule: the label must stay true &#8212; don&#8217;t flip a &#8220;6&#8221; into a &#8220;9&#8221;",
], d5_aug()))

# 6
slides.append(slide_html(6, "PRE-TRAINED VISION ENCODERS", "ResNet: skip connections made depth work", [
  "Plain deep CNNs became <b>hard to train</b> &#8212; the training signal degrades through many layers",
  "ResNet&#8217;s fix: each block outputs <b>x + F(x)</b> &#8212; the input plus a learned correction",
  "Gradients flow straight through the shortcut &#8594; 50&#8211;152-layer networks train reliably",
  "Trained on ImageNet&#8217;s millions of photos, ResNet became the standard <b>pre-trained encoder</b>",
  "One line: <b>torchvision.models.resnet50(weights=&#8230;)</b> &#8212; reusable features for any task",
], d6_resnet()))

# 7
slides.append(slide_html(7, "MODEL FINETUNING", "Finetuning: start smart, not from scratch", [
  "<b>Transfer learning</b>: take a pre-trained encoder, swap the last layer for your classes",
  "Tiny data &#8594; <b>freeze</b> the backbone, train only the new head",
  "More data &#8594; <b>finetune everything</b> gently, with a low learning rate",
  "<b>Parameter-efficient finetuning</b>: train small inserted adapters (LoRA-style); backbone stays frozen",
  "Why it wins competitions: small datasets + pre-trained features beat training from zero",
], d7_finetune()))

# 8
slides.append(slide_html(8, "OBJECT DETECTION", "Detection: what is where &#8212; YOLO, SSD, DETR", [
  "Detection = classification <b>+ localization</b>: a box, label, and confidence per object",
  "<b>YOLO</b>: one single pass predicts boxes over a grid &#8212; built for real-time speed",
  "<b>SSD</b>: single pass, predicts from feature maps at several scales &#8594; small and large objects",
  "<b>DETR</b>: a transformer outputs a direct <b>set</b> of detections &#8212; no anchor boxes, no NMS cleanup",
  "Pick: YOLO for speed &#183; SSD classic multi-scale &#183; DETR clean end-to-end",
], d8_detect()))

# 9
slides.append(slide_html(9, "IMAGE SEGMENTATION", "Segmentation: a label for every pixel &#8212; U-Net", [
  "Output is a full-resolution <b>mask</b>: each pixel gets a class",
  "<b>Encoder</b> downsamples to understand <b>what</b>; <b>decoder</b> upsamples to recover <b>where</b>",
  "<b>Skip connections</b> copy fine detail across the U &#8594; sharp mask boundaries",
  "Born in medical imaging; works well even with few training images",
  "Same skip idea as ResNet &#8212; here the skips carry spatial detail",
], d9_unet()))

# 10
slides.append(slide_html(10, "ATTENTION &#183; TRANSFORMERS", "ViT: cut the image into patches, treat them like words", [
  "<b>Attention</b>: each element scores its relevance to every other element, then gathers info by those weights",
  "Mechanic: each patch emits a <b>query</b>, compares to all <b>keys</b>, mixes the <b>values</b>",
  "<b>ViT</b>: slice the image into 16&#215;16 patches &#8594; embed each as a token &#8594; add position &#8594; transformer",
  "Global from layer one: patch 1 can directly attend to patch 196 &#8212; unlike a conv&#8217;s local window",
  "Trade-off: no built-in locality bias &#8594; ViTs need large-scale pre-training to shine",
], d10_vit(), theory=True))

# 11
slides.append(slide_html(11, "SELF-SUPERVISED LEARNING", "Learning features without labels", [
  "Human labels are expensive and slow; unlabeled images are nearly infinite",
  "<b>Self-supervision</b>: invent a training task from the data itself",
  "<b>Contrastive idea</b>: two augmented views of one image &#8594; pull embeddings together; other images &#8594; push apart",
  "Augmentations (slide 5) define what the model should <b>ignore</b>",
  "Result: a strong encoder from raw images &#8212; then finetune on your small labeled set",
], d11_ssl()))

# 12
slides.append(slide_html(12, "VISION&#8211;TEXT ENCODERS", "CLIP: images and text in one shared space", [
  "Two encoders &#8212; image and text &#8212; trained on huge sets of <b>(image, caption)</b> pairs",
  "Contrastive: matching pairs &#8594; similar embeddings; mismatched &#8594; dissimilar",
  "Result: <b>&#8220;a photo of a dog&#8221;</b> (text) lands next to actual dog photos",
  "<b>Zero-shot classification</b>: embed candidate captions + the image, pick the closest &#8212; no training",
  "Also powers image search and guides text-to-image generators",
], d12_clip()))

# 13
slides.append(slide_html(13, "GENERATING IMAGES &#183; GANS", "GANs: a forger and a detective in competition", [
  "<b>Generator</b> turns random noise into images; <b>discriminator</b> judges real vs. fake",
  "Adversarial loop: better detection forces better forgery &#8212; both improve together",
  "At equilibrium, fakes become hard to distinguish from real photos",
  "Strengths: sharp images, <b>one-pass</b> fast generation",
  "Pain points: unstable training, <b>mode collapse</b> (only a few &#8220;safe&#8221; outputs)",
], d13_gan()))

# 14
slides.append(slide_html(14, "DIFFUSION MODELS", "Diffusion: learn to denoise, then start from pure noise", [
  "<b>Forward</b> (fixed): add a little noise to a real image, step by step, until pure static",
  "<b>Reverse</b> (learned): a network predicts the noise so each step can subtract it",
  "<b>Generation</b>: start from random static, denoise step by step &#8594; a new image condenses out",
  "Condition on text embeddings (CLIP-style) &#8594; text-to-image, e.g. Stable Diffusion",
  "vs. GANs: stabler training, more diverse outputs &#8212; but many steps, so slower",
], d14_diffusion()))

# 15 — syllabus table
rows = [
  ("Convolutional layers", "THEORY + PRACTICE", "03", True),
  ("Image classification (+ pooling)", "PRACTICE", "04", False),
  ("Image augmentation &#8212; flip / crop / noise / patching", "PRACTICE", "05", False),
  ("Pre-trained vision encoders (ResNet)", "PRACTICE", "06", False),
  ("Model finetuning", "PRACTICE", "07", False),
  ("Object detection &#8212; YOLO, SSD, DETR", "PRACTICE", "08", False),
  ("Image segmentation &#8212; U-Net", "PRACTICE", "09", False),
  ("Attention / Transformers &#8594; ViT, image embeddings", "THEORY (SUPPORTING)", "10", True),
  ("Self-supervised learning for vision", "PRACTICE", "11", False),
  ("Vision&#8211;text encoders (CLIP)", "PRACTICE", "12", False),
  ("Generating images with GANs", "PRACTICE", "13", False),
  ("Diffusion models", "PRACTICE", "14", False),
]
trs = "".join(
  f'<tr class="{"theory" if th else ""}"><td>{t}</td><td class="lvl">{l}</td><td class="num">{s}</td></tr>'
  for t, l, s, th in rows)
slides.append(f'''
<div class="slide">
  <div class="s-eyebrow eyebrow">IOAI 2026 &#183; SYLLABUS MAP</div>
  <div class="s-head"><h1 class="s-title">Where each topic sits in the syllabus</h1></div>
  <table class="syl">
    <tr><th>Topic</th><th style="width:300px;">Level required</th><th style="width:90px; text-align:right;">Slide</th></tr>
    {trs}
  </table>
  <div class="s-num">15</div>
</div>''')

# 16 — recap
slides.append(f'''
<div class="slide">
  <div class="s-eyebrow eyebrow">RECAP</div>
  <div class="s-head"><h1 class="s-title">From pixels to diffusion &#8212; and what I&#8217;d build next</h1></div>
  <div style="margin-top: 90px;">{d16_journey()}</div>
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 60px; margin-top: 110px;">
    <div>
      <div class="eyebrow" style="margin-bottom: 20px;">TWO THEORY ANCHORS</div>
      <div style="font-size: 24px; line-height: 1.45; color: rgba(0,0,0,0.8);">Convolution and attention &#8212; be able to explain both on paper, cold.</div>
    </div>
    <div>
      <div class="eyebrow" style="margin-bottom: 20px;">ONE WINNING STRATEGY</div>
      <div style="font-size: 24px; line-height: 1.45; color: rgba(0,0,0,0.8);">Pre-trained encoder + strong augmentation + careful finetuning.</div>
    </div>
    <div>
      <div class="eyebrow" style="margin-bottom: 20px;">NEXT PROJECT</div>
      <div style="font-size: 24px; line-height: 1.45; color: rgba(0,0,0,0.8);">Finetune ResNet on a small custom dataset; compare against CLIP zero-shot as the baseline.</div>
    </div>
  </div>
  <div class="s-num">16</div>
</div>''')

with open("/work/projects/ioai-prep/vision-models/brand.css") as f:
    BRAND_CSS = f.read()

html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
{BRAND_CSS}
{CSS_EXTRA}
</style></head><body>
{"".join(slides)}
</body></html>'''

with open("/work/projects/ioai-prep/vision-models/deck.html", "w") as f:
    f.write(html)

from weasyprint import HTML, default_url_fetcher
def fetcher(url, t=15):
    try: return default_url_fetcher(url, timeout=t)
    except Exception: return {'string': b'', 'mime_type': 'image/jpeg'}
HTML(string=html, url_fetcher=fetcher).write_pdf("/work/projects/ioai-prep/vision-models/vision_models_deck.pdf")
print("rendered")
