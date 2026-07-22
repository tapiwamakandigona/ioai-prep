# LOCK IN — what truly matters (Jul 23 → Aug 8)

> Written 2026-07-22, right after live-validating the playbook against the **real contest bot**
> (chat.ioai2026.kz, Gemma 4 **E4B**, zwe104, 3 test messages). You don't need the whole repo.
> You need this page, `plan/playbook.md`, and the three 2026 task pages on the hub. That's it.

## 0. The model gap — settled (VERIFIED 2026-07-22)

The drills were validated against `gemma-4-31b-it` (Google's API). The real GAITE bot is
**Gemma 4 E4B** — much smaller. I ran 3 live tests on the real bot today:

| Test | Result |
|---|---|
| T4 head-surgery + SUFFIX | ✅ Single clean code block, correct copy-weights logic. **But it invented a `MockModel` placeholder instead of trusting that `model` exists.** |
| T9 error-fix (+ "no mocks" line) | ✅ Perfect format, no mock. ⚠️ The fix was a **blind cast pattern-matched from the error text** — it never questioned whether the setup made sense. |
| 45-line full training script + OPENER | ✅ Complete, non-truncated, correct structure (`.logits`, best-checkpoint save). ⚠️ Dead/wrong imports (`transformers.AdamW`), ignored the 45-line cap. |

**Verdict: the playbook carries over.** Same magic strings, same templates. E4B is just a
dumber colleague than 31B, so three amendments:

1. **New third magic string** (add to every code prompt):
   > Do not create mock or placeholder objects; assume all named variables exist.
2. **Trust T9 less.** E4B pattern-matches the error message. Always paste the FULL traceback
   + real shapes, always RUN the fix, and if the fix is just a `.float()`/`.reshape()` cast,
   be suspicious — re-check with a fresh chat if it fails once.
3. **Line caps are soft, verify imports.** It will exceed "max N lines" and add unused or
   deprecated imports. Read the code before running (30 seconds), delete junk imports.

## 1. The only 4 things that matter

1. **The playbook** (`plan/playbook.md`): 3 magic strings + T1 (briefing), T9 (fix), T10
   (one improvement) + the 5 recovery moves. Memorize to the point of writing them from memory.
2. **The 8-step flow** (`research/05`): metric first → baseline submitted in 30 min → one
   change at a time → never leave zero → verify the submission file before the freeze.
3. **The three 2026 home tasks** (hub cards): Day 1 extends these. Know what each baseline
   does and what its known weakness is (T1 label noise, T2 loss-weighting/loop-handling, T3 fp16 precompute).
4. **Quota discipline**: 60 msg/h ≈ 1 message per 6 minutes if you burn evenly. 10-msg memory
   → fresh chat per job, re-paste the T1 briefing. 2,000-char input → paste code in chunks.

Everything else in the repo is reference. Do not "study" it.

## 2. Day by day (drills, not studying)

| Date | Do (45–60 min unless marked) |
|---|---|
| **Jul 23** | Read hub: Task 1 (audio) page + this page. Then **Drill 1 vs the REAL bot** (chat.ioai2026.kz): run the drill-card prompts, budget ≤20 messages. Log what broke. |
| **Jul 24** | Read hub: Task 2 (robot) page. **Drill 2 vs the real bot**, ≤20 messages. |
| **Jul 25** | Playbook self-test: write the 3 magic strings + T1/T9/T10 from memory. Read hub: Task 3 (oracle) page. |
| **Jul 26** | **Drill 3 vs the real bot**, ≤20 messages. |
| **Jul 27** | Yandex example task (new.contest.yandex.ru/contests/93047) — the real on-site platform. Get comfortable with the interface. |
| **Jul 28** | Rest / catch-up day (life happens; this slot absorbs slippage). |
| **Jul 29** | **Timed mock, 3 h:** one home task from scratch, contest rules, real bot, ≤60 messages total. Baseline on the board in 30 min or you failed the mock. |
| **Jul 30** | Review the mock with me (Viktor): what broke, ≤3 corrections. Update `plan/snippets.md`. |
| **Jul 31** | Second playbook self-test + logistics: pack, download offline copies of the hub pages, charge everything. |
| **Aug 1** | Rest. Seriously. |
| **Aug 2** | Travel / opening ceremony. Watch Discord + email for GALBOT window reopening + quota announcements. |
| **Aug 3** | **07:30 Practice Round (OBLIGATORY):** confirm real quotas, test the chat UI + JupyterLab, learn how the final solution is designated, request own keyboard/mouse. 14:00 GAITE meeting + Team Challenge R1. |
| **Aug 4** | **Contest Day 1 (09:00–15:00).** Run the play: 5-min triage of all tasks → baseline in 30 min → improvement loop → freeze 45 min early, verify submissions. |
| **Aug 5** | Recover. Note what worked/broke while fresh. |
| **Aug 6** | **Contest Day 2 (09:00–15:00).** Same play. |
| **Aug 7–8** | Team Challenge Final (if top 10) / closing. |

## 3. Rules that bite (one-line reminders)

- zwe104 is YOUR account only; never log into teammates'.
- Appeals: official forms only, one per contestant per task. Extra time: file immediately, in-hall.
- Hidden Scoreboard B decides medals — don't overfit the public leaderboard.
- 20-min notebook runtime, 60 submissions/task, 1 GPU / 18 GB RAM.
- Anything Gemma gives you is legal. Using it hard is the intended playstyle, not cheating.
