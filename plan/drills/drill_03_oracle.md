# DRILL 3 — Home Task 3: "The Analytical Language of John Wilkins" (20 Questions vs an LLM oracle)

**Time box: 45 min of hands-on play (+ one unattended precompute you start first). No studying. Follow the play, run the final-scoring cell, log your score.**

> Status: ✅ **VALIDATED 2026-07-11** — all prompts (P1–P3) tested live against **Gemma 4 (`gemma-4-31b-it`)** via the free Gemini API, each in a fresh chat with P0 pasted first; every final prompt produced a correct, single code block. The P4 sanity check is a provided copy-paste cell instead of a prompt — Gemma failed it 3 times running (empty replies), see "Validation notes". This task surfaced one NEW Gemma quirk (silent empty replies on "thinky" asks); the mitigation is baked into the prompts.

## What the task is (30-second version)
A hidden animal (out of **1,472**) sits behind an oracle — a local LLM (Qwen2.5-3B-Instruct) that answers yes/no questions from a fixed pool of **559** questions. You get **15 queries** per animal; **asks AND guesses both cost 1 query**. Score per animal = `max(0, (1 if guessed right) − 0.02 × queries_used)` — right on query 10 = 0.80. The trick the notebook itself tells you: the oracle is deterministic, so **precompute its answers offline with your own copy of the model** (costs no budget), then each round ask the question that best splits the remaining candidates. This task is **local in Colab, not on Kaggle** — your "submission" is a screenshot of the notebook's final summary table.

