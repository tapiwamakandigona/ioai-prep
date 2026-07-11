# IOAI Official Discord — Intel Digest

> Scraped from the **IOAI Official** Discord server (invite: https://discord.gg/GNtKU55Cr8) on **2026-07-11**.
> Channels covered: `#home-task`, `#important`, `#welcome`, 2026-Kazakhstan `#general` and `#questions`.
> "Khan" below = Head of the Host Scientific Committee (IOAI 2026, Astana) — his answers are official rulings.

## 🔑 Action items for us
1. **Verify the Discord account** to unlock all channels (it can read but not post right now): create a thread in `#verification-threads` named `"<last name>-verify"`, write `"<last name>-<country>-<year(s)>-<role(s)>"`, tag `@Admin`, and set the server nickname to `"Full Name [country code]"` (ISO 3166 alpha-2).
2. **Submit Home Tasks 1–2 on Kaggle** (live since Jul 7, links below) — real leaderboard practice against other contestants.
3. Ignore/avoid **ioai2026.kz** — confirmed fake/scam site (not official; flagged by the KZ hosts in #general).

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
- **Task 3 reference solution runtime is way off:** multiple people report the "~5–15 min on T4" cell actually takes **~1.5 h on a Colab T4** (confirmed by several). Budget for this; precompute overnight.
- **Task 1 label noise:** several audio clips look misclassified — specifically some of **class 3 vs 7 (cow vs sheep)** and **11 vs 15 (thunderstorm vs rain)**. Raised with organizers Jul 10–11, no ruling yet. Implication: don't over-trust those labels; label-noise-robust choices help.
- **Kaggle submission gotcha (Task 1):** the competition data has **no `val` split** (unlike the original notebook). Take the `path` column from the provided `submission.csv`, predict a target for each path, and comment out baseline lines that depend on the val split.
- Community scores mentioned: Task 1 — "87%" reported by a Mali contestant (Jul 3), so beating high-80s is a real target.
- Official Home Round solutions / best scores before Aug 2: asked; Khan deferred to an ISC discussion, no answer posted yet.

## 🌍 Server facts
- The server is the **IOAI Alumni Network**, renamed "IOAI Official" (run by alumni like Hendrik Pärli [EE]; organizers hold the `@Organizer` role — ping only for urgent matters).
- 2026-specific channels: `2026 Kazakhstan` → `#general`, `#photos`, `#questions`; plus `#home-task` (requested by Khan).
- IOAI is now on X/Twitter: https://x.com/aiolympiad (announced Jun 18).

## How this was gathered (repeatable)
Discord web login as the team account → scrape channels (`li[id^='chat-messages-']` DOM extraction after scrolling). Re-scrape before travel (late July) for last-minute logistics in `2026 Kazakhstan #general` and any Task 1 label-noise ruling.
