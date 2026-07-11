# IOAI 2026 / GAITE — Competition Intelligence

> Compiled July 2026 from the official IOAI 2026 Contest Rules + Technical Appendix v4 (June 2026),
> ioai-official.org, Wikipedia, and the IOAI-official GitHub repos. All facts below are verified against
> the official rules PDF: https://ioai-official.org/wp-content/uploads/2026/06/IOAI2026-Contest-Rules-and-Tehnical-Appendix.pdf

## The event
- **What:** International Olympiad in Artificial Intelligence (IOAI), 3rd edition
- **Where/when:** Astana, Kazakhstan, **August 2–8, 2026** (relocated from Abu Dhabi)
- **Host:** Competitive Programming Federation of Kazakhstan (CPFED)
- **Contests:** Individual Contest, Team Challenge, and **GAITE Contest**

## What GAITE actually is (this is your contest)
- GAITE = **Global AI Talent Empowerment** — a special version of the Individual Contest for countries newer to science olympiads.
- **Same tasks, same days, same 6-hour duration** as Individual Contest Day 1 and Day 2.
- Differences that work in your favor:
  1. **You get hints** with the tasks.
  2. **More LLM support: Gemma 4 with up to 2000 output tokens per query** (Individual contestants only get Gemma 3 with 1000 tokens).
  3. **Separate scoreboard** — you're only ranked against other GAITE participants, and score normalization uses the *top GAITE score*, not the top IOAI score.
- Awards: GAITE Level One/Two/Three Awards with the same 1/12, 1/4, 1/2 cutoff logic as gold/silver/bronze. Top ~50% of GAITE participants get an award. **Realistic goal: an award is genuinely achievable.**

## Contest structure
| Stage | What | When |
|---|---|---|
| At-Home Round | 3 problems, educational, doesn't count. **LIVE NOW:** [GitHub](https://github.com/IOAI-official/IOAI-2026/tree/main/Home%20Task) since Jun 30; Tasks 1–2 on Kaggle since Jul 7 ([Audio Classifier](https://www.kaggle.com/t/5fccd4b322b345b39210b52eeabf9df9), [Robot Delivery](https://www.kaggle.com/t/06b232bc145b47c78022bcd0c53231c9), 20 subs/day); Task 3 is interactive → local only | now → Aug 2 |
| Practice session | Familiarize with contest hall/system | on-site, before Day 1 |
| Contest Day 1 | 3 tasks, each connected to an at-home task, **6 hours** | on-site |
| Contest Day 2 | 3 novel tasks, **6 hours** | on-site |
| Team Challenge | separate team event, all teams participate | on-site |

**Huge implication:** Half the contest (Day 1) is *extensions of the at-home tasks*. If you master the 3 at-home problems inside-out before arriving, you walk into Day 1 already knowing half the exam.

## Scoring (how to think about points)
- Each task = max 100 points, may have subtasks. Score is normalized:
  `Norm = (your_score − baseline_score) / (max_score − baseline_score) × 100`
- `max_score` = max(0.9 × committee solution, best contestant submission) — **on the GAITE scoreboard, best GAITE submission**.
- **Beating the baseline at all already puts you on the board.** Every small improvement counts. Never leave a task at 0 — always submit at least a modified baseline.
- **Live scoreboard (Scoreboard A):** you see your own score on the *validation* set, PLUS the baseline `Min_Score` AND the anonymous `Max_Submission` (highest unnormalized score by anyone, live, per task). Use `Max_Submission` for triage: if the top score on a task is barely above baseline, small gains there are worth a lot of normalized points.
- **Official scores come from Scoreboard B** — your *final* solution re-evaluated on a hidden **test** set after the contest ends. Medals/awards use ONLY Scoreboard B. ⚠️ Don't burn hours overfitting the live validation leaderboard; simple robust improvements transfer, leaderboard-chasing hacks often don't.
- **Evaluation limits (Tech Appendix §6):** submitted notebook must run in **max 20 minutes** per task (unless the statement says otherwise); **max 60 submissions per task**; concurrent submissions get queued. Plan "train small/fast" — no giant training runs inside the graded notebook. 60 subs ≈ 10/hour: submit early and often.
- **Clarifications must be Yes/No questions**; the committee may refuse to answer and will point you to the dataset/baseline first. Paste confusing statements to Gemma for interpretation before burning a clarification.

