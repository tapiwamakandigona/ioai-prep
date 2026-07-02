"""The three REAL IOAI 2026 At-Home tasks — deepest pages on the site."""
from build import chat, vs

# ============================================================ TASK 1
night_watch = {
    "slug": "night-watch", "group": "2026", "emoji": "🌃",
    "title": "Operation Night Watch",
    "one_liner": "Teach an audio model 13 new sounds without it forgetting the 16 it already knows.",
    "tags": ["Audio", "Transformers", "Continual learning", "Hugging Face"],
    "difficulty": "★★★☆ deep-learning heavy",
    "sections": {},
}

night_watch["sections"]["task"] = """
<p>You are given a deployed sound-recognition model — an <b>Audio Spectrogram Transformer (AST)</b> — that already
recognizes <b>16 sound classes</b> (city sounds). Your city now needs it to also recognize <b>13 new classes</b>:
chainsaws, gunshots, and four insect species among them. The catch: after adding the new classes, the model
will be tested on <b>all 29 classes together</b>, and old and new count equally.</p>
<table>
<tr><th>Input</th><td>5-second mono audio clips, 16 kHz (.wav files)</td></tr>
<tr><th>Output</th><td>One of 29 class labels per clip</td></tr>
<tr><th>Training data</th><td><code>train.csv</code> — a small <i>retained</i> subset of the old 16 classes · <code>fine_tune.csv</code> — the 13 new classes, imbalanced (24–60 clips each)</td></tr>
<tr><th>Metric</th><td><code>Score = ½ · Accuracy(old 16) + ½ · Accuracy(new 13)</code> on a hidden 29-class test set</td></tr>
<tr><th>Compute</th><td>Free Colab T4 is enough</td></tr>
</table>
<div class="callout warn"><div class="co-title">The trap in the metric</div>
The 50/50 weighting is the whole game. If you fine-tune only on new sounds, the model learns them fast — and
<b>destroys</b> the old 16 classes within a few hundred training steps. New-class accuracy 90%, old-class accuracy 10% → score ≈ 50.
Keeping BOTH high is the actual exam. This failure mode has a name: <b>catastrophic forgetting</b>.</div>
"""

night_watch["sections"]["baseline"] = """
<p>The notebook walks you through: loading the pretrained AST from Hugging Face
(<code>ASTForAudioClassification</code>), turning waveforms into 128-band log-mel spectrograms with the
feature extractor, and running the standard fine-tuning loop on the new data. Structure:</p>
<ol>
<li><b>Feature extraction</b> — waveform → spectrogram "image" → 16×16 patches → 12 transformer layers (~86M params) → tiny linear classification head.</li>
<li><b>The naive path</b> (shown on purpose): replace the 16-way head with a 13-way head and fine-tune on <code>fine_tune.csv</code> only. Result: new classes learned, old classes obliterated. The notebook <i>wants</i> you to watch this happen.</li>
<li><b>Diagnostics provided</b> — per-class accuracy, confusion matrix, t-SNE of embeddings, audio players so you can listen to mistakes.</li>
</ol>
<p>The stated limitations (= your to-do list): the naive approach forgets; the new data is small and imbalanced;
training the full 86M-parameter encoder is slow and risky.</p>
"""

night_watch["sections"]["solution"] = vs(
    """<ul>
<li>New 13-way head, old head thrown away</li>
<li>Fine-tunes <b>all</b> 86M parameters on new data only</li>
<li>No old data in the training mix</li>
<li>Watches accuracy on new classes only</li>
<li>Old-class knowledge collapses within a few hundred steps</li>
</ul>""",
    """<ul>
<li><b>Expand the head 16 → 29</b>: build a new linear head with 29 outputs, <i>copy the old 16 rows of weights into it</i>, initialize only the 13 new rows fresh</li>
<li><b>Experience replay</b>: every training batch mixes retained old clips with new clips (tune the ratio — start 50/50)</li>
<li><b>Freeze most of the encoder</b> (or use LoRA via <code>peft</code>): train the head + last block(s) only — faster AND less forgetting</li>
<li>Optionally: <b>knowledge distillation</b> — keep a frozen copy of the original model and penalize your new model when its outputs on old classes drift away from it</li>
<li>Verify with <b>per-class accuracy on BOTH groups</b> every epoch</li>
</ul>"""
)
night_watch["sections"]["solution"] += """
<div class="callout win"><div class="co-title">Why this works</div>
Forgetting happens because gradient updates from new data overwrite weights that encoded old knowledge.
Every fix above attacks that directly: replay keeps old gradients in the mix, freezing/LoRA limits how many weights
can be overwritten, distillation explicitly punishes drift, and copying the old head rows preserves the old
decision boundaries as the starting point.</div>
"""

