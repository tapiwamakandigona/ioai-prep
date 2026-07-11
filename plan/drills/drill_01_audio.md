# DRILL 1 — Home Task 1: "Operation Night Watch" (audio, 16 → 29 classes)

**Time box: 45 min. No studying. Follow the play, submit to Kaggle, log your score.**

> Status: ✅ **VALIDATED 2026-07-11** — all prompts (P1–P5) tested live against **Gemma 4 (`gemma-4-31b-it`)** via the free Gemini API. Every prompt produced correct, working code (head surgery, replay sampling, dual-LR optimizer, split-accuracy eval, submission writer — all right on the first try). See "Validation notes" at the bottom for the two quirks that matter.

## What the task is (30-second version)
You get a trained 16-class audio classifier (AST) + data for 13 new classes. Make one model that classifies all **29** classes. Score = ½·(accuracy on old) + ½·(accuracy on new) — forgetting old classes costs as much as failing new ones. Training budget ≈ 10 GPU-minutes.

## Setup check (do once, ~1 min)
1. Tab 1: [aistudio.google.com](https://aistudio.google.com) → log in → model dropdown → **Gemma 4** (the free API exposes `gemma-4-31b-it` and `gemma-4-26b-a4b-it` — same family as the GAITE contest bot, better practice than Gemma 3).
2. Tab 2: open the task notebook in Colab (from [kaggle.com/competitions/ioai-2026-home-task-1](https://www.kaggle.com/competitions/ioai-2026-home-task-1)) → Runtime → T4 GPU.
3. Run the baseline cells top to bottom until the "baseline score" cell prints. **Write that number down.**

## The play (one chat = one job; always end prompts with "Code only, max 30 lines. Reply with ONLY a single python code block — no explanation, no reasoning, no bullet points.")

> ⚠️ **Why the extra suffix:** Gemma 4 "thinks out loud" — it writes pages of bullet-point reasoning before the code. In the contest, replies are capped at 2000 tokens, so on longer asks (like P3) the rambling can eat the whole budget and **cut off the code**. The suffix keeps replies tight. If a reply still gets truncated mid-code, just say: "Continue the code from the last line." or re-ask with "shorter".

**P0 — Briefing (paste once at the top of every new chat):**
> I'm working in a Colab notebook. I have a Hugging Face `ASTForAudioClassification` checkpoint trained on 16 audio classes, loaded from a local folder. I must extend it to 29 classes (16 old + 13 new) and fine-tune on ~10 GPU minutes without forgetting the old classes. Data: `train.csv` (old classes) and `fine_tune.csv` (new classes), columns include filepath, target, split. Metric: mean of old-class accuracy and new-class accuracy.

**P1 — Grow the head:**
> Write code that replaces the model's 16-output classifier head with a 29-output head, copying the original 16 rows of weights and bias into the first 16 outputs and randomly initializing the rest. Code only, max 30 lines.

**P2 — Combined dataset:**
> Write a PyTorch Dataset that loads both CSVs' train splits into one dataframe, loads each audio file with librosa at 16 kHz, and returns the AST feature extractor's output plus the integer label. Code only, max 30 lines.

**P3 — Training loop with replay:**
> Write a training loop (AdamW, lr 1e-5 for the encoder and 1e-3 for the head, ~3 epochs, batch size 8) over a mix of ALL new-class training clips and an equal number of randomly sampled old-class clips per epoch, so the model learns new classes without forgetting old ones. Code only, max 30 lines.

**P4 — Score it:**
> Write evaluation code that predicts on the val splits of both CSVs and prints accuracy on old classes (targets 0–15), accuracy on new classes (targets 16–28), and their mean. Code only, max 30 lines.

**P5 — Kaggle submission:**
> Write code that runs the model on every filepath listed in the Kaggle `submission.csv`, writes the predicted class index into its target column, and saves it. Code only, max 30 lines.
> *(Kaggle version has NO val split — you predict straight on submission.csv paths.)*

## Recovery moves (when something breaks)
1. **Any error** → new message: paste the FULL traceback + the failing cell. "Fix this. Code only."
2. **Shape/size mismatch** → add: "The model expects input shape X; my batch is shape Y" (print both first).
3. **CUDA out of memory** → "Rewrite with batch size 4 and gradient accumulation of 2. Code only."
4. **Training too slow for 10 min** → "Freeze all encoder layers except the last 2 blocks. Code only."
5. **Score too low** → paste your P4 numbers: "Old acc X, new acc Y. Give me ONE change to improve the weaker side. Code only."

## Known traps (from official Discord — don't burn time on these)
- Classes 3/7 (cow vs sheep) and 11/15 (thunderstorm vs rain) have **label noise** — some errors there are not your fault.
- 20 submissions/day limit. Community score to beat: **~87%**.
- New classes have only 24–60 clips each — replay mixing (P3) is the whole game.

## Validation notes (Viktor, 2026-07-11 — live run against `gemma-4-31b-it`)
- **All 5 prompts produced correct code.** Highlights: P1 did proper weight-slicing head surgery (`new.weight[:16] = old.weight`) and remembered `model.config.num_labels = 29`; P3 got the dual learning rates and per-epoch replay sampling right; P4 masked old/new accuracy exactly as the metric demands.
- **Quirk 1 — rambling:** without the "ONLY a single code block" suffix, P3's reply hit the 2000-token cap mid-code. The suffix (now baked into the play above) is mandatory.
- **Quirk 2 — flaky API:** the free API threw intermittent HTTP 500s. Not your prompt's fault — just resend. In the actual contest UI this shouldn't apply, but if the chatbot errors, retry before rewording.
- One thing to watch: Gemma sometimes assumes `processor`/`train_df` already exist. If a snippet references an undefined variable, ask: "Define X too. Code only."

## Log it (2 min, in this file's table or DM Viktor)
| Date | Baseline score | Your score | Kaggle LB | What broke | Prompts that saved you |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
