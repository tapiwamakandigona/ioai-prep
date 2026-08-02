# ioailab GitHub Repo — Deep Dive (2026-08-02)

> Source: **cloned https://github.com/galbot-ioai/ioailab (commit `88fb237`, Jul 17) and read every doc
> page + the online mdBook (galbot-ioai.github.io/ioailab)** — the site is just a render of `docs/`,
> identical content. Everything below is VERIFIED from the repo unless marked ASSUMED.
> Companion to `research/09` (the Jul 22 first-hand platform walkthrough). This doc covers only
> **what changed / what's new** since then, and what to actually do about it for the Team Challenge
> (Aug 3, 14:00 GAITE meeting + Team Challenge R1 — see `plan/01_lock_in.md`).

## Headline: the repo is no longer a stub

On Jul 22 the GitHub mirror was an empty README. Now it's the **full platform stack**: complete
source (`src/ioailab/`), all 7 numbered examples, a new `examples/vision_baseline/` suite, tests,
Docker setup, and a 3-chapter tutorial. **Everything the cloud desktop runs can now be read offline
before the contest.** You cannot *run* it without a beefy NVIDIA GPU + Isaac Sim (Docker-first,
`make build && make shell`), but reading beats nothing — and the contest desktop already has it
installed, so your job is to know the commands, not install anything.

## Confirmed unchanged from research/09 (don't re-learn)

- Core loop, agent taxonomy, task IDs, collect→mimic→train→evaluate pipeline, cameras
  (`front_head`/`left_wrist`/`right_wrist`), scenario YAMLs, Docker workflow, GP001 teleop —
  all exactly as documented in `research/09`. That doc still stands.
- The intended contest pipeline is still the numbered examples in order:
  `01_collect.py → 02_mimic.py → 03_train.py → 04_eval.py` (+ `06`/`07` for compound tasks).

## New / now-visible things worth knowing

### 1. SortToShelf is the newest, most polished task family (likely contest-relevant)
The changelog's whole "Unreleased" section is SortToShelf work: 4 colored objects
(`red_cube`, `blue_cuboid`, `yellow_cylinder`, `green_cylinder`) sorted into a 2×2 shelf,
selected via `--sorting-object` / `task_options={"sorting_object": ...}`. Slot assignment is
**randomized per reset** (`ObjectSlotAssignmentRandomizer`). ASSUMED but strongly indicated:
the contest task will be SortToShelf-shaped (newest code, most tuning commits, has its own
tutorial chapter and a full perception baseline).

### 2. A complete vision baseline: YOLO-seg + FoundationPose (`examples/vision_baseline/`, docs/yolo_seg.md)
This did not exist in the Jul 22 docs. It's a **perception-based alternative to ground-truth
scene state**, i.e. what you'd need if the contest hides object poses:
- `01_generate_yolo_dataset.py` — render a YOLO-seg dataset straight from the task scene
  (default `GalbotG1-SortToShelf-Pick-v0`, `front_head_rgb_camera`, 50 images, `--mask-source rgb-color`).
- `02_train_yolo.py` — train `yolo26n-seg.pt`, ~200 epochs, imgsz 320.
- `03_predict_yolo.py` — visual sanity check.
- `04–08_fp_*.py` — FoundationPose 6-DoF server (file-bridge) + eval of pick phase / full task /
  cyclic multi-object with perception instead of ground truth.
Note: `--mask-source rgb-color` exists **because fractional vGPU profiles (like the contest
desktops) can't run Isaac semantic segmentation** — that's a strong hint this pipeline was
built to run on the contest hardware.

### 3. Task-flow refactor (API changed since research/09's platform docs)
- Legacy flow state-machine / `Snapshot` APIs are **gone**. Coherent tasks are one continuous env
  driven by `TaskFlowAgent` (`TaskFlowAgent.from_env(env)`; override any phase:
  `agents={"pick": ..., "nav": ..., "place": ...}`).
- `SequenceAgent` = ordered agents inside one phase (SortToShelf nav uses `nav_sequence_agent`).
- `env.collect(...)` now also ends a row on **observed task success**, not just termination/timeout.
- PickToShelf place success = cube placed + gripper fully open for **20 consecutive steps** —
  don't yank the arm away early in teleop.

### 4. LeRobot v3 export exists (`ioailab.datasets.motion_plan_lerobot`)
Probably irrelevant for scoring, but if a task says "submit a LeRobot dataset", the exporter is
`MotionPlanLeRobotExporter(hdf5_path=..., lerobot_root=...).export()` — root must NOT pre-exist.

### 5. Tutorials (docs/tutorials/01–03)
Chapter 1: build a task (PickCube reference). Chapter 2: PickToShelf components→compound.
Chapter 3: SortToShelf with task options + sequence agents. Only relevant if the contest asks
you to *author/modify* a task; skim chapter headings, don't study.

## The 5-line crib (memorize; everything else is lookup)

```python
from ioailab.agents import CuroboPlannerAgent, TaskFlowAgent
from ioailab.envs import make_env
env = make_env("GalbotG1-SortToShelf-v0", num_envs=1, task_options={"sorting_object": "red_cube"})
agent = CuroboPlannerAgent.from_task(...)          # expert demos for free
dataset = env.collect(agent=agent, episodes=N, path="data/demos.hdf5")
```
then `02_mimic.py` (expand) → `03_train.py` (Diffusion Policy) → `04_eval.py --headless`.
**cuRobo demos are free expert data — always collect with the planner first, train second,
teleop only if the planner is disallowed.**

## Contest-day plan for the Team Challenge slot (concrete)

1. **Minute 0–10:** read the task statement; find the submission folder path in the HUD
   (research/09: submit from inside the session, server-side transfer, one at a time).
2. **Minute 10–30: baseline on the board.** Run the relevant numbered example **as-is, headless**
   (`python examples/01_collect.py` etc.). 1 GPU / 18 GB RAM → `num_envs` small (1–4), `--headless`.
3. Whole pipeline once end-to-end with tiny numbers (few episodes, few epochs) → submit → only
   then scale episodes/epochs. Same "never leave zero" rule as GAITE.
4. Roles (single shared login): one driver, one navigator reading these docs on their own laptop
   (repo is public — everyone can have it open), one watching the HUD clock (red ≤ 5 min;
   ending a session is irreversible; don't background the tab).
5. If perception is required: `vision_baseline` scripts in order, `--mask-source rgb-color`,
   defaults are tuned — change nothing on the first pass.

## Watch items
- Practice window reopening (Discord/email) — if it reopens, run PickCube end-to-end once as a
  team; that alone removes most contest friction (research/09 §prep still applies, ~239 h unused).
- Repo updates: last commit Jul 17; `git pull` on Aug 3 morning in case they push contest tasks.
