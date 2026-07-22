# Final Community Meeting (Jul 22) + Official ChatBot — Intel

> Sources: (1) meeting notes relayed by Tapiwa (joined late, so partial), 2026-07-22;
> (2) **first-hand verified exploration of the official contestant chatbot** at
> https://chat.ioai2026.kz/ (Viktor, 2026-07-22). Credentials are NOT in this repo.

## 🚨 Was due Jul 22 — confirm with team leaders that it happened

- **Team leader form (language support etc.) was "long overdue" — deadline was TODAY (Jul 22).**
  If your language isn't listed on the form, there will be **no support for that language** at the
  competition. At the meeting: 44 countries had filled it, 60 had not. → Daphne/Esau must have submitted
  it; if unsure, chase them NOW.
- **At-home task appeals** (problems in the at-home tasks) were also **due ~Jul 22**, and **only via the
  official form** — written emails/letters will NOT be acknowledged.
  - **One form per contestant per task** — multiple issues in multiple tasks = the team leader submits
    multiple forms. Be detailed and specific.
  - This was our channel for the Task 1 label-noise issue (see `06_discord_intel.md`).
- Feedback form link (also used for chatbot-limits feedback): https://forms.gle/LANDqyX6r876sbZq9

## Simulation site (Team Challenge)

- Organizers are **considering extending a day / reopening simulation.galbot.com** so participants can
  learn the platform: *"We will update regular channels as to whether we will reopen the simulation site."*
  → Watch Discord + email daily. If it reopens, schedule a full team session immediately
  (we have ~14,329 min unused — see `09_galbot_simulation_platform.md`).

## ✅ Official contestant ChatBot — VERIFIED first-hand

- URL: **https://chat.ioai2026.kz/** — one account per contestant (Zimbabwe = zwe101–zwe104;
  Tapiwa is **zwe104**). Login = contestant ID + password (sent to team leaders).
  - ⚠️ Note: our Jul 11 intel flagged `ioai2026.kz` as a scam — **that ruling is outdated/wrong for this
    subdomain**: `chat.ioai2026.kz` is the real official chatbot (official credentials work; UI matches
    the described contest assistant). Treat the chat subdomain as legit.
- A similar chatbot will be available **during the Individual/GAITE contests** for questions and
  issue-resolution.
- **"Assistant limits" page (zwe104, GAITE track) — read directly off the site:**
  | Setting | Value |
  |---|---|
  | Track | **GAITE** |
  | Model | **Gemma 4 E4B** |
  | Max reply length | **~2,000 tokens (~1,500 words)** |
  | Conversation memory | **last 10 messages** |
  | Max message length | **2,000 characters** |
  | Rate limit | **60 messages per hour** |
  - Site's own words: "The assistant is here to help you think — it will not solve the problems for you."
  - **Individual Contest limits are MORE restricted than GAITE** (per the meeting; matches our Jul 11
    intel: Gemma 3 / 1,000-token cap for individual). Feedback on limits → the form above.
- **Functional test passed:** asked for a PyTorch training-loop skeleton → clean, correct code came back.
  Meeting confirmation: **anything from Gemma is legal, including skeleton code** ("ask it even the name
  of your Grandpa 😂"). This validates the entire Gemma-first strategy (`00_current_strategy.md`).
- **Prep implication:** the practice chatbot is live NOW with the real contest limits — use it for the
  drills instead of AI Studio when possible. The 10-message memory + 2,000-char input cap mean: keep
  prompts self-contained, re-paste crucial context, and use the playbook's compressed prompt templates.

## Contest-day procedures (from the meeting — write these on your hand)

- **Computer freezes / connection drops:** raise your hand immediately, get help/another computer.
  **If you lost meaningful time (even ~10 min), fill in the extra-time request form RIGHT THEN, on the
  spot** — that's how the jury grants additional time.
- **If the round ends and your extra time wasn't approved yet: STAY SEATED.** Even if someone who is not
  jury tells you to stand up — don't. **If you leave the competition hall, your matter will not be
  resolved** and you may get no extra time.
- After the contest ends you may write down issues you faced, and you can talk to your team leader once
  you leave the competition ground.
- **Read the contest rules, especially the scoring section** (organizers stressed this):
  https://ioai-official.org/wp-content/uploads/2026/06/IOAI2026-Contest-Rules-and-Tehnical-Appendix.pdf

## On-site resources (from the meeting)

- **1 GPU slot and 18 GB RAM total** — whatever we run must fit in 18 GB RAM.
  → practice memory-frugal habits: small batch sizes, `del`/gc big objects, don't load full datasets into
  RAM, prefer streaming/`Dataset` generators, watch `nvidia-smi`/`free`.
- The **Jupyter Lab server will contain a few models pre-loaded and documentation on how to use a
  specific model** — on contest day, READ the provided docs first before improvising.
