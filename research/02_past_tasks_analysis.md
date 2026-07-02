# Past Tasks Analysis — What IOAI/GAITE Actually Asks

> Analyzed from https://github.com/IOAI-official/IOAI-2025 (full statements, baselines, official solutions),
> IOAI 2024 archives, and https://github.com/open-cu/awesome-ioai-tasks.

## IOAI 2025 — every task, decoded

### At-Home Round (these repeat as Day-1 extensions!)
| Task | Domain | What it really tests |
|---|---|---|
| **Chameleon** | NLP/Multimodal | Word-guessing game: given an ordered sequence of icons (with text descriptions), predict the secret word. Tests **embeddings + semantic similarity** (sentence-transformers, CLIP-style thinking). |
| **Radar** | CV/Signals | Detect humans in radar heatmaps (static + dynamic range-azimuth maps). Really an **image classification/detection on non-photo images** problem. Tests CNN skills + handling weird data. |
| **Weather** | CV/Tabular hybrid | Predict rain from GOES-16 satellite images + context features (sun angle, time, location). Tests **combining image encoders with tabular features**. |

### Individual Contest Day 1 (extensions of at-home)
| Task | Domain | What it really tests |
|---|---|---|
| **Radar (v2)** | CV | Same domain, new twist. Reuse of at-home pipeline. |
| **Weather-related task** | CV/Tabular | Extension of at-home version. |
| **Concepts** (Chameleon extension) | NLP + LLM | Now *generate* hints / harder guessing, with an **official LLM API proxy allowed** ($10 credits, 12,500 judge calls). Tests prompt engineering + embeddings. |

### Individual Contest Day 2 (novel tasks)
| Task | Domain | What it really tests |
|---|---|---|
| **Antique** | Classical ML | Semi-supervised tabular classification: 5 features, labels 1/-1/0(unknown), 500 samples. Tests **scikit-learn, semi-supervised tricks, label propagation, careful validation**. Tiny data — no deep learning needed! |
| **Chicken Counting** | CV | Density-estimation counting: frozen pretrained encoder provided, you **design + train the decoder**. Tests PyTorch model surgery. |
| **Restroom** | CV/Metric learning | Match male↔female restroom icons from the same restroom. Tests **image embeddings + similarity matching** (metric learning idea). |
| **Pixel** | CV | Pick the most informative pixels per image (masking under a budget). Tests creative thinking + model probing. |

### GAITE 2025 extra tasks
| Task | Domain | What it really tests |
|---|---|---|
| **Word Segmentation** | NLP | Split German compound words (binary label per character). 94k training examples. A **character-level sequence labeling** problem — solvable with a simple LSTM/transformer or even clever classical approaches. |
| **Synthetic Speech Detector** | Audio-as-CV | Detect AI-generated speech from **Mel spectrograms** (given as tensors). The task statement literally says: treat it as image classification, ResNet18 is enough, ~1 epoch. |

### IOAI 2024 (1st edition, Bulgaria)
- ML: feature engineering for a *fixed* model on matrix-shaped samples (they choose the model, you make the features).
- NLP: fine-tune a language model on ciphered text of an unknown language; later extend the classifier to more classes.
- CV: edit SDXL-mini weights so "giraffe" prompts make zebras (and later: make a hydrant appear alongside cows) — **model-editing / weight surgery**.

## Patterns — what this competition IS
1. **Every task ships with a baseline notebook.** Your job is to *improve* the baseline, not build from scratch. Reading + modifying existing PyTorch/sklearn code is THE core skill.
2. **Small-to-medium data, short training budgets** (e.g., 20-min scoring limits). Clever > big. 1–3 training epochs typical.
3. **Recurring themes:**
   - Embeddings + cosine similarity (Chameleon, Restroom, Concepts) — appears in some form almost every year
   - Image classification with a small CNN / ResNet (Radar, Speech Detector, Weather)
   - Tabular ML with scikit-learn/gradient boosting (Antique, Tricky Table, Kazakhstan TST clustering)
   - "Weird data as images" (spectrograms, radar heatmaps, satellite bands)
   - Sequence labeling / simple NLP (Word Segmentation, masked word position)
   - Model surgery: freeze encoder, train head; repair/edit weights (Chicken Counting, Broken BERT, SDXL editing)
4. **Hints are written into GAITE statements** ("use ResNet18", "1 epoch is enough", "don't obsess over the metric"). READ THE STATEMENT TWICE. The organizers tell you the intended solution.
5. **Submission mechanics matter:** notebooks that must run in ~20 min, produce specific CSV/zip formats, limited submission counts (e.g., 50), choose-2-for-final-score. Practicing the *mechanics* is free points; format errors are the #1 beginner killer.
6. Scoring is normalized against baseline → **any improvement over baseline scores points**. Never submit nothing.

## What this means for a beginner with 30 days
- You do NOT need: theory-heavy math, building transformers from scratch, TensorFlow, reinforcement learning, big-model training.
- You DO need, in priority order:
  1. Python + numpy/pandas fluency (read/manipulate data without fear)
  2. scikit-learn workflow: fit/predict, train/val split, metrics (accuracy, F1, AUC)
  3. PyTorch training loop literacy: Dataset/DataLoader, nn.Module, loss, optimizer, epochs — enough to *modify* a baseline
  4. Transfer learning recipe: load pretrained ResNet/BERT-like encoder, freeze, replace head, fine-tune
  5. Embeddings + cosine similarity with sentence-transformers / vision encoders
  6. Submission discipline: producing exactly the required file format, fast
- Practice targets (all free, all in awesome-ioai-tasks):
  - IOAI 2025 At-Home: Chameleon, Radar, Weather (run in Colab/Kaggle)
  - GAITE 2025: Word Segmentation, Synthetic Speech Detector
  - Antique (great sklearn practice)
  - NEOAI 2025 Kaggle comps (Tricky Table, Underfitting CV, Cluster Pictures)
  - Kazakhstan TST solutions repo: https://github.com/batyrq (the host country's own selection tasks!)
