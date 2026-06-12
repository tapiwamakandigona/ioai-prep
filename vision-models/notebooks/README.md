# Vision Models — Hands-On Notebooks (IOAI / GAITE Prep)

Two teaching notebooks for a beginner olympiad contestant who knows basic Python.
Read the markdown cells carefully — they explain the **why**; the code shows the **how**.
Both notebooks are seeded, CPU-friendly, and run top-to-bottom without edits.

## The notebooks

| # | Notebook | What you'll learn | Expected runtime (CPU) |
|---|----------|-------------------|------------------------|
| 1 | `01_cnn_from_scratch.ipynb` | Build & train a small CNN on CIFAR-10: how convolution and pooling actually work (with the output-size formula), flip/crop **augmentation**, the universal 5-step PyTorch training loop, accuracy + **confusion matrix** evaluation, visualizing **learned filters** and **misclassified images** | ~3–6 min (+~1–2 min one-time CIFAR-10 download, 170 MB) |
| 2 | `02_transfer_learning_and_clip.ipynb` | **Transfer learning** with pretrained ResNet18 (why pretraining works, residual connections), **freeze-backbone vs full finetune** compared head-to-head on 1,000 images, then **CLIP zero-shot classification** — classifying images using only English text prompts (ViT patches, attention, contrastive image–text embeddings) | ~4–8 min (+ one-time downloads: ResNet18 ~45 MB, CLIP ~600 MB) |

**Do them in order.** Notebook 2 deliberately beats Notebook 1's from-scratch result with 4× less data — that comparison *is* the lesson.

## Mapping to the IOAI 2026 syllabus

| Syllabus topic | Where |
|---|---|
| Convolutional Layers (Theory + Practice) | NB1 §1, §4 |
| Image Classification (Practice) | NB1 throughout; NB2 throughout |
| Image Augmentation (Practice) — flips/crops | NB1 §3 (+ light use in NB2 §3) |
| Pooling: max/avg (supporting) | NB1 §1, §4 (max pool in blocks, global average pool as embedding) |
| Image data embeddings (supporting) | NB1 §4 (global-avg-pool vector); NB2 §1, §6 (ResNet/CLIP embedding spaces) |
| Pre-trained Vision Encoders, e.g. ResNet (Practice) | NB2 §1, §4 |
| Model Finetuning (supporting, Practice) | NB2 §5 (frozen linear probe vs full finetune) |
| Vision-text encoders, e.g. CLIP (Practice) | NB2 §6 |
| Transformers / attention / patching (supporting theory for ViT) | NB2 §6 (CLIP's ViT image encoder explained) |

Other syllabus vision topics (object detection — YOLO/SSD/DETR, segmentation — U-Net,
GANs, self-supervised learning, diffusion models) are **not** in these two notebooks;
NB2 §7 points out how the pretrained-encoder ideas here carry into them.

## How to run — locally

```bash
# 1. Create an environment (any Python 3.10+ works)
python -m venv .venv && source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 2. Install dependencies (CPU-only PyTorch shown; drop the index-url if you have a GPU)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install matplotlib scikit-learn transformers pillow jupyter

# 3. Launch
jupyter notebook        # then open the .ipynb files and Run All
```

Notes:
- Datasets download into `./data/` next to the notebooks (CIFAR-10, ~170 MB, downloaded once and shared by both notebooks).
- CLIP weights (~600 MB) are cached by Hugging Face under `~/.cache/huggingface/`.
- **No internet?** Both notebooks contain a clearly marked fallback: CIFAR-10 is replaced by `torchvision.datasets.FakeData` (random noise) so everything still executes — accuracies will sit near 10% chance, which is expected. NB2 falls back to random ResNet weights and skips the CLIP demo if those downloads fail.

## How to run — Google Colab (recommended if your laptop is slow)

1. Go to [colab.research.google.com](https://colab.research.google.com) → **File → Upload notebook** → pick the `.ipynb`.
2. (Optional but nice) **Runtime → Change runtime type → T4 GPU.** The notebooks auto-detect CUDA and run several times faster; no code changes needed.
3. Colab already ships `torch`, `torchvision`, `matplotlib`, `scikit-learn`, and `transformers` — just **Runtime → Run all**. If an import ever fails, run `!pip install transformers scikit-learn` in a new top cell.
4. Colab VMs are wiped between sessions, so the CIFAR/CLIP downloads repeat each session (they're quick on Colab's connection).

## Reproducibility & knobs

- Everything is seeded (`SEED = 42`); reruns give the same numbers (tiny nondeterminism in low-level libraries can shift accuracy by a fraction of a percent).
- Want better accuracy and have time/GPU? Increase `N_TRAIN`, `EPOCHS`, and (NB2) the resize resolution — each is a single clearly named constant near the top of the data/training cells.
