# The Copy-Paste Prompt Pack — contest day with zero coding knowledge

> Written 2026-07-29 after reviewing the actual zwe104 chat history with the
> Gemma 4 E4B assistant from the Eastern Practice Round. Every rule below fixes
> a mistake that actually happened in those chats. This is the *cram sheet*:
> memorize the RULES, save the PROMPTS somewhere you can copy from.
>
> **v3 (2026-07-30):** live-tested against all five remaining task archetypes
> (docs 13 + 14). Four new failure modes found and covered; P3/P4 hardened;
> free-wins table extended to eight archetypes.

## What went wrong in the practice-round chats (so we never repeat it)

Reviewed all 8 chats on `chat.ioai2026.kz`. The recurring failure modes:

1. **Truncated code.** Replies are capped (~2,000 tokens). Asking for "the
   improved solution" produced code cut off mid-line; three "continue" messages
   later the pieces didn't fit together. → Ask for **one cell at a time**.
2. **NameError from partial cells.** Ran a "modified CELL 2" without re-running
   CELL 1, got `NameError: name 'TRAIN' is not defined`. → After ANY change:
   **Run → Run All Cells**, always.
3. **Wrong problem in the wrong chat.** Problem B's baseline was pasted into
   the clustering (C) chat; the model called it out but wasted 2 messages.
   → **One chat per problem**, check the title before pasting.
4. **Banned suggestions.** The model proposed CNNs, PyTorch, `pip install
   Pillow` — all impossible (allowed libs only, no internet). → Every code
   prompt must end with the allowed-libraries line.
5. **The augmentation trap.** It suggested *rotating images inside `load_X`* —
   which also corrupts the TEST images at predict time. This exact bug is what
   the shipped baseline planted. → Hard rule: **never modify test data**.
6. **Vague improvement loops.** "give improved v2" without pasting the current
   code/score → model drifted to GMM/PCA that changed nothing. → Always paste
   current code + current score, ask for **ONE** change.

Found in the 2026-07-30 archetype tests (doc 14):

7. **Silent spec changes.** Asked for a CNN on a 6-channel grid; it wrote
   `Conv2d(1, 32, ...)` with a comment "assuming 1 channel" — crashes on real
   data. → After P3, check every NUMBER you specified appears in the reply.
8. **Mock-data injection.** "runnable as-is" made it invent a fake `train`
   and a line that silently replaces real labels with zeros. → P3/P4 now
   forbid mock data; still delete any "mock/example" lines before pasting.
9. **Deprecated APIs.** It wrote `df.append(...)` (removed in pandas 2.x).
   → Crash is fine: P4 with the full traceback fixed it first try.
10. **Runs-but-wrong.** It packed context chars into one list value; the code
   ran without error but scored F1 0.66 instead of 1.00. → No traceback to
   paste. Only defense: compare the self-score after EVERY change, revert if
   not better.
11. **Stray `python` first line** when copying code from the chat UI — it's
   part of the fence, not the code. Delete it or you get a SyntaxError.
12. **P7 false PASS on the test-data trap** (found 2026-08-02, zwe101 round): fed
   a cell that visibly rotates test images at predict time, P7 quoted the
   offending line and called it PASS — while correctly failing the banned
   import. → P7 is trustworthy for mechanical checks (imports, output file)
   only. **The "never modify test data" check is YOURS**: before every submit,
   personally scan for rotate/noise/augment/random near anything test. 30 s.

## The assistant's real limits (verified live)

| Limit | Value | Consequence |
|---|---|---|
| Reply length | ~2,000 tokens | ask for one short cell at a time |
| Your message | 2,000 chars | paste long statements in parts ("say Noted") |
| Memory | last 10 messages only | re-paste code/problem when it gets confused |
| Rate | 60 msgs/hour | ≈20 per problem — never waste one on "thanks" |

**Hard rule #0 — ALWAYS paste, NEVER reference.** Live-tested: saying "check
the same code again" without re-pasting it made the model invent a completely
different problem (GPS distances!) and return garbage code — even though the
code was still inside its 10-message window. Every single prompt that talks
about code must contain the code, pasted fresh. No "the code above", no "the
same cell", no "it".

## The game plan (same 7 steps, every problem)

1. Open the problem, read it once. Open its JupyterLab via the **Server** button.
2. **New chat** in the assistant. One chat = one problem.
3. Feed it the problem + baseline with **P1** (paste in <2,000-char parts).
4. **Submit the baseline untouched first**: Run All Cells → Git: stage
   `solution.ipynb` → Commit → Push → contest page → **Check**. Points on the
   board before any improvement. Verify the score appears under Submissions
   (grading takes 5–9 min).
5. Ask for the plan (**P2**), then apply ONE improvement via **P3**.
6. Run All Cells → compare self-score → keep if better, revert if not.
   Errors → **P4**. Cut-off reply → **P6**. Two failed fixes → new chat.
7. Before final push, run the safety check (**P7**). Then commit → push → Check.

## The prompts (fill the {braces}, paste, send)

**P1 — feed the problem (multi-part paste)**
```
I am in a coding contest. I will paste the problem statement and the baseline
notebook code in several parts. Reply only "Noted." until I write DONE.
```
…paste parts… then:
```
DONE. Summarize in 5 short bullets: the input data, the exact output file I
must write, the scoring metric, the allowed libraries, and the one thing most
likely to go wrong.
```

