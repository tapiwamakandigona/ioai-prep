# 🚨 THE ACTUAL IOAI 2026 AT-HOME TASKS — Deep Dive

> Found in https://github.com/IOAI-official/IOAI-2026 (`Home Task/` folder). These are the real
> 2026 At-Home Round notebooks. **Contest Day 1's three tasks will each connect to one of these.**
> Working these three notebooks until you understand every cell is the single highest-value prep activity that exists.

All three run in Google Colab (badges included; data auto-downloads from Google Drive via `gdown`).

---

## Home Task 1 — "Operation Night Watch" (Audio, continual learning)
**Story:** A deployed audio classifier (Audio Spectrogram Transformer, AST) knows 16 sound classes. Teach it 13 new classes (chainsaws, gunshots, 4 insect species…) **without forgetting the old 16**.

- **Model:** AST (`ASTForAudioClassification` from transformers) — treats audio like an image: waveform → 128-band log-mel spectrogram → 16×16 patches → 12 transformer layers → linear head. ~86M-param encoder + tiny linear head.
- **Data:** 5s mono 16kHz wavs; `train.csv` (small retained subset of old 16 classes), `fine_tune.csv` (13 new classes, imbalanced: 24–60 clips/class).
- **Metric:** `Score = ½·Acc_old + ½·Acc_new` on a hidden 29-class test set. The 50/50 weighting is the whole game: a model that nails the new classes but forgets the old ones scores ~nothing.
- **The concept being taught: catastrophic forgetting.** Naive fine-tuning on new data destroys old classes "within a few hundred steps."
- **Stated solution paths (the hints ARE the syllabus):**
  1. **Expand the head** 16 → 29 outputs (copy old weights into new head).
  2. **Experience replay:** mix old clips into fine-tuning batches (tune the ratio).
  3. **Knowledge distillation** against the frozen original model.
  4. **Freeze or LoRA** parts of the encoder; per-module learning rates (peft is in the contest library list — not a coincidence).
  5. Diagnose with per-class accuracy, confusion matrices, embeddings (t-SNE), and your ears.
- **Likely Day-1 extension:** same AST/audio setup with a twist — more classes, fewer retained old clips, distribution shift, or stricter compute. Master: loading HF checkpoints, swapping/expanding a classifier head, replay-ratio experiments, confusion-matrix reading.

## Home Task 2 — "Robot Delivery Academy" (Behavioral cloning / imitation learning)
**Story:** A robot on an 8×8 grid must pick up a package at one depot and deliver it to another, learning **from expert demonstrations only** (supervised observation → action). Search/planning algorithms are explicitly forbidden — they want *learning*, not A*.

- **Data:** `train_demos.pkl` trajectories; each step has `grid` (6×8×8 tensor: walls/depots/robot/package/destination/carrying), `vector` (13 features), `action_mask` (6 valid-action flags). Actions: south/north/east/west/pickup/dropoff.
- **Baseline:** flattens the grid + trains a 2-hidden-layer MLP with cross-entropy, 30 epochs. Its stated flaws = your improvement checklist:
  - Flattening destroys spatial structure → **use a small CNN on the 6×8×8 grid** (their own hint).
  - Rare actions (pickup/dropoff) under-learned → class weighting / oversampling.
  - Action mask only used at inference → mask logits during training too.
  - **Key trap:** high per-action accuracy ≠ episode success. One early wrong step compounds (distribution drift). Evaluate with full-episode success rate, replay failed episodes in the provided simulator, categorize failures (before pickup? near walls?).
- **Metric:** episode Success Rate. **Submission:** `predictions.zip` containing `predictions.jsonl` (one JSON per scenario: layout_id, episode_seed, actions list).
- **Likely Day-1 extension:** bigger grids, partial observability, noisy demos, or a "Robot Training" sequel (the notebook literally calls itself the "preparatory program for the Robot Training task").

## Home Task 3 — "The Analytical Language of John Wilkins" (LLM-driven 20 Questions)
**Story (Borges-themed):** A hidden animal sits behind an oracle — a local LLM (**Qwen2.5-3B-Instruct**) that answers yes/no questions about it. Budget: **15 questions** per animal; ~1,400 candidate animals; question pool is fixed (`questions_pool.txt`).

- **Scoring:** `max(0, correct − 0.02 × queries_used)` → guess right in fewer questions = more points.
- **The intended solution (they spell it out):**
  1. **Precompute offline** (free!): run your *own* copy of the same LLM over every (animal, question) pair → a bit-vector table per animal. The oracle is deterministic at temperature 0.
  2. **Adaptive question selection:** keep the set of animals consistent with answers so far; each turn ask the question that **most evenly splits** the remaining candidates (max information gain). Information theory: log₂(1400) ≈ 10.5 bits, so ~11 perfect questions suffice.
  3. **Robustness:** the oracle occasionally answers "wrong" — don't hard-eliminate; use soft scoring so one surprising bit can't kill the true animal.
- **This is a *thinking* task more than an ML task** — binary search + information gain + fault tolerance. Perfect for you.
- **Likely Day-1 extension:** same interactor pattern with a different domain, tighter budget, larger pool, or a noisier oracle.

---

## What the three tasks tell us about IOAI 2026's flavor
1. **Transformers + Hugging Face are front and center** (AST checkpoint, Qwen oracle). Learn: `from_pretrained`, feature extractors, model surgery on heads, `output_hidden_states`.
2. **Themes:** continual learning (forgetting), imitation learning (distribution drift), LLM-as-tool + information theory. All about *understanding failure modes*, not exotic architectures.
3. **Every notebook hands you the baseline, the metric function, the submission writer, and explicit hints.** The exam is: can you read the baseline, see its stated weaknesses, and fix them methodically?
4. Compute stays modest: Colab T4 is enough for all three at home; contest gives you an 18GB H200 slice.
