# The Copy-Paste Prompt Pack — contest day with zero coding knowledge

> Written 2026-07-29 after reviewing the actual zwe104 chat history with the
> Gemma 4 E4B assistant from the Eastern Practice Round. Every rule below fixes
> a mistake that actually happened in those chats. This is the *cram sheet*:
> memorize the RULES, save the PROMPTS somewhere you can copy from.

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

## The assistant's real limits (verified live)

| Limit | Value | Consequence |
|---|---|---|
| Reply length | ~2,000 tokens | ask for one short cell at a time |
| Your message | 2,000 chars | paste long statements in parts ("say Noted") |
| Memory | last 10 messages only | re-paste code/problem when it gets confused |
| Rate | 60 msgs/hour | ≈20 per problem — never waste one on "thanks" |

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

**P3 — the workhorse: rewrite ONE cell**
```
Rewrite this exact notebook cell with ONE change: {the improvement}.
Rules: reply with ONLY the complete new cell in a single python code block,
max 50 lines, runnable as-is, keep the same variable names and output format,
use ONLY these libraries: {allowed}. My current cell:
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
Check this notebook code and answer PASS or FAIL for each point, one line each:
1) It never modifies/rotates/adds noise to test data before predicting.
2) It reads dataset/test_public/ dynamically and never assumes answers.json
   exists there.
3) It writes {output file} in the working directory, one entry per test row.
4) It uses no library outside {allowed} and never needs internet.
Code:
{paste all cells}
```

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
- **Always** submit the baseline before improving. **Never** chase the live
  leaderboard (set A); the final score is hidden set B — prefer safe, simple
  improvements.

## The submit ritual (memorize)

Run All Cells → output file exists → Git tab → stage `solution.ipynb` →
Commit → Push → contest page → **Check** → wait 5–9 min → score visible in
Submissions. If the last submission is broken, fix and resubmit — assume the
latest one counts.