night_watch["sections"]["beginner"] = """
<p><b>Analogy:</b> imagine a waiter who has memorized 16 regular customers' orders. You now ask him to memorize
13 new customers — but you drill him <i>only</i> on the new ones for a week. When an old regular walks in, he blanks.
That's catastrophic forgetting. The fixes are common sense:</p>
<ul>
<li><b>Replay</b> = while drilling new orders, keep quizzing him on a few old ones every session.</li>
<li><b>Freezing</b> = tell him "don't restructure your whole memory system, just add new entries."</li>
<li><b>Distillation</b> = keep a photo of his old notebook and check his answers against it.</li>
</ul>
<p><b>What's a spectrogram?</b> Sound is a wave. A spectrogram slices it into tiny time windows and plots which
frequencies are loud in each window — producing a 2-D picture where time runs left→right and pitch runs bottom→top.
Once sound is a picture, image models (like this transformer) can classify it. This trick — <i>"turn weird data into
an image"</i> — shows up at IOAI every single year.</p>
<p><b>What's a "head"?</b> Big pretrained models = a huge <i>encoder</i> (understands the input, 86M params here)
+ a tiny final layer, the <i>head</i>, that maps understanding → class scores. Swapping/expanding heads is cheap
surgery and an IOAI yearly ritual: the encoder already "hears" — you just re-wire what it reports.</p>
"""

