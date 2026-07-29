# Eastern Practice Round — first-hand walkthrough (solved 2026-07-29)

> Live intel from actually logging into the contest platform and solving all 3
> problems on the **Eastern Practice Round** (GAITE track). This is the concrete
> "what the judge actually looks like and how you submit" that the earlier intel
> files could only describe second-hand. **This round is unscored** (a warm-up;
> does not affect official ranking) — value here is the *process* and the
> reusable solution patterns.

## How the platform is wired

Three layers, don't confuse them:

1. **`chat.ioai2026.kz`** — the **AI-assistant helper only** (Gemma 4 E4B, GAITE
   limits: ~2,000-token replies, last-10-message memory, 2,000-char messages,
   60 msg/hr). Log in with your *contestant ID*. Its `/instructions` page holds
   your **separate contest-platform login** + a link to the real judge.
2. **`contest.app/contests/<id>`** — the **online judge** (Yandex Contest style).
   Separate login (`ioai26-trial-e-<user>` / its own password from the
   instructions page). Shows Problems, per-problem statement, Submissions,
   Messages, and a **countdown timer** (window was 2h30). A left "Server /
   JupyterLab" button opens the coding env for that problem.
3. **`jupyter.contest.app/user/<...>`** — a per-participant **JupyterLab**. The
   "Server" button hits `/hub/token-login?token=<TOKEN>` which logs you in.

### Submission flow (per problem)
1. Edit `solution.ipynb` in JupyterLab so it **reads `dataset/test_public/`
   dynamically and writes its output** (`answers.json` for batch problems, or a
   `MySolution` class for interactive ones).
2. **Git tab → stage `solution.ipynb` → Commit → Push** (each problem is its own
   git repo on `contest.gitlab.yandexcloud.net`).
3. Back on the contest page, click **Check**. The grader pulls your repo,
   **swaps `test_public/` for a hidden set**, re-runs the notebook, scores the
   output, updates the leaderboard.
4. Two hidden splits: `test_leaderboard_a` (live board) and `test_leaderboard_b`
   (final). Per-problem grade **time limits** are short (5–9 min) — keep grade-time
   compute cheap.

### 🔑 Critical rules learned
- **Never hard-code / assume `answers.json` is present** at grade time — read
  whatever files exist. Any leakage attempt is against the honor code.
- The notebook is **re-run from scratch** on hidden data — the *code* is graded,
  not the file you produced locally.
- **No internet inside JupyterLab** (`pip install`, downloads, HF hub all blocked
  at grade time). Only the listed libraries + provided local models.
- Each problem's git repo is independent; commit the **notebook + any artifacts
  it needs** (e.g. a precomputed table). Large binaries go through Git LFS
  automatically.

### ⚙️ Environment facts (this round)
- JupyterLab box had a **GPU (CUDA available)**, 24 CPUs, ~196 GB RAM. Handy for
  precompute, but grade-time limits are short so don't rely on heavy per-row work.
- The Jupyter server's login **token doubles as a REST API token**
  (`Authorization: token <TOKEN>` against `/api/contents`, `/api/kernels`) — you
  can read/write files and run kernels programmatically. Batched **forward-pass
  logit compare** (yes/no) reproduced the oracle LLM's greedy `generate` output
  **100%** and is ~10× faster than generating.

---

## The three problems + winning patterns

These three are archetypes worth drilling — they map onto the recurring IOAI
task families (vision classifier, unsupervised clustering, interactive/deduction).

### A. Digit Recognition (computer vision, sklearn only)
- 8×8 grayscale PNG digits, "rotated and noisy"; write `answers.json = {id: label}`,
  scored by accuracy. Allowed: scikit-learn, numpy, Pillow.
- **Trap in the shipped baseline:** it applied a *random rotation to the test
  images at predict time*, destroying the digit right before classifying it.
  A "data augmentation" line in the wrong place tanks the score.
- **Fix:** don't touch test images. Clean **`SVC(kernel="rbf", C=10)`** on
  pixels normalized to `[0,1]` → **~83.7% local**. (Augmenting *train* with large
  rotations *hurt* — creates 6↔9 ambiguity; KNN underperformed SVM.)
- **Lesson:** augment *training* data, never the evaluation input. Read every
  cell of the baseline before trusting it.

### B. The Analytical Language of John Wilkins (interactive deduction)
- Identify a hidden animal (pool of **1,472**) via yes/no questions (pool of
  **559**), ≤**15** queries/row. Score per row = `max(0, solved − 0.02×queries)`.
- The oracle is a **local Qwen3-0.6B** answering deterministically (greedy,
  thinking disabled). Prompt: *"The animal is: {animal}. Answer yes or no.
  Question: {question}"*, take first word.
- **Intended approach (what scored):** load the *same* model offline and
  **precompute the oracle's yes/no answer** for a curated question subset × all
  animals into a lookup table. Ship the table in the repo. At **grade time load
  the table — no model needed** — and play adaptively:
  - keep a candidate mask over animals;
  - ask the pool question that **most evenly splits** current candidates (max
    information gain);
  - track candidates by **agreement count** (robust: one surprising answer
    doesn't permanently kill the true animal);
  - **guess** when one candidate dominates, in order of (fewest mismatches, then
    a popularity prior).
- Result: **88% solved, ~12 queries avg → 70.8** on the hidden set (≈ the max).
- **Speed trick:** compare `yes`/`no` first-token **logits** in one forward pass
  instead of `.generate()` — identical answers, far faster for building tables.
  A ~56-question × 1,472-animal table took ~a few minutes on the GPU.
- **Lesson for the real contest:** for interactor/deduction tasks, do the
  expensive reasoning **offline in `__init__`/precompute**, keep per-row solve
  cheap, and never let a single noisy oracle bit be fatal.

### C. Customer Segments (unsupervised clustering, sklearn only)
- 800+250 customers, 3 features on **very different scales** (`annual_spend`
  ~500–4500, `visit_freq` ~1–7, `avg_basket` ~10–70); assign 4 segments; scored
  by **Adjusted Rand Index** (relabel-invariant).
- Baseline: **raw KMeans** → dominated by `annual_spend` → ARI ~0.56.
- **Fix (one line):** **`StandardScaler` before `KMeans(4)`** → **ARI = 1.0**.
- **Lesson:** always standardize features before distance-based clustering when
  scales differ. This is the single most common "free win" in these tasks.

---

## Reusable checklist (paste into contest-day notes)
- [ ] Read the *whole* baseline notebook first — look for a planted bug / a
      preprocessing step in the wrong place (see A).
- [ ] Confirm the notebook **reads `test_public/` dynamically** and writes the
      required output; never assume labels are present.
- [ ] Distance/clustering task on mixed-scale features → **StandardScaler first**.
- [ ] Interactive/oracle task → **precompute offline, cheap per-row, tolerate
      noise**, mind the grade-time limit.
- [ ] Test locally, then **Git stage → commit → push → Check**; verify the score
      registered in Submissions.
- [ ] No internet at grade time — everything must be local.
