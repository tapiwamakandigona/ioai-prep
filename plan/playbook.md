# THE PLAYBOOK — one page, memorize it

> Every line here was **validated live against Gemma 4 (`gemma-4-31b-it`)** across drills 1–3 and the real Kaggle Task-1 run (val 93.5%, LB 0.80773). **Re-validated 2026-07-22 against the REAL contest bot (Gemma 4 E4B on chat.ioai2026.kz)** — everything carries over, plus the E4B amendments at the bottom. This is the cheat sheet for self-practice AND contest day. Practice it until you can do it without looking.

## The two magic strings (append/prepend to EVERY prompt)

**THE SUFFIX** — ends every prompt, no exceptions:
> Code only, max 30 lines. Reply with ONLY a single python code block — no explanation, no reasoning, no draft versions, no bullet points.

**THE OPENER** — prepend when the ask needs any thinking (algorithms, multi-step logic):
> Answer immediately with code — do not deliberate, do not analyze, do not restate the context.

*Why: the 2000-token cap counts Gemma's hidden thinking. Without these, long asks come back truncated mid-code or completely empty.*

## The 10 prompt templates

**T1 — Briefing (paste once at the top of every new chat):**
> I'm working in a Colab/contest notebook. Task: [2–3 sentences: input, output, metric, submission format]. The notebook already defines: [list the variables/functions that exist]. Data shapes: [paste them].

**T2 — Decode the task:**
> Summarize this task statement in 5 bullets: input, output, metric, submission format, constraints. `<paste statement>`

**T3 — Explain the baseline (one chunk at a time):**
> Explain what this code does, line by line, for a beginner: `<paste one baseline cell>`

**T4 — Extend/modify the model** (head surgery, new layers):
> Write code that [ONE precise change, e.g. "replaces the 16-output classifier head with a 29-output head, copying the original 16 rows of weights/bias and randomly initializing the rest"]. + SUFFIX

**T5 — Dataset class:**
> Write a PyTorch Dataset that [what it loads, from which files/variables] and for one index returns [exact tensors, shapes, dtypes]. + SUFFIX

**T6 — Training loop:**
> Write a training loop ([optimizer, lr(s), epochs, batch size], [any special sampling/weighting/masking spelled out step by step]). My loader yields [exact tuple order]; the model is called as [exact signature]. + SUFFIX

**T7 — Evaluation:**
> Write evaluation code that predicts on [val split] and prints [the exact contest metric, spelled out]. + SUFFIX

**T8 — Submission writer:**
> Write code that runs the model on [test source], writes predictions in [exact format, one example line], saves as [filename], then prints the first line and total line count to verify. + SUFFIX

**T9 — Fix my error (the highest-value template — fixed every bug first try):**
> Fix this. Code only. `<paste the failing cell>` `<paste the FULL traceback>`

**T10 — Raise my score (ONE change at a time):**
> [Paste your eval numbers, e.g. "old acc 93.3, new acc 93.6" or "success_rate 0.76, 12 failures before pickup, 3 after"]. Give me ONE change to improve the weaker side. + SUFFIX

## The 5 recovery moves

1. **Truncated mid-code** → "Continue the code from the last line." (or re-ask with "shorter").
2. **Empty reply** → resend the SAME prompt once. Still empty → add THE OPENER + "max 20 lines". Two rewordings still empty → stop prompting; ask for the pieces separately or write it yourself.
3. **Two code blocks in one reply** → Gemma drafts then finalizes: **always copy the LAST block.**
4. **Undefined variable in the snippet** → "Define X too. Code only." (Gemma assumes `processor`/`train_df` exist.)
5. **Fix failed twice** → open a **fresh chat**, paste T1 + the new traceback. Never argue with a confused model.

## Ground rules (non-negotiable)

- **One chat = one job.** Fresh chat per subproblem; T1 briefing at the top of each.
- **Prescribe, don't ask it to invent.** Spell out the algorithm as numbered steps, the batch tuple order, the forward signature. Vague asks are what fail.
- **Verify before trusting:** read the code (do the variables exist?), run on a tiny slice first, `print(x.shape)` liberally.
- **Baseline on the board in 30 min**, then the Improvement Loop: diagnose → ONE targeted change (T10) → run → measure → keep or revert.
- **Never leave a broken submission as your last.** Verify the file format (T8's print check) before the final freeze.

## E4B amendments (validated live on chat.ioai2026.kz, 2026-07-22)

The real contest bot (Gemma 4 **E4B**) is smaller than the 31B used in drills. Same playbook, three additions:

- **THE THIRD MAGIC STRING** — add to every code prompt: *"Do not create mock or placeholder objects; assume all named variables exist."* (Without it, E4B invents `MockModel` stand-ins instead of using your `model`.)
- **Trust T9 less.** E4B pattern-matches the error text (e.g. reflexively casts `.float()`). Paste the FULL traceback + shapes, RUN every fix, and treat one-line cast fixes with suspicion — if it fails once, fresh chat.
- **Line caps are soft; imports get sloppy.** It exceeds "max N lines" and adds unused/deprecated imports (`transformers.AdamW`). 30-second code read before running; delete junk imports.
- Quotas on the real bot: **60 msg/h, 10-msg memory, 2,000-char input** — fresh chat per job, re-paste T1, budget messages.

## Self-practice protocol (how to drill with this page)

1. Open [aistudio.google.com](https://aistudio.google.com) → **Gemma 4** (`gemma-4-31b-it`). Pretend replies are capped at 2000 tokens.
2. Pick a drill card (`plan/drills/`) or any past task. 45-minute time box.
3. Use ONLY this page: T1 briefing → templates → recovery moves. No googling, no other chatbots.
4. Log score + what broke in the drill card's table. That's the whole session.