night_watch["sections"]["gemma"] = """
<p>How you'd drive this on contest day with a 2000-token cap (≈120 lines of code per reply) and unlimited fresh chats.
Notice: one chat = one job, code requested in pieces, everything verified on a tiny slice.</p>
""" + chat(
    ("divider", "Chat 1 · Strategy (no code yet)"),
    ("user", "", "Task: audio classifier (AST, Hugging Face) knows 16 classes. I must add 13 new classes from a small imbalanced dataset. Metric = 0.5*acc_old + 0.5*acc_new on all 29 classes. Baseline naively fine-tunes on new data only and forgets old classes. List the 5 highest-impact fixes ordered by (score gain ÷ implementation time) for a 6-hour contest. One line each, no code."),
    ("gemma", "", "1. Expand head to 29 outputs, copy old 16 weight rows (5 min, prevents starting from zero)\n2. Experience replay: mix retained old clips into every batch ~50/50 (15 min, biggest anti-forgetting win)\n3. Freeze encoder, train head + last transformer block only (5 min, faster + less forgetting)\n4. Class-balanced sampling for the 13 imbalanced new classes (10 min)\n5. Distillation vs frozen original model on old classes (45 min, do only if time remains)"),
    ("note", "", "You now have a ranked plan. Fresh chat for each code piece."),
    ("divider", "Chat 2 · Head surgery only"),
    ("user", "", "transformers ASTForAudioClassification, loaded from a local path. Current classifier head: Linear(768, 16). Write ONLY the code to replace it with Linear(768, 29), copying the existing 16 rows of weight and bias into the first 16 outputs. Code only, max 20 lines."),
    ("gemma", "", "import torch, torch.nn as nn\n\nold_head = model.classifier.dense          # Linear(768, 16)\nnew_head = nn.Linear(768, 29)\nwith torch.no_grad():\n    new_head.weight[:16] = old_head.weight\n    new_head.bias[:16]   = old_head.bias\nmodel.classifier.dense = new_head\nmodel.config.num_labels = 29\nprint(model.classifier.dense)   # sanity check"),
    ("note", "", "VERIFY before trusting: print(model.classifier) first — the real attribute path may differ. If it errors, paste the printed module tree into a fresh chat."),
    ("divider", "Chat 3 · Replay dataset"),
    ("user", "", "I have two pandas DataFrames: old_df (16 classes, cols: path,label) and new_df (13 classes, labels 16..28). Write ONLY a PyTorch Dataset + DataLoader that samples each batch ~50% from old_df and ~50% from new_df using WeightedRandomSampler. Assume a function load_features(path) exists. Code only, max 40 lines."),
    ("gemma", "", "import pandas as pd, torch\nfrom torch.utils.data import Dataset, DataLoader, WeightedRandomSampler\n\nfull = pd.concat([old_df, new_df], ignore_index=True)\nis_old = (full.label < 16).values\nw = torch.where(torch.tensor(is_old),\n                0.5/ is_old.sum(),\n                0.5/ (~is_old).sum())\n\nclass AudioDS(Dataset):\n    def __init__(self, df): self.df = df.reset_index(drop=True)\n    def __len__(self): return len(self.df)\n    def __getitem__(self, i):\n        r = self.df.iloc[i]\n        return load_features(r.path), int(r.label)\n\nsampler = WeightedRandomSampler(w.double(), num_samples=len(full))\nloader = DataLoader(AudioDS(full), batch_size=16, sampler=sampler)"),
    ("divider", "Chat 4 · Freeze + train"),
    ("user", "", "Freeze all AST encoder params except the last transformer layer and the classifier head, then a training loop: AdamW lr=1e-4, cross-entropy, 3 epochs, print loss per epoch. Variables that exist: model, loader, DEVICE. Code only, max 40 lines."),
    ("note", "", "…Gemma returns the loop. You run it for ONE batch first (break after 1 step, print loss + logits.shape == [16, 29]) before the full run."),
    ("divider", "Chat 5 · The check that actually matters"),
    ("user", "", "Write an eval function that computes accuracy separately for labels 0-15 and labels 16-28 given (model, val_loader, DEVICE), then prints 0.5*acc_old + 0.5*acc_new. Code only, max 30 lines."),
    ("note", "", "Run after every experiment. If acc_old crashed, your replay ratio is off — raise old fraction, or freeze more."),
)

night_watch["sections"]["takeaways"] = """
<ul>
<li><b>Pattern family:</b> "frozen encoder + head surgery" (yearly ritual) + continual learning (new for 2026).</li>
<li><b>The metric defines the game.</b> Read the scoring cell before the story. 50/50 weighting = protect old knowledge at all costs.</li>
<li><b>peft/LoRA is in the contest library list</b> — that's a hint from the organizers, not an accident.</li>
<li><b>Likely Day-1 extension:</b> same AST audio setup with a twist — more/fewer retained clips, additional class batches (continual learning in multiple steps), distribution shift (noisy recordings), or a stricter compute budget. If you've tuned replay ratios once, you'll do it in minutes on Day 1.</li>
</ul>
"""

# ============================================================ TASK 2
robot = {
    "slug": "robot-delivery", "group": "2026", "emoji": "🤖",
    "title": "Robot Delivery Academy",
    "one_liner": "Teach a robot to deliver packages by copying an expert — and learn why copying is harder than it looks.",
    "tags": ["Behavioral cloning", "PyTorch", "CNN", "Imitation learning"],
    "difficulty": "★★★☆ conceptually subtle",
    "sections": {},
}

