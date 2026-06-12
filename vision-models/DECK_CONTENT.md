# Vision Models: From Pixels to Diffusion
Slide-by-slide content — 16 slides, mapped to the IOAI 2026 syllabus (Section 3 Computer Vision + supporting Section 1/2 topics).

---

## Slide 1 — Title

**Title:** Vision Models: From Pixels to Diffusion

**Bullets:**
- A tour of modern computer vision, from convolutions to image generation
- Built around the IOAI 2026 syllabus, Section 3: Computer Vision
- Presented by [student name] — IOAI / GAITE preparation

**Speaker notes (60–90 words):**
Hi everyone. Today I'll walk you through how computers learn to see. We'll start with the basic question — what an image actually is to a computer — then build up through convolutional networks, detection and segmentation, transformers, and finally models that can generate brand-new images from noise. Everything here comes straight from the official IOAI 2026 syllabus for computer vision, so this is exactly the material I'm preparing for the olympiad.

**Visual:** Clean title slide. Small visual motif: a row of squares morphing from random noise pixels into a recognizable shape (hinting at diffusion), drawn as simple colored grid cells.

---

## Slide 2 — Why Vision Is Hard

**Title:** An image is just a tensor of numbers

**Bullets:**
- A color image is a grid of pixels: height × width × 3 channels (red, green, blue), each value 0–255
- A small 224×224 photo is already ~150,000 numbers — and meaning lives in *patterns*, not individual pixels
- The same object looks different under shifts, lighting, rotation, scale — the model must learn invariance
- Goal: turn raw pixels into a compact, meaningful representation — an **embedding**

**Speaker notes:**
To a computer, a photo of a cat is not a cat — it's a giant grid of numbers, one brightness value per pixel per color channel. The hard part is that the meaning is spread across patterns of thousands of pixels, and those patterns move around: the cat can be anywhere in the frame, in any lighting. So vision models have one core job: compress this huge tensor of raw numbers into a short vector — an embedding — that captures *what's in the image* rather than where each pixel is.

**Visual:** A small cat-like icon next to a zoomed-in pixel grid showing actual numeric values in cells, with an arrow to a compact vector (embedding) — "150,528 numbers → 512 numbers that mean something".

---

## Slide 3 — Convolutional Layers (THEORY)

**Title:** Convolution: a small filter slides over the image

**Bullets:**
- A **filter (kernel)** is a tiny grid of learned weights, e.g. 3×3, slid across the whole image
- At each position: multiply filter weights by the pixels underneath, sum them up → one output number
- The output grid is a **feature map** — it lights up wherever the filter's pattern appears (e.g. a vertical edge)
- Key properties: **weight sharing** (same filter everywhere → few parameters) and **translation equivariance** (pattern detected anywhere)
- Many filters per layer → many feature maps; stacking layers detects edges → textures → parts → objects

**Speaker notes:**
This is the core idea of the whole field. Instead of connecting every pixel to every neuron, we use a tiny window of weights — say 3 by 3 — and slide it across the image. At each spot we multiply and sum, producing one number that says "how strongly does this patch match my pattern?" The result is a feature map. Because the *same* filter is reused everywhere, we need very few parameters, and a pattern is found no matter where it sits. Early layers learn edges; deeper layers combine them into textures and object parts.

**Visual:** Diagram of a 3×3 filter overlaid on a 6×6 input grid, with the multiply-and-sum producing one highlighted cell in the output feature map. Arrow sequence showing the filter at two slide positions.

---

## Slide 4 — Pooling and a Full CNN Classifier

**Title:** Pooling + stacking = a CNN for image classification

**Bullets:**
- **Max pooling:** keep only the largest value in each small window (e.g. 2×2) → halves the resolution, keeps the strongest signal
- **Average pooling:** take the mean instead — often used once at the very end (global average pooling)
- Pooling adds robustness to small shifts and shrinks the data flowing through the network
- Classic recipe: [conv → activation → pool] repeated, then a final linear layer → class scores (softmax → probabilities)
- This pipeline = **image classification**: one label for the whole image

