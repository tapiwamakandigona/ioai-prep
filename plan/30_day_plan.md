# 30-Day Zero-to-GAITE Plan — v2, baseline-first (July 3 → Aug 1, 2026)

**Who this is for:** zero coding experience, zero AI background, competing in GAITE at IOAI 2026 (Astana, Aug 2–8).

## Why v2? Two facts change everything
1. **Every IOAI task ships a runnable baseline.** You will never start from a blank cell. Contest day begins with working code that already scores points.
2. **Gemma 4 writes code for you** (2000-token replies, unlimited chats). You will never need to author code — you need to *read, assemble, verify, and direct*.

So the plan is no longer "learn to code, then apply it." It trains **one loop** on progressively harder baselines:

> **The Baseline Improvement Loop (BIL)** — the only drill that matters:
> 1. Run the baseline untouched → confirm the score / submission format
> 2. Understand every cell (LLM explains, you re-explain in your own words)
> 3. Diagnose: *where* are points lost? (confusion matrix, failed cases, per-class accuracy)
> 4. Ask Gemma for ONE targeted change (chunked, ≤~30 lines, code only)
> 5. Verify (read it → tiny slice → shapes) → run → measure → keep or revert
> 6. Repeat 3–5

**The two skills you're actually training:** (a) *diagnosis* — spotting where a baseline loses points; (b) *Gemma-driving* — extracting correct code in small pieces and verifying it. Python/PyTorch literacy exists only to serve those two.

**Daily rhythm (4–6 focused hours):**
- Every session is LLM-paired **under contest rules from Day 1**: one chat = one job, ask in chunks ("code only, max 30 lines"), pretend replies are capped at 2000 tokens, verify by running. By August this is muscle memory.
- ~50% running/modifying baselines, ~30% LLM-paired reading & prompting, ~20% journal + snippets file (`plan/snippets.md`) — anything you looked up twice goes in.
- Everything in **Kaggle Notebooks or Colab** (Kaggle hosts the official At-Home round).

---

## Week 1 (Days 1–7): Read code before you write code
Goal: read an unfamiliar notebook and explain every cell — not author one.

- **Day 1 — Demystification day.** Create Kaggle account. Open a finished Titanic notebook, press "Run All", watch it work. Then open the **real 2026 Night Watch baseline** (IOAI-official/IOAI-2026, Colab-ready) and run it untouched, top to bottom. You understand nothing yet — that's fine. Lesson: *the baseline already works; contest day starts from here.*
- **Day 2 — Python by interrogation I.** Variables, lists, loops, `if/else` — learned by pasting cells from the Titanic notebook into an LLM chat: "explain this line by line for a beginner." Then Kaggle Learn Python lessons 1–3 to consolidate. Exercise: change 5 things in the notebook and *predict* each outcome before running.
- **Day 3 — Python by interrogation II.** Functions, dictionaries, imports, try/except, and the skill of **reading a traceback bottom-up**. Break the notebook on purpose 5 ways; for each, read the traceback, then ask the LLM for the minimal fix. Kaggle Python lessons 4–7.
- **Day 4 — numpy + the shape ritual.** Arrays, indexing, `mean/sum/argmax`, reshaping. **Shapes are the #1 debugging skill.** Ritual to make automatic: `print(x.shape)` after every operation. Exercise: 3×224×224 fake image → normalize → per-channel means, narrating shapes at each step.
- **Day 5 — pandas I.** `read_csv`, `head/describe`, selection, filtering (Kaggle Learn Pandas). Exercise: answer 5 questions about Titanic — first ask Gemma-style ("code only") for each, read the answer, run it, explain it back.
- **Day 6 — pandas II + matplotlib.** groupby, missing values, hist/scatter. Exercise: survival by class/sex plots, same ask→read→run→explain rhythm.
- **Day 7 — Checkpoint.** Take an *unseen* Kaggle starter notebook. Explain every cell in your own words (LLM verifies). Make 3 modifications with predicted outcomes. ✅ Pass = you never froze; you knew *what to ask*.

## Week 2 (Days 8–14): The sklearn improvement loop
Goal: run the full BIL on tabular baselines. This alone scores points (see Antique, IOAI 2025).

