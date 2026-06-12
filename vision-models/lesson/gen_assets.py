#!/usr/bin/env python
"""Generate all real-image assets for the from-scratch vision lesson deck.

Every asset is derived from a real photograph (skimage chelsea / astronaut)
or from real pretrained model weights. PNGs are written at the EXACT pixel
size they will be displayed at in the 1920x1080 deck (1:1, no resampling).
"""
import json, math, random
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image, ImageDraw

random.seed(0); np.random.seed(0); torch.manual_seed(0)

A = "/work/projects/ioai-prep/vision-models/lesson/assets"
chel = Image.open(f"{A}/chelsea.png").convert("RGB")          # 451x300
astro = Image.open(f"{A}/astronaut.png").convert("RGB")       # 512x512
W, H = chel.size

# ---------------------------------------------------------------- 1. pixel zoom
# find a high-contrast 10x10 window inside the eye region (viewer-left eye)
gray = np.array(chel.convert("L"), dtype=np.int32)
best, bx, by = -1, 0, 0
for y in range(80, 160):
    for x in range(130, 230):
        win = gray[y:y+10, x:x+10]
        c = int(win.max() - win.min())
        if c > best:
            best, bx, by = c, x, y
print("pixel crop at", bx, by, "contrast", best)
crop_vals = gray[by:by+10, bx:bx+10].tolist()
json.dump({"x": bx, "y": by, "values": crop_vals}, open(f"{A}/pixel_grid.json", "w"))

# full photo with crop marked, displayed at 640x426
disp_w = 640
disp_h = round(H * disp_w / W)
marked = chel.resize((disp_w, disp_h), Image.LANCZOS)
d = ImageDraw.Draw(marked)
sx = disp_w / W
box = [bx*sx-2, by*sx-2, (bx+10)*sx+2, (by+10)*sx+2]
for off in range(4):
    d.rectangle([box[0]-off, box[1]-off, box[2]+off, box[3]+off], outline=(255,255,255))
for off in range(4,7):
    d.rectangle([box[0]-off, box[1]-off, box[2]+off, box[3]+off], outline=(0,0,0))
marked.save(f"{A}/chelsea_marked.png")
print("chelsea_marked", marked.size)

# the zoomed crop itself as a blocky image (no numbers; numbers drawn in HTML)
zoom = chel.crop((bx, by, bx+10, by+10)).convert("L").resize((420, 420), Image.NEAREST)
zoom.save(f"{A}/chelsea_zoom.png")

# ---------------------------------------------------------------- 2. feature maps
# hand-written 3x3 edge filters applied to the real photo via real conv2d
g = torch.tensor(np.array(chel.convert("L"), dtype=np.float32) / 255.0)[None, None]
sobel_x = torch.tensor([[-1.,0.,1.],[-2.,0.,2.],[-1.,0.,1.]])[None, None]
sobel_y = sobel_x.transpose(2, 3).clone()
def fmap(k, name, w=400):
    out = F.conv2d(g, k, padding=1)[0,0].abs()
    out = (out / out.max()).numpy()
    img = Image.fromarray((out*255).astype(np.uint8))
    h = round(img.size[1] * w / img.size[0])
    img.resize((w, h), Image.LANCZOS).save(f"{A}/{name}.png")
    print(name, (w, h))
fmap(sobel_x, "fmap_vertical")
fmap(sobel_y, "fmap_horizontal")
chel.convert("L").resize((400, 266), Image.LANCZOS).save(f"{A}/chelsea_gray.png")

# ---------------------------------------------------------------- 3. ResNet18 learned filters
from torchvision.models import resnet18, ResNet18_Weights
rn = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
wts = rn.conv1.weight.detach()           # (64, 3, 7, 7)
wmin, wmax = wts.min(), wts.max()
wn = ((wts - wmin) / (wmax - wmin) * 255).byte().permute(0, 2, 3, 1).numpy()
cell, gap, cols, rows = 56, 8, 16, 4     # 7px filter -> 56 (8x nearest)
gw = cols*cell + (cols-1)*gap
gh = rows*cell + (rows-1)*gap
grid = Image.new("RGB", (gw, gh), (255, 255, 255))
for i in range(64):
    f = Image.fromarray(wn[i]).resize((cell, cell), Image.NEAREST)
    r, c = divmod(i, cols)
    grid.paste(f, (c*(cell+gap), r*(cell+gap)))
grid.save(f"{A}/resnet_filters.png")
print("resnet_filters", grid.size)

