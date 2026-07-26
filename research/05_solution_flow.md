# The Universal IOAI Task Anatomy & Solution Flow

> Result of a code-level pass over ALL baseline notebooks in github.com/IOAI-official:
> IOAI-2024 (Help_BOBAI, Lost_in_Hyperspace, Madarian_Cow), IOAI-2025 (all 11 tasks incl. GAITE), IOAI-2026 (3 home tasks).
> They are strikingly similar. Learn the skeleton once and every task becomes familiar.

## Every IOAI notebook has the same 8 sections
| # | Section | What it looks like | What YOU do with it |
|---|---|---|---|
| 1 | Story + task statement | Cute narrative wrapper (chickens, robots, Borges) | Strip the story. Extract: input → output → metric → constraints. 4 bullet points. |
| 2 | Data download | `gdown`/`load_from_disk`/Kaggle mount, fixed folder layout | Just run it. Never modify. |
| 3 | Data exploration | `df.head()`, plots, audio players, sample images | Actually look. Class imbalance, sizes, weirdness = where points hide. |
| 4 | Provided model/baseline | A `Dataset` class, a small model, a training loop | **Read every line.** The baseline's stated limitations are a literal TODO list of improvements. |
| 5 | Metric function | Exact scoring code, e.g. `competition_score()`, F1, success-rate | Read this FIRST (before the story even). The metric defines the game — e.g. 2026 Task 1's 50/50 old/new weighting changes everything. |
| 6 | "Your mission" + hints | Numbered suggested paths (GAITE versions have even more) | The organizers tell you the intended solution. Follow it before inventing your own. |
| 7 | Submission writer | Produces `submission.csv` / `predictions.jsonl` / zip | Run early. Submit the plain baseline first — points on the board + format verified. |
| 8 | Constraints | Time limits (~20 min scoring), submission caps (~50), no internet | Plan experiments around them. |

## The 8-step solution flow (the "thinking" you asked about)
This is the flow that outweighs syntax knowledge. Memorize it as a checklist:

1. **Metric first.** Find the scoring cell. What exactly is measured? Any weighting/penalty (e.g. −0.02/query)? Optimize *that*, nothing else.
2. **Run the baseline untouched → submit it.** Confirms environment + format, and any score > 0 beats an empty submission (scores are normalized against baseline).
3. **Diagnose before improving.** Confusion matrix / failed-episode replays / per-class accuracy. Ask: *where* does the baseline lose points? (Gemma prompt: "Given this confusion matrix, which 2 fixes give the most points?")
4. **Read the hints; rank improvements by points-per-hour.** GAITE statements literally contain the intended approach ("use ResNet18", "mix in old clips", "pick the question that splits candidates in half").
5. **One change at a time, measure each.** Change two things at once and you learn nothing. Keep a scrappy log: change → score.
6. **Respect the failure mode the task is *about*.** Every task is secretly a lesson: 2026-T1 = catastrophic forgetting, 2026-T2 = distribution drift (action accuracy ≠ episode success), 2026-T3 = information gain + noisy oracle, Antique = unlabeled data, Pixel = what CNNs attend to. Name the lesson → you know the solution family.
7. **Guard the clock.** ~30 min per task to a submitted baseline; stop experimenting 45 min before the end; verify your best 2 submissions are selected and formats are valid.
8. **Never leave a task at zero.**

## Honest answer: is "flow > coding" true?
**~70% true, with a dangerous 30%.**

**Where you're right:** Gemma 4 can write any code you need. The scarce skill on contest day is exactly what's above: extracting the metric, diagnosing failure modes, ranking improvements, managing time. Past GAITE hints show the organizers *want* to hand you the "how"; they're testing whether you can execute the "what/why". Two contestants with the same Gemma access are separated by their questions, not their typing.

**Where the 30% bites:**
1. **You can't ask about what you can't read.** To prompt "fix my replay ratio," you must first *find* the training loop in the baseline and understand what it does. Code reading is non-optional.
2. **The 2000-token cap means assembly.** Gemma gives you fragments; you must know where each fragment plugs into the notebook, which variables exist, and what shapes flow between cells.
3. **Gemma is confidently wrong sometimes.** If you can't run-on-a-tiny-slice, print shapes, and read a traceback, one hallucinated argument costs you an hour.
4. **Latency.** Trivial edits (change a path, a hyperparameter, a loop range) must be instant finger-memory, or you burn your 6 hours on round trips to the chatbot.

**So the target skill level is: code *literacy*, not code *authorship*.** You must read and modify PyTorch/sklearn confidently; you almost never need to write from a blank cell. That's exactly what the 30-day plan trains — and why Weeks 1–3 can't be skipped, but also why they stop at literacy instead of going deeper into theory.

## Cross-year similarities worth knowing (fast pattern-recognition on contest day)
- **"X as an image":** spectrograms (2025 GAITE speech, 2026 audio), radar heatmaps, satellite bands → CNN/ViT recipes transfer across all of them.
- **"Frozen encoder, trainable head":** Chicken Counting (2025), AST head expansion (2026), Help_BOBAI (2024). Model surgery on the last layer is a yearly ritual.
- **"Embeddings + similarity":** Chameleon/Concepts/Restroom (2025), Lost in Hyperspace (2024). sentence-transformers + cosine similarity.
- **"LLM as a component with a budget":** Concepts' judge API (2025, 12.5k calls), Wilkins' oracle (2026, 15 questions). Pattern: precompute/simulate offline for free, spend the budget adaptively, be robust to noise.
- **"The baseline's disclaimer is the answer key":** every year, the listed limitations of the baseline are the intended improvements.
