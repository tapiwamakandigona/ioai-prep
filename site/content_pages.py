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
<h1>🗓️ The 30-Day Plan</h1>
<p class="tagline">July 3 → August 1. Code literacy, not code authorship — then the real 2026 tasks.</p></header>

<section class="sec">
<div class="callout"><div class="co-title">The philosophy</div>
You never need to write models from a blank cell — every IOAI task ships a baseline. You DO need to <b>read</b>
baselines, <b>assemble</b> Gemma's fragments, and <b>debug</b> shapes and tracebacks. Weeks 1–3 build exactly that
literacy; Week 4 spends it on the real 2026 tasks. Daily: ~2–4 focused hours beat 8 distracted ones.</div>

<div class="week"><h3>Week 1 · Days 1–7 — Python + data literacy</h3>
<p>Kaggle Learn: Python → pandas → numpy basics. Goal: read/manipulate a DataFrame without fear, slice arrays,
write functions. Everything in Kaggle/Colab notebooks (that's the contest environment's cousin). Daily ritual:
one chatbot "explain like I'm 15" session on the day's concept.</p></div>

<div class="week"><h3>Week 2 · Days 8–14 — scikit-learn workflow</h3>
<p>fit/predict, train/val split, cross-validation, accuracy/F1/AUC, RandomForest & gradient boosting, pipelines.
<b>Checkpoint: the <a href="tasks/antique.html">Antique</a> task</b> — tiny data, pure sklearn. If you can run the
model bake-off + self-training there, Week 2 is done.</p></div>

<div class="week"><h3>Week 3 · Days 15–21 — PyTorch literacy</h3>
<p>Dataset/DataLoader, nn.Module, the training loop, transfer learning (the ResNet recipe), embeddings + cosine
similarity. <b>Checkpoint: <a href="tasks/speech-detector.html">Synthetic Speech Detector</a></b> end-to-end in
under two hours. Learn the debugging rituals: shape printing, overfit-10-samples, tiny-slice-first.</p></div>

<div class="week w4"><h3>Week 4 · Days 22–28 — THE REAL 2026 TASKS + mock contest</h3>
<p>Days 22–23: <a href="tasks/night-watch.html">Operation Night Watch</a> (watch catastrophic forgetting happen,
then fix it). Day 24: <a href="tasks/robot-delivery.html">Robot Delivery</a> (CNN + rare actions + mask).
Day 25: <a href="tasks/john-wilkins.html">John Wilkins</a> (precompute + info gain).
<b>Day 26: full 6-hour mock</b> on three unseen 2025 tasks, contest rules enforced. Day 27: review + grow your
snippets file. Day 28: second pass on your weakest 2026 task.</p></div>

<div class="week"><h3>Days 29–30 — Package & rest</h3>
<p>All three 2026 submissions in exact required formats. Reread the rules and the
<a href="gemma.html">Gemma playbook</a>. Sleep. No new theory.</p></div>

<div class="callout win"><div class="co-title">If you fall behind</div>
Priority order: sklearn workflow → PyTorch reading fluency → the three 2026 home tasks → everything else.
The 2026 tasks are non-negotiable; a skipped Day-14 exercise is.</div>
</section>
"""
