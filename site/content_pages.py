"""Landing page, Gemma playbook, and 30-day plan pages."""
from build import esc

def index_body(tasks):
    def card(t):
        return (
            f'<a class="tcard" href="tasks/{t["slug"]}.html"><span class="t-emoji">{t["emoji"]}</span>'
            f'<h3>{esc(t["title"])}</h3><p>{esc(t["one_liner"])}</p>'
            f'<div class="t-meta">{esc(t["difficulty"])}</div></a>'
        )
    groups = {
        "2026": "🚨 The real 2026 Home Tasks — start here",
        "2025h": "2025 At-Home Round — practice material",
        "2025c": "2025 Contest Days",
        "2025g": "2025 GAITE extras — friendliest tasks",
        "2024": "2024 — where the patterns started",
    }
    grids = ""
    for gid, gtitle in groups.items():
        cards = "".join(card(t) for t in tasks if t["group"] == gid)
        grids += f'<div class="section-band">{gtitle}</div><div class="grid-cards">{cards}</div>'

    return f"""
<div class="hero">
<div class="crumb">GAITE · Astana, Kazakhstan · August 2–8, 2026</div>
<h1>The IOAI Field Manual</h1>
<p>Every IOAI task from 2024 to the <b>actual 2026 home tasks</b>, decoded for someone starting from zero:
what the task really asks, how the given baseline works, how the winning solution differs, and exactly how you'd
get there driving <b>Gemma 4 under a 2000-token limit</b>.</p>
<div class="hero-stats">
<div class="stat"><b>16</b><span>tasks decoded</span></div>
<div class="stat"><b>3</b><span>real 2026 tasks</span></div>
<div class="stat"><b>6h</b><span>per contest day</span></div>
<div class="stat"><b>2000</b><span>tokens per Gemma reply</span></div>
</div>
</div>

<div class="section-band">How every task page works</div>
<p>Each page has the same six sections: <b>📜 the task in plain English</b> (story stripped, metric extracted) ·
<b>🔧 the baseline you're given</b> · <b>🚀 baseline vs. solution</b> side by side · <b>🧒 a from-zero explanation</b>
of the concepts · <b>💬 a simulated Gemma 4 playthrough</b> — the literal chats that would solve it under the
token cap · <b>🎯 takeaways</b> and likely Day-1 extensions.</p>

<div class="section-band">The 8-step solution flow (works on every task)</div>
<ol class="flow-steps">
<li><b>Metric first.</b> Find the scoring cell before reading the story. The metric defines the game.</li>
<li><b>Run the baseline untouched → submit it.</b> Points on the board; format verified; scores are normalized against the baseline, so any improvement counts.</li>
<li><b>Diagnose before improving.</b> Confusion matrix, failed-episode replays, per-class accuracy — find <i>where</i> points are lost.</li>
<li><b>Read the hints; rank fixes by points-per-hour.</b> GAITE statements contain the intended solution.</li>
<li><b>One change at a time, measure each.</b> Keep a scrappy log: change → score.</li>
<li><b>Name the lesson.</b> Every task secretly teaches one failure mode (forgetting, drift, noisy oracle). Name it and you know the solution family.</li>
<li><b>Guard the clock.</b> Baseline submitted in 30 min; freeze experiments 45 min before the end.</li>
<li><b>Never leave a task at zero.</b></li>
</ol>

{grids}

<div class="section-band">Guides</div>
<div class="grid-cards">
<a class="tcard" href="gemma.html"><span class="t-emoji">💬</span><h3>Gemma 4 Playbook</h3>
<p>Chunked prompting under the 2000-token cap, one-chat-per-job, verification rituals, the contest-day prompt bank.</p>
<div class="t-meta">read before any mock</div></a>
<a class="tcard" href="plan.html"><span class="t-emoji">🗓️</span><h3>The 30-Day Plan</h3>
<p>July 3 → August 1, day by day: Python literacy → sklearn → PyTorch → the real 2026 tasks under contest conditions.</p>
<div class="t-meta">your daily map</div></a>
</div>
"""


