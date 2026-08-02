# Day-2 wildcard archetypes — the gaps the free-wins table didn't cover (2026-08-02)

> Built by cross-referencing every task in [open-cu/awesome-ioai-tasks](https://github.com/open-cu/awesome-ioai-tasks)
> (all years, all national selections) against the 8 live-verified archetypes in
> `research/12_gemma_prompt_pack.md`. Day 1 extends the home tasks (covered). **Day 2 is
> "novel tasks"** — these are the recurring families across IOAI 2024/2025, NEOAI, JOAI,
> Polish/Romanian/Kazakh olympiads that could show up and are NOT yet in the free-wins table.
>
> ✅ Status: **all 6 recipes live-tested against the real E4B bot on 2026-08-02** (zwe101
> round, doc 16) — every returned cell executed locally. 3 of 6 needed the pack's recovery
> moves (P4/P5/fresh-chat) to reach a working cell; all 6 ended verified. Drive them with
> P3 exactly like the free wins, and expect the recovery loop to be part of the play.

## The 6 uncovered families (frequency-ordered)

### 1. Text classification / AI-text detection (very frequent)
Seen: NEOAI "Evading AI-Generated Text Detection", Romania nationals "human vs AI text",
China NOAI news classification, code-difficulty classification (Kazakhstan TST day 3).
**Recipe:** `TfidfVectorizer(ngram_range=(1,2), min_df=2)` → `LogisticRegression(C=1.0, max_iter=1000)`.
Char n-grams (`analyzer="char_wb", ngram_range=(2,5)`) beat word n-grams for AI-text detection
and short/noisy text. If a provided BERT-family model exists, mean-pool its embeddings →
LogisticRegression before considering fine-tuning (20-min budget!).

### 2. Model repair / weight surgery (IOAI signature move)
Seen: NEOAI "Broken BERT" (corrupted embeddings), IOAI 2024 SDXL zebra↔giraffe weight editing,
2025 Chicken Counting (design a decoder on a frozen encoder), planted-bug baselines (Eastern round A).
**Recipe:** diff against a reference: compare `state_dict()` tensors (shape, mean, std, norm) between
broken and healthy checkpoints; the corrupted module is a statistical outlier. Fix by copying healthy
weights / re-initializing only the broken rows. For "add a capability" surgery: new `nn.Linear`, copy
old rows, train only the new parts. (Same pattern as the T1 head expansion free win — generalize it.)

### 3. Segmentation (rising: 2 of the last 3 Polish editions + NEOAI)
Seen: NEOAI "Cuties Segmentation", Poland 2026 "Multispectral Segmentation".
**Recipe:** per-pixel classification. Small data → classical: flatten per-pixel features
(all channels + neighborhood stats) → LightGBM/LogisticRegression. Deep path: provided
segmentation model or frozen encoder + 1×1 conv decoder head, 1–3 epochs. Metric is usually
IoU/Dice — optimize the threshold on validation predictions (free ~2–5 points, one line).

### 4. Time series / regression (JOAI 2026 is literally this)
Seen: JOAI 2026 lever-position from brain activity, China NOAI pendulum motion (missing points).
**Recipe:** lag/rolling features (`shift(1..k)`, rolling mean/std per channel) → LightGBM/Ridge.
Never shuffle-split time series — split by time. For missing-point interpolation: fit on observed
index → predict missing (`scipy.interpolate` or Ridge on polynomial features often suffices).

### 5. Feature engineering for a fixed model (IOAI 2024's whole ML track)
Seen: IOAI 2024 at-home + on-site ML (model is fixed, you craft features), NEOAI "Tricky Table".
**Recipe:** you can't touch the model, so points live in: aggregations per group (mean/std/min/max),
ratios & differences of correlated columns, datetime decomposition, target encoding (fit on train
folds only), and for matrix-shaped samples: row/col means, stds, SVD top-k components. One feature
family per P3/P5 iteration, measure, revert if not better.

### 6. Multimodal fusion (JOAI 2025 gold-medal pattern, Weather 2025, France 2026)
Seen: JOAI 2025 (sensor table + image + text), IOAI 2025 Weather (satellite image + tabular),
France OFIA 2026 ("Où est Spy-C?" tabular + images).
**Recipe:** late fusion, always: get a vector per modality (frozen encoder embeddings for
image/text, raw or engineered features for tabular), `np.hstack` them, one LightGBM/LogReg on top.
Never train a joint deep model under a 20-min budget. If one modality dominates on validation,
drop the others — simpler transfers better to hidden set B.

## Families checked and consciously NOT added
- **Audio classification** → already covered: spectrogram = image ("X as an image" pattern).
- **Counting/density** → covered by model-surgery recipe #2 (frozen encoder + trainable decoder).
- **Adversarial attacks / quantization / pruning (Poland stage 1)** → rare outside Poland, low
  expected value for GAITE; skip.
- **RL** → officially out (Task 2 ruling: supervised only; syllabus keeps RL "aware-only").
- **Generative practical round (album covers)** → 2024-only format, replaced by Team Challenge.

## How to use on Day 2 (30 seconds per task)
1. Name the family (the 8 free wins + these 6 cover every task in awesome-ioai-tasks since 2024).
2. Paste the family's recipe line into P3 as "{the improvement}".
3. If the task fits nothing → it's a thinking task (Wilkins/Pixel style): find the budget +
   the metric, precompute what's free, spend the budget greedily on information gain.