# ---------------------------------------------------------------- 4. augmentation
import torchvision.transforms as T
side = min(W, H)
sq = chel.crop(((W-side)//2, 0, (W-side)//2 + side, side)).resize((280, 280), Image.LANCZOS)
sq.save(f"{A}/aug_original.png")
sq.transpose(Image.FLIP_LEFT_RIGHT).save(f"{A}/aug_flip.png")
torch.manual_seed(7)
T.RandomResizedCrop(280, scale=(0.45, 0.6))(sq).save(f"{A}/aug_crop.png")
torch.manual_seed(3)
T.ColorJitter(brightness=0.5, contrast=0.4, saturation=0.6)(sq).save(f"{A}/aug_jitter.png")
arr = np.array(sq, dtype=np.float32)
noisy = np.clip(arr + np.random.normal(0, 28, arr.shape), 0, 255).astype(np.uint8)
Image.fromarray(noisy).save(f"{A}/aug_noise.png")
print("aug set done 280x280 x5")

# ---------------------------------------------------------------- 5. diffusion noise chain
sq2 = chel.crop(((W-side)//2, 0, (W-side)//2 + side, side)).resize((250, 250), Image.LANCZOS)
arr = np.array(sq2, dtype=np.float32) / 255.0
for i, t in enumerate([0.0, 0.35, 0.65, 0.88, 1.0]):
    a = math.cos(t * math.pi / 2)        # cosine-ish schedule
    mixed = a * arr + math.sqrt(max(1 - a*a, 0)) * np.random.normal(0, 1, arr.shape) * 0.55
    img = np.clip((mixed - mixed.min()) / (mixed.max() - mixed.min()), 0, 1) if t == 1.0 else np.clip(mixed, 0, 1)
    Image.fromarray((img*255).astype(np.uint8)).save(f"{A}/diff_{i}.png")
print("diffusion chain done 250x250 x5")

# ---------------------------------------------------------------- 6. real detection (SSDlite)
try:
    from torchvision.models.detection import ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights
    wts_d = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
    det = ssdlite320_mobilenet_v3_large(weights=wts_d).eval()
    cats = wts_d.meta["categories"]
    def detect(img, name, w=560, thr=0.45):
        x = torch.tensor(np.array(img), dtype=torch.float32).permute(2,0,1) / 255.0
        with torch.no_grad():
            out = det([x])[0]
        h = round(img.size[1] * w / img.size[0])
        vis = img.resize((w, h), Image.LANCZOS)
        dd = ImageDraw.Draw(vis)
        s = w / img.size[0]
        kept = []
        for b, lab, sc in zip(out["boxes"], out["labels"], out["scores"]):
            if sc < thr: continue
            b = [v.item()*s for v in b]
            for off in range(4):
                dd.rectangle([b[0]-off, b[1]-off, b[2]+off, b[3]+off], outline=(255,255,255))
            kept.append((cats[lab.item()], round(sc.item()*100)))
        vis.save(f"{A}/{name}.png")
        print(name, (w, h), kept)
        return kept
    k1 = detect(chel, "det_chelsea")
    k2 = detect(astro, "det_astronaut")
    json.dump({"chelsea": k1, "astronaut": k2}, open(f"{A}/det_results.json", "w"))
except Exception as e:
    print("DETECTION FAILED:", e)

# ---------------------------------------------------------------- 7. real segmentation (LR-ASPP)
try:
    from torchvision.models.segmentation import lraspp_mobilenet_v3_large, LRASPP_MobileNet_V3_Large_Weights
    wts_s = LRASPP_MobileNet_V3_Large_Weights.DEFAULT
    seg = lraspp_mobilenet_v3_large(weights=wts_s).eval()
    classes = wts_s.meta["categories"]
    cat_idx = classes.index("cat")
    tf = wts_s.transforms()
    with torch.no_grad():
        out = seg(tf(chel).unsqueeze(0))["out"][0]
    mask = (out.argmax(0) == cat_idx).numpy().astype(np.uint8)
    mimg = Image.fromarray(mask*255).resize(chel.size, Image.NEAREST)
    w = 400; h = round(H * w / W)
    chel.resize((w, h), Image.LANCZOS).save(f"{A}/seg_photo.png")
    mimg.resize((w, h), Image.NEAREST).save(f"{A}/seg_mask.png")
    cut = np.array(chel).copy()
    m = np.array(mimg) > 127
    cut[~m] = 255
    Image.fromarray(cut).resize((w, h), Image.LANCZOS).save(f"{A}/seg_cutout.png")
    print("segmentation done; cat pixels:", int(m.sum()))
except Exception as e:
    print("SEGMENTATION FAILED:", e)

# ---------------------------------------------------------------- 8. real CLIP zero-shot on chelsea
try:
    from transformers import CLIPModel, CLIPProcessor
    cm = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    cp = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    prompts = ["a photo of a cat", "a photo of a dog", "a photo of a tiger", "a photo of a pizza"]
    inputs = cp(text=prompts, images=chel, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = cm(**inputs).logits_per_image      # v5 gotcha: use logits_per_image
    probs = logits.softmax(dim=1)[0].tolist()
    json.dump({"prompts": prompts, "probs": probs}, open(f"{A}/clip_results.json", "w"))
    print("CLIP:", [(p, round(pr*100, 1)) for p, pr in zip(prompts, probs)])
    chel.resize((400, 266), Image.LANCZOS).save(f"{A}/chelsea_400.png")
except Exception as e:
    print("CLIP FAILED:", e)

print("ALL DONE")