robot["sections"]["task"] = """
<p>A delivery robot lives on an <b>8×8 grid city</b>. Each episode: start somewhere, drive to the depot holding a
package, <code>pickup</code>, drive to the destination depot, <code>dropoff</code>. Walls block movement, and every
map is a bit different. You must train a model that <b>learns this behavior purely from expert demonstrations</b> —
supervised pairs of <code>observation → action</code>. Writing a path-finding algorithm (A*, BFS, planning) is
<b>explicitly forbidden</b>: they're testing whether a <i>model can learn</i> the behavior, not whether you can code a solver.</p>
<table>
<tr><th>Input (one observation)</th><td><code>grid</code>: 6×8×8 tensor (channels: walls, depots, robot, package, destination, carrying-flag) · <code>vector</code>: 13 numeric features · <code>action_mask</code>: which of the 6 actions are legal right now</td></tr>
<tr><th>Output</th><td>One action id 0–5: south / north / east / west / pickup / dropoff</td></tr>
<tr><th>Training data</th><td><code>train_demos.pkl</code> — successful expert trajectories (observation + action at each step)</td></tr>
<tr><th>Metric</th><td><b>Episode Success Rate</b>: package delivered within 120 steps, replayed in the provided simulator</td></tr>
<tr><th>Submission</th><td><code>predictions.zip</code> → <code>predictions.jsonl</code>, one line per test scenario: <code>{"layout_id": ..., "episode_seed": ..., "actions": [1,1,2,4,0,5]}</code></td></tr>
</table>
<div class="callout warn"><div class="co-title">The trap in the metric</div>
You train per-step (predict the expert's next action) but you're scored per-episode. A model that's 95% right per
step still makes ~1 error every 20 steps — and one early wrong turn puts the robot in states the expert never
visited, where it has no idea what to do. Errors <b>compound</b>. This is the classic imitation-learning lesson:
<b>action accuracy ≠ episode success</b>.</div>
"""

robot["sections"]["baseline"] = """
<p>A complete, honest baseline is provided — and its own description lists its flaws:</p>
<ol>
<li><b>Dataset:</b> flattens every observation — the 6×8×8 grid is reshaped into a 384-long vector and concatenated with the 13 features → 397 numbers.</li>
<li><b>Model:</b> a two-hidden-layer MLP (397 → 128 → 128 → 6), cross-entropy loss, Adam, 30 epochs.</li>
<li><b>Inference:</b> picks the argmax action; the <code>action_mask</code> is applied only at inference time, not during training.</li>
<li><b>Evaluation:</b> full-episode rollouts in the provided simulator, with GIF replays of episodes so you can literally watch it fail.</li>
</ol>
<p>Stated limitations (= your to-do list, verbatim from the notebook): flattening destroys spatial structure;
rare actions (<code>pickup</code>/<code>dropoff</code> occur ~2× per episode vs dozens of moves) are under-learned;
the mask isn't used in training; the architecture is deliberately small.</p>
"""

robot["sections"]["solution"] = vs(
    """<ul>
<li>Grid flattened to 384 numbers — the model can't "see" that a wall is <i>next to</i> the robot</li>
<li>MLP treats position 27 and position 28 as unrelated inputs</li>
<li><code>pickup</code>/<code>dropoff</code> drowned out by thousands of move actions</li>
<li>Trains on all logits incl. illegal actions</li>
<li>Only per-action accuracy watched during training</li>
</ul>""",
    """<ul>
<li><b>Small CNN on the 6×8×8 grid</b> (2–3 conv layers) so spatial patterns — "wall ahead", "depot two cells east" — are visible; concatenate the 13-dim vector after the conv features</li>
<li><b>Weight rare actions</b>: class weights in the loss or oversample pickup/dropoff steps</li>
<li><b>Mask during training too</b>: set illegal-action logits to −∞ so the model never wastes capacity on them</li>
<li><b>Evaluate with episode success rate</b> after every change, not accuracy — replay failures in the simulator and categorize them (lost before pickup? circling near walls? wrong dropoff?)</li>
<li>Light data augmentation if legal (e.g., exploiting grid symmetry) and longer training with early stopping on episode SR</li>
</ul>"""
)
robot["sections"]["solution"] += """
<div class="callout win"><div class="co-title">Why the CNN matters most</div>
Convolutions slide a small window across the grid, so "wall directly north of robot" produces the same feature
wherever it happens on the map. The MLP has to re-learn that fact separately for all 64 positions. Same data,
same labels — but the CNN generalizes to maps it never saw, which is exactly what the test measures.</div>
"""

