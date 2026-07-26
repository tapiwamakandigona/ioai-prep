# IOAI Official Discord — Intel Digest

> Scraped from the **IOAI Official** Discord server (invite: https://discord.gg/GNtKU55Cr8), first sweep **2026-07-11**, full post-verification sweep same day (9 channels incl. newly unlocked ones).
> "Khan" below = Head of the Host Scientific Committee (IOAI 2026, Astana) — his answers are official rulings.
> Account status: **VERIFIED** ✅ (nickname "Tapiwa Makandigona[ZW]") — all member channels unlocked, posting enabled.

## 🔑 Action items for us
1. **Submit Home Tasks 1–2 on Kaggle** (live since Jul 7, links below) — real leaderboard practice against other contestants.
2. Ignore/avoid **ioai2026.kz** — confirmed fake/scam site (not official; flagged by the KZ hosts in #general).
3. **Re-download Home-Task-3.ipynb** — official notebook updated Jul 9 (fp16 fix; see rules audit `08_rules_audit_2026-07-11.md`).

## 🏠 Home Task round — official rulings (from Khan, in #home-task)
- Home Task problems: https://github.com/IOAI-official/IOAI-2026/tree/main/Home%20Task (announced Jun 30).
- **Kaggle hosting (announced Jul 7):**
  - Task 1 "Audio Classifier" (Operation Night Watch): https://www.kaggle.com/t/5fccd4b322b345b39210b52eeabf9df9
  - Task 2 "Robot Delivery Academy": https://www.kaggle.com/t/06b232bc145b47c78022bcd0c53231c9
  - Task 3 is **interactive** → not on Kaggle, local notebooks only. A Yandex Contest hosting "is being worked on" (also expected to have a leaderboard).
  - Kaggle submission limit was 5/day; after complaints an organizer **raised it to 20** (Jul 10).
- **Pretrained models are allowed** — including pretrained LLMs and embedding models for Task 3. Confirmed twice.
- **Time limit: 20 minutes — train + inference together** must fit (ruling on the "hard-code a precomputed decision tree?" question; a self-contained notebook must do its work within 20 min).
- **Task 2 is NOT reinforcement learning.** Official: "the setup was intentionally designed as a supervised learning task" — fixed training examples, learn a mapping observation → action. RL techniques not required (RL is not in the syllabus).
- **Task 2 boundaries:** do NOT generate additional expert trajectories via search/planning/another expert model (explicit in the task statement; a BFS question was shot down). Stacking previous frames into the input is not allowed (must predict from the current observation). Pure **geometric augmentation** (rotate/flip) of existing trajectories is the community's read as OK — no official ruling yet.

## 🏟 On-site contest — official answers
- **No competition task requires external LLMs, LLM APIs, or any installation.** Everything is provided and ready to use — zero setup time on contest day (Khan, Jul 1).
- The provided chatbot is **Gemma** (not Gemini) — confirmed in #general. Individual contest: Gemma 3, 1000-token output cap. (GAITE = Gemma 4, 2000 tokens — per contest rules.)
- Open (asked, not yet answered publicly): input-token cap for the provided Gemma (committee meeting reportedly said *no input limit*, context not saved between queries); whether it's INT4-quantized (it-qat vs normal instruct); whether on-site tasks will include interactive problems like Home Task 3.

## ⚠️ Known issues & community findings (#home-task, #questions)
- **Task 3 runtime — FIXED Jul 9:** the "~5–15 min on T4" cell used to take ~1.5 h (bf16 is slow on T4); the official notebook now uses a **batched fp16** approach and precompute takes minutes. Re-download the notebook; batching is now a contestant-side optimization hint, not provided code. Even post-fix, contestants say full brute-force (animal × question) precompute is heavy — batch + checkpoint.
- **Task 1 label noise:** several audio clips look misclassified — specifically some of **class 3 vs 7 (cow vs sheep)** and **11 vs 15 (thunderstorm vs rain)**. Raised with organizers Jul 10–11, no ruling yet. Implication: don't over-trust those labels; label-noise-robust choices help.
- **Kaggle submission gotcha (Task 1):** the competition data has **no `val` split** (unlike the original notebook). Take the `path` column from the provided `submission.csv`, predict a target for each path, and comment out baseline lines that depend on the val split.
- Community scores mentioned: Task 1 — "87%" reported by a Mali contestant (Jul 3), so beating high-80s is a real target.
- Official Home Round solutions / best scores before Aug 2: asked; Khan deferred to an ISC discussion, no answer posted yet.

## 🆕 Post-verification sweep (Jul 11) — newly unlocked channels
**Task 2 (Robot Delivery) community intel (#home-task, main #general):**
- Score landscape: plain behavioral cloning ≈ **76%** success rate; with fixes (CNN, loss weighting, augmentation) ≈ **91%**; Kaggle leaderboard top ≈ **99.75%** — but some top scores likely use the rule-violating greedy "vector" heuristic (obs channels 7+8 encode direction-to-target). Don't chase them with illegal tricks.
- **#1 failure mode: robot stuck in loops.** Loop-exit wrappers using visit counts were asked about (does it count as planning/search?) — **ruling pending**, treat as grey-zone.
- Loss weighting on rare pickup/dropoff actions: confirmed helpful by multiple contestants.
- Geometric augmentation (flips/rotations of existing trajectories): community consensus is allowed ("not new expert trajectories"), still no official ruling.
- Kaggle format gotcha: the baseline outputs a dataframe whose **two columns must be combined** into the expected submission format — "Submission File Not Found" = wrong file/format.
- Kaggle splits: **GitHub's val set = Kaggle's test set**; public leaderboard only, no private split. (One contestant noted you could extract answers from the published val split — leaderboard scores are unreliable as a skill signal.)
- gdown `FileURLRetrievalError` on Task 2 data: workaround = files re-shared in #general; upload the 3 files to Colab under a `data/` folder.

**Task 1 (Audio):** label-noise complaints escalated to `@Organizer` Jul 11 (classes 3 vs 7 cow/sheep, 11 vs 15 thunderstorm/rain misclassified) — still no ruling. 100% leaderboard scores were achieved by extracting labels from the published val split → ignore them.

**Task 3 (Oracle):** contestants confirm the intended approach is precompute-in-`__init__` with your own oracle copy; "train + inference under 20 min" ruling applies (Khan). Post-fp16-fix this is feasible.

**Other useful facts:**
- **The IOAI Slack is NOT for contestants** (it's for organizers/team leaders/delegations). Contestant comms = this Discord. Don't waste time seeking Slack access.
- Platform: community says IOAI 2026 uses **Yandex Contest** (mentor-posted link: new.contest.yandex.ru/contests/93047) — matches our intel doc.
- Team Challenge credentials went out **via email to Team Leaders** (Jul 10, Ali Sharifi); if none received, email isc@ioai-official.org.
- `#kz-questions` exists for official questions; pinging `@Organizer` is enabled but only for urgent matters.
- Unlocked channels worth monitoring: `#travel-meet` (meetups, mostly stale), `#our-own-projects`, `#news-discussion`, `#casual`, `#trivia`, plus 2025-China archive channels. Nothing strategy-relevant in them as of Jul 11 beyond the above.
- IOAI 2027 host: **Singapore** (mentioned casually by alumni).
- IOAI 2025 online practice problems are public on Bohrium (e.g. Chemical Kinetics: bohrium.com/en/competitions/25136176824) — extra practice material if needed; APOAI 2026 problems also public on Bohrium.

## 🌍 Server facts
- The server is the **IOAI Alumni Network**, renamed "IOAI Official" (run by alumni like Hendrik Pärli [EE]; organizers hold the `@Organizer` role — ping only for urgent matters).
- 2026-specific channels: `2026 Kazakhstan` → `#general`, `#photos`, `#questions`; plus `#home-task` (requested by Khan).
- IOAI is now on X/Twitter: https://x.com/aiolympiad (announced Jun 18).

## How this was gathered (repeatable)
Discord web login as the team account → scrape channels (`li[id^='chat-messages-']` DOM extraction after scrolling). Re-scrape before travel (late July) for last-minute logistics in `2026 Kazakhstan #general` and any Task 1 label-noise ruling.
