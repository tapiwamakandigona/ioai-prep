# Prompt pack live test #2 — the other archetypes (2026-07-30)

Round 2 of live testing on `chat.ioai2026.kz` (Gemma 4 E4B). Round 1
(doc 13) covered the three Eastern Practice Round problems. This round
covers the **other task archetypes** from the official IOAI-2026 home tasks
and past-task analysis (docs 02/04), so the pack is proven against every
family we expect on contest day. ~30 messages spent across 6 fresh chats.
Every returned cell was executed locally against synthetic equivalents of
the real data shapes — "ran + scored" below means verified by execution,
not by reading.

## What was tested

| # | Archetype | Source | Prompts used |
|---|---|---|---|
| T1 | Audio continual learning (old 16 + new 13 commands, score = ½·acc_old + ½·acc_new) | Home Task 1 "Night Watch" | P1, P2, P3×2, P4 |
| T2 | Behavioral cloning on grid observations (8×8 robot delivery, episode success rate) | Home Task 2 "Robot Delivery" | P1, P2, P3×2, P7 |
| T3 | Embedding matching (two sets of N embeddings, pair them 1:1) | Restroom/Chameleon family | P1, P3 |
| T4 | Semi-supervised tabular (200 labeled / 300 unknown, mixed feature scales) | Antique family | P1, P2, P3 |
| T5 | Character sequence labeling (compound-word segmentation, char-level F1) | Word Segmentation family | P1, P2, P3, P4 |

## Results per test

### T1 — audio continual learning
- **P1 feed**: clean "Noted." discipline, correct 5-bullet summary; it spotted
  catastrophic forgetting as the main risk unprompted. ✅
- **P2 plan**: **weak** — generic advice (feature engineering, hyperparameters,
  augmentation), never mentioned replay or head expansion. The Free-wins table
  must carry this archetype; P2 will not. ⚠️
- **P3 head expansion** (Linear 768→16 to 768→29, copy old rows): correct final
  code, verified locally (old weights preserved, new shape works). But the code
  was buried in rambling comments and the copied block starts with a stray
  `python` line from the fence rendering. ✅ with cleanup
- **P3 replay** (mix old train.csv into fine-tune set): right concept, but used
  `df.append()` — **removed in pandas 2.x, crashes**. New failure mode:
  deprecated APIs. ⚠️
- **P4 with the AttributeError traceback**: perfect one-line fix
  (`pd.concat([ft_df, train_df], ignore_index=True)`). The P4 loop rescues
  deprecated-API bugs reliably. ✅

### T2 — behavioral cloning (robot delivery)
- **P1 feed**: correct summary; flagged "flattening the grid loses spatial
  info" as top risk — exactly the official hint. ✅
- **P2 plan**: **excellent** — CNN on the grid, class weights for rare
  pickup/dropoff actions, action-mask in training loss. Matches the official
  organizer hints 3-for-3. ✅
- **P3 CNN rewrite**: **spec silently violated.** Asked for Conv2d on the
  (6,8,8) grid, 6→32 channels. Gemma wrote `nn.Conv2d(1, 32, ...)` and a
  comment "assuming grid is 1 channel". Verified locally: **crashes** on real
  (B,6,8,8) input (`expected input to have 1 channels, but got 6`). It even
  wrote its wrong assumption in a comment. New failure mode: **silent spec
  changes** — check the numbers in the reply match the numbers you asked for. ❌→fixable
- **P3 training loop** (class weights via bincount, mask logits to -1e9 before
  loss): ran end-to-end locally, loss decreases. Slow Python loop for masking
  but correct. ✅
- **P7 safety check with a planted A\* planner**: correctly answered
  `1) FAIL — "path = astar(...)"` and also caught the simulator import on
  point 4. The strict per-line format keeps working. ✅

