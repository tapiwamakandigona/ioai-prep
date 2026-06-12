# Vision Models: From Pixels to Diffusion — Study Guide

Deep-dive companion to the deck. One section per slide, plus a teacher-FAQ at the end. Everything maps to the IOAI 2026 syllabus, Section 3 (Computer Vision) and the supporting items from Sections 1–2 (embeddings, pooling, attention, transformers, finetuning, augmentation, patching).

---

## 1. Title — framing the talk

The arc of the presentation mirrors the history and logic of the field: first we learn to **understand** images (classification, detection, segmentation), then to **learn without labels** (self-supervision, CLIP), then to **generate** images (GANs, diffusion). If you remember one sentence: *modern vision is about turning huge grids of pixel numbers into compact representations — and, recently, about running that pipeline in reverse to create images.*

## 2. An image is a tensor of numbers

A digital color image is stored as a 3-dimensional array (a **tensor**): height × width × 3 color channels (red, green, blue), with each entry typically an integer 0–255 (or a float 0–1 after normalization). A 224×224 RGB image therefore contains 224 × 224 × 3 = **150,528 numbers**.

Two things make vision hard:

1. **Meaning is distributed.** No single pixel says "cat". The signal lives in spatial patterns spanning thousands of pixels.
2. **Nuisance variation.** The same object produces wildly different pixel values under translation, scale, rotation, lighting, occlusion, and background changes. A good model must be **invariant** to these (output unchanged) while staying sensitive to what actually matters.

The unifying concept is the **embedding**: a learned function maps the raw tensor to a short vector (e.g., 512 numbers) where semantic similarity becomes geometric closeness — two photos of dogs land near each other even if their pixels barely correlate. Almost every model in this deck is, at heart, a machine for producing good embeddings.

## 3. Convolutional layers (THEORY — know this cold)

A **convolutional layer** applies a small grid of learnable weights — a **filter** or **kernel**, commonly 3×3 — across every spatial position of the input. At each position you take the element-wise product of the filter with the patch of input underneath, sum it (plus a bias), and write a single number to the output. Sliding the filter over the whole input produces a **feature map**: a spatial map of "how strongly does my pattern appear here?"

Key vocabulary you may be asked about:
- **Stride**: how many pixels the filter jumps each step. Stride 2 halves the output resolution.
- **Padding**: adding zeros around the border so the output keeps the same size (otherwise a 3×3 filter shrinks a 7×7 input to 5×5).
- **Channels**: a filter actually spans all input channels (a 3×3 filter on an RGB image has 3×3×3 = 27 weights + 1 bias). A layer has many filters; each produces one output channel. Output for a layer with 64 filters: H × W × 64.

Why convolution beats fully-connected layers for images:
1. **Weight sharing** — the same few weights are reused at every position, so parameter count is tiny and independent of image size (27 weights vs. millions for a dense layer on raw pixels).
2. **Translation equivariance** — if the input shifts, the feature map shifts the same way; the pattern detector works anywhere in the image. (Pooling and global averaging later turn this into approximate translation *invariance*.)
3. **Local connectivity matches image structure** — nearby pixels are strongly correlated; a hierarchy of local detectors composes naturally into global understanding: early layers learn edges and color blobs, middle layers textures and motifs, deep layers object parts and whole objects. This hierarchy has been confirmed by visualizing what trained filters respond to.

Worked micro-example you can do on a whiteboard: a vertical-edge filter `[[-1,0,1],[-2,0,2],[-1,0,1]]` (the Sobel kernel) gives large outputs where brightness increases left-to-right and ~0 in flat regions. CNNs *learn* such filters (and far better ones) from data instead of having them hand-designed.

## 4. Pooling and the full CNN classifier

**Max pooling** slides a window (typically 2×2, stride 2) and keeps only the maximum value; **average pooling** keeps the mean. Effects:
- **Downsampling**: each 2×2 pool halves height and width, quartering the computation for deeper layers and growing the **receptive field** (the input region each deep neuron can see).
- **Local invariance**: if a feature shifts by one pixel, the max in its window usually doesn't change — small translations stop mattering.
- **Global average pooling** (averaging each whole feature map to one number) is the standard final step in modern CNNs: it converts the last H×W×C feature maps into a C-dimensional vector regardless of input size, feeding one linear layer.

