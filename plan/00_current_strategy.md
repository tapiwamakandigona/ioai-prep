# CURRENT STRATEGY — Drill-based, Gemma-first (adopted 2026-07-11)

> **This supersedes `30_day_plan.md`.** Read this file first; everything else in the repo is reference material.

## Reality check (why the plan changed)
- It's **Jul 11**; the 30-day curriculum (started Jul 3 on paper) was never begun — uni prep took priority. **22 days remain** to Astana (Aug 2).
- Starting point: no coding/ML background; strength = **vibe coding** (directing an LLM to produce working code and iterating).
- Curricula and self-study sites get ignored (proven twice). Anything that looks like "studying" will not happen. **Drills with a scoreboard will.**
- This is fine, because **GAITE is designed for exactly this**: Gemma 4, 2000-token replies, generous chat access (exact quotas TBA — confirm at the Aug 3 practice round), hints allowed, separate scoreboard. Heavy chatbot use isn't a hack — it's the intended playstyle of the track.

## The strategy: train the operator, not the engineer
The single skill being trained: **driving Gemma to a scoring submission**. No theory, no lessons.

### Step 1 — Viktor validates the route (Jul 11–14)
Viktor solves all 3 At-Home Tasks using **only prompts to Gemma 4** (`gemma-4-31b-it` — the actual contest-bot family, available on the free Gemini API), no expert knowledge injected. Output: **prompt scripts** per task — "paste this → then this → if you see error X, paste that." Any spot that can't be cheesed gets a scripted workaround.

### Step 2 — One-page playbook (Jul 14)
`plan/playbook.md`: ~10 prompt templates (run-the-baseline, fine-tune-a-classifier, fix-my-error, raise-my-score, write-the-submission-file) + ~5 recovery moves. Short enough to memorize. Replaces the site as the prep artifact.

### Step 3 — Drills, 2–3×/week, ~45 min (Jul 14 → Aug 1)
Colab + Gemma + drill card → submit to the **Kaggle leaderboard** (Home Tasks 1–2 are live, 20 subs/day). No studying — run the play. Viktor reviews the notebook + score afterwards, gives **max 3 corrections**. Leaderboard = honest signal whether the cheese works, weeks before the flight.

### Step 4 — Dry runs (late Jul)
- The official **Yandex Contest example task**: https://new.contest.yandex.ru/contests/93047 (the real on-site platform).
- One timed mock "contest day" in the last week of July.
- Team Challenge practice session on the GALBOT simulator with the ZW team (single shared login — coordinate with team leaders).

## Ground rules (from the old plan, still true)
- Every drill runs **under contest rules**: one chat = one job, ask in chunks ("code only, ≤30 lines"), treat replies as capped at 2000 tokens, verify by running.
- The **Baseline Improvement Loop** stays the core play: run baseline → diagnose where points are lost → ask Gemma for ONE targeted change → verify → measure → keep or revert.
- Anything looked up twice goes into `plan/snippets.md`.

## Status log
| Date | What happened |
|---|---|
| 2026-07-11 | Strategy adopted. Discord intel + Team Challenge email captured (`research/06`, `research/07`). Discord verification submitted ("Makandigona-verify"). |
| 2026-07-11 | **Drill #1 drafted** → `plan/drills/drill_01_audio.md` (Task 1 audio: P0–P5 prompt scripts + 5 recovery moves, built from the official notebook). |
| 2026-07-11 | **Drill #1 VALIDATED live vs `gemma-4-31b-it`** — all 5 prompts returned correct code first try. Key finding: Gemma 4 rambles before code, so every prompt must end with "Reply with ONLY a single python code block" or the 2000-token cap truncates the answer. Gemma 4 (not just Gemma 3) is on the free API — practice against the real contest model family. |
| 2026-07-11 | **Full rules re-audit** vs official IOAI page (`research/08_rules_audit_2026-07-11.md`). All core GAITE assumptions confirmed; fixes: no device quarantine, live baseline+max scoreboard visible, official scores come from a hidden "Scoreboard B" (don't overfit the public LB), 20-min notebook runtime + 60 submissions/task, Yes/No-only clarifications, obligatory practice round Aug 3. **Home-Task-3 notebook was fixed Jul 9 (fp16 batching — precompute now minutes, not hours): re-download it.** |
| 2026-07-11 | **Drills #2 (Robot Delivery) and #3 (Wilkins 20Q) built and VALIDATED live vs `gemma-4-31b-it`** → `plan/drills/drill_02_robot.md`, `plan/drills/drill_03_oracle.md`. New Gemma quirk found on Task 3: algorithm-design asks can come back **completely empty** (2000-token budget eaten by hidden deliberation) — fix: "Answer immediately with code — do not deliberate." + prescribe the algorithm step by step. All 3 home tasks now have a validated prompt script. |
| 2026-07-11 | **Post-verification Discord sweep** (9 channels) → `research/06_discord_intel.md`. Highlights: Task 2 plain BC ≈76% success, with loss-weighting + loop-handling ≈91%; Task 1 label noise (cow/sheep, thunderstorm/rain) escalated to organizers, LB unreliable; Kaggle limit now 20 subs/day; platform = Yandex Contest. |