def gemma_body():
    return """
<header class="task-head"><div class="crumb">Guide</div>
<h1>💬 The Gemma 4 Playbook</h1>
<p class="tagline">2000 output tokens per reply. Unlimited new chats. Here's how that becomes a superpower.</p></header>

<section class="sec"><h2>The two constraints, decoded</h2>
<ul>
<li><b>2000 output tokens ≈ ~120 lines of code or ~1200 words.</b> Long answers get cut off mid-line. So never ask for "the whole solution" — ask for <i>pieces</i>.</li>
<li><b>Unlimited new chats = unlimited retries with a clean slate.</b> Fresh chats are free. Use them aggressively; never argue with a confused model in a long thread.</li>
</ul></section>

<section class="sec"><h2>Core rules</h2>
<ol class="flow-steps">
<li><b>Chunk everything.</b> Ask for ONLY the Dataset class → ONLY the model → ONLY the training loop → ONLY the submission writer. Magic phrases: <i>"Code only, no explanation." · "Max 30 lines." · "Continue exactly from this line: …"</i> (when cut off).</li>
<li><b>One chat = one job.</b> Explainer chat, bug-fixer chat, strategy chat, API-lookup chat. Contexts stay clean, answers stay sharp.</li>
<li><b>Paste context, always.</b> Gemma can't see your screen. Every prompt: the task in 1–2 sentences, the smallest relevant code, exact error/traceback, tensor shapes, one specific question.</li>
<li><b>Verify everything.</b> Read the code before running (does it use variables that exist?) → run on a tiny slice → <code>print(x.shape)</code> liberally → if a fix fails twice, fresh chat with the new traceback.</li>
<li><b>You are the manager.</b> You choose the plan (the 8-step flow); Gemma writes boilerplate, fixes bugs, explains baselines, and recalls API signatures.</li>
</ol></section>

<section class="sec"><h2>Contest-day prompt bank</h2>
<pre>“Summarize this task statement in 5 bullets: input, output, metric, submission format: &lt;paste&gt;”
“Baseline does X and scores Y. List 5 improvements ordered by (impact ÷ time) for a 6-hour contest.”
“Explain what this code does, line by line, for a beginner: &lt;paste baseline chunk&gt;”
“This code raises this error. Code + full traceback below. Give the minimal fix only.”
“Rewrite this training loop to add early stopping on validation loss. Change nothing else.”
“My model overfits (train 0.99 / val 0.70). The 3 fastest fixes for a CNN in torch?”
“Write code to save predictions as CSV, one 0/1 per line, no header, from tensor preds.”
“How do I load a pre-cached Hugging Face model from a local path, no internet?”</pre></section>

<section class="sec"><h2>Time economics (6 hours, 3 tasks)</h2>
<ul>
<li><b>First 5 min:</b> read all 3 statements; rank by expected points-per-hour.</li>
<li><b>First 30 min per task:</b> baseline running and submitted.</li>
<li><b>While models train:</b> a Gemma chat plans the next improvement in parallel.</li>
<li><b>Last 45 min:</b> freeze experiments; verify formats; confirm your best submissions are the selected ones.</li>
</ul>
<div class="callout win"><div class="co-title">Practice this NOW</div>
During the 30-day prep, study with any free chatbot but impose contest rules on yourself: pretend replies are
capped, ask in chunks, fresh chat per topic, verify by running. By August, driving an LLM under constraints is
muscle memory. Every task page's 💬 section on this site is a rehearsal script.</div></section>
"""


