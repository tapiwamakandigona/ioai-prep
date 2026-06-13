# IOAI Prep

Preparation materials for the [International Olympiad in Artificial Intelligence (IOAI)](https://ioai-official.org/) / GAITE competition.

## Contents

| Path | Description |
|------|-------------|
| `ioai_2026_syllabus.md` | Official IOAI 2026 syllabus (extracted from ioai-official.org) |
| `vision-models/` | Vision Models presentation project (see below) |

### Vision Models (`vision-models/`)

| Artifact | Description |
|----------|-------------|
| `vision_models_deck.pdf` | 16-slide presentation (primary artifact) |
| `vision_models_deck.pptx` | Same deck with speaker notes embedded |
| `DECK_CONTENT.md` | Slide-by-slide content + speaker notes + visual descriptions |
| `STUDY_GUIDE.md` | Deep-dive companion + teacher FAQ |
| `notebooks/` | Hands-on teaching notebooks (CNN from scratch, transfer learning + CLIP) |
| `lesson/` | Expanded lesson deck (19 slides) with real-image assets and presenter guide |

All content is scoped strictly to the IOAI 2026 syllabus, Section 3 (Computer Vision) plus supporting deep-learning topics.

## Quick start — running the notebooks

```bash
# 1. Create an environment (Python 3.10+)
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# For CPU-only PyTorch (smaller download):
# pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
# pip install matplotlib scikit-learn transformers pillow jupyter

# 3. Launch
cd vision-models/notebooks
jupyter notebook
```

See [`vision-models/notebooks/README.md`](vision-models/notebooks/README.md) for detailed instructions including Google Colab setup, expected runtimes, and reproducibility notes.

## Requirements

- Python 3.10+
- See `requirements.txt` for pinned dependencies
- Both notebooks are seeded (`SEED = 42`) and run top-to-bottom on CPU without edits
- Graceful offline fallbacks: if dataset/model downloads fail, notebooks substitute synthetic data and still execute

## Repository structure

```
ioai-prep/
├── README.md
├── requirements.txt
├── ioai_2026_syllabus.md
└── vision-models/
    ├── vision_models_deck.pdf / .pptx
    ├── DECK_CONTENT.md
    ├── STUDY_GUIDE.md
    ├── build_deck.py          # generates the PDF deck (WeasyPrint)
    ├── build_pptx.py          # generates the PPTX deck
    ├── lesson/                # expanded lesson deck + assets
    ├── notebooks/
    │   ├── 01_cnn_from_scratch.ipynb
    │   └── 02_transfer_learning_and_clip.ipynb
    └── _build/                # notebook build scripts (dev tooling)
```

## License

Not yet specified. Consider adding a LICENSE file (e.g., MIT or CC BY 4.0 for educational content).
