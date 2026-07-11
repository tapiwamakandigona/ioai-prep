# DRILL 2 — Home Task 2: "Robot Delivery Academy" (behavioral cloning, 8×8 grid)

**Time box: 45 min. No studying. Follow the play, submit to Kaggle, log your score.**

> Status: ✅ **VALIDATED 2026-07-11** — all prompts (P1–P5) tested live against **Gemma 4 (`gemma-4-31b-it`)** via the free Gemini API. P1/P2/P5 returned correct code on the first try; P3 and P4 each needed one rewrite (see "Validation notes"). Transcripts archived by Viktor.

## What the task is (30-second version)
A robot on an 8×8 grid must walk to a depot, **pick up** a package, walk to another depot, and **drop it off**. You train it purely by copying expert demonstrations (`observation → action`, plain supervised learning). The baseline is an MLP on a flattened grid; the notebook itself tells you its weaknesses — your job is to fix them. Score = **episode Success Rate** (delivered within 120 steps). Actions 0–5 = south / north / east / west / pickup / dropoff.

**Hard rules (official Discord rulings — breaking these disqualifies the approach):**
- This is **NOT reinforcement learning**. Supervised only.
- **NO search/planning** (no BFS/A*), no generating extra expert trajectories, no other expert models.
- **NO frame stacking** — predict from the *current* observation only.
- 20-min limit = training + inference combined. Kaggle: 20 submissions/day.