## Setup check (do once, ~2 min)
1. Tab 1: [aistudio.google.com](https://aistudio.google.com) → log in → model dropdown → **Gemma 4** (`gemma-4-31b-it`).
2. Tab 2: open the official notebook in Colab: [github.com/IOAI-official/IOAI-2026 → Home Task → Home-Task-3.ipynb](https://github.com/IOAI-official/IOAI-2026/blob/main/Home%20Task/Home-Task-3.ipynb) (badge at the top opens Colab) → Runtime → **T4 GPU**.
3. Run the notebook top to bottom through **Step 2** (downloads the dataset + loads the oracle; first model download ~6 GB, 30–60 s) and the **RandomBaseline** cell in Step 3. Its `mean_score` will be ~0.00 — **that's the floor; write it down.** Make sure the little cell that converts the model to **float16** ran (it prints `oracle model -> float16 (faster on T4)`).

## The play (one chat = one job; paste P0 at the top of EVERY new chat, then the numbered prompt)

> ⚠️ **Two Gemma quirks, both handled:** (1) Gemma 4 rambles reasoning before code — every prompt ends with the "ONLY a single python code block" suffix. (2) NEW on this task: on algorithm-heavy asks Gemma can burn its whole 2000-token budget "thinking" and send you a **completely empty reply**. The fix that worked live: start the prompt with **"Answer immediately with code — do not deliberate."** (already baked in below). If you still get an empty or cut-off reply, resend the same prompt — don't reword first.

**P0 — Briefing (paste once at the top of every new chat):**
> You are my code generator inside a Colab session. Standing rule for EVERY reply in this chat: output ONLY one python code block and absolutely nothing else — no reasoning, no bullet points, no checklists, no text before or after the block. Start your reply with \`\`\`python.
>
> Context: I'm working in the IOAI Colab notebook "The Analytical Language of John Wilkins". A hidden animal sits behind an oracle object: `interactor.ask(question)` returns 'yes' or 'no' (the question must be a line from the question pool), `interactor.guess(animal)` returns 'correct' or 'wrong'; BOTH cost 1 query from a budget of 15; per-row score = max(0, (1 if solved else 0) - 0.02*queries_used). I have `animals_pool` (list of 1472 lowercase animal names) and `questions_pool` (list of 559 lowercase yes/no questions). The oracle is Qwen/Qwen2.5-3B-Instruct at temperature 0, already loaded in memory as `Interactor._model` (a Hugging Face CausalLM on cuda, float16) and `Interactor._tokenizer`. For each question it builds this exact user message: "You are answering a question about one specific animal.\nThe animal is: {animal}.\nAnswer with a single word, yes or no.\nQuestion: {question}", applies the chat template with add_generation_prompt=True, generates with max_new_tokens=5, do_sample=False, and checks whether the reply starts with "yes".

**P1 — Batched oracle predictor (your own copy of the oracle, free of budget):**
> Your reply must be nothing but one python code block. Write a function `predict_answers(animal, questions)` that predicts the oracle's answers using the already-loaded `Interactor._model` and `Interactor._tokenizer`: build the exact prompt described above for each question, apply the chat template per prompt (tokenize=False, add_generation_prompt=True), set tokenizer.padding_side='left', tokenize all prompts as one padded batch, run ONE batched `generate(max_new_tokens=5, do_sample=False, pad_token_id=tokenizer.eos_token_id)`, decode only the newly generated tokens, and return a list with 1 if a reply starts with "yes" (case-insensitive) else 0, one per question. Code only, max 30 lines. Reply with ONLY a single python code block — no explanation, no reasoning, no bullet points.

Then, **before P2**, run this one-liner in a new notebook cell yourself (no prompt needed):
```python
QUESTIONS = questions_pool[:120]
```
120 questions ≫ the ~11 bits you need (log₂1472 ≈ 10.5), and keeps the precompute to a coffee break instead of a day.

**P2 — Precompute the animal × question table (checkpointed — start it, walk away):**
> I defined `QUESTIONS = questions_pool[:120]` and I have the `predict_answers(animal, questions)` function from before. Write code that builds a numpy int8 array `table` of shape (len(animals_pool), len(QUESTIONS)), one row per animal in animals_pool order, by calling `predict_answers(animal, QUESTIONS)`. It must mount Google Drive, use checkpoint path '/content/drive/MyDrive/wilkins_table.npz': if the file exists, load it and resume from the first unfinished row (store a `done` count in the file); save the checkpoint every 25 animals and at the end; print progress with elapsed time every 25 animals. Code only, max 30 lines. Your ENTIRE reply must be exactly one python code block starting with \`\`\`python — no text, no bullet points, no reasoning before or after it.

> ⏱️ **Timing reality check:** with the float16 cell run and P1's batching, expect roughly **20–45 min on a T4** for 1472 × 120. **If it looks like it will take hours, something is wrong**: you're on an old copy of the notebook or the model is still in bfloat16 (the pre-Jul-9 notebook had this bug — early Discord reports of "~1.5 h for the tiny reference table" were exactly this). Re-open the notebook from the GitHub link above and confirm the fp16 cell printed its message. Either way the checkpoint saves to your Drive every 25 animals — a Colab disconnect costs you at most 25 animals of work: reconnect, rerun the cells (P1 + the QUESTIONS line + P2) and it resumes where it left off. If you'd rather not babysit it, start P2 in the evening and do the rest of the drill next session — the table lives in your Drive.

**P3 — The solver: greedy question choice + soft (noise-tolerant) scoring:**
> Answer immediately with code — do not deliberate. I have two globals in memory: `QUESTIONS` (a 120-question subset of questions_pool) and `table` (numpy 0/1 array of shape (len(animals_pool), len(QUESTIONS)): rows = animals in `animals_pool` order, columns = QUESTIONS, values = the oracle's predicted answers). Write class `MySolution` with `__init__(self, animals_pool, questions_pool)` and `solve(self, interactor)` implementing exactly this:
> 1. weights w = numpy ones(len(animals_pool)).
> 2. While `interactor.remaining_budget()` > 4 and best weight < 0.9 * w.sum(): loop j over range(len(QUESTIONS)) (the global QUESTIONS, NOT questions_pool) and pick the unasked j minimizing abs(weighted yes-fraction of table[:, j] - 0.5); ans = 1 if interactor.ask(QUESTIONS[j]) == 'yes' else 0; w = w * where(table[:, j] == ans, 0.9, 0.1). Never zero out a weight — the oracle is sometimes wrong.
> 3. Then guess animals in descending weight order until `interactor.is_done()`.
> Code only, max 30 lines. Reply with ONLY a single python code block — no explanation, no reasoning, no bullet points.

*(Why soft weights instead of crossing animals off: the oracle answers from the model's beliefs and is occasionally wrong — the notebook says so explicitly. A hard filter kills the true animal on one bad bit; ×0.1 just demotes it, and 10 good bits bring it back.)*

**P4 — Free sanity check (no Gemma, no GPU, no oracle — run BEFORE the real eval):**
This one is NOT a prompt — Gemma reliably choked on it during validation (see notes), so just paste this cell into the notebook as-is. It replays your strategy against your own table (pretending the table rows are the oracle) for 40 random animals:
```python
import numpy as np
rng = np.random.default_rng(0)
counts = []
for i in rng.integers(0, len(animals_pool), size=40):
    w = np.ones(len(animals_pool)); asked = set(); c = 0
    for _ in range(15):
        j = min((q for q in range(len(QUESTIONS)) if q not in asked),
                key=lambda q: abs((w * table[:, q]).sum() / w.sum() - 0.5))
        asked.add(j); c += 1
        w *= np.where(table[:, j] == table[i, j], 0.9, 0.1)
        if np.argmax(w) == i: break
    counts.append(c)
counts = np.array(counts)
print(f"mean {counts.mean():.1f}  max {counts.max()}  <=11 questions: {(counts <= 11).mean():.0%}")
```
*(Good sign: mean around 8–12 and most runs ≤ 11. If nearly every run needs all 15, your table probably didn't finish — check the P2 progress printout / `done` count.)*

**P5 — Score it (no prompt needed — the notebook does this):**
Run the notebook's own Step 4 cell (`my_dev = evaluate(MySolution(animals_pool, questions_pool), 'dev.csv')`) — it prints `Mean score / Solved rate / Mean queries` on the 150 dev animals. Each dev row makes real oracle calls, so expect ~15–30 min. Then run the **Step 5 final-scoring cell** unchanged — it evaluates dev + test1 (+ test2 if present) and prints the summary table with the **FINAL** row. **Screenshot that table — that IS your submission.**

## Recovery moves (when something breaks)
1. **Any error** → new message: paste the FULL traceback + the failing cell. "Fix this. Code only."
2. **Empty or cut-off reply** → resend the exact same prompt once (Gemma sometimes thinks itself out of tokens — see quirk box). Still empty? Prepend "Answer immediately with code — do not deliberate." and add "max 20 lines".
3. **`ValueError: ... is not in questions_pool.txt`** → costs no budget. It means the code asked a made-up question — tell Gemma: "Only ask strings from the QUESTIONS list, exactly as they appear. Fix. Code only."
4. **CUDA out of memory during P2** → "Rewrite predict_answers to process the questions in chunks of 32 per generate call. Code only."
5. **Precompute crawling (hours)** → you're in bfloat16 or on an old notebook — re-open from GitHub, run the fp16 cell (it prints `oracle model -> float16`), rerun P2 (it resumes from Drive).
6. **Dev score low but P4 looked fine** → the live oracle disagrees with your table more than expected; make the update gentler: "Change the weight update factors from 0.9/0.1 to 0.9/0.2. Code only." and re-run P5.

## Known traps (don't burn time on these)
- **Guesses cost budget too.** 10 asks + 1 correct guess = 11 queries = 0.78, not 0.80. The P3 policy stops asking at ≤4 remaining so there's always room to guess.
- **This task is NOT on Kaggle.** Local notebook only; the Step 5 summary-table screenshot is the deliverable (a Yandex Contest hosting was "being worked on" per Discord). Organizers also re-score your `MySolution` on a hidden test set — don't hand-tune to dev animals.
- **The "~5–15 min" reference-cell estimate was famously wrong pre-Jul-9** (bf16 on T4 → ~1.5 h reports on Discord). The Jul 9 notebook fix (fp16) + batching makes precompute minutes-to-a-coffee-break. If you see hours, see recovery move 5.
- **Deterministic ≠ infallible.** Same (animal, question) always gives the same answer, but the answer itself can be "wrong" (the model's belief). That's why P3 never hard-eliminates.
- **20-minute rule (Discord ruling):** train + inference must fit in 20 min for the official run — precompute in `__init__` with your own model copy is the intended approach; loading a table you computed offline into `__init__` is exactly the pattern the notebook teaches. Keep your `MySolution.__init__` fast at eval time (load the .npz, don't recompute).

## Validation notes (Viktor, 2026-07-11 — live run against `gemma-4-31b-it`, fresh chat per prompt, P0 pasted first)
- **P1 (batched predictor): PASS.** Correct on the merits every attempt: left padding, per-prompt chat template, one batched generate, slicing off only new tokens, `startswith("yes")` parsing — even added `torch.no_grad()` unprompted.
- **P2 (checkpointed precompute): PASS first try.** Drive mount, resume-from-`done`, save every 25 — exactly as asked.
- **P3 (solver): PASS on iteration 3.** Iter 1 came back **completely empty** — Gemma spent all 2000 tokens on hidden deliberation before writing any visible code. Fix #1: start the prompt with "Answer immediately with code — do not deliberate." Iter 2 then produced clean code but looped over `questions_pool` (559) instead of `QUESTIONS` (120 table columns) — would have crashed on `table[:, j]`. Fix #2: spell out "loop j over range(len(QUESTIONS)) (the global QUESTIONS, NOT questions_pool)". Iter 3: correct, including the `best_j == -1` guard and soft ×0.9/×0.1 update.
- **P4 (sanity sim): FAILED as a prompt — converted to a provided cell.** Three iterations (plain ask → pseudocode skeleton → skeleton + "do not deliberate" opener, plus retries) all returned **empty replies**: Gemma burned the whole 2000-token budget deliberating and emitted zero visible code. Rather than burn drill time on a coin-flip prompt, the sanity check is now a paste-this-cell (verified by running it: on a synthetic 1472×120 table it prints `mean 9.8  max 12  <=11 questions: 92%`). Contest takeaway: if two rewordings of a simulation-style ask come back empty, stop prompting and ask Gemma for the pieces separately — or skip the nicety.
- **Big lesson (new since drill 1):** on algorithm-design asks, Gemma 4's failure mode isn't rambling *around* the code — it can produce **no visible output at all** (budget eaten by deliberation). "Answer immediately with code — do not deliberate." + prescribing the algorithm as numbered steps (so there's nothing left to design) rescued P3; it was not enough for P4's nested simulation. Prescribe the algorithm; don't ask Gemma to invent it; and have a fallback plan for prompts that stay empty.
- **Flaky API:** repeated HTTP 500 storms during validation (one prompt needed 6+ retries). Not your prompt's fault — resend before rewording. The contest UI shouldn't have this, but the same rule applies: retry first.
- Strategy logic double-checked offline in plain numpy (synthetic 1472×120 table, 5% injected noise): the greedy+soft-weights policy puts the true animal top-1 ~83% within 15 asks even under noise; with the deterministic real table it should be substantially better.

## Log it (2 min, in this file's table or DM Viktor)
| Date | Baseline (random) | P4 sim mean | Dev score | FINAL score | What broke | Prompts that saved you |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