The classic image classification pipeline: `[Conv → ReLU → Pool] × N → global average pool → Linear → softmax`. **ReLU** (`max(0, x)`) is the nonlinearity that lets stacked layers express more than a single linear map; **softmax** turns the final scores into probabilities that sum to 1; training minimizes **cross-entropy loss** between predicted probabilities and the true label, by gradient descent / backpropagation. In PyTorch the whole model is `nn.Conv2d`, `nn.ReLU`, `nn.MaxPool2d`, `nn.AdaptiveAvgPool2d`, `nn.Linear` inside an `nn.Sequential`.

## 5. Image augmentation

**Augmentation** = applying random, label-preserving transformations to training images on the fly, so the network never sees exactly the same input twice. Standard transforms: horizontal **flip**, random **crop** (with resize), additive **noise**, small rotations, color jitter (brightness/contrast/saturation), and **patch-based occlusion** — cutting out random rectangles (often called random erasing / Cutout-style augmentation) so the model can't depend on any single local cue.

Why it works: it injects our prior knowledge of which variations don't change the label, effectively multiplying the dataset and acting as a regularizer against overfitting. It is most valuable exactly when data is scarce — the typical olympiad situation.

Practical notes:
- Implemented in `torchvision.transforms` or `albumentations`; applied only to the **training** set, never to validation/test (except controlled "test-time augmentation", where you average predictions over several augmented copies).
- Augmentations must preserve the label: horizontal flips are fine for animals, wrong for digit datasets ("6"→"9"-like failures) or text.
- Aggressiveness is a hyperparameter: too strong and you destroy the signal.
- Connection forward: augmentation is also the *engine* of contrastive self-supervised learning (slide 11) — there it defines which variations the embedding should ignore.

## 6. Pre-trained encoders and ResNet

Around 2012–2015, deeper CNNs kept winning ImageNet (a benchmark with ~1.28M training images, 1000 classes) — until depth itself broke training. Plain 30+ layer stacks performed *worse* than shallower ones **even on training data**, so it wasn't overfitting; the optimization signal degrades as gradients pass through many layers (the **degradation problem**, related to vanishing gradients).

**ResNet (2015)** introduced the **residual block**: instead of learning a full transformation H(x), a block learns a residual F(x) and outputs **x + F(x)**, with the input carried over by an identity **skip connection**. Two consequences:
1. The default behavior of a block is "do nothing" (F≈0), so extra depth can't easily hurt.
2. During backpropagation the gradient has a direct path through the additions, so it reaches early layers undiminished. This made 50-, 101-, and 152-layer networks train reliably, and ResNet won the ImageNet classification competition in 2015.

A network trained on a huge dataset becomes a **pre-trained encoder** (a "backbone"): its convolutional features — edges, textures, parts — are generic enough to transfer to almost any visual task. In practice you load one with a single line (`torchvision.models.resnet50(weights=...)` or `timm.create_model(..., pretrained=True)`) and either extract features or finetune it (next section). ResNet remains the default CNN backbone; detection and segmentation models usually contain one inside.

## 7. Transfer learning and finetuning

**Transfer learning**: reuse knowledge from a model trained on a large source dataset (e.g., ImageNet) for a new target task. Recipe: replace the final classification layer (the "head") with a fresh one sized for your classes, then choose a training regime:

- **Feature extraction / linear probing**: freeze the entire backbone, train only the new head. Fastest, safest with very small datasets (hundreds of images); the backbone is used as a fixed embedding function.
- **Full finetuning**: train everything with a *small* learning rate (often 10× smaller for pre-trained layers than for the new head). More accurate with moderate data, but risks **catastrophic forgetting** — large updates can destroy the useful pre-trained features.
- **Parameter-efficient finetuning (PEFT)**: keep the backbone frozen and insert small trainable modules — e.g., **LoRA** (low-rank adaptation) adds low-rank update matrices to existing weight layers; adapter layers insert small bottleneck MLPs between blocks. Only ~1–5% of parameters train, which means less memory, less overfitting, and you can keep one backbone with many small task-specific add-ons. PEFT originated for large language models but applies directly to vision transformers and CNNs.

