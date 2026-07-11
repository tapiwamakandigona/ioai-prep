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
- You can typically only see your own score during the contest.

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
- GAITE: **Gemma 4, max 2000 output tokens per query**, integrated into the platform. Unlimited new chats (per current info; exact rate limits/quotas announced before the contest).
- ❌ No external LLMs, copilots, browser assistants, AI coding agents, or APIs (unless a task explicitly allows it — e.g., IOAI 2025 "Concepts" task had an official LLM proxy).

### Allowed websites (whitelist, expected)
python.org · pypi.org · numpy.org · pandas.pydata.org · scikit-learn.org · pytorch.org · matplotlib.org · scipy.org · **huggingface.co/docs** (+ docs for other provided tools)
- No Stack Overflow, no GitHub, no arXiv, no Google-anything. **Gemma 4 is effectively your Stack Overflow.**

## Rules that can get you disqualified (memorize)
- No communication with anyone during contests; phones/devices surrendered the night before each contest day.
- No pre-trained models or external data unless the task statement allows it.
- No tampering with scoring, no trying to access test data.

## Sources
- Official rules PDF (v4, June 2026) — primary source
- https://ioai-official.org/republic-of-kazakhstan/2026-contest-rules/
- https://ioai-official.org/gaite/
- https://en.wikipedia.org/wiki/International_Olympiad_in_Artificial_Intelligence
- https://github.com/IOAI-official/IOAI-2025 (all 2025 tasks + solutions)
- https://github.com/open-cu/awesome-ioai-tasks (task collection across countries)