robot["sections"]["beginner"] = """
<p><b>Analogy:</b> learning to drive by watching dashcam videos of a perfect driver. You learn "in this exact
situation, she turned left." Two problems: (1) if you only ever memorize photo→action pairs, you never learn the
<i>concept</i> of a road; (2) the moment you make one mistake she never made — you drift onto the shoulder — you're
in a situation that appeared in zero videos, and you panic. That's behavioral cloning and its compounding-error
problem in a nutshell.</p>
<ul>
<li><b>Why a CNN?</b> An image (or a grid) has <i>local structure</i> — nearby cells matter to each other. A CNN is a model that looks through a small sliding window, so it learns "wall next to me" once, instead of 64 times.</li>
<li><b>Why do rare actions need help?</b> If 95% of your flashcards say "drive forward," you'll answer "drive forward" to everything and still score 95% — while failing every pickup. Weighting tells the loss: the rare cards count more.</li>
<li><b>What's an action mask?</b> A list of which moves are legal right now. Using it during training is like removing impossible answers from a multiple-choice exam <i>before</i> studying.</li>
</ul>
"""

robot["sections"]["gemma"] = chat(
    ("divider", "Chat 1 · Understand the baseline (paste code, ask for reading help)"),
    ("user", "", "Beginner here. This is the Dataset + model from a baseline I must improve (behavioral cloning, 8x8 grid, 6 actions). Explain in 8 bullet points max what it does and its 3 biggest weaknesses:\n<paste the ~40 lines of Dataset + MLP code>"),
    ("gemma", "", "• Collects (observation, action) pairs from every expert trajectory step\n• Flattens the 6×8×8 grid + 13-dim vector into one 397-dim input\n• 2-layer MLP classifies the next action, cross-entropy loss\n• Action mask applied only at inference\nWeaknesses:\n1. Flattening discards spatial structure a CNN would exploit\n2. pickup/dropoff are rare classes — will be under-predicted\n3. Per-action accuracy is optimized but episode success is scored"),
    ("divider", "Chat 2 · CNN in one piece"),
    ("user", "", "Write ONLY a PyTorch nn.Module: input a (B,6,8,8) grid tensor and a (B,13) vector. Two Conv2d layers (6→32→64, 3x3, padding=1, ReLU), flatten, concat the vector, then Linear(64*64+13 → 128) → ReLU → Linear(128 → 6). Code only, max 35 lines."),
    ("gemma", "", "import torch, torch.nn as nn\n\nclass GridPolicy(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.conv = nn.Sequential(\n            nn.Conv2d(6, 32, 3, padding=1), nn.ReLU(),\n            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(),\n        )\n        self.head = nn.Sequential(\n            nn.Linear(64*8*8 + 13, 128), nn.ReLU(),\n            nn.Linear(128, 6),\n        )\n    def forward(self, grid, vec):\n        z = self.conv(grid).flatten(1)\n        return self.head(torch.cat([z, vec], dim=1))"),
    ("note", "", "Verify: x = torch.randn(2,6,8,8); v = torch.randn(2,13); print(GridPolicy()(x,v).shape) → torch.Size([2, 6]). ALWAYS this ritual before wiring it in."),
    ("divider", "Chat 3 · Rare-action weighting"),
    ("user", "", "My action labels are ints 0-5 in a list y_all. Actions 4 and 5 are rare. Give ONLY code to compute inverse-frequency class weights and use them in nn.CrossEntropyLoss. Max 10 lines."),
    ("divider", "Chat 4 · Mask in training"),
    ("user", "", "Each sample has action_mask, a (6,) 0/1 array of legal actions. Modify this line of my training step so illegal logits become -1e9 before the loss:\nloss = criterion(model(grid, vec), y)\nGive only the replacement lines."),
    ("gemma", "", "logits = model(grid, vec)\nlogits = logits.masked_fill(mask == 0, -1e9)\nloss = criterion(logits, y)"),
    ("divider", "Chat 5 · Debugging a failed episode (the real skill)"),
    ("user", "", "My per-action accuracy is 0.96 but episode success rate is only 0.55. Replays show the robot reaches the package depot but oscillates north-south next to it without pressing pickup. 3 most likely causes + fastest fix for each, no code."),
    ("gemma", "", "1. pickup under-predicted (rare class) → increase its class weight / oversample pickup steps\n2. Model can't tell 'on depot' vs 'next to depot' → check the carrying/depot channels reach the conv input correctly\n3. Deterministic argmax loops between two equal logits → add the action mask at inference and break ties, or sample from softmax with low temperature"),
)