### T3 — embedding matching
- **Best result of the day.** Summary flagged "greedy argmax violates the
  one-to-one constraint" unprompted; plan #1 was Hungarian algorithm
  (`scipy.optimize.linear_sum_assignment`) + cosine normalization; final cell
  was clean, minimal, correct. Verified locally on 60 synthetic noisy pairs:
  **100% matching accuracy** (greedy argmax scores lower under noise). ✅✅

### T4 — semi-supervised tabular
- Summary and plan correct (StandardScaler first — consistent with the
  clustering free win). Final cell: scale on labeled rows, fit
  LogisticRegression, predict the unknown rows in order. Verified locally on
  synthetic data with wildly different feature scales: **0.98 accuracy vs
  0.90 unscaled baseline**. ✅

### T5 — char sequence labeling (the sneakiest failure)
- Summary/plan correct (context window features).
- **P3 rewrite subtly wrong**: asked for separate feature keys `c-3..c+3`;
  Gemma packed all 7 chars into ONE list value `{"c_context": [...]}`.
  DictVectorizer accepts that without error — the code **runs, no crash**, but
  positional information collapses: local test F1 **0.66 vs 1.00** for the
  correct version. This is the worst failure type: no traceback, just a bad
  score. Defense = the existing plan-step "compare self-score, revert if not
  better", plus checking the reply matches what you asked for. ❌→caught by score
- **P4 follow-up** produced the correct per-offset keys (`f"c{offset}"`) —
  but wrapped them in **invented mock data** ("Mock data structures to make
  the code runnable", a fake `train`, and a `y_corrected` line that would
  silently replace real labels with zeros). Pasting that into the notebook
  verbatim would destroy the solution while still running. New failure mode:
  **mock-data injection**. Fixed version verified locally: **F1 1.00** vs
  0.00 single-char baseline. ⚠️→prompt fix added

## New failure modes found (now covered in doc 12 / the PDF)

1. **Silent spec changes** — the model changes your numbers (6 channels → 1)
   and notes the wrong assumption only in a comment. Check that every number
   you specified appears in the reply.
2. **Mock-data injection** — "runnable as-is" pushes it to invent fake
   `train`/labels that overwrite real variables. Fix: P3/P4 now say *"Assume
   all variables already exist; do NOT create mock, example, or placeholder
   data."*
3. **Deprecated APIs** (`df.append`) — code from an old training cut. The P4
   loop with the full traceback fixes these reliably.
4. **Runs-but-wrong** (list-valued dict features) — no crash, silently worse
   score. Only defense: always compare the self-score and revert.
5. **Stray `python` first line** when copying from the chat UI — delete it
   before running, it's a SyntaxError.
6. **P2 is archetype-dependent** — excellent on behavioral cloning, useless on
   continual learning. The Free-wins table outranks P2 in both directions.

## Free wins added to the pack (all live-verified this round)

- **Continual learning**: expand the classifier head (new Linear, copy old
  weights into the first rows) + replay (concat a slice of the ORIGINAL
  train.csv into the fine-tune set with `pd.concat`). Never fine-tune on new
  classes only — the ½·old + ½·new metric punishes forgetting.
- **Behavioral cloning on grids**: CNN on the grid + concat the state vector,
  class weights (1/bincount) for rare actions, mask invalid actions in the
  loss. Never use BFS/A*/planning — supervised on demonstrations only.
- **Matching two embedding sets**: L2-normalize, cosine similarity matrix,
  `linear_sum_assignment(-sims)`. Never greedy argmax.
- **Semi-supervised tabular**: StandardScaler fit on labeled rows →
  LogisticRegression → predict unknowns in original order.
- **Char sequence labeling**: context-window features, one dict key per
  offset (`c-3`…`c+3`, `#` out of range) → DictVectorizer → LogisticRegression.

## Verdict

The pack survives all five archetypes: every failure the assistant produced
was either caught by an existing pack rule (P7 trap check, self-score
comparison, P4 error loop) or is now covered by a new rule / prompt fix in
v3. The P1→P2→P3→P4→P7 loop never derailed; fresh-chat discipline and the
2,000-char limit held. PDF v3 regenerated with all of the above.
