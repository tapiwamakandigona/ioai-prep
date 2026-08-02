# Drill 04 — Free-Win Radar (trigger words → targeted prompts)

> Created 2026-08-02 after M1 attempt 1. Purpose: train the ONE skill that failed —
> **detecting the free win in the statement and firing a targeted prompt** instead of
> "improve this code". Interactive trainer (use this, it's the actual drill):
> **https://coin-corto-a4a1d3.viktor.page/freewin-radar**
> This file is the offline copy + the paper spotting drill for the flight.

## The method (why the trainer is a quiz, not notes)

1. **Testing beats re-reading** (Rowland 2014 meta-analysis; Karpicke 2025). Reading the
   cram sheet again ≈ nothing sticks. Being forced to retrieve = memory. Expect to miss
   most cards in round 1 — that IS the method working, not you being dumb.
2. **Say the answer out loud before flipping.** "Yeah I kinda know it" is familiarity,
   not memory. Grade honestly; missed cards recycle until got.
3. **Space the rounds** (Cepeda 2008; Kornell 2009 — even 1–2 spaced cycles inside
   3 days beat pure cramming by ~30–40 points): now → tonight before bed → Aug 3 before
   the 07:30 practice → Aug 3 evening → 5-min family-name pass on contest mornings.
4. **Contest day is easier than the drill.** You train free recall; the exam only needs
   *recognition* of trigger words sitting in the statement. Overtrained on purpose.
5. Silly hooks (grandpa at dinner, Hungarian wedding) are dual-coded — they surface
   under stress when dry facts don't.

## The radar table (memorize cue → family; the recipe lives in the cram sheet)

| Trigger words in the statement | Family | The one move |
|---|---|---|
| "already recognizes N classes… score averages old and new" | Continual learning | expand head, COPY old rows, REPLAY old data; acc_old=0.00 ⇒ dead |
| "expert demonstrations… grid… action mask… planning forbidden" | Behavioral cloning | CNN on full grid + vector; class weights; mask logits −1e9; judge by episode success |
| "at most N questions… penalty per query… oracle sometimes wrong" | Oracle/budget | precompute offline free; ask 50/50 splitters; soft scores, never hard-eliminate |
| weighting inside the metric cell | Metric-first | the weighting IS the game; print both sides after every change |
| "the baseline does not… / this simple approach…" | Disclaimer = answer key | its confessions are the ordered TODO list |
| numbered "you may want to…" hints | Hints = intended path | execute in order before inventing |
| cluster + features in different units | Clustering | **StandardScaler** before KMeans(n_init=10) |
| tiny images, sklearn-only | Small-image | pixels 0–1 → SVC(rbf, C=10); NEVER augment |
| "match each X to exactly one Y" | Assignment | cosine sims → linear_sum_assignment; never greedy argmax |
| "only some rows labeled" | Semi-supervised | Scaler fit on labeled → LogReg → predict rest in original order |
| "label each character / restore boundaries" | Seq labeling | window features, ONE key per offset → DictVectorizer → LogReg |
| "human vs AI text / classify texts" | Text clf | TF-IDF char_wb (2,5) → LogReg |
| "corrupted model + healthy reference" | Weight surgery | diff state_dicts stats; fix the outlier module only |
| "label every pixel" | Segmentation | per-pixel features → LightGBM, or frozen encoder + 1×1 conv; TUNE the threshold |
| "predict future from readings over time" | Time series | lag + rolling features → LightGBM/Ridge; split BY TIME |
| "you may not modify the model" | Feature engineering | aggregations, ratios, datetime, target-enc (folds), SVD; one family per lap |
| "image + table + text per sample" | Multimodal | late fusion: hstack embeddings → one LogReg |
| P2 suggests augment/rotate | ⚠️ TRAP | free-wins list outranks P2; test data is sacred; P7 false-PASSes this |

Reflexes (violated in M1 attempt 1 — drill until automatic): metric→run→**submit baseline**
first · after a plan: "implement step 1, minimal diff, keep signatures" · errors = goal
line + cell + full traceback · reject oversized rewrites · green cells lie, only the
self-score tells truth · 2 failed fixes → fresh chat · always re-paste, never "the code
above" · closing ritual: Run All → personal test-data scan → commit → push → Check.

## Paper spotting drill (transfer test — do after 2 trainer rounds)

Cover the answer key. For each statement: underline triggers, name the family, write
the exact P3 ask. Then check.

**S1.** *"The observatory's classifier knows 10 star types. Astronomers discovered 5 new
ones (only ~30 examples each). Your score is the mean of accuracy on known and new types.
Note: the provided baseline fine-tunes on the new types only, which may degrade
performance on known types."*

**S2.** *"One of 800 components is faulty. Query the diagnostic tool with yes/no checks
from the provided list — max 10 queries, −0.03 points each. The tool misreports ~5% of
the time."*

**S3.** *"Predict next-hour air quality from a photo of the station surroundings plus the
last 48 hours of sensor readings. You may not retrain the provided image encoder."*

<details><summary>Answer key</summary>

- **S1:** triggers = *knows 10 / 5 new / mean of known-and-new / baseline fine-tunes on new only*.
  Family: continual learning + the disclaimer is the answer key. Moves: submit baseline →
  head 10→15 copying old rows → replay old data → per-side accuracies. Bonus trigger:
  ~30 examples each = imbalance → class weights.
- **S2:** triggers = *max 10 queries / −0.03 each / misreports 5%*. Family: oracle/budget.
  Moves: precompute all (component, check) pairs offline; 50/50 splitters; soft scoring
  (one mismatch never eliminates); stop when expected gain < 0.03.
- **S3:** triggers = *over time (48h) / photo + table / encoder fixed*. Family: time series
  + multimodal late fusion. Moves: lag/rolling features from the 48h; frozen-encoder
  embedding of the photo; hstack → LightGBM/Ridge; split by time; if the photo adds
  nothing on validation, drop it.
</details>

## Log

| Date | Round | First-try score | Notes |
|---|---|---|---|
| | | | |
