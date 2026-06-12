# Vision Models From Zero — beginner deck content draft (v1, pre-research-merge)

Audience: 14–18, zero coding/AI. Presenter: Rone (~20, no background).
Per-topic ladder: plain words → analogy → picture → proper name → code → knobs.
Rule: ONE new idea per slide. A term is never used before it is earned.

## PART 0 — SETUP

### S1 Cover
Eyebrow: IOAI 2026 SYLLABUS · SECTION 3 · COMPUTER VISION
Title: How machines learn to see
(whitespace)

### S2 The promise
Title: One day, one story
- Part 1 — The trick: how a computer turns numbers into "cat". We compute it by hand.
- Part 2 — The learning: nobody programs it; it practices and improves.
- Part 3 — The shortcut: borrow a model someone already trained.
- Part 4 — The superpowers: find objects, cut them out, talk to images, create images.
- Part 5 — The cheat sheets: every term and every knob on two slides you can keep.
Dek: If you can multiply small numbers, you can follow every step today.

### S3 Five words we'll use all day (base vocabulary, earned up front)
Plain table, 5 rows:
- MODEL — a machine made of numbers that turns an input into a guess. (vending machine for answers)
- DATASET — the pile of examples we teach with (photos + correct answers).
- LABEL — the correct answer attached to an example ("this photo is a cat").
- TRAINING — showing the model examples until its guesses get good.
- ACCURACY — out of 100 tries, how many guesses were right.
Note: only these five. Everything else gets introduced when earned.

### S4 Statement (dark): A computer has never seen a cat.

### S5 A photo is just a grid of numbers
- Zoom into any photo far enough → squares. One square = one PIXEL.
- Each pixel is one number: 0 = black, 255 = white, in-between = gray.
- Color photo = three grids stacked: red, green, blue.
Visual: chelsea_marked.png + real 10×10 pixel grid (values from pixel_grid.json)
NAME box: pixel; the grid is called a TENSOR (just "a grid of numbers, possibly stacked").
Knob: image size 32×32 = 3,072 numbers → 224×224 = 150,528 numbers. More numbers = more detail = more work.
Interaction: which corner has the big numbers — bright fur or dark pupil?

## PART 1 — THE TRICK