## Contest environment (Technical Appendix v4)
- Platform: **Yandex Contest system** for statements/datasets/submissions; **JupyterLab** in the browser is the main dev environment (this is where the GPU lives).
- Laptops run **Ubuntu**, no local GPU; VSCode available offline as an editor.
- **Python 3.13**, pinned package versions (published before the contest).
- GPU: slice of an NVIDIA H200 (MIG), **18 GB VRAM** — decent, but you must manage batch size/model size.
- Pretrained models: **only organizer-provided, pre-cached models**. No downloading models. Docs available via Hugging Face docs pages.

### Available libraries (learn ONLY these)
- **Core AI/ML:** torch, torchvision, torchaudio, transformers, accelerate, peft, trl, scikit-learn, xgboost, lightgbm, catboost, sentence-transformers, datasets, evaluate, spacy, nltk, gensim, fasttext
- **Data:** numpy, pandas, scipy, polars, pyarrow, h5py
- **CV:** opencv-python, Pillow, scikit-image, albumentations
- **Viz:** matplotlib, seaborn, plotly
- **Utils:** tqdm, joblib, tensorboard, pytorch-lightning, pydantic, pyyaml
- ❌ **NO TensorFlow/Keras. NO pip install during contest. No AutoML/hyperparameter-tuning libs.**

### LLM access
- GAITE: **Gemma 4, max 2000 output tokens per query**, integrated into the platform. ⚠️ Chat/rate quotas are NOT specified anywhere official — the rules only say "exact model, context window, rate limits, and usage quotas will be announced before the contest." Confirm at the obligatory Aug 3 practice round; have a fallback style (fewer, denser chats) in case quotas are tight.
- ❌ No external LLMs, copilots, browser assistants, AI coding agents, or APIs (unless a task explicitly allows it — e.g., IOAI 2025 "Concepts" task had an official LLM proxy).

### Allowed websites (whitelist, expected)
python.org · pypi.org · numpy.org · pandas.pydata.org · scikit-learn.org · pytorch.org · matplotlib.org · scipy.org · **huggingface.co/docs** (+ docs for other provided tools)
- No Stack Overflow, no GitHub, no arXiv, no Google-anything. **Gemma 4 is effectively your Stack Overflow.**

## Rules that can get you disqualified (memorize)
- No communication with anyone during contests. **No devices in the contest hall** (computers, phones, earphones, calculators…).
- **But: no quarantine before the contest** — you keep your phone/laptop the evening and morning before each contest day (rules PDF §2.4: "There is no quarantine for the contestants before the contest"). Use that time to review your at-home task notes and Gemma prompt bank right up to the hall door. (Quarantine only applies to team leaders/observers in the translation session.)
- No pre-trained models or external data unless the task statement allows it.
- No tampering with scoring, no trying to access test data.

## Key schedule facts (official schedule page)
- **Aug 3, 07:30–09:30: Practice Round — OBLIGATORY.** Your one chance to test the Gemma chat UI + JupyterLab, confirm chat quotas and how the "final solution" is designated, and request your own keyboard/mouse (allowed on request; external monitor is not).
- **Aug 3, 14:00–19:00: Team Challenge Round 1 ("Simulation")** — same day as the practice round; Aug 3 is packed.
- **Aug 3, 14:00–15:00: GAITE Meeting.**
- **Aug 4 & Aug 6, 09:00–15:00: GAITE/Individual Contest Days 1 & 2** (6 hours confirmed).
- **Aug 7, 09:00–12:00: Team Challenge Final** (top 10 teams, at Alem.ai).

## Sources
- Official rules PDF (v4, June 2026) — primary source
- https://ioai-official.org/republic-of-kazakhstan/2026-contest-rules/
- https://ioai-official.org/gaite/
- https://en.wikipedia.org/wiki/International_Olympiad_in_Artificial_Intelligence
- https://github.com/IOAI-official/IOAI-2025 (all 2025 tasks + solutions)
- https://github.com/open-cu/awesome-ioai-tasks (task collection across countries)