robot["sections"]["takeaways"] = """
<ul>
<li><b>Pattern family:</b> supervised classification wearing a robot costume — plus the imitation-learning lesson (distribution drift).</li>
<li><b>The notebook's stated limitations are the answer key.</b> CNN, rare-action weighting, mask-in-training: all three are literally listed for you.</li>
<li><b>Diagnose by replaying episodes</b>, not by staring at accuracy. The simulator + GIF tools are given to you for exactly this.</li>
<li><b>Format discipline:</b> <code>predictions.jsonl</code> inside <code>predictions.zip</code>, exact field names. Submit the plain baseline's zip in the first 30 minutes.</li>
<li><b>Likely Day-1 extension:</b> the notebook calls itself the "preparatory program for the <i>Robot Training</i> task" — expect bigger maps, partial observability, noisier demos, or multi-package episodes. The CNN + weighting + mask toolkit transfers directly.</li>
</ul>
"""

# ============================================================ TASK 3
wilkins = {
    "slug": "john-wilkins", "group": "2026", "emoji": "🗄️",
    "title": "The Analytical Language of John Wilkins",
    "one_liner": "20 Questions against an LLM oracle: find 1 animal among ~1,400 in 15 yes/no questions.",
    "tags": ["LLM", "Information theory", "Strategy", "Qwen 2.5"],
    "difficulty": "★★☆☆ pure thinking — your kind of task",
    "sections": {},
}

wilkins["sections"]["task"] = """
<p>A hidden animal sits behind an oracle. The oracle is a <b>local LLM (Qwen2.5-3B-Instruct)</b> that truthfully-ish
answers yes/no questions about the hidden animal, at temperature 0 (fully deterministic). You get at most
<b>15 questions per animal</b>, the questions must come from a fixed pool (<code>questions_pool.txt</code>), and the
animal is one of <b>~1,400 candidates</b> (<code>animals_pool.txt</code>).</p>
<table>
<tr><th>API</th><td><code>interactor.ask(question)</code> → "yes"/"no" · <code>interactor.guess(animal)</code> → "correct"/"wrong" · both count against the 15-query budget</td></tr>
<tr><th>Scoring per animal</th><td><code>max(0, correct − 0.02 × queries_used)</code> — right on question 1 = 0.98, on question 15 = 0.70, never = 0</td></tr>
<tr><th>Your deliverable</th><td>A class: <code>__init__(animals_pool, questions_pool)</code> (precompute anything, free) + <code>solve(interactor)</code> (runs per animal)</td></tr>
<tr><th>Key freedom</th><td>You may run <b>your own copy of the same LLM</b> offline, without spending budget</td></tr>
</table>
<div class="callout"><div class="co-title">The information-theory heart</div>
log₂(1400) ≈ 10.5 bits. Each yes/no answer gives <i>at most</i> 1 bit — and only if the question splits the
remaining candidates ~50/50. So ~11 <i>perfect</i> questions + 1 guess fits in 15. But most questions are lopsided
("does it have a backbone?" → yes for the vast majority), yielding far less than 1 bit. Choosing the right
<i>next</i> question given everything you've learned is the entire game.</div>
"""