def plan_body():
    return """
<header class="task-head"><div class="crumb">Guide</div>
<h1>🗓️ The 30-Day Plan <span style="font-size:.55em;opacity:.6">(v2 · baseline-first)</span></h1>
<p class="tagline">July 3 → August 1. You'll never start from a blank cell — so we don't train like you will.</p></header>

<section class="sec"><h2>Why v2? Two facts change everything</h2>
<ul>
<li><b>Every IOAI task ships a runnable baseline.</b> Contest day begins with working code that already scores points.</li>
<li><b>Gemma 4 writes code for you.</b> You never need to <i>author</i> code — you need to read, assemble, verify, and direct.</li>
</ul>
<div class="callout"><div class="co-title">The Baseline Improvement Loop (BIL) — the only drill that matters</div>
<b>1.</b> Run the baseline untouched → confirm score &amp; submission format &nbsp;<b>2.</b> Understand every cell
(LLM explains, you re-explain) &nbsp;<b>3.</b> Diagnose <i>where</i> points are lost (confusion matrix, failed cases)
&nbsp;<b>4.</b> Ask Gemma for ONE targeted change (chunked, ≤30 lines) &nbsp;<b>5.</b> Verify → run → measure →
keep or revert &nbsp;<b>6.</b> Repeat. <br><br>The 30 days = this loop on progressively harder baselines. The two
skills being trained: <b>diagnosis</b> and <b>Gemma-driving</b>. Python literacy exists only to serve them.</div>
<p><b>Daily rhythm:</b> every session is LLM-paired <b>under contest rules from Day 1</b> — one chat = one job,
chunked asks ("code only, max 30 lines"), pretend replies are capped, verify by running. ~50% baselines,
~30% LLM-paired reading, ~20% journaling + growing your snippets file. Everything in Kaggle/Colab.</p>

<div class="week"><h3>Week 1 · Days 1–7 — Read code before you write code</h3>
<p><b>Day 1 is demystification day:</b> press "Run All" on a finished Titanic notebook, then run the <i>real 2026
<a href="tasks/night-watch.html">Night Watch</a> baseline</i> untouched. You understand nothing yet — fine. Lesson:
the baseline already works; contest day starts from here. Days 2–3: Python <i>by interrogation</i> — paste real
notebook cells into an LLM ("explain line by line"), break the notebook on purpose, read tracebacks bottom-up.
Day 4: numpy + the <code>print(x.shape)</code> ritual. Days 5–6: pandas by asking→reading→running→explaining back.
<b>Checkpoint Day 7:</b> explain every cell of an unseen notebook; make 3 modifications with predicted outcomes.</p></div>

<div class="week"><h3>Week 2 · Days 8–14 — The sklearn improvement loop</h3>
<p>Day 8: metric-first reading + first full BIL on Titanic. Day 9: metrics — the confusion matrix is your diagnosis
tool. Day 10: validation. Day 11: the 4-model bake-off via ONE chunked prompt. Day 12: feature engineering as loop
iterations (change → measure → keep/revert). Day 13: embeddings as a black box + cosine similarity (IOAI's favorite
pattern — usable without understanding transformers). <b>Checkpoint Day 14: <a href="tasks/antique.html">Antique</a></b>
— full BIL: baseline → diagnose → bake-off → self-training. Pass = beat the baseline and say <i>why</i>.</p></div>

<div class="week"><h3>Week 3 · Days 15–21 — PyTorch = surgery, not authorship</h3>
<p>Day 15: tensors + shapes. Day 16: the sacred training loop, <i>assembled from 3 chunked asks</i> (data / model /
loop), then explained back. Day 17: <b>surgery drills</b> — head swap, backbone freeze (+ param-count check), loss
change, class weights: four moves that solve half of IOAI history. Day 18: the transfer-learning recipe. Day 19:
training hygiene + the wiring tests (overfit-10-samples, tiny-slice-first). Day 20: embeddings + Hungarian matching.
<b>Checkpoint Day 21: <a href="tasks/speech-detector.html">Speech Detector</a> in under 2 hours, contest rules,
zero hand-authored code.</b></p></div>

<div class="week w4"><h3>Week 4 · Days 22–28 — THE REAL 2026 TASKS + dress rehearsal</h3>
<p><b>Hard rule from here:</b> only whitelisted docs + one LLM chat with self-imposed 2000-token discipline — every
line of code comes from the baseline or from Gemma. Days 22–23: <a href="tasks/night-watch.html">Night Watch</a>
(watch forgetting happen, then head expansion + replay). Day 24: <a href="tasks/robot-delivery.html">Robot
Delivery</a> (CNN + rare actions + mask). Day 25: <a href="tasks/john-wilkins.html">John Wilkins</a> (precompute +
info gain). <b>Day 26: full 6-hour mock</b> on 3 unseen 2025 tasks — baselines submitted in the first 30 min each?
Day 27: post-mortem, grow snippets + prompt bank. Day 28: second pass on your weakest 2026 task.</p></div>

<div class="week"><h3>Days 29–30 — Package & rest</h3>
<p>All three 2026 submissions in exact required formats. Reread the rules and the
<a href="gemma.html">Gemma playbook</a>. Sleep. No new theory.</p></div>

<div class="callout win"><div class="co-title">Milestones (honest self-check)</div>
<b>W1:</b> I can read an unfamiliar notebook, explain every cell, and I've already run a real 2026 baseline ·
<b>W2:</b> I can run the full improvement loop on a tabular baseline and beat it ·
<b>W3:</b> I can do model surgery using only chunked Gemma-style asks ·
<b>W4:</b> 6-hour mock → 3 valid submissions, each beating baseline, zero hand-authored code.<br><br>
<b>If you fall behind, never cut:</b> the checkpoints (Days 14, 21), surgery drills (17–18), the three 2026 tasks,
the mock (26).</div>
</section>
"""
