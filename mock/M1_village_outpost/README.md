# 🌙 Mock Task M1 — Operation Night Watch: The Village Outpost

A **format-faithful practice task** in the style of the IOAI 2026 At-Home Round (Home Task 1 family:
continual learning / catastrophic forgetting). Built 2026-08-02 by Tapiwa for contest-condition practice.

## How to run it (contest conditions)

1. Open `night_watch_village_outpost.ipynb` (locally or in Colab — the first cell clones this repo if needed).
2. Start the clock: **90 minutes** suggested.
3. Help allowed: **the Gemma chatbot only** — drive it with the prompt pack (`research/12`), just like contest day.
4. Run the baseline top-to-bottom, note its validation score (~0.43), write `submission.csv` early.
5. Improve it (the mission section lists the intended paths), one change at a time, log every score.
6. Send the **updated notebook + `submission.csv`** to Tapiwa on Slack for grading against the hidden test set.

## Facts

- 8 old classes (base model already knows them) + 5 new classes (imbalanced fine-tune set).
- `Score = 0.5·Acc_old + 0.5·Acc_new` on a hidden test set (40 clips/class, labels not in this repo).
- Baseline hidden-test score: **0.38** (acc_old = 0.00 — total forgetting). Target: ≥0.85 val / ≈0.80+ hidden.
- Everything runs on CPU in minutes. `pip install torch numpy pandas matplotlib` is all you need.

## Files

| File | What |
|---|---|
| `night_watch_village_outpost.ipynb` | The task notebook (8-section IOAI anatomy) |
| `base_model.pt` | Deployed model, trained on the old 8 classes only |
| `data/train_old.npz` | Retained old-class subset (25/class) |
| `data/fine_tune.npz` | New-class clips (12–40/class, imbalanced) |
| `data/val.npz` | Labeled validation, all 13 classes |
| `data/test.npz` | Hidden-test features (no labels) |
| `data/classes.json`, `data/sample_submission.csv` | Class list + submission format |
