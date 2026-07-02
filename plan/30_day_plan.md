# 30-Day Zero-to-GAITE Plan (July 3 → Aug 1, 2026)

**Who this is for:** zero coding experience, zero AI background, competing in GAITE at IOAI 2026 (Astana, Aug 2–8).
**Philosophy:** You are not becoming an AI researcher in 30 days. You are becoming someone who can *read a baseline notebook, understand it, improve it, and submit correctly* — with Gemma 4 as your assistant. That is exactly what GAITE rewards.

**Daily rhythm (aim for 4–6 focused hours/day):**
- 60% hands-on coding (typing, not watching)
- 25% chatting with an LLM as your tutor (see `research/03_gemma4_playbook.md`)
- 15% reviewing/journaling: keep a `notes/` file per day with what you learned + code snippets you want to reuse

**Non-negotiable rule:** everything happens in **Kaggle Notebooks or Google Colab** (free GPU, and Kaggle is the official At-Home platform for IOAI 2026 — you MUST be comfortable there).

---

## Week 1 (Days 1–7): Python + data handling — the survival kit
Goal: read and write basic Python without panic; slice data with numpy/pandas.

- **Day 1 — Setup + Python basics I.** Create Kaggle account, run your first notebook. Learn: variables, numbers, strings, lists, `print`. Resource: Kaggle Learn "Python" course (lessons 1–3). Exercise: FizzBuzz, sum a list, reverse a string — write them yourself, then ask the LLM to critique.
- **Day 2 — Python basics II.** Loops, `if/else`, functions, dictionaries. Kaggle Python course lessons 4–7. Exercise: write a function that counts word frequencies in a sentence.
- **Day 3 — Python basics III.** Reading files, imports, list comprehensions, try/except (you'll need it to read tracebacks). Exercise: load a `.csv` by hand with the `csv` module, then never do that again.
- **Day 4 — numpy.** Arrays, shapes, indexing/slicing, `mean/sum/argmax`, reshaping. **Shapes are the #1 thing.** Exercise: create a 3×224×224 fake "image", normalize it to [0,1], compute per-channel means.
- **Day 5 — pandas I.** DataFrames, `read_csv`, `head/describe`, column selection, filtering. Kaggle Learn "Pandas". Exercise: load Titanic dataset on Kaggle, answer 5 questions about it.
- **Day 6 — pandas II + matplotlib.** groupby, sorting, missing values (`fillna`), simple plots (hist, scatter). Exercise: plot survival rate by class/sex on Titanic.
- **Day 7 — Checkpoint.** Redo everything without looking at notes. Take Kaggle's Titanic "Getting Started" and just *explore* the data. Journal: write (in your own words) what a train/test split is.

## Week 2 (Days 8–14): Classical ML with scikit-learn
Goal: the full ML workflow — fit, predict, evaluate, improve — on tabular data. This alone can score points (see the "Antique" task, IOAI 2025).

- **Day 8 — The ML idea + first model.** Concepts: features/labels, train vs test, overfitting. Code: `LogisticRegression` on Titanic; make a real Kaggle submission. Kaggle Learn "Intro to Machine Learning".
- **Day 9 — Metrics.** Accuracy, precision/recall, **F1** (IOAI's favorite), confusion matrix, AUC. Exercise: compute each by hand on a tiny example, then with `sklearn.metrics`.
- **Day 10 — Validation.** `train_test_split`, cross-validation, why you NEVER evaluate on training data. Exercise: show overfitting by training a deep DecisionTree vs a shallow one.
- **Day 11 — Tree ensembles.** RandomForest, then **XGBoost/LightGBM** (contest-available!). Exercise: beat your Day-8 Titanic score.
- **Day 12 — Feature engineering + preprocessing.** One-hot encoding, normalization/standardization, imputation. This was an entire IOAI 2024 task. Exercise: engineer 3 new Titanic features, measure the gain.
- **Day 13 — Unsupervised.** KMeans, PCA (+ what t-SNE plots mean). Exercise: cluster the Iris dataset, visualize with PCA. (Kazakhstan's own TST had a clustering task!)
- **Day 14 — Checkpoint: real olympiad task.** Solve **Antique** (IOAI 2025, tabular semi-supervised) from the IOAI-official repo. Just try: train on labeled rows, predict the rest. Then read the official solution and write down 3 things you'd never have thought of.

## Week 3 (Days 15–21): PyTorch + deep learning — baseline-modification bootcamp
Goal: not "build networks from scratch" but *understand and modify a training loop*. Resource: pytorch.org "60 Minute Blitz" + "Training a Classifier" tutorial (allowed website!).

- **Day 15 — Tensors.** torch tensors ↔ numpy, shapes, `.to('cuda')`, GPU vs CPU. Exercise: matrix multiply on GPU in Colab.
- **Day 16 — The training loop (the sacred pattern).** `Dataset`/`DataLoader` → `nn.Module` → loss → optimizer → epoch loop. Type it out 3 times from memory for a tiny MLP on synthetic data. This pattern is 90% of every baseline notebook.
- **Day 17 — Your first image classifier.** CNN on MNIST or CIFAR-10 with torchvision. Concepts: convolution (intuition only), ReLU, pooling, softmax, cross-entropy.
- **Day 18 — Transfer learning (THE recipe).** Load pretrained ResNet18, freeze backbone, replace `fc` head, fine-tune on a small dataset. This *directly* solves Synthetic-Speech-Detector-style tasks. Exercise: fine-tune ResNet18 on a small Kaggle image dataset.
- **Day 19 — Fighting overfitting + training hygiene.** Early stopping, data augmentation (torchvision transforms / albumentations), learning rate, Adam vs SGD, saving/loading `.pth`. Exercise: add augmentation + early stopping to Day 18.
- **Day 20 — Embeddings + similarity (IOAI's favorite trick).** sentence-transformers: encode texts, cosine similarity, nearest-neighbor search. Exercise: build a mini "guess the word from a description" system — this is literally Chameleon.
- **Day 21 — Checkpoint: real olympiad task.** Solve **GAITE 2025 Synthetic Speech Detector** (spectrogram classification — it's just images!). Follow its own hints: ResNet18, few epochs. Then read the reference solution.

## Week 4 (Days 22–28): Contest simulation — past tasks under real conditions
Goal: speed, submission discipline, LLM-driving under constraints. From now on: **impose contest rules on yourself** (only docs websites + one LLM chat, chunked answers).

- **Day 22 — At-Home task 1: Chameleon** (IOAI 2025). Time-boxed 4h: read statement → summarize with LLM → run baseline → one improvement → produce submission file.
- **Day 23 — At-Home task 2: Radar.** Same drill. Radar heatmaps = images; reuse Week-3 recipes.
- **Day 24 — At-Home task 3: Weather.** Same drill. Image + tabular features combined.
- **Day 25 — GAITE Word Segmentation** (char-level sequence labeling) OR a NEOAI Kaggle task (Tricky Table / Underfitting CV). Pick your weakest area.
- **Day 26 — FULL 6-HOUR MOCK, Day-1 style.** 3 tasks (pick 3 you haven't fully solved: e.g., Restroom, Chicken Counting, a NEOAI task). Score yourself: did you submit *something* for all 3? Where did time vanish?
- **Day 27 — Review the mock.** Read official solutions for all 3. Build your personal **snippets file** (`plan/snippets.md`): training loop, transfer-learning recipe, CSV submission writer, early stopping, embedding similarity — code you can retype fast.
- **Day 28 — Audio + odd data types day.** Mel spectrograms (librosa concept, torchaudio), treating signals as images, padding variable-length sequences. Skim: what Whisper/HuBERT are (names appear in the 2026 syllabus).

## Final stretch (Days 29–30 + travel)
- **Day 29 — 2026 At-Home Round.** The real at-home tasks are released ~1 month before the contest — **ask your team leader for them TODAY if you don't have them yet**; they are the direct basis of Contest Day 1. Work them seriously; ask Gemma/LLM to explain every line of their baselines.
- **Day 30 — Light review + logistics.** Reread `research/01_competition_intel.md` (rules!), your snippets file, and the Gemma playbook. Sleep. Do not cram new theory.
- **On-site practice session:** use it to learn the Yandex Contest platform + JupyterLab + how the Gemma 4 chat behaves (test the 2000-token limit immediately).

---

## Priority triage (if you fall behind)
Cut in this order — LAST to cut is first priority:
1. ~~Audio day (28)~~ → 2. ~~Unsupervised (13)~~ → 3. ~~Word segmentation (25)~~ → … but **never cut**: the training-loop days (16–18), embeddings (20), scikit-learn workflow (8–11), and the mock contest (26).

## Resources (all free)
- Kaggle Learn: Python, Pandas, Intro to ML, Intro to Deep Learning — short, hands-on
- pytorch.org/tutorials — official, and it's on the contest whitelist so learn to navigate it now
- scikit-learn.org user guide — same, whitelisted
- IOAI-official/IOAI-2025 GitHub repo — every task + solution
- github.com/open-cu/awesome-ioai-tasks — more practice tasks incl. Kazakhstan's own selection tasks (github.com/batyrq)
- huggingface.co/docs — whitelisted during contest; practice finding things in it

## Weekly milestones (honest self-check)
- ✅ W1: I can load a CSV and answer questions about it with pandas.
- ✅ W2: I can train + evaluate a scikit-learn/XGBoost model and make a correct Kaggle submission.
- ✅ W3: I can take a PyTorch baseline, explain each block, and fine-tune a pretrained ResNet.
- ✅ W4: In 6 hours I can produce valid submissions for 3 unseen tasks, each beating baseline.
