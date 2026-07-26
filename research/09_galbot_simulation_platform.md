# GALBOT Simulation Platform — Full First-Hand Walkthrough

> Source: **logged into https://simulation.galbot.com with the Zimbabwe team account and explored every
> page + the built-in Player User Guide + the full ioailab docs** (Viktor, 2026-07-22). Everything below
> is VERIFIED first-hand unless marked otherwise. Credentials are NOT in this repo — ask the team leaders.

## ⚠️ Status as of 2026-07-22 (evening)

- The **at-home practice window has ENDED**: event window was **Jul 9 00:00 – Jul 22 00:00 (Asia/Almaty)**.
  The "Enter remote desktop" button is disabled with "Availability window has ended".
- Zimbabwe's counter still shows **14,329 min remaining (~239 h) of a per-session limit of 480 min (8 h)**
  — i.e. the team barely used the practice window.
- The organizers said at the Jul 22 community meeting they **may reopen the site / extend a day** so teams
  can learn the platform — "We will update regular channels as to whether we will reopen the simulation site."
  **Watch Discord/email; if it reopens, book a full team session immediately.**
- The **Submission tab is locked**: "Submission opens during the contest." Stickers upload is open now.

## What the platform is

"IOAI Simulation Console · Team Challenge" (title: **IOAI Lab**) — a lobby that hands each country a
**cloud GPU remote desktop** (streamed in the browser) running the **ioailab** simulation stack on
**NVIDIA Isaac Sim / IsaacLab** with the **Galbot G1 humanoid robot**. Login is the shared per-country
account; **only one login can be active at a time**, so the whole team works in one session.
UI is EN/中文; a "?" button (bottom-right of every page) opens the Player User Guide; full guide at `/doc`.

## Platform mechanics (from the Player User Guide)

**Flow:** Sign in → Lobby (shows time remaining + availability window in Almaty time and your local time)
→ Enter remote desktop (queues + boots your dedicated GPU desktop, 10–30 s) → work → End session.

**Time rules (memorize these):**
- Time is allotted by the committee. **The countdown starts the moment you enter** and runs whether or not
  you're working. Auto-recycles when due.
- Enter button is disabled when: no time remaining · window not started · window ended · committee disabled connections.
- **Do not background the browser tab for more than a minute** — the session may be recycled.
- **Ending a session is irreversible** — desktop stops, recycles, and anything not saved externally is lost.
  Submit/save before ending. HUD clock turns red at ≤ 5 min.

**In-session HUD (floating panel, top-right, draggable):** time remaining · RTT/FPS/Mbps network stats ·
**File transfer** (move files between your machine and the cloud desktop) · **Submission** · End session.

**Submission (opens during the contest only):**
- Submit **from inside the session** via HUD → Submission. Lobby only shows history.
- Put results in the submission folder (default path pre-filled by the committee, e.g.
  `/home/ioai-sg-005/ioailab/answer`), confirm, tick acknowledgement, submit.
- Transfer runs **server-side** — closing the page/ending the session does NOT interrupt it.
- One submission at a time; **don't touch the folder while a submission runs**; failed submissions can be retried;
  any Completed submission can be downloaded back to verify what was delivered.

**Stickers (open NOW):** design a robot sticker in the **Galbot Logo Editor at developer.galbot.com**
("Sticker design" entry), export, upload SVG/ZIP ≤ 10 MB in the lobby Stickers tab. Committee reviews each
upload (Pending/Approved/Rejected; resubmit allowed). The editor's second entry "Edit → Isaac" exports an
appearance bundle (apply_logo.py + decals/ + textures/) you can apply to the robot in Isaac Sim locally —
cosmetic only, nothing to do with scoring.

## The ioailab stack (docs at simulation.galbot.com/lab-docs — mdBook, summarized)

