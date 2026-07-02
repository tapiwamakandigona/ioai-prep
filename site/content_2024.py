"""IOAI 2024 (1st edition, Bulgaria) — compact pages: the patterns started here."""
from build import chat, vs

bobai = {
    "slug": "help-bobai", "group": "2024", "emoji": "🩹",
    "title": "Help BOBAI (fix the model)",
    "one_liner": "A model is broken or must grow new abilities — repair and extend instead of rebuilding.",
    "tags": ["NLP", "Fine-tuning", "Model repair"],
    "difficulty": "★★★☆ historical",
    "sections": {
        "task": """
<p>IOAI 2024's NLP thread: work with a language model on <b>ciphered text of an unknown language</b> — fine-tune it
for classification, then <b>extend the classifier to more classes</b> than it was trained for. You can't rely on
pretrained knowledge of the language (it's ciphered!) — the model must learn structure from the data itself.</p>
""",
        "baseline": """
<p>A standard fine-tuning setup for the original label set. Limitation by design: the head has the wrong number of
outputs the moment new classes appear, and naive re-training risks losing what was learned.</p>
""",
        "solution": vs(
            """<ul><li>Fixed-size head for the original classes</li><li>Naive full re-training when classes change</li></ul>""",
            """<ul><li><b>Head surgery:</b> expand the classification layer, preserve learned weights for old classes, initialize new rows fresh</li>
<li>Keep old-class data in the training mix to avoid forgetting</li>
<li>Sound familiar? This is 2026 Night Watch's exact skeleton, two years earlier, in text instead of audio</li></ul>"""
        ),
        "beginner": """
<p><b>The lesson that repeats every year:</b> competition models are rarely built from scratch — they're
<i>adapted</i>. Load pretrained thing → change the last layer → train carefully without destroying what works.
2024 did it with text, 2025 with chicken counting, 2026 with audio. Learn the move once.</p>
""",
        "gemma": chat(
            ("divider", "The prompt pattern for any head surgery"),
            ("user", "", "Here is the printed module tree of my model: <paste print(model)>. I need the final classification layer expanded from N to M outputs keeping existing weights. Give ONLY the surgery code for THIS structure. Max 15 lines."),
            ("note", "", "Always paste the real printed structure — attribute paths differ between models, and guessing them is the #1 way LLM code fails."),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> model repair / head surgery — a yearly ritual since the first edition.</li></ul>
""",
    },
}

hyperspace = {
    "slug": "lost-in-hyperspace", "group": "2024", "emoji": "🌌",
    "title": "Lost in Hyperspace",
    "one_liner": "Navigate embedding space itself — vectors, distances, and what 'nearby' means.",
    "tags": ["Embeddings", "Feature space"],
    "difficulty": "★★☆☆ historical",
    "sections": {
        "task": """
<p>IOAI 2024's embedding-space thread: tasks built around <b>working directly with high-dimensional vector
representations</b> — measuring similarity, navigating neighborhoods, and engineering features for a fixed model
(one 2024 ML task literally fixed the model and judged only your <i>features</i>).</p>
""",
        "baseline": """
<p>Raw features / raw embeddings fed straight to the fixed model. Limitation: the representation, not the model,
is the score bottleneck — which is the point.</p>
""",
        "solution": vs(
            """<ul><li>Raw vectors as-is</li><li>No normalization or feature thinking</li></ul>""",
            """<ul><li>Normalize, combine, and transform features; measure what actually helps via validation</li>
<li>Distances in high dimensions behave unintuitively — cosine similarity over Euclidean for embeddings</li>
<li>Feature engineering is experimentation with a scoreboard: try → measure → keep</li></ul>"""
        ),
        "beginner": """
<p><b>Why embeddings keep appearing:</b> modern AI's universal trick is turning anything (words, icons, sounds)
into vectors where geometry = meaning. Every year at least one task boils down to "embed, then do geometry."
2024 made the geometry itself the task.</p>
""",
        "gemma": chat(
            ("divider", "Typical ask"),
            ("user", "", "X is (n, 512) embeddings. Give ONLY code for L2-normalizing rows and computing the full cosine similarity matrix with numpy. Max 6 lines."),
            ("gemma", "", "import numpy as np\nXn = X / np.linalg.norm(X, axis=1, keepdims=True)\nsim = Xn @ Xn.T"),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> embeddings + similarity — the through-line of the entire olympiad.</li></ul>
""",
    },
}

cow = {
    "slug": "madarian-cow", "group": "2024", "emoji": "🐄",
    "title": "Madarian Cow (edit the weights)",
    "one_liner": "Make an image generator draw zebras when asked for giraffes — surgery inside the model.",
    "tags": ["CV", "Model editing", "Diffusion"],
    "difficulty": "★★★★ historical, most exotic",
    "sections": {
        "task": """
<p>IOAI 2024's most memorable task: edit a small Stable-Diffusion-class model (SDXL-mini) so that prompts saying
<b>"giraffe" generate zebras</b> — and in an extension, make a hydrant appear alongside cows. Not prompting — actual
<b>weight/concept editing</b> inside the model.</p>
""",
        "baseline": """
<p>The unedited generator plus scaffolding to run generations and evaluate. Limitation: the whole task IS the
modification — the baseline draws giraffes when asked for giraffes.</p>
""",
        "solution": vs(
            """<ul><li>Stock model, stock associations</li></ul>""",
            """<ul><li>Targeted editing of the text-encoder/cross-attention associations so the "giraffe" token steers toward zebra visuals</li>
<li>The general recipe: find WHERE a concept lives (which embeddings/attention weights), then change the smallest thing that flips the behavior</li>
<li>Evaluate by generating and checking — behavioral tests over theory</li></ul>"""
        ),
        "beginner": """
<p><b>Don't fear this one</b> — it's the hardest task of the easiest year, and it teaches one durable idea:
models aren't black boxes. Concepts live in inspectable, editable places (token embeddings, attention layers).
"Which smallest part do I change to alter behavior X?" is the same question behind head surgery — just deeper
inside the network.</p>
""",
        "gemma": chat(
            ("divider", "Typical ask"),
            ("user", "", "Explain in max 10 lines where the association between a text token and generated imagery lives in a Stable-Diffusion-style model, and what the smallest edit to remap token A's visual concept to token B's would be. No code."),
            ("note", "", "For exotic tasks, use Gemma as a *concept map* first, code second. One explainer chat before any code chat saves an hour of flailing."),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> model surgery, extreme edition. If 2026 Day 2 goes exotic, the meta-skill is the same: locate the concept, change the smallest thing, verify behaviorally.</li></ul>
""",
    },
}

TASKS_2024 = [bobai, hyperspace, cow]