## Setup check (do once, ~2 min)
1. Tab 1: [aistudio.google.com](https://aistudio.google.com) → log in → model dropdown → **Gemma 4** (`gemma-4-31b-it`).
2. Tab 2: open the task notebook in Colab (from [kaggle.com/competitions → IOAI 2026 Home Task 2](https://www.kaggle.com/t/06b232bc145b47c78022bcd0c53231c9), or `Home-Task-2.ipynb` from the official GitHub) → Runtime → T4 GPU.
3. Run ALL baseline cells top to bottom — data download, simulator, `train_trajectories`, the MLP training, and the evaluation cell that prints `success_rate` for `random` and `MLP`. **Write the MLP success_rate down.** That's your baseline to beat.

## The play (one chat = one job; always end prompts with "Code only, max 30 lines. Reply with ONLY a single python code block — no explanation, no reasoning, no draft versions, no bullet points.")

> ⚠️ **Why the extra suffix:** Gemma 4 "thinks out loud" — bullet-point reasoning before code. Replies are capped at 2000 tokens; the rambling can eat the budget and **cut off the code**. On this task Gemma sometimes also writes a *draft* code block, critiques it, then writes the final one — hence "no draft versions" in the suffix. If a reply has two code blocks, **use the LAST one**. If it truncates mid-code: "Continue the code from the last line."

**P0 — Briefing (paste once at the top of every new chat):**
> I'm working in the official IOAI 'Robot Delivery Academy' Colab notebook. A robot on an 8x8 grid must pick up a package at one depot and deliver it to another. I train by behavioral cloning on expert demonstrations only (pure supervised learning — no RL, no search or planning). Each observation is a dict: obs['grid'] is a numpy array of shape (6, 8, 8) (channels: walls, depots, robot, package, destination, carrying flag), obs['vector'] is 13 floats, obs['action_mask'] is 6 booleans marking valid actions. Actions 0-5 = south, north, east, west, pickup, dropoff. The notebook already defines: train_trajectories (list of dicts, each with 'observations' and 'actions' lists), valid_scenarios, test_scenarios, DEVICE, ACTION_NAMES, run_episode(scenario, action_fn), evaluate_action_model(scenarios, action_fn, limit) which returns a dict with success_rate/avg_steps/avg_invalid_pickup_or_dropoff/results, generate_predictions(scenarios, action_fn, limit), and save_predictions_zip(predictions, path). The baseline flattens the grid into an MLP; I am replacing it with a small CNN.

**P1 — Dataset that keeps the grid shape (the baseline flattens it — that's flaw #1):**
> Write a PyTorch Dataset class GridDemoDataset that collects every (observation, action) pair from all trajectories in train_trajectories and, for one index, returns four tensors: the grid as float32 of shape (6, 8, 8), the vector as float32 of shape (13,), the action_mask as bool of shape (6,), and the action as a long. Then create grid_dataset = GridDemoDataset(train_trajectories) and grid_loader = DataLoader(grid_dataset, batch_size=128, shuffle=True). Code only, max 30 lines. Reply with ONLY a single python code block — no explanation, no reasoning, no draft versions, no bullet points.

**P2 — Small CNN (the notebook's own hint: "preserve the 8×8 spatial structure"):**
> Write a PyTorch nn.Module named CNNActionModel whose forward takes (grid, vector): two Conv2d layers on the (6, 8, 8) grid (6->32 then 32->64 channels, kernel 3, padding 1, ReLU after each), flatten, concatenate the 13-feature vector, then Linear to 128 with ReLU and Linear to 6 action logits. Then create cnn_model = CNNActionModel().to(DEVICE) and print the parameter count. Code only, max 30 lines. Reply with ONLY a single python code block — no explanation, no reasoning, no draft versions, no bullet points.

**P3 — Train with class weights + masked logits (flaws #2 and #3 in one loop):**
> My grid_loader yields four tensors per batch in this order: grid (B, 6, 8, 8) float, vector (B, 13) float, action_mask (B, 6) bool, action (B,) long — and cnn_model's forward is called as cnn_model(grid, vector). Write a training loop: 30 epochs, Adam lr 1e-3. First collect all action labels by iterating grid_dataset (the fourth element of each sample), use torch.bincount to count the 6 actions, and build class weights = 1/counts, normalized, for nn.CrossEntropyLoss so rare pickup/dropoff actions are not under-learned. In each batch compute logits = cnn_model(grid, vector), then set logits where action_mask is False to -1e9 before the loss. Print the average loss every 5 epochs. Code only, max 30 lines. Reply with ONLY a single python code block — no explanation, no reasoning, no draft versions, no bullet points.
> *(Why: pickup/dropoff appear ~once per episode vs dozens of moves — without weighting the model under-learns exactly the two actions that decide success. Masking during training stops the model wasting capacity on actions the simulator would reject anyway.)*

**P4 — Full-episode evaluation + failure replay (the key trap: action accuracy ≠ episode success):**
> Write, in one short script: a function cnn_action(obs) that makes float32 tensors from obs['grid'] and obs['vector'] on DEVICE each with unsqueeze(0), runs cnn_model(grid, vector) in eval mode under torch.no_grad, sets logits where obs['action_mask'] is False to -1e9, and returns int(logits.argmax()). Then cnn_eval = evaluate_action_model(valid_scenarios, cnn_action, limit=100); print success_rate, avg_steps, avg_invalid_pickup_or_dropoff. Then from the failed results in cnn_eval['results'] print how many have no action 4 in r['actions'] (failed before pickup) and how many do (failed after pickup). Code only, max 25 lines. Reply with ONLY a single python code block and nothing else — no explanation, no reasoning, no plan, no draft version, no self-check, no line counting. Write the final code directly.
> *(To actually WATCH a failure: pick a failed scenario index i and run the notebook's own `show_episode_gif(valid_scenarios[i], run_episode(valid_scenarios[i], cnn_action)["actions"])`.)*

**P5 — Kaggle submission (predictions.jsonl → predictions.zip):**
> Write code that generates the Kaggle submission: test_predictions = generate_predictions(test_scenarios, cnn_action, limit=None), then save_predictions_zip(test_predictions, 'predictions.zip'), then open predictions.zip with zipfile, read predictions.jsonl and print its first line and the total line count to verify the format. Code only, max 30 lines. Reply with ONLY a single python code block — no explanation, no reasoning, no draft versions, no bullet points.
> *(Each line must look like `{"layout_id": "test_0000", "episode_seed": 300000, "actions": [1, 1, 2, 4, 0, 5]}` — the print check confirms that. Download predictions.zip from Colab's file panel and upload it to Kaggle.)*

## Recovery moves (when something breaks)
1. **Any error** → new message: paste the FULL traceback + the failing cell. "Fix this. Code only."
2. **Two code blocks in one reply** → use the LAST one (Gemma drafts, then finalizes).
3. **Snippet references an undefined variable** → "Define X too. Code only." (Gemma likes assuming `grid_dataset.actions` exists — it doesn't; samples are tuples.)
4. **Success rate barely beats baseline** → paste your P4 numbers: "success_rate X, Y failures before pickup, Z after pickup. Give me ONE change to fix the bigger failure mode. Code only."
5. **Training slow / near 20 min** → "Rewrite with 15 epochs and batch size 256. Code only." (This model is tiny — 30 epochs takes only a few minutes on T4; the real time sink is running episodes.)

## Known traps (from official rulings + Discord intel — don't burn time on these)
- **Do NOT reach for BFS/A\*** even "just to generate more data" — explicitly forbidden (a Discord BFS question was shot down). Rule-based/hard-coded solutions get reviewed by the Scientific Committee. In particular: the observation's direction-to-target features would let you write a greedy "walk toward the target" heuristic — some suspiciously-high leaderboard scores likely do this, and **it's a violation**. Your model must *learn*.
- **No frame stacking** — current observation only. No generating new expert trajectories.
- **High action accuracy is a lie.** 95% per-step accuracy can still fail episodes: one early wrong step drifts the robot into states it never saw in demos. Only `success_rate` from P4 counts. The #1 community-reported failure mode is the robot **stuck in a loop** — that's what your P4 failure counts catch. (Loop-exit hacks like visit counters may count as "planning" — grey zone, ruling pending. The clean fix is a better model, not a hack.)
- `avg_invalid_pickup_or_dropoff` > 0 after masking at inference means your mask isn't applied — check cnn_action.
- **Score calibration (community reports):** plain behavioral cloning ≈ 76% SR; with the P1–P3 fixes ≈ 91%; leaderboard top ≈ 99.75% (some likely rule-breaking heuristics — don't chase them).
- **If you still have budget:** geometric augmentation (flipping/rotating existing trajectories, remapping the move actions to match) is the community consensus legal move ("the ban is on NEW trajectories") and reportedly helps — but there's **no official ruling yet**. Use it only after P1–P5 work, and be ready to drop it.
- **Kaggle gotchas:** 20 subs/day. "Submission File Not Found" = wrong file/format — the Kaggle variant may expect the baseline's two dataframe columns combined; re-read the Kaggle data page before panicking. The GitHub `valid_scenarios` = Kaggle's test set; there's only a public leaderboard, no private split — your P4 number should track the LB closely. Deterministic predictions required (seeds already fixed in the notebook).

## Validation notes (Viktor, 2026-07-11 — live run against `gemma-4-31b-it`)
- **P1, P2, P5: correct on the first try.** P2 computed the flatten size (64·8·8+13=4109) itself; P5 reused the notebook's own `generate_predictions`/`save_predictions_zip` and verified the jsonl format.
- **P3 failed once, fixed by one rewrite.** The vague first version ("count each action in grid_dataset") made Gemma invent `grid_dataset.actions`, unpack the loader as 3 tensors instead of 4, and call `cnn_model(grids)` without the vector — plus it emitted a draft code block *and* a final one. Lesson: **spell out the batch tuple order and the forward signature in the prompt** (now baked into P3 above).
- **P4 failed once, fixed by one rewrite.** The first version's three-part ask made Gemma draft, self-check line-by-line, redraft — and the final code block got **cut off at the 2000-token cap**. Lesson: on multi-part asks, shorten the wording, drop the limit to 25 lines, and extend the suffix with "no plan, no draft version, no self-check, no line counting. Write the final code directly." (now baked into P4 above).
- **Quirk — rambling persists:** even with the suffix, Gemma 4 wraps the code in bullet-point plans and post-checks. Harmless as long as the code block itself is complete; if it truncates, say "shorter" or "Continue the code from the last line."
- **Quirk — flaky API:** intermittent HTTP 500 on the free tier, including one ~10-minute full outage during validation. Not your prompt's fault — resend/retry before rewording.

## Log it (2 min, in this file's table or DM Viktor)
| Date | Baseline SR | Your SR (P4) | Fail before/after pickup | Kaggle LB | What broke | Prompts that saved you |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