> This is the software you drive on the cloud desktop. Source: https://git.galbot.com/astra-synth/ioailab
> (mirror repo announced: https://github.com/galbot-ioai/ioailab — "[IOAI 2026 Team Challenge] The official
> simulation platform", currently just a stub README).

**Core loop — every workflow is the same 4 lines:**
```python
from ioailab.agents import CuroboPlannerAgent
from ioailab.envs import make_env

env = make_env("GalbotG1-PickCube-v0", num_envs=1)
agent = CuroboPlannerAgent.from_task("GalbotG1-PickCube-v0")
dataset = env.collect(agent=agent, episodes=1, path="data/demos.hdf5")
```

**Registered task IDs (G1 robot):**
| Task ID | What |
|---|---|
| `GalbotG1-Reach-v0` | left-arm reaching |
| `GalbotG1-PickCube-v0` (+ `-Teleop-v0`, `-Mimic-v0`) | pick up a cube (the reference/tutorial task) |
| `GalbotG1-StackCube-v0` | stack cubes |
| `GalbotG1-BaseNav-v0` | mobile-base navigation |
| `GalbotG1-PickToShelf-v0` (+ `-Pick/-Nav/-Place-v0` components) | coherent pick → navigate → place |
| `GalbotG1-SortToShelf-v0` (+ components) | sort objects to shelf; `--sorting-object` ∈ red_cube, blue_cuboid, yellow_cylinder, green_cylinder |

**Agent types (all interchangeable, all return full IsaacLab action tensors):**
`CuroboPlannerAgent` (cuRobo v2 motion-planning expert — generates demos for free!), `PolicyAgent`
(checkpoint replay/eval), `TeleopAgent` (GP001 device), `TaskFlowAgent` (dispatches per-phase agents in
compound tasks), `SequenceAgent`, `GoalNavAgent`/`ProportionalNavAgent`/`TrajectoryNavAgent` (navigation).

**The intended competition pipeline (numbered examples, run in order):**
```
examples/01_collect.py   # collect expert demos (cuRobo planner) → HDF5
examples/02_mimic.py     # expand dataset with IsaacLab Mimic (36 eps from few demos)
examples/03_train.py     # train robomimic **Diffusion Policy** on the demos
examples/04_eval.py      # evaluate the checkpoint (env.evaluate → metrics)
examples/05_custom_agent.py          # write your own BaseAgent
examples/06_collect_component_task.py # per-phase collection (Pick/Nav/Place presets)
examples/07_compound_task.py          # run the full long-horizon task
```
This is **exactly the Home Task 2 (Robot Delivery / behavioral cloning) pattern scaled up**:
collect expert data → (augment) → imitation-learn → evaluate. Compound tasks add phase logic
(pick success → nav phase → place success → episode success; per-env rows advance independently).

**Environment details worth knowing:**
- Docker-first: `make shell` (headless) / `make shell-gui` (GUI Isaac Sim). Host `/home/ioai-sg-005/ioailab`
  is mounted as `/workspace/ioailab` inside the container — container paths, not host paths, in scripts.
- Cameras: G1 mounts `front_head`, `left_wrist`, `right_wrist`; read via
  `env.scene["left_wrist_rgb_camera"].data.output["rgb"]`.
- Data: HDF5 collection, Mimic expansion, robomimic Diffusion Policy training, LeRobot v3 export,
  YOLO-seg dataset generation from task scenes.
- Scenario YAMLs = reset-state overlays to start a component task mid-story (e.g. Place starting with
  object already held).

## What this means for our prep (ASSUMED, but strongly indicated)

1. **The Team Challenge round (Aug 3, 14:00–19:00) will be: drive the G1 in ioailab tasks, collect data,
   train a policy, submit results from the desktop's answer folder.** The 480-min per-session cap ≈ the
   5-h contest slot.
2. **Practice the pipeline vocabulary now** even without the platform: robomimic Diffusion Policy,
   HDF5 demos, Mimic augmentation, `env.collect`/`env.evaluate` — plus our Home Task 2 drill is directly relevant.
3. **Meeting note (Jul 22): on-site resources = 1 GPU slot, 18 GB RAM total** — keep num_envs small,
   don't load giant models; know how to run headless.
4. If the practice window reopens: run `examples/01_collect.py` → `03_train.py` → `04_eval.py` on PickCube
   end-to-end once as a team; that alone removes most contest-day friction. Assign one driver (single login),
   others navigate via screen share.
5. Optional but fun: submit a Zimbabwe sticker design (open now, committee-reviewed).