**P2 — get the plan (no code yet)**
```
List the 3 changes to this baseline most likely to improve the score, ordered
by impact. Use ONLY these libraries: {allowed}. No code yet, max 80 words.
```
⚠️ **P2's #1 suggestion can be the trap.** Live-tested: for the digit problem
the model's top suggestion was "data augmentation (rotations, flips)" — the
exact planted bug. Before acting on ANY P2 suggestion, check it against the
**Free wins** list and the hard rules below. If P2 says augment/rotate/modify
images or data: ignore it. The Free wins list always outranks P2.

**P3 — the workhorse: rewrite ONE cell**
```
Rewrite this exact notebook cell with ONE change: {the improvement}.
Rules: reply with ONLY the complete new cell in a single python code block,
max 50 lines, keep the same variable names and output format, assume all
variables and data already exist — do NOT create mock, example, or
placeholder data. Use ONLY these libraries: {allowed}. My current cell:
{paste the cell}
```

**P4 — fix an error**
```
My notebook cell crashed. Reply with ONLY the complete corrected cell in one
python code block, no explanation. Use ONLY these libraries: {allowed}.
The cell:
{paste the cell}
The full error:
{paste the whole red traceback}
```

**P5 — improve the score**
```
My current self-score is {X}. Here is the code that produced it:
{paste the key cells}
Suggest the ONE change most likely to raise the score and reply with only the
complete modified cell. Do not change the output file name or format. Do not
modify or augment the test data. Use ONLY: {allowed}.
```

**P6 — reply got cut off**
```
Your code block was cut off. Continue EXACTLY from this line, code only,
do not repeat anything before it:
{paste the last complete line}
```

**P7 — pre-submit safety check**
```
Check this notebook code against 4 points. For EACH point reply on its own
line in exactly this format: "<point number>) PASS or FAIL — <quote the one
code line that decides it>".
1) It never modifies/rotates/adds noise to test data before predicting.
2) It reads dataset/test_public/ dynamically and never assumes answers.json
   exists there.
3) It writes {output file} in the working directory, one entry per test row.
4) It uses no library outside {allowed} and never needs internet.
Code:
{paste all cells}
```
(Live-tested: without the strict per-line format the model answered
"FAIL FAIL FAIL FAIL" on one line — useless. The quoted code line forces it
to point at the actual problem. ⚠️ 2026-08-02: P7 gave a **false PASS on point 1**
while quoting the very line that rotated the test images — trust P7 on
imports/format only; check test-data modification with your own eyes.)

**P8 — explain (when lost)**
```
Explain what this cell does in max 5 simple sentences for a beginner: {paste}
```

## Free wins to cram (the recurring archetypes)

- **Clustering, features on different scales** → `StandardScaler` **before**
  `KMeans(n_clusters=K, n_init=10, random_state=0)`. One line, took ARI
  0.56 → 1.00 in practice. Say the word "StandardScaler" in your P3 prompt.
- **Small-image classification, sklearn only** → pixels scaled to 0–1, then
  `SVC(kernel="rbf", C=10)`. Beat LogisticRegression 0.65 → ~0.84. Do NOT
  augment/rotate anything for tiny 8×8 images.
- **Interactive/oracle task** → run the shipped baseline as-is first; heavy
  work belongs in `__init__`/precompute; ask questions that split remaining
  candidates ~50/50; never eliminate a candidate on one mismatched answer.
- **Continual learning** (old classes + new classes, score averages both) →
  expand the classifier head: new `Linear(768, old+new)`, copy the old rows of
  weights/bias in, AND replay — `pd.concat` a slice of the ORIGINAL train.csv
  into the fine-tune data. Never fine-tune on the new classes alone.
- **Behavioral cloning on grid observations** → CNN on the grid (keep ALL its
  channels!) + concatenate the state vector, class weights = 1/bincount for
  rare actions, set invalid-action logits to -1e9 in the training loss.
  Never BFS/A*/planning — supervised on the demonstrations only.
- **Match two sets of embeddings 1:1** → L2-normalize, cosine similarity
  matrix, `scipy.optimize.linear_sum_assignment(-sims)`. Never greedy argmax
  (it double-assigns). Live-tested: 100% on noisy pairs.
- **Semi-supervised tabular** (some rows labeled, predict the rest) →
  StandardScaler fit on labeled rows → LogisticRegression → predict unknown
  rows in their original order. Tested: 0.98 vs 0.90 unscaled.
- **Char-level sequence labeling** (word segmentation) → context-window
  features with ONE dict key per offset (`c-3`…`c+3`, `#` when out of range)
  → DictVectorizer → LogisticRegression. One key per offset matters: a single
  list-valued key runs fine but scores F1 0.66 instead of 1.00.
- **Always** submit the baseline before improving. **Never** chase the live
  leaderboard (set A); the final score is hidden set B — prefer safe, simple
  improvements.

## The submit ritual (memorize)

Run All Cells → output file exists → Git tab → stage `solution.ipynb` →
Commit → Push → contest page → **Check** → wait 5–9 min → score visible in
Submissions. If the last submission is broken, fix and resubmit — assume the
latest one counts.