### S6 Statement-ish setup → hand convolution (centerpiece)
Title: The trick, by hand (it's just times tables)
Visual: three grids — 5×5 input (columns of 2s then 0s), 3×3 stencil (1 0 -1 ×3 rows), multiply-and-add = 6; flat region = 0.
- Take a tiny 3×3 grid of numbers — a stencil.
- Lay it on the photo. Multiply matching cells. Add the nine answers.
- Big total = "my pattern is HERE". Zero = "nothing here".
Interaction: compute the nine products together.
NAME box: this operation = CONVOLUTION. The stencil = FILTER (or KERNEL).

### S7 Run the filter everywhere → feature map
- Slide the stencil across the whole photo, write down the answer at every stop.
- You get a new "image" that glows where the pattern lives.
Visual: chelsea_gray → fmap_vertical (whiskers glow) → fmap_horizontal.
NAME box: the output map = FEATURE MAP.
Knob: rotate the filter 90° → finds horizontal edges instead. Different numbers in the stencil = different pattern found.

### S8 Stride & padding (the two sliding rules)
Plain: stride = how big a step the stencil takes. padding = invisible zeros glued around the border so the edges get a turn.
Visual: SVG — same 6×6 grid, stride 1 vs stride 2 positions; padding ring shown as dashed cells.
Knobs:
- stride 1 → output almost same size; stride 2 → output half size (cheaper, blurrier view).
- no padding: 3×3 filter shrinks 7×7 → 5×5; padding 1 keeps 7×7 → 7×7.
- kernel 3×3 → 7×7: sees bigger patterns at once, but 27 → 147 weights per filter (slower, needs more data).

### S9 Pooling — shrink and forgive
Plain: look at each little 2×2 window, keep only the biggest number ("was the pattern here at all?").
- Photo shrinks to half → deeper layers are cheaper.
- Pattern moved by one pixel? The max usually doesn't change → small shifts stop mattering.
- AVERAGE pooling = take the mean instead. GLOBAL average pooling at the very end = average each whole map to ONE number → a short list summarizing the photo.
Visual: SVG 4×4 grid → 2×2 max pooled, colored quadrants.
NAME box: MAX POOLING / AVERAGE POOLING / GLOBAL AVERAGE POOLING.
Knob: pool 2×2 → image halves; pool too much → you throw away where things were.

### S10 ReLU — the "keep the good news" switch
Plain: after each conv, replace every negative number with 0; keep positives.
Why: without a bend between layers, stacking layers = one big layer (a stack of rulers is still a ruler). The bend lets layers build on each other.
Visual: SVG graph of max(0,x).
NAME box: ACTIVATION FUNCTION; this one is ReLU. (Others exist: sigmoid squashes to 0–1, tanh to −1–1.)

### S11 The full machine: a CNN classifier
Pipeline: photo → [filter → ReLU → pool] → [again] → global average → short list of numbers → score per class → highest score wins.
- The short list of numbers that summarizes the photo = EMBEDDING.
- Scores turned into percentages that add to 100 = SOFTMAX.
- One label for the whole photo = IMAGE CLASSIFICATION.
Visual: horizontal pipeline SVG ending in "cat 92%".
NAME box: CONVOLUTIONAL NEURAL NETWORK (CNN). EMBEDDING. SOFTMAX. IMAGE CLASSIFICATION.

### S12 Code card 1 — the whole eye in a few lines
```python
import torch.nn as nn
model = nn.Sequential(
    nn.Conv2d(3, 32, kernel_size=3, padding=1),  # 32 stencils, 3x3
    nn.ReLU(),                                   # keep the good news
    nn.MaxPool2d(2),                             # shrink, forgive shifts
    nn.Conv2d(32, 64, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.AdaptiveAvgPool2d(1), nn.Flatten(),       # summarize -> embedding
    nn.Linear(64, 10),                           # 10 class scores
)
```
Knobs: out_channels 32→64: more patterns per layer, slower; kernel_size 3→7: bigger view, many more weights; remove ReLU → whole stack collapses to one layer (accuracy tanks).

## PART 2 — THE LEARNING

### S13 Statement (dark): Nobody programs the filters. The network finds them.

### S14 Learning = the hot-and-cold game
Loop: photo → model guesses ("70% dog") → compare with label ("cat") → one number says how wrong = LOSS → nudge every filter number a tiny step that makes it less wrong → repeat.
Visual: loop SVG.
NAME box: LOSS (wrongness score). The nudging recipe = BACKPROPAGATION + GRADIENT DESCENT. One full pass through the dataset = EPOCH.

### S15 Gradient descent = ball rolling downhill
Plain: imagine wrongness as a hilly landscape; training rolls the ball downhill step by step. Step size = LEARNING RATE.
Visual: SVG hill with ball + arrows; second panel: too-big steps bouncing across the valley.
Knobs:
- learning rate too small → crawls, training takes forever.
- learning rate 10× too big → loss jumps around or explodes; never settles.
- typical: start ~0.001 (Adam) and let it shrink. ADAM = gradient descent with momentum & per-knob step sizes — the sensible default.

### S16 Overfitting — memorizing vs understanding
Plain: a student who memorizes past papers aces practice, fails the real exam. Networks do that too.
- Split data: TRAIN (study material) vs TEST (the real exam, never studied).
- Train accuracy keeps climbing; test accuracy rises then FALLS → it started memorizing.
Visual: SVG two curves (train up, test up-then-down) with "stop here" marker.
NAME box: OVERFITTING, TRAIN/TEST SPLIT, EARLY STOPPING.
Knobs: more epochs → train acc up forever, test acc up then down; more/varied data → overfitting later; dropout/weight decay = built-in "forget a little on purpose" brakes.

### S17 Augmentation — free extra photos
Plain: a flipped cat is still a cat. Flip, crop, recolor, add noise → the model never sees the exact same photo twice → it can't memorize.
Visual: aug_original/flip/crop/jitter/noise row (REAL images).
Code card 2:
```python
train_tf = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
])
```
Knobs: only on TRAINING photos, never the test; too strong (crop 90% away) → label destroyed, accuracy drops; classic trap: flipping digits turns 6 into 9 — augmentation must keep the label true.

### S18 What the network actually learned
Visual: resnet_filters.png — all 64 first-layer filters of ResNet18 (trained on 1.28M photos).
- These are real learned stencils. Nobody drew them.
- They look like edge & color detectors — the network DISCOVERED that edges are the right first step.
- Layer 2 looks at edge maps → finds textures (fur, stripes). Higher layers: parts (ear, eye) → whole objects.
Ladder graphic: edges → textures → parts → objects.

### S19 Receipts — real numbers from this repo's notebooks
Bar chart: 50.0% small CNN from scratch (4,000 photos, 3 epochs) → 74.2% finetuned ResNet18 (1,000 photos!) → 88.5% CLIP (0 training photos).
Random guessing on 10 classes = 10%.
Interaction: guess the from-scratch score before reveal.
Dek: the rest of the deck explains the two bigger bars.

## PART 3 — THE SHORTCUT

### S20 Statement (dark): Don't start from scratch. Borrow trained eyes.

### S21 Pre-trained encoders
Plain: someone already trained a big CNN on 1.28 million photos (ImageNet, 1000 classes). Its filters already know edges, fur, wheels, faces. Download it, reuse it.
NAME box: PRE-TRAINED ENCODER / BACKBONE. ImageNet.
- The early layers are general-purpose: useful for ANY photo task — X-rays, satellites, your dataset.
Visual: stack diagram "1.28M photos → trained filters → reusable".

### S22 ResNet — the skip connection
Why famous: deeper SHOULD be better, but stacks past ~30 layers trained WORSE — the learning signal faded passing through so many layers.
Fix: each block outputs input + small correction (x + F(x)); a shortcut wire carries the input around the block.
- If a block has nothing to add, it can pass the input through untouched → extra depth can't hurt.
- The learning signal flows back through the shortcuts undiminished → 50/101/152 layers train fine.
Visual: SVG residual block (two paths joining at +).
NAME box: RESNET, SKIP (RESIDUAL) CONNECTION.

### S23 Transfer learning & finetuning
Plain: take the pretrained backbone, rip off its last layer (it answers the wrong question: 1000 ImageNet classes), bolt on a fresh small layer for YOUR classes, train gently.
Three gears:
- FREEZE backbone, train only new head → tiny data (hundreds of photos), fastest, safest.
- FINETUNE everything with a small learning rate → moderate data, best accuracy, can "wreck" good filters if LR too big.
- PARAMETER-EFFICIENT (LoRA/adapters): add tiny trainable side-pieces, keep backbone frozen → cheap, low memory.
Code card 3:
```python
from torchvision.models import resnet18, ResNet18_Weights
model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
model.fc = nn.Linear(512, 10)   # new head: my 10 classes
```
Knobs: data tiny → freeze more; LR for pretrained layers ~10× smaller than for the new head; forget to normalize inputs the way the backbone expects → accuracy silently drops.
This is the 74.2%-with-1,000-photos recipe.

## PART 4 — THE SUPERPOWERS

### S24 Statement (dark): Same trick. Four superpowers.

### S25 Object detection — what AND where
Plain: classification says "there's a cat somewhere"; detection draws a BOX around every object + label + confidence %.
Visual: det_chelsea (CAT 97%), det_astronaut (PERSON 91%) — real outputs.
Plain-words extras:
- IoU = how much the predicted box overlaps the true box (0 = miss, 1 = perfect).
- NMS = the cleanup step that deletes duplicate boxes for the same object.
Knob: confidence threshold 0.9 → fewer, surer boxes (misses shy objects); 0.3 → catches more, more false alarms.

### S26 The three detector families (table)
- YOLO — "You Only Look Once": one single pass over a grid → fastest, real-time video.
- SSD — single pass but predicts from several map sizes → catches small AND large objects.
- DETR — a transformer (S29 vocabulary...?) emits a set of boxes directly; no anchors, no NMS cleanup; cleaner but slower to train.
Choosing: speed → YOLO; classic multi-scale → SSD; end-to-end clean → DETR.
(In practice: download pretrained, finetune on your boxes.)

### S27 Segmentation — cut out the exact shape
Plain: boxes are rough. Segmentation decides for EVERY pixel: cat or not-cat → a mask.
Visual: seg_photo → seg_mask → seg_cutout (real outputs).
U-Net plain: an hourglass. Left side shrinks (WHAT is here), right side grows back (WHERE exactly), and skip wires hand the sharp details across, otherwise masks come out blobby.
NAME box: SEGMENTATION, MASK, U-NET, ENCODER–DECODER.
Where you've seen it: background blur in video calls, portrait mode, outlining organs in scans.

### S28 Self-supervised learning — learning without labels
Plain: labels are expensive (doctors, experts). But photos are free. Trick: make two different crops/recolors of the SAME photo and tell the network "these two must land at the same spot in your embedding space; different photos must land apart."
- The augmentations from S17 are the engine here.
- Result: a pretrained backbone with ZERO human labels.
NAME box: SELF-SUPERVISED LEARNING, CONTRASTIVE LEARNING.
Visual: SVG — one photo → two augmented views → arrows to nearby points; different photo → far point.

### S29 CLIP — a model that speaks image AND text
Plain: CLIP read 400 million internet photos WITH their captions. Two towers: one embeds images, one embeds sentences, trained so matching pairs land close.
Superpower: classify with SENTENCES — no training. "a photo of a cat" vs "a photo of a dog" → whichever sentence lands closest to the image wins.
Visual: clip bar row — cat 97.9%, tiger 1.6%, dog 0.5%, pizza 0.0% (real outputs).
Code card 4 (3 lines).
NAME box: CLIP, ZERO-SHOT.
Knob: change the wording → results change ("a photo of a cat" beats just "cat"; add "a blurry photo…" prompts for blurry datasets).
(One-line honesty: inside CLIP's image tower is a TRANSFORMER — it chops the image into 16×16 patches and lets every patch look at every other patch. That's all we need today.)

### S30 GANs — the forger and the detective
Plain: two networks play a game. The FORGER (generator) makes fake images from random noise; the DETECTIVE (discriminator) guesses real or fake. Each round both get better. Eventually the fakes fool everyone.
NAME box: GAN — GENERATOR vs DISCRIMINATOR (adversarial = "playing against").
Knob/note: famously unstable to train (if one player gets too good, the game collapses).

### S31 Diffusion — images out of static
Plain: train by RUINING photos — add a little noise, again and again until pure static. The network learns ONE humble skill: undo a little bit of noise.
Generate: start from fresh static, apply the cleanup over and over → an image crystallizes.
Visual: diff_0..diff_4 chain with arrow pointing BACKWARD labeled "generation runs this way".
NAME box: DIFFUSION MODEL. This is the engine of the famous image generators.

## PART 5 — CHEAT SHEETS

### S32 The map — syllabus checklist
Table: every Section 3 syllabus row → where it lives in this deck → six-word summary.

### S33 Glossary — every term in plain words (2 columns, ~24 terms)

### S34 Knob cheat sheet
Table: knob → turn it up → turn it down (kernel size, stride, padding, pooling, learning rate, epochs, augmentation strength, freeze vs finetune, confidence threshold, prompt wording).

### S35 Close (mirror cover)
- Everything here is the official IOAI 2026 syllabus, Section 3.
- Two notebooks in this repo rerun every number you saw (50.0 → 74.2 → 88.5).
- You computed a convolution by hand. The rest is that, repeated. Questions.