wilkins["sections"]["baseline"] = """
<p>Two reference points are given:</p>
<ol>
<li><b>Random baseline (the floor):</b> never asks anything, just guesses random animals 15 times. Expected score ≈ 0 (15/1400 ≈ 1% hit rate). Exists so any real strategy beats it.</li>
<li><b>Fixed-questions reference (deliberately weak):</b> precomputes, with its own LLM copy, the oracle's answer to <b>12 fixed broad questions</b> ("is it a mammal?", "can it fly?"…) for every animal → one 12-bit vector per animal. At solve time it asks the same 12 questions, then guesses the animals whose stored bit-vector is closest. It works but leaves points everywhere: the questions never adapt to what's already known, and 12 lopsided bits ≪ 10.5 good bits.</li>
</ol>
<p>The notebook then says outright: your job is (1) the <i>full</i> animal × question table, (2) <i>adaptive</i>,
information-gain question selection, (3) robustness to the oracle's occasional wrong answer.</p>
"""

wilkins["sections"]["solution"] = vs(
    """<ul>
<li>Same 12 questions for every animal, in the same order</li>
<li>Broad questions with lopsided answers (≪ 1 bit each)</li>
<li>Hard nearest-neighbor match at the end</li>
<li>One surprising oracle answer can eliminate the true animal permanently</li>
<li>Spends all 12 questions + guesses even when 3 would do</li>
</ul>""",
    """<ul>
<li><b>Precompute everything</b> in <code>__init__</code>: run your own Qwen copy over every (animal, question) pair → full binary table. Slow (~thousands of LLM calls) but completely free of budget</li>
<li><b>Adaptive greedy selection:</b> keep candidate weights; each turn pick the question whose yes/no split of the <i>remaining</i> candidates is closest to 50/50 (max expected information gain)</li>
<li><b>Soft updates, not hard filters:</b> multiply a candidate's weight by e.g. 0.15 when it disagrees with an answer instead of deleting it — one weird oracle bit can't kill the truth</li>
<li><b>Guess timing:</b> guess when one candidate holds ~most of the probability mass, or when expected gain of another question &lt; the 0.02 cost — usually around question 9–12</li>
</ul>"""
)
wilkins["sections"]["solution"] += """
<div class="callout win"><div class="co-title">Why this is beatable by a beginner</div>
There is almost no machine learning here. It's binary search + bookkeeping. The LLM calls are boilerplate
(the notebook already shows how to instantiate the Interactor with any gold animal to build your table).
The winning ingredients are careful logic and the humility to handle a lying oracle — pure thinking.</div>
"""

wilkins["sections"]["beginner"] = """
<p><b>This is "20 Questions" played perfectly.</b> When you play it with a friend, good players don't ask
"is it a platypus?" first — they ask "is it bigger than a breadbox?" because <i>either</i> answer removes half the
possibilities. That halving idea is called <b>information gain</b>, and log₂(1400) ≈ 10.5 just means: 1,400
possibilities can be halved down to 1 in about 11 perfect halvings.</p>
<p><b>The cheat code the task hands you:</b> the oracle is a deterministic robot. You can build an identical robot
at home and ask it <i>every question about every animal in advance</i> — for free. On game day you're not guessing
what the oracle will say; you're looking answers up in your own table and just narrowing down which row of the
table you're in.</p>
<p><b>The one twist:</b> the oracle is an LLM with occasionally odd beliefs (it might insist a penguin "can fly").
Your table has the same odd beliefs (same model — that's the point!), but edge cases can still mismatch. So never
<i>delete</i> a candidate on one disagreement — just make it less likely. Detective work, not courtroom verdicts.</p>
"""