Practical details that matter: normalize inputs with the same mean/std the pre-trained model expects; resize to its expected input resolution; consider freezing batch-norm statistics for tiny datasets. Why this wins competitions: with 1–5k labeled images, a from-scratch CNN badly overfits, while a pre-trained backbone already knows generic visual features and only needs to adapt — routinely a double-digit accuracy gap.

## 8. Object detection: YOLO, SSD, DETR

**Object detection** outputs, for every object in an image: a **bounding box** (4 coordinates), a **class label**, and a **confidence score**. Quality is measured by **IoU** (intersection-over-union of predicted vs. true box) and summarized as **mAP** (mean average precision).

- **YOLO** ("You Only Look Once"): divides the image into a grid and, in a **single forward pass**, predicts boxes and class probabilities for each cell. Framing detection as one regression problem made it dramatically faster than older two-stage pipelines (which first proposed regions, then classified each) — fast enough for real-time video. The family has many successive versions; the core single-pass idea is unchanged.
- **SSD** ("Single Shot MultiBox Detector"): also one pass, but predicts boxes from **feature maps at multiple resolutions** — early high-resolution maps catch small objects, deep low-resolution maps catch large ones. It popularized heavy use of **anchor boxes** (predefined default box shapes that predictions refine).
- **DETR** ("DEtection TRansformer"): a CNN backbone feeds a **transformer** that emits a fixed-size *set* of predictions via learned "object queries". Trained with a bipartite (Hungarian) matching loss that assigns each prediction to at most one ground-truth object, it eliminates hand-engineered components: no anchor boxes and no **NMS** (non-maximum suppression — the post-processing step other detectors need to delete duplicate boxes for the same object). Cleaner pipeline; the original version trained slowly and was weaker on small objects, which follow-ups improved.

Choosing in practice: YOLO when speed/real-time matters; SSD as the classic multi-scale single-shot baseline; DETR when you want an end-to-end transformer pipeline. For an olympiad task you would almost always load a pre-trained detector (Ultralytics YOLO, or Hugging Face `DetrForObjectDetection`) and finetune it on the task's boxes.

## 9. Image segmentation and U-Net

**Semantic segmentation** assigns a class to **every pixel**, producing a mask the same size as the image. (Vocabulary if asked: *instance* segmentation additionally separates individual objects of the same class; the syllabus model U-Net is the semantic workhorse.)

The challenge: classification networks deliberately throw away spatial precision (pooling, downsampling) to gain semantic understanding — but a mask needs both *what* and *exactly where*.

**U-Net (2015, medical imaging)** resolves this with a symmetric **encoder–decoder**:
- **Encoder** (contracting path): conv + pool blocks downsample, capturing context — *what is in the image*.
- **Decoder** (expanding path): upsampling/transposed-conv blocks restore resolution — *where it is*.
- **Skip connections**: feature maps from each encoder level are concatenated into the matching decoder level, handing the decoder the high-resolution detail that downsampling destroyed. Without skips, masks come out blobby; with them, boundaries are sharp.
- Final layer: 1×1 convolution → per-pixel class scores; trained with per-pixel cross-entropy (or Dice loss for class imbalance).

U-Net was designed to work with very few training images (its original biomedical setting) and remains the default segmentation baseline; `segmentation_models_pytorch` gives you a U-Net with a pre-trained ResNet encoder in one line. Note the conceptual rhyme with ResNet: both use skip connections, but ResNet's fix optimization *within* a block while U-Net's carry *spatial information across* the network.

## 10. Attention and Vision Transformers (THEORY — know this cold)

**Attention** lets each element of a set gather information from all other elements, weighted by learned relevance. Mechanics (self-attention): each token produces three vectors via learned linear maps — a **query** Q ("what am I looking for?"), a **key** K ("what do I contain?"), and a **value** V ("what do I communicate?"). Token i attends to token j with weight softmax(Qᵢ·Kⱼ / √d); its output is the weighted sum of all values. **Multi-head** attention runs several of these in parallel so different heads can track different relationships. A **transformer** block = self-attention + a small MLP, each wrapped with residual connections and normalization.