- **Day 8 — Metric-first reading + first BIL.** Open Kaggle's Titanic tutorial baseline. Find the metric BEFORE reading anything else. Run → submit → one improvement via a chunked ask. Concepts: features/labels, train/test, overfitting.
- **Day 9 — Metrics.** Accuracy, precision/recall, **F1** (IOAI's favorite), confusion matrix, AUC. The confusion matrix is your main *diagnosis* tool — practice reading one aloud: "the model confuses X for Y, so…"
- **Day 10 — Validation.** `train_test_split`, cross-validation, why single splits lie on small data. Exercise: demonstrate overfitting with a deep vs shallow DecisionTree.
- **Day 11 — The model bake-off.** Ask for a 4-model `cross_val_score` bake-off (LogReg / RandomForest / XGBoost / SVC) in ONE chunked prompt, ≤25 lines. Read it, run it, beat Day-8's score. This exact prompt is in the site's Antique page.
- **Day 12 — Feature engineering as BIL steps.** One-hot, scaling, imputation, 3 new Titanic features — each one = one loop iteration: change → measure → keep/revert. Log every result.
- **Day 13 — Embeddings as a black box + clustering.** sentence-transformers: encode texts, cosine similarity, nearest neighbors — you can USE this without understanding transformers. Plus KMeans/PCA in an hour. (Embeddings + similarity is IOAI's single favorite pattern.)
- **Day 14 — Checkpoint: Antique (IOAI 2025), full BIL.** Baseline on labeled rows → diagnose → bake-off → self-training on the unlabeled rows. Then read the official solution; write down 3 things you'd never have thought of. ✅ Pass = you beat the naive baseline and can say *why*.

## Week 3 (Days 15–21): PyTorch = surgery, not authorship
Goal: modify any training loop with confidence. You assemble Gemma's pieces; you never write a network from scratch.

- **Day 15 — Tensors.** torch ↔ numpy, shapes, `.to('cuda')`. The shape ritual, GPU edition.
- **Day 16 — The sacred training loop, assembled.** `Dataset`/`DataLoader` → `nn.Module` → loss → optimizer → epochs. Get it via 3 chunked asks (data / model / loop), assemble in one notebook, explain each block back. Then type it ONCE from memory — reading fluency, not authorship. This pattern is 90% of every baseline.
- **Day 17 — Surgery drills.** On a CIFAR-10 notebook, perform each with one chunked ask: (a) swap the final layer for a different class count, (b) freeze the backbone (`requires_grad=False` + verify with a param count), (c) change the loss, (d) add class weights. These four moves solve half of IOAI history.
- **Day 18 — Transfer learning (THE recipe).** Pretrained ResNet18 → freeze → replace `fc` → fine-tune on a small image dataset. Directly solves Speech-Detector-style tasks.
- **Day 19 — Training hygiene.** Early stopping, augmentation, LR, save/load `.pth`, plus the two wiring tests: overfit-10-samples, tiny-slice-first.
- **Day 20 — Embeddings + similarity, contest edition.** Build mini-Chameleon: encode descriptions, cosine-match to words. Add the Hungarian-algorithm one-liner (`linear_sum_assignment`) for matching tasks.
- **Day 21 — Checkpoint: Speech Detector (GAITE 2025) in <2 hours, contest rules.** Its own statement says ResNet18, ~1 epoch. All code from the baseline or chunked asks — none hand-authored. ✅ Pass = under 2h with a valid submission.

## Week 4 (Days 22–28): THE REAL 2026 HOME TASKS + full dress rehearsal
> Contest Day 1 extends these three tasks (see `research/04_2026_home_tasks_deep_dive.md`).
> **Hard rule from here:** only whitelisted docs sites + one LLM chat with self-imposed 2000-token discipline. Every line of code comes from the baseline or from Gemma — you only read, assemble, verify, and measure.

- **Days 22–23 — Night Watch** (audio continual learning). Day 22: full BIL pass — reproduce the baseline score, *watch catastrophic forgetting happen* by naive fine-tuning, read the confusion matrix. Day 23: head expansion 16→29 (copy old weights), experience-replay ratios, optional LoRA via peft.
- **Day 24 — Robot Delivery** (behavioral cloning). Baseline MLP → replay failed episodes → the notebook's own hints: CNN on the 6×8×8 grid, oversample rare pickup/dropoff, apply the action mask in training.
- **Day 25 — John Wilkins** (LLM 20-questions). Mostly logic: precompute the animal×question table (free!), greedy information-gain, soft-downweighting for noisy answers.
- **Day 26 — FULL 6-HOUR MOCK.** 3 unseen 2025 tasks (Restroom, Chicken Counting, Radar). Score honestly: something submitted for all 3? Baselines submitted in the first 30 min each? Where did time vanish?
- **Day 27 — Mock post-mortem.** Read official 2025 solutions. Grow the snippets file. Update your personal prompt bank with the asks that worked.
- **Day 28 — Second pass on your weakest 2026 task.** Squeeze more score; note open questions for your team leader.

## Final stretch (Days 29–30 + travel)
- **Day 29 —** All three 2026 submissions in exact required formats (zip/jsonl/csv). Reread `research/05_solution_flow.md`.
- **Day 30 —** Reread the rules + Gemma playbook + snippets. Sleep. No new theory.
- **On-site practice session:** learn Yandex Contest + JupyterLab; immediately probe how the real Gemma 4 chat behaves at the 2000-token limit.

---

## Priority triage (if you fall behind)
Never cut: the BIL checkpoints (Days 14, 21), surgery drills (17–18), the three 2026 tasks (22–25), the mock (26). First to cut: unsupervised extras (13, second half), second passes.

## Weekly milestones (honest self-check)
- ✅ W1: I can read an unfamiliar notebook, explain every cell (with LLM help), and I've already run a real 2026 baseline.
- ✅ W2: Given a tabular baseline, I can run the full improvement loop and beat it — and say why the improvement worked.
- ✅ W3: I can do model surgery (head swap, freeze, transfer recipe) using only chunked Gemma-style asks.
- ✅ W4: In a 6-hour mock I produce 3 valid submissions, each beating baseline, with zero hand-authored code.

## Resources (all free)
- Kaggle Learn: Python, Pandas, Intro to ML — used as consolidation, not as the spine
- pytorch.org/tutorials + scikit-learn.org user guide + huggingface.co/docs — all on the contest whitelist; practice *navigating* them now
- IOAI-official repos (2024/2025/2026) — every baseline and solution
- github.com/open-cu/awesome-ioai-tasks + Kazakhstan's TST tasks (github.com/batyrq)