wilkins["sections"]["gemma"] = chat(
    ("divider", "Chat 1 · Confirm the strategy"),
    ("user", "", "Task: identify 1 of 1400 animals via yes/no questions to a deterministic LLM oracle, 15-question budget, score = 1 - 0.02*queries. I can run the same LLM offline free. My plan: (1) precompute full animal-x-question answer table offline, (2) at solve time pick the question that best splits remaining candidates 50/50, (3) soft-downweight instead of eliminating on mismatch, (4) guess when one candidate dominates. Any flaw or improvement? Max 6 lines."),
    ("gemma", "", "Plan is sound and matches the intended solution. Improvements:\n1. Cache the table to disk — don't recompute across runs\n2. Weight information gain by current candidate weights, not raw counts\n3. Stop early: if best candidate > ~70% of total weight, guess (each extra question costs 0.02)\n4. If a guess is wrong, zero that animal's weight and continue — you still have budget"),
    ("divider", "Chat 2 · Precompute the table"),
    ("user", "", "I have Interactor(gold_animal, animals_pool, questions_pool, budget) whose .ask(q) returns 'yes'/'no' using a local LLM. Write ONLY code to build table[animal] = list of 0/1 for every question in questions_pool, for every animal in animals_pool, with tqdm and saving to table.json every 100 animals. Code only, max 30 lines."),
    ("gemma", "", "import json\nfrom tqdm import tqdm\n\ntable = {}\nfor i, animal in enumerate(tqdm(animals_pool)):\n    sim = Interactor(gold_animal=animal, animals_pool=animals_pool,\n                     questions_pool=questions_pool, budget=10**9)\n    table[animal] = [1 if sim.ask(q) == 'yes' else 0\n                     for q in questions_pool]\n    if (i + 1) % 100 == 0:\n        with open('table.json', 'w') as f:\n            json.dump(table, f)\nwith open('table.json', 'w') as f:\n    json.dump(table, f)"),
    ("note", "", "Test on animals_pool[:3] first and time it. 1400 animals × ~200 questions is hours on a T4 — start it EARLY and work on the solver while it runs. (Batch the LLM calls if too slow — ask a fresh chat how.)"),
    ("divider", "Chat 3 · The greedy solver"),
    ("user", "", "Given table (dict animal -> 0/1 list), write ONLY a solver class: keep weights w[animal]=1.0; each turn pick question index j minimizing |weighted_yes_fraction - 0.5| among unasked; ask it; multiply weights of disagreeing animals by 0.15; if top candidate weight > 0.7 * total weight OR budget nearly gone, guess top candidate; on 'wrong', set its weight to 0 and continue. Code only, max 45 lines."),
    ("note", "", "…Gemma returns ~40 lines. You dry-run it against a SIMULATED interactor (your own Interactor with a known gold animal) 20 times and print mean queries used. Expect ~10-12."),
    ("divider", "Chat 4 · Tune with numbers, not vibes"),
    ("user", "", "My solver averages 12.8 queries with 96% solve rate on dev. Score formula is solved - 0.02*queries. Is it better to guess earlier? Give the expected-score math for guessing at threshold 0.5 vs 0.7 vs 0.9 assuming my top-candidate accuracy at those thresholds is 82%/94%/98%. Short answer."),
    ("gemma", "", "E[score] ≈ P(correct at guess) − 0.02·E[queries].\n0.5: 0.82 − 0.02·9  = 0.640\n0.7: 0.94 − 0.02·11 = 0.720\n0.9: 0.98 − 0.02·13 = 0.720\n→ 0.7 and 0.9 tie; prefer 0.7 (fewer queries = more headroom for the wrong-guess recovery path). Measure on dev to confirm."),
)

wilkins["sections"]["takeaways"] = """
<ul>
<li><b>Pattern family:</b> "LLM as a budgeted component" — 2025's Concepts task had a 12,500-call judge API; 2026 has a 15-question oracle. Rule: <b>simulate offline for free, spend the budget adaptively, expect noise</b>.</li>
<li><b>The scoring formula is a strategy dial</b> (−0.02/query): compute when to stop asking; don't feel it out.</li>
<li><b>Start long-running precomputes immediately</b> and build the rest while they run — contest time management in miniature.</li>
<li><b>Likely Day-1 extension:</b> same interactor pattern, different domain (objects? words?), tighter budget, larger pool, or a noisier oracle. Your greedy-info-gain solver is nearly domain-agnostic — keep it.</li>
</ul>
"""

TASKS_2026 = [night_watch, robot, wilkins]