**Vision Transformer (ViT)** adapts this to images:
1. Split the image into fixed-size **patches** (16×16 pixels is standard → a 224×224 image gives 196 patches).
2. Flatten each patch and project it linearly to an embedding — patches become **tokens**, exactly like words in a sentence.
3. Add **position embeddings** (attention itself is order-blind; without them the model couldn't know the spatial layout).
4. Feed through a stack of transformer blocks; a special classification token (or mean of tokens) becomes the image embedding.

CNN vs. ViT in one contrast: a convolution sees a small local window and builds global context slowly through depth; attention is **global from layer one** — any patch can directly exchange information with any other. The price: ViTs lack convolution's built-in assumptions (**inductive biases**) of locality and translation equivariance, so they must learn them from data — with small datasets CNNs tend to win, with large-scale pre-training ViTs match or surpass them. ViT backbones now power CLIP, DETR-style detectors, and diffusion model components.

## 11. Self-supervised learning for vision

**Motivation**: labels are the bottleneck — expert annotation (medical, scientific) is expensive and slow, while unlabeled images exist in practically unlimited quantities. **Self-supervised learning (SSL)** creates a training signal from the data itself via a **pretext task**, producing a pre-trained encoder without any human labels.

The flagship idea on the syllabus is **contrastive learning**:
1. Take an image; create **two views** with random augmentations (crop, flip, color jitter, blur — slide 5's toolbox).
2. Pass both through the same encoder.
3. Loss pulls the two views' embeddings **together** (positive pair) while pushing embeddings of **other images** in the batch **apart** (negatives). SimCLR is the canonical formulation (large batches supply the negatives); related families avoid explicit negatives (BYOL-style) or use clustering (DINO-style), but the syllabus-level idea is the same: *invariance to augmentations + spread over the dataset*.

The augmentation choice is the supervision: by declaring "a crop and a recolor of this image are the same thing", we force the encoder to capture object identity, not superficial appearance. Other pretext tasks worth naming: predicting masked-out patches (masked autoencoders — the vision version of masked language modeling), solving jigsaw orderings, predicting rotation.

Workflow: SSL pre-train on lots of unlabeled images → evaluate by **linear probing** (train one linear layer on frozen features) → **finetune** with your small labeled set. SSL features now rival supervised pre-training on many transfer tasks.

## 12. CLIP — vision–text encoders

**CLIP** (Contrastive Language–Image Pre-training, OpenAI 2021) trains **two encoders jointly** — an image encoder (ResNet or ViT) and a text encoder (transformer) — on hundreds of millions of (image, caption) pairs from the web. Training is contrastive across modalities: in each batch, embed N images and N captions, compute all N×N cosine similarities, and optimize so the N true pairs (the diagonal of the matrix) score high and all mismatched pairs score low.

The result is a **shared embedding space** where images and texts are directly comparable: "a photo of a dog" lands near actual dog photos.

**Zero-shot classification** — the signature trick:
1. Write a text prompt per class: "a photo of a cat", "a photo of a dog", …
2. Embed all prompts with the text encoder; embed the test image with the image encoder.
3. Predict the class whose prompt embedding has highest cosine similarity with the image embedding.

No task-specific training images at all, and accuracy is strong across many datasets (prompt wording matters — "a photo of a {class}" beats the bare class name). Limits: CLIP struggles with fine-grained counting, reading text reliably, and very specialized domains far from web imagery.

Beyond classification: CLIP embeddings power semantic **image search** (embed query text, retrieve nearest images), and CLIP's text encoder provides the conditioning signal in text-to-image generators. In code: `pip install open_clip_torch` or Hugging Face `CLIPModel` — a zero-shot classifier is ~10 lines.

## 13. GANs — generative adversarial networks

A **GAN** (2014) trains two networks in opposition:
- **Generator** G: maps a random noise vector z (e.g., 100 numbers from a Gaussian) to an image. It never sees real images directly — it only gets gradient feedback through the discriminator.
- **Discriminator** D: a binary classifier trained to output "real" for dataset images and "fake" for G's outputs.

Training alternates: improve D at catching fakes, then improve G at fooling the *current* D. Formally a two-player minimax game; at the ideal equilibrium, G's distribution matches the data distribution and D is reduced to 50/50 guessing. Intuition: forger vs. detective, each forcing the other to improve.

Strengths: **sharp, realistic outputs** and **fast generation** — one forward pass per image (vs. many steps for diffusion). GANs produced the first convincing photorealistic synthetic faces.

Weaknesses you should be able to name:
- **Training instability**: the two-player dynamics can oscillate or diverge; balance between G and D is delicate.
- **Mode collapse**: G discovers a few outputs that reliably fool D and produces only those, losing diversity.
- No straightforward training-progress metric (loss curves don't track image quality well; people use scores like FID).

Vocabulary: the noise vector space is the **latent space**; walking through it smoothly morphs the generated images, and conditional GANs add a class label or text input to control what is generated.

## 14. Diffusion models

**Idea**: learn to reverse a gradual noising process.

- **Forward process** (fixed, no parameters): repeatedly add small amounts of Gaussian noise to a real image over many steps (hundreds to ~1000 in the classic formulation) until it is indistinguishable from pure noise.
- **Reverse process** (learned): train a network — typically a **U-Net** (slide 9 returns!) or a transformer — that takes a noisy image plus the step number and **predicts the noise** that was added. Subtracting the predicted noise performs one small denoising step. The training objective is essentially a simple regression (mean-squared error on the noise), which is why training is so much more stable than a GAN's adversarial game.
- **Generation**: sample pure Gaussian noise, then apply the learned denoiser step by step; structure gradually condenses until a clean, novel image remains.

**Text-to-image**: condition every denoising step on a text embedding (from a CLIP-style or T5 text encoder), usually with cross-attention layers inside the U-Net; classifier-free guidance scales how strongly the image follows the prompt. **Latent diffusion** (the design behind Stable Diffusion) runs the whole process in the compressed latent space of an autoencoder instead of pixel space, cutting compute dramatically.

Diffusion vs. GANs: stable training, excellent diversity and quality, a meaningful likelihood-flavored objective — but generation requires many network evaluations, so it is slower (active research compresses this to few steps). Diffusion is the engine of current image generators (Stable Diffusion, DALL·E-class systems, Imagen).

## 15. Syllabus map

In IOAI terms: **Theory** = explain the mechanism on paper (convolutional layers; plus attention/transformers as supporting theory for ViT). **Practice** = know what the tool does, when to use it, and how to apply it with standard libraries (PyTorch, torchvision, timm, Hugging Face, Ultralytics) — typically by loading something pre-trained and finetuning, not implementing from scratch. Every Section-3 topic appears in this deck: convolutions (3), classification (4), augmentation (5), pre-trained encoders/ResNet (6), finetuning (7), YOLO/SSD/DETR (8), U-Net (9), ViT + image embeddings (10), self-supervised learning (11), CLIP (12), GANs (13), diffusion (14). Nothing off-syllabus (no 3D, video, or optical flow) is included.

## 16. Recap and next project

The single storyline: pixels → convolutional features → deep reusable encoders (ResNet) → localized understanding (detection, segmentation) → global attention (ViT) → label-free pre-training (SSL) → language-connected vision (CLIP) → generation (GANs, diffusion). The proposed next project is deliberately syllabus-shaped: finetune a pre-trained ResNet on a small custom dataset with strong augmentation, and benchmark it against CLIP zero-shot — exercising slides 5, 6, 7, and 12 in one experiment, and producing a concrete accuracy comparison to talk about.

---

# FAQ — 8 questions a teacher might ask

**1. Why use convolutions at all instead of a plain fully-connected network on the pixels?**
Three reasons. Parameters: a dense layer from a 224×224×3 image to even 1000 neurons needs ~150 million weights; a conv layer needs a few thousand, because the same small filter is shared across all positions. Generalization: weight sharing encodes the prior that a useful pattern (an edge, an eye) is useful *anywhere* in the image — a dense net would have to relearn it at every location. Structure: stacking local detectors builds a hierarchy (edges → textures → parts → objects) that matches how visual scenes are composed.

**2. What exactly is the difference between max pooling and average pooling, and when do you use each?**
Max pooling keeps the strongest activation in each window — it asks "was the feature present here at all?" and is the standard choice between conv blocks because it preserves sharp detections and adds small-shift invariance. Average pooling smooths — it summarizes overall activity — and its main modern use is **global** average pooling at the end of the network, collapsing each feature map to one number to form the final feature vector regardless of input size.

**3. Why does the skip connection in ResNet help — what was actually going wrong without it?**
Plain deep networks suffered the *degradation problem*: past ~20–30 layers, adding layers increased even the **training** error, so it wasn't overfitting — the optimizer simply couldn't fit deep stacks, partly because gradients degrade as they pass through many transformations. The skip makes each block compute x + F(x): the identity is the built-in default, so extra layers can't easily make things worse, and during backpropagation gradients flow through the addition directly to earlier layers. Same principle, different purpose, in U-Net: there skips carry high-resolution spatial detail from encoder to decoder.

**4. Are skip connections in U-Net the same thing as in ResNet?**
Same mechanism — copy information forward past intermediate layers — but different role. ResNet's skips are short-range, inside each block, and exist to make *optimization* of very deep networks possible. U-Net's skips are long-range, jumping from each encoder level across the "U" to the matching decoder level, and exist to restore *spatial precision*: the decoder gets back the fine detail (exact edges) that pooling destroyed, which is why U-Net masks have sharp boundaries.

**5. When would you choose a ViT over a CNN, and why does data size matter so much?**
A CNN hard-wires two assumptions: nearby pixels matter most (locality) and patterns can appear anywhere (translation equivariance). These *inductive biases* are a head start when data is limited, so on small datasets CNNs usually win. A ViT makes neither assumption — attention is global and position is only a learned embedding — so it must learn those regularities from data, which takes large-scale pre-training; given that scale, ViTs match or beat CNNs and scale better. Practical rule: small data + training from scratch → CNN; large-scale pre-trained checkpoint available (often via finetuning) → ViT is excellent. Hybrids and strongly-augmented training narrow the gap.

**6. How can CLIP classify images of classes it was never explicitly trained on?**
CLIP wasn't trained for any fixed class list — it was trained to align images with free-form *text* over hundreds of millions of web pairs. Classification is then re-cast as retrieval: embed prompts like "a photo of a cat" and "a photo of a dog", embed the image, and pick the most similar prompt in the shared space. Any concept that web captions describe reasonably well can be a "class" at test time, with zero training images. The cost: it inherits web-data biases and weakens on domains or distinctions rarely captioned online (fine-grained species, medical scans, counting).

**7. If GANs generate in one fast pass, why has the field moved to diffusion models?**
Training, not inference. A GAN is a two-player adversarial game — unstable, hard to tune, prone to mode collapse, with loss values that don't track quality. A diffusion model trains on a plain regression objective (predict the added noise), which is stable, scales well, and covers the data distribution much better, giving higher diversity and reliable prompt-following at large scale. The slowness of many denoising steps is real but is being engineered away (latent-space diffusion, few-step samplers and distillation), whereas GAN instability resisted a decade of fixes. GANs still matter where single-pass speed is critical.

**8. With a small labeled dataset in a competition, what is your concrete plan?**
(1) Look at the data and set up a trustworthy validation split. (2) Baselines first: CLIP zero-shot costs no training and sets a floor. (3) Load a pre-trained backbone (ResNet or a small ViT); train a linear head on frozen features. (4) If validation says there's headroom, unfreeze and finetune end-to-end with a low learning rate — or use a parameter-efficient method like LoRA if compute or data is tight. (5) Add strong but label-safe augmentation (flips, crops, color jitter, patch cut-out). (6) Iterate against validation only; consider test-time augmentation or averaging a couple of models at the end. The theme: never train from scratch when a pre-trained model exists.

---

*Companion files: `DECK_CONTENT.md` (slide content + speaker notes), `vision_models_deck.pdf` (presenting deck), `vision_models_deck.pptx` (same content with speaker notes embedded).*