**Speaker notes:**
After convolution, we usually pool. Max pooling looks at each small window and keeps only the biggest value — "was the feature here at all?" — which makes the network tolerant of the pattern shifting a pixel or two, and shrinks the feature maps so deeper layers are cheaper. Stack a few conv-and-pool blocks, flatten or average at the end, add one linear layer, and you have a complete image classifier: image in, probability per class out. In code, this is a few lines of PyTorch with nn.Conv2d, nn.MaxPool2d, and nn.Linear.

**Visual:** Two-part: (a) a 4×4 grid → 2×2 max-pool result with the max value of each colored quadrant kept; (b) a horizontal CNN pipeline: image → conv block → pool → conv block → pool → vector → "cat 0.92".

---

## Slide 5 — Image Augmentation

**Title:** Augmentation: free training data from the data you have

**Bullets:**
- Idea: apply label-preserving changes — **flip**, **random crop**, **noise**, rotation, color jitter — during training
- The model sees a "new" version of each image every epoch → less overfitting, better generalization
- **Patching / random erasing:** hide or cut out patches so the model can't rely on one local cue
- Cheap, applied on-the-fly (e.g. torchvision.transforms / albumentations) — often the single best accuracy boost in competitions
- Rule: augmentations must keep the label true (don't vertically flip a "6" into a "9")

**Speaker notes:**
Labeled images are expensive, so we stretch what we have. During training we randomly flip, crop, add noise, or jitter the colors of each image — a flipped cat is still a cat, so the label survives, but the pixels are different. The model can't memorize exact pictures anymore and is forced to learn the real concept. Cutting out random patches goes further: the model must recognize a dog even when its head is hidden. In practice this is one line per transform in torchvision, and it's frequently the difference between an overfit model and a winning one.

**Visual:** One source image (simple icon) fanning out into 4 variants: flipped, cropped, noisy, and with a gray patch cut out — each labeled, all still tagged "cat ✓".

---

## Slide 6 — Pre-trained Encoders & ResNet

**Title:** ResNet: skip connections made deep networks work

**Bullets:**
- Deeper CNNs *should* be better, but plain deep stacks became hard to train (gradients fade through many layers)
- **ResNet's fix — the skip connection:** each block outputs **x + F(x)**, i.e. "input + a learned correction"
- Gradients flow straight through the shortcut → networks with 50, 101, 152 layers train reliably
- A network trained on a huge dataset (e.g. ImageNet) becomes a **pre-trained encoder**: its features transfer to new tasks
- One line in code: `torchvision.models.resnet50(weights=...)` — then reuse its features

**Speaker notes:**
For years, making CNNs deeper eventually made them *worse* — not from overfitting, but because the training signal degraded through so many layers. ResNet solved this with an almost embarrassingly simple idea: let each block learn only a correction to its input, and add the input back via a shortcut. If a block has nothing useful to add, it can pass the input through untouched. This made 50-plus-layer networks trainable, and ResNets trained on millions of ImageNet photos became the standard reusable "vision backbone" everyone downloads instead of training from scratch.

**Visual:** A residual block diagram: input x splits into two paths — one through conv layers F(x), one a curved shortcut arrow — merging at a "+" node, output labeled "x + F(x)".

---

## Slide 7 — Transfer Learning & Finetuning

**Title:** Finetuning: start smart, not from scratch

**Bullets:**
- **Transfer learning:** take a pre-trained encoder, replace the final classification layer with one for *your* classes
- Options: **freeze** the backbone and train only the new head (fast, tiny data) or **finetune** all layers gently (low learning rate)
- **Parameter-efficient finetuning:** train only small added pieces (e.g. low-rank adapter layers, "LoRA"-style) — most weights stay frozen
- Why it wins competitions: olympiad datasets are small; pre-trained features + light finetuning beat from-scratch training almost always
- Practical care: lower learning rate for pre-trained weights; match the model's expected input normalization

**Speaker notes:**
Here's the most practical slide of the talk. In a competition you might get two thousand labeled images — nowhere near enough to train a deep network from zero. So you don't. You download a model already trained on millions of images, chop off its last layer, and attach a new one for your classes. If data is tiny, freeze everything and train just that head. With a bit more data, unfreeze and finetune everything with a small learning rate. Parameter-efficient methods go further, training only small inserted adapter weights — cheaper and less likely to wreck the good pre-trained features.

**Visual:** Diagram: pre-trained backbone drawn as a stack of frozen (snowflake-labeled) blocks, with the last block swapped for a small "new head" in a highlight, plus a second variant showing tiny adapter blocks inserted between frozen layers.

---

## Slide 8 — Object Detection

**Title:** Object detection: what is where — YOLO, SSD, DETR

**Bullets:**
- Detection = classification **plus localization**: output a box + label + confidence for every object
- **YOLO** ("You Only Look Once"): one single pass predicts boxes on a grid — built for real-time speed
- **SSD** ("Single Shot Detector"): also one pass, but predicts from feature maps at several scales → handles small + large objects
- **DETR** ("DEtection TRansformer"): a transformer emits a *set* of box predictions directly — no hand-made anchor boxes or NMS cleanup
- Choosing: YOLO for speed/real-time; SSD as the classic multi-scale single-shot design; DETR for a cleaner, end-to-end pipeline

**Speaker notes:**
Classification says "there's a dog somewhere." Detection says "a dog *here*, a ball *there*," each with a rectangle and a confidence score. YOLO's idea is to do this in one single network pass over a grid of the image, which is why it runs in real time. SSD is also single-pass but predicts from several feature-map resolutions, so it catches both small and large objects. DETR replaces all the hand-engineered parts — anchor boxes, duplicate-removal — with a transformer that directly outputs a set of detections. In practice you'd load any of these pre-trained and finetune on your boxes.

**Visual:** A scene with two labeled bounding boxes (dog 0.94, ball 0.88), then three mini-panels: YOLO = grid over image with boxes per cell; SSD = three stacked feature maps of decreasing size each emitting boxes; DETR = image → transformer → row of "object slots".

---

## Slide 9 — Image Segmentation & U-Net

**Title:** Segmentation: a label for every pixel — U-Net

**Bullets:**
- Segmentation outputs a full-resolution **mask**: each pixel gets a class (sky, road, tumor, background…)
- **U-Net** = encoder–decoder: the encoder downsamples to understand *what*; the decoder upsamples to recover *where*
- **Skip connections** copy fine detail from each encoder level straight to the matching decoder level → sharp boundaries
- Born in medical imaging (works well even with few training images); now the default segmentation baseline
- Same skip-connection spirit as ResNet — but here skips carry spatial detail across the "U"

**Speaker notes:**
Sometimes a box isn't enough — a medical model needs the exact outline of a tumor, pixel by pixel. That's segmentation. U-Net does it with a U-shaped network: the left side is a normal CNN encoder that shrinks the image while figuring out what's in it; the right side mirrors it, upsampling back to full resolution to decide where everything is. The trick is the skip connections across the U: they hand the decoder the fine details the encoder saw before downsampling, so the predicted mask has crisp, accurate edges instead of blurry blobs.

**Visual:** Classic U-shaped diagram: descending encoder blocks on the left, ascending decoder blocks on the right, horizontal skip-connection arrows bridging matching levels, with input image at top-left and colored mask at top-right.

---

## Slide 10 — Attention & Vision Transformers (THEORY)

**Title:** ViT: cut the image into patches, treat them like words

**Bullets:**
- **Attention:** every element computes how relevant every other element is, and gathers information weighted by that relevance
- (Mechanic: each patch makes a **query**, compares it to all **keys**, mixes the corresponding **values**)
- **Vision Transformer (ViT):** slice the image into fixed patches (e.g. 16×16 px), embed each patch as a token, add position info, feed to a transformer
- Attention is global from layer one — patch 1 can directly talk to patch 196 — unlike a conv's small local window
- Trade-off: ViTs lack convolution's built-in locality bias, so they shine with large-scale (pre-)training; CNNs are stronger on small data

**Speaker notes:**
Transformers conquered language first, and the question was: how do we feed an image to a model designed for word sequences? The Vision Transformer's answer: chop the image into a grid of small patches, flatten each into a vector — a token — and add a position signal so the model knows the layout. Then attention takes over: every patch asks, "which other patches matter for understanding me?" and pulls in information accordingly, across the whole image at once. The catch is that ViTs don't have convolution's head start of assuming nearby pixels matter, so they need lots of pre-training data to win.

**Visual:** An image divided into a 4×4 patch grid, patches peeling off into a row of tokens entering a transformer block; above it, attention lines connecting one highlighted patch to several distant patches with varying line thickness (= attention weight).

---

## Slide 11 — Self-Supervised Learning for Vision

**Title:** Self-supervised learning: features without labels

**Bullets:**
- Human labels are expensive and slow; unlabeled images are nearly infinite
- **Self-supervision:** invent a task from the data itself — no human labels needed
- **Contrastive idea:** two augmented views of the *same* image → embeddings pulled together; different images → pushed apart
- Augmentations (slide 5!) define what the model should ignore: crop, flip, color changes
- Result: a strong pre-trained encoder learned from raw images — then finetune on your small labeled set

**Speaker notes:**
Everything so far assumed someone labeled the data — and labeling a million images is brutally expensive. Self-supervised learning sidesteps that: the data supervises itself. The most intuitive version is contrastive learning. Take one photo, make two random augmented versions — different crops, flips, colors. Tell the network: these two must land close together in embedding space, while views of other images get pushed away. To succeed, the network must learn what makes that image *itself*, ignoring superficial changes. You get a powerful encoder from unlabeled data, then finetune it with the few labels you have.

**Visual:** One image splitting into two augmented views (crop + color-shift), both flowing through the same encoder into a 2D embedding plot where their two dots are pulled together by inward arrows, while a different image's dot is pushed away by an outward arrow.

---

## Slide 12 — CLIP: Vision–Text Encoders

**Title:** CLIP: images and text in one shared space

**Bullets:**
- Two encoders — one for images, one for text — trained on huge sets of (image, caption) pairs
- Contrastive training: matching image–caption pairs → similar embeddings; mismatched pairs → dissimilar
- Result: a **shared embedding space** where "photo of a dog" (text) lands near actual dog photos
- **Zero-shot classification:** embed prompts like "a photo of a cat / dog / car", embed the image, pick the closest — no task-specific training at all
- CLIP-style encoders also power image search and guide text-to-image generators

**Speaker notes:**
CLIP takes the contrastive idea from the last slide and applies it across two worlds at once. One encoder turns images into vectors; another turns text into vectors; training pulls each image toward its true caption and away from all wrong ones, over hundreds of millions of pairs. The payoff is a shared space where words and pictures are directly comparable. That enables something remarkable: zero-shot classification. Want a cat-versus-dog classifier with zero training images? Embed the sentences "a photo of a cat" and "a photo of a dog," embed your image, and pick the nearest sentence. It just works, and it's a go-to tool in olympiad tasks.

**Visual:** Dual-encoder diagram: image stack → image encoder; caption stack → text encoder; both arrows landing in one shared embedding plane where a dog photo dot sits next to the "a photo of a dog" text dot; a small similarity matrix with the bright diagonal.

---

## Slide 13 — GANs

**Title:** GANs: a forger and a detective, trained against each other

**Bullets:**
- Two networks: a **generator** turns random noise into images; a **discriminator** judges real vs. fake
- Adversarial training loop: discriminator learns to catch fakes → generator learns to fool it → repeat
- At equilibrium, generated images become hard to distinguish from real ones
- Strengths: sharp results, fast generation (one forward pass). Pain points: unstable training, **mode collapse** (generator produces only a few "safe" outputs)
- First family of models to make photorealistic generated faces possible

**Speaker notes:**
Now we flip the direction: instead of understanding images, we create them. A GAN is a game between two networks. The generator is a forger: it takes random noise and tries to paint a convincing image. The discriminator is a detective: shown real photos and forgeries, it learns to tell them apart. Each one's progress forces the other to improve — better detection demands better forgery. When training goes well, the fakes become indistinguishable. The catch is that this two-player game is unstable: it can oscillate, or the generator can collapse to producing the same few images over and over.

**Visual:** A circular loop: "noise z" → Generator box → fake image → Discriminator box (also fed real images from a small dataset stack) → "real/fake?" verdict → feedback arrows back to both networks.

---

## Slide 14 — Diffusion Models

**Title:** Diffusion: learn to remove noise, then start from pure noise

**Bullets:**
- **Forward process** (fixed, no learning): gradually add random noise to a real image over many steps until it's pure static
- **Learned reverse process:** a network is trained to predict and remove a little noise at each step
- **Generation:** start from pure random noise, denoise step by step → a brand-new image emerges
- Add text conditioning (often via CLIP-style embeddings) → text-to-image systems like Stable Diffusion
- vs. GANs: much more stable training and diverse outputs, but generation needs many steps, so it's slower

**Speaker notes:**
Diffusion models are today's state of the art for image generation, and the idea is beautifully simple. First, destroy: take real images and add a bit of noise, again and again, until nothing but static remains — that part needs no learning. Then teach a network to undo one small step of that noising: given a noisy image, predict the noise so we can subtract it. To generate, hand the model pure random static and let it denoise step by step — an image gradually condenses out of the noise. Condition each step on a text embedding and you get text-to-image generation, like Stable Diffusion.

**Visual:** A horizontal chain of 5 image frames going from a clear picture to pure noise (forward arrows above, labeled "add noise — fixed"), with reverse arrows below labeled "remove noise — learned", and a star on the right-to-left direction as "generation path".

---

## Slide 15 — Mapping to the IOAI 2026 Syllabus

**Title:** Where each topic sits in the IOAI 2026 syllabus

**Bullets (rendered as a table):**

| Syllabus topic | Level required | Covered on slide |
|---|---|---|
| Convolutional layers | Theory + Practice | 3 |
| Image classification (+ pooling) | Practice | 4 |
| Image augmentation (flip/crop/noise/patching) | Practice | 5 |
| Pre-trained vision encoders (ResNet) | Practice | 6 |
| Model finetuning | Practice | 7 |
| Object detection: YOLO, SSD, DETR | Practice | 8 |
| Image segmentation: U-Net | Practice | 9 |
| Attention / Transformers → ViT, image embeddings | Theory (supporting) | 10 |
| Self-supervised learning for vision | Practice | 11 |
| Vision–text encoders (CLIP) | Practice | 12 |
| Generating images with GANs | Practice | 13 |
| Diffusion models | Practice | 14 |

**Speaker notes:**
Quick orientation: this is the official checklist. In IOAI terms, "Theory" means I must be able to explain how something works on paper — that's convolutions, and the attention mechanism behind vision transformers. "Practice" means I need working intuition: what the tool does, when to reach for it, and how to use it with standard libraries like PyTorch, torchvision, and Hugging Face — typically loading something pre-trained and finetuning it rather than building it from scratch. Every row on this table maps to one slide you've just seen.

**Visual:** The table itself, clean and minimal, with the "Theory" rows subtly emphasized.

---

## Slide 16 — Recap & What I'd Build Next

**Title:** From pixels to diffusion — and what I'd build next

**Bullets:**
- One storyline: pixels → conv features → pre-trained encoders → detect / segment → attention & ViT → learn without labels → connect to text → generate
- Two theory anchors to master cold: **convolution** and **attention**
- One strategy that wins: pre-trained encoder + augmentation + careful finetuning
- Next project: finetune a pre-trained ResNet on a small custom dataset with heavy augmentation, then add CLIP zero-shot as a baseline comparison
- Questions welcome — the study guide has the details

**Speaker notes:**
So, the whole field in one breath: images are tensors; convolutions extract local patterns cheaply; ResNets made depth trainable and gave us reusable encoders; detection and segmentation localize what classifiers can only name; transformers brought global attention to vision via patches; self-supervision and CLIP removed the labeling bottleneck; and GANs and diffusion turned the pipeline around to generate images. My next step is hands-on: finetune a pre-trained ResNet on a small dataset with strong augmentation, and compare it against CLIP's zero-shot predictions as a baseline. Thanks — happy to take questions.

**Visual:** A single horizontal journey line with small labeled nodes: pixels → conv → ResNet → detect/segment → ViT → SSL → CLIP → GAN/diffusion, mirroring the deck's arc.
