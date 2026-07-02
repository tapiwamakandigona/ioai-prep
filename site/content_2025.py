"""IOAI 2025 tasks — At-Home, Contest Days, GAITE extras."""
from build import chat, vs

# ------------------------------------------------ Chameleon (At-Home)
chameleon = {
    "slug": "chameleon", "group": "2025h", "emoji": "🦎",
    "title": "Chameleon",
    "one_liner": "Guess the secret word from a sequence of icons — embeddings and semantic similarity.",
    "tags": ["NLP", "Embeddings", "sentence-transformers"],
    "difficulty": "★★☆☆ great first embeddings task",
    "sections": {
        "task": """
<p>A word-guessing game: you see an <b>ordered sequence of icons</b> (each icon comes with a text description),
chosen by a "clue-giver" to hint at a secret word. Your model must predict the secret word. Example: icons for
<i>water</i> + <i>fall</i> + <i>mist</i> → "waterfall". The order and combination of clues carry meaning.</p>
<table>
<tr><th>Input</th><td>Sequence of icons with text descriptions</td></tr>
<tr><th>Output</th><td>The secret word (from a vocabulary)</td></tr>
<tr><th>Really tests</th><td>Text <b>embeddings</b> + semantic similarity: mapping words and descriptions into vector space and measuring closeness</td></tr>
</table>
""",
        "baseline": """
<p>The baseline embeds icon descriptions and candidate words with a pretrained sentence encoder
(<code>sentence-transformers</code>) and picks the candidate whose embedding is most similar (cosine) to a simple
average of the clue embeddings. Limitations: naive averaging treats clues as an unordered bag, ignores that some
clues matter more, and never adapts the embedding space to the game.</p>
""",
        "solution": vs(
            """<ul><li>Mean of clue embeddings → nearest word</li>
<li>Ignores clue order and importance</li>
<li>Off-the-shelf encoder, no task adaptation</li></ul>""",
            """<ul><li>Better pooling: weighted combination of clues (position weighting, max-sim per clue)</li>
<li>Score candidates by <b>sum of similarities to each clue</b> rather than similarity to the average — combinations like water+fall need both parts to match</li>
<li>Try stronger sentence encoders from the provided model list; ensemble two encoders' rankings</li>
<li>Validate on the provided games; inspect misses — most fixes come from reading errors, not more math</li></ul>"""
        ),
        "beginner": """
<p><b>What's an embedding?</b> A function that turns text into a list of ~400 numbers such that <i>similar meanings
get nearby numbers</i>. "dog" and "puppy" land close together; "dog" and "carburetor" don't. Once everything is a
point in space, "which word do these clues point at?" becomes geometry: measure distances (cosine similarity) and
pick the closest. That one idea — <b>embed, then compare</b> — solves Chameleon, Restroom, Concepts, and appears at
IOAI every year.</p>
""",
        "gemma": chat(
            ("divider", "Chat 1 · Recipe"),
            ("user", "", "I have clue descriptions (list of strings) and candidate words (list of strings). Using sentence-transformers (model already cached locally), write ONLY code to embed both, and rank candidates by the SUM of cosine similarities to each clue. Code only, max 25 lines."),
            ("gemma", "", "from sentence_transformers import SentenceTransformer\nimport torch\n\nmodel = SentenceTransformer('/path/to/local/model')\nE_clues = model.encode(clues, convert_to_tensor=True, normalize_embeddings=True)\nE_cand  = model.encode(candidates, convert_to_tensor=True, normalize_embeddings=True)\n\nsims = E_cand @ E_clues.T          # (n_cand, n_clues)\nscores = sims.sum(dim=1)\nbest = [candidates[i] for i in scores.argsort(descending=True)[:5]]\nprint(best)"),
            ("note", "", "Verify on 3 games where you know the answer before trusting the pipeline."),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> embeddings + cosine similarity — the most reliably recurring IOAI pattern.</li>
<li>On the real Day 1 of 2025, this at-home task evolved into <a href="concepts.html">Concepts</a> — same semantic-similarity core with an LLM judge added. Master the simple version and the extension is incremental.</li></ul>
""",
    },
}

# ------------------------------------------------ Radar (At-Home)
radar = {
    "slug": "radar", "group": "2025h", "emoji": "📡",
    "title": "Radar",
    "one_liner": "Detect humans in radar heatmaps — image classification on data that isn't photos.",
    "tags": ["CV", "CNN", "Weird data as images"],
    "difficulty": "★★☆☆ core CNN reps",
    "sections": {
        "task": """
<p>Given <b>radar range–azimuth heatmaps</b> (static and dynamic maps from a radar sensor), decide whether a human
is present. The data looks nothing like a photo — it's a 2-D intensity map — but that doesn't matter: it's a grid of
numbers, so it's an image to a CNN.</p>
<table><tr><th>Input</th><td>Radar heatmap tensors (static + dynamic channels)</td></tr>
<tr><th>Output</th><td>Human present: yes/no (classification)</td></tr>
<tr><th>Really tests</th><td>Running an image-classification pipeline on unfamiliar data; channel handling; not panicking at non-photo inputs</td></tr></table>
""",
        "baseline": """
<p>A small CNN (or simple classifier) trained on the raw heatmaps with a standard loop. Limitations: minimal
architecture, no normalization/augmentation strategy tuned to radar data, static and dynamic maps possibly
underused as complementary channels.</p>
""",
        "solution": vs(
            """<ul><li>Small CNN on raw maps</li><li>Channels handled naively</li><li>Little augmentation, default preprocessing</li></ul>""",
            """<ul><li>Stack static + dynamic maps as <b>channels of one input</b> so the network sees both views at once</li>
<li>Normalize per channel (radar intensities have very different scales than photos)</li>
<li>Transfer learning: adapt a pretrained ResNet18 — replace the first conv (accept N channels instead of 3) and final layer (2 classes)</li>
<li>Augment thoughtfully: flips may be fine, but rotations can break range/azimuth semantics — think before augmenting non-photo data</li></ul>"""
        ),
        "beginner": """
<p><b>Key mental unlock:</b> a CNN doesn't know what a photo is. It sees a grid of numbers with local structure.
Spectrograms, radar maps, satellite bands, even game boards — if nearby values relate to each other, CNN recipes
apply. IOAI loves this trick: <a href="speech-detector.html">Speech Detector</a> (spectrograms), Weather (satellite),
Night Watch 2026 (audio-as-image). Learn the ResNet transfer recipe once, reuse forever.</p>
""",
        "gemma": chat(
            ("divider", "Chat 1 · Adapt ResNet to N-channel input"),
            ("user", "", "torchvision resnet18 (weights already local). My input is a 2-channel 64x64 tensor, 2 output classes. Give ONLY the code to modify the first conv layer to accept 2 channels and the fc layer for 2 classes. Max 12 lines."),
            ("gemma", "", "import torch.nn as nn\nfrom torchvision.models import resnet18\n\nm = resnet18()\nm.load_state_dict(torch.load('resnet18.pth'))\nm.conv1 = nn.Conv2d(2, 64, kernel_size=7, stride=2, padding=3, bias=False)\nm.fc = nn.Linear(m.fc.in_features, 2)"),
            ("note", "", "Check: out = m(torch.randn(2,2,64,64)); print(out.shape) → [2,2]. Note pretrained conv1 weights are lost when replaced — fine here; you keep the pretrained deeper layers."),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> "weird data as images". The 2025 Contest Day 1 shipped a Radar v2 extension — new twist, same pipeline. If your at-home pipeline is clean, Day 1 is a re-run with edits.</li></ul>
""",
    },
}

# ------------------------------------------------ Weather (At-Home)
weather = {
    "slug": "weather", "group": "2025h", "emoji": "🌧️",
    "title": "Weather",
    "one_liner": "Predict rain from satellite images plus context features — fusing two data types in one model.",
    "tags": ["CV", "Tabular", "Multimodal fusion"],
    "difficulty": "★★★☆ fusion practice",
    "sections": {
        "task": """
<p>Predict rainfall from <b>GOES-16 satellite imagery</b> combined with <b>context features</b> (sun angle, time of
day, location). Neither source is enough alone: clouds look different at different sun angles and locations.</p>
<table><tr><th>Input</th><td>Satellite image bands + a small vector of numeric context features</td></tr>
<tr><th>Output</th><td>Rain prediction</td></tr>
<tr><th>Really tests</th><td><b>Fusing image features with tabular features</b> in one network — a pattern 2026's Robot Delivery reuses (grid + 13-dim vector)</td></tr></table>
""",
        "baseline": """
<p>Typically an image-only CNN or a features-only model. Limitation: ignores half the signal — the fusion is the point.</p>
""",
        "solution": vs(
            """<ul><li>Uses image OR features, not both</li><li>Basic CNN, default preprocessing of satellite bands</li></ul>""",
            """<ul><li><b>Two-branch network:</b> CNN encodes the image → feature vector; concatenate the context features; a small MLP head makes the prediction</li>
<li>Normalize satellite bands per channel; normalize tabular features too (models hate mixed scales)</li>
<li>Sanity baseline first: gradient boosting on context features alone — know what the "cheap" signal is worth before fusing</li></ul>"""
        ),
        "beginner": """
<p><b>Fusion in one sentence:</b> run the image through a CNN until it becomes a vector of learned features, then
just <i>staple the extra numbers onto that vector</i> (concatenate) and let a final small network combine them.
That "encode → concat → head" template is the standard way to mix images/audio/text with plain numbers, and it
appears in 2026's Robot task verbatim.</p>
""",
        "gemma": chat(
            ("divider", "Chat 1 · Two-branch skeleton"),
            ("user", "", "Write ONLY a PyTorch nn.Module: branch A = a provided encoder `enc` mapping (B,C,H,W) to (B,512); input B = (B,7) float features. Concat both, then Linear(519→64) → ReLU → Linear(64→1). Code only, max 20 lines."),
            ("note", "", "Same shape ritual: random tensors in, print output shape, then train on 100 samples to see the loss move before the full run."),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> multimodal fusion (encode → concat → head).</li>
<li>Also a lesson in <b>cheap baselines</b>: always know what tabular-only or majority-class scores before investing in the fancy model.</li></ul>
""",
    },
}

TASKS_2025H = [chameleon, radar, weather]

# ------------------------------------------------ Concepts (Day 1)
concepts = {
    "slug": "concepts", "group": "2025c", "emoji": "💡",
    "title": "Concepts (Chameleon's Day-1 extension)",
    "one_liner": "The at-home guessing game returns — now with an official LLM judge API and a call budget.",
    "tags": ["NLP", "LLM", "Prompting", "Budgeted API"],
    "difficulty": "★★★☆ shows how Day 1 extends at-home",
    "sections": {
        "task": """
<p>Contest Day 1, 2025: the Chameleon word/concept-guessing idea extended — contestants worked with hint
generation / harder guessing, and were given an <b>official LLM API proxy</b> ($10 credits ≈ 12,500 judge calls) as
part of the task. The exam: combine embeddings with <b>prompt engineering under a budget</b>.</p>
<div class="callout"><div class="co-title">Why this page matters even though you'll get different tasks</div>
It's the clearest historical proof of the At-Home → Day 1 mechanic: same core (semantic similarity), new twist
(an LLM component with a budget). 2026 will do the same thing to Night Watch, Robot Delivery, and John Wilkins.</div>
""",
        "baseline": """
<p>A working pipeline from the at-home version (embed + compare) plus starter code for calling the judge API.
Limitation: naive use burns the call budget fast, and unprompted LLM calls give noisy results.</p>
""",
        "solution": vs(
            """<ul><li>Spends judge calls freely, one candidate at a time</li><li>Vague prompts → inconsistent judgments</li></ul>""",
            """<ul><li><b>Filter cheap, judge expensive:</b> use free embeddings to shortlist candidates, spend LLM calls only on the shortlist</li>
<li>Tight, structured prompts ("Answer only YES or NO") — parseable outputs</li>
<li>Track budget in code; decide spend-per-item up front</li>
<li>Cache every (input → judgment) pair; never pay twice</li></ul>"""
        ),
        "beginner": """
<p><b>The budgeted-LLM pattern:</b> when an LLM call costs something (money, queries, time), sandwich it:
cheap tools (embeddings) narrow 1,000 options to 10, the expensive LLM picks among the 10, and a cache remembers
everything. Recognize this? It's exactly <a href="john-wilkins.html">John Wilkins</a> 2026 — precompute what's free,
spend the budget only where it decides something.</p>
""",
        "gemma": chat(
            ("divider", "Chat 1 · Budget math first"),
            ("user", "", "I have 12500 LLM judge calls, 400 test items, and a shortlist of 20 candidates per item from embeddings. Judging one candidate = 1 call. What's my per-item budget and a sensible allocation? Short answer, no code."),
            ("gemma", "", "12500/400 ≈ 31 calls/item. Allocation: judge top 10 shortlist candidates (10 calls), keep ~20 calls of headroom for re-judging ties and the hardest items. Reserve ~10% of total budget for the end."),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> LLM as a budgeted component (→ recurs as 2026's John Wilkins oracle).</li>
<li>Day 1 = at-home + one twist. Whoever mastered the at-home version spends Day 1 adapting, not learning.</li></ul>
""",
    },
}

# ------------------------------------------------ Antique (Day 2)
antique = {
    "slug": "antique", "group": "2025c", "emoji": "🏺",
    "title": "Antique",
    "one_liner": "500 rows, 5 features, some labels unknown — classical sklearn beats deep learning here.",
    "tags": ["Classical ML", "scikit-learn", "Semi-supervised"],
    "difficulty": "★★☆☆ your Week-2 checkpoint",
    "sections": {
        "task": """
<p>A <b>tiny tabular dataset</b>: 500 samples, 5 features. Labels are 1, −1, or 0 — where 0 means <i>unknown</i>.
Classify the unknowns. That's it. No images, no GPUs, no transformers.</p>
<table><tr><th>Input</th><td>500 × 5 numeric table</td></tr>
<tr><th>Output</th><td>Labels for the unlabeled rows</td></tr>
<tr><th>Really tests</th><td>scikit-learn fluency, semi-supervised thinking, and <b>not overfitting 500 rows</b></td></tr></table>
""",
        "baseline": """
<p>Train a basic classifier on the labeled rows only, predict the rest. Limitations: throws away the structure in
the unlabeled data; tiny data makes validation noisy; feature scales may be uncalibrated.</p>
""",
        "solution": vs(
            """<ul><li>Fits only on labeled rows</li><li>Single model, single train/val split</li><li>No use of unlabeled structure</li></ul>""",
            """<ul><li><b>Cross-validation, not one split</b> — with 500 rows, a single split lies to you</li>
<li>Semi-supervised tricks: <code>sklearn.semi_supervised</code> label propagation / self-training (predict unknowns, add confident ones to training, repeat)</li>
<li>Compare several cheap models (logistic regression, random forest, gradient boosting, SVM) — 5 minutes each</li>
<li>Scale features; plot them — with 5 features you can literally LOOK at the data</li></ul>"""
        ),
        "beginner": """
<p><b>Why this task exists:</b> to catch people who reach for deep learning on 500 rows. Small tabular data is
classical-ML territory: fit/predict in scikit-learn, cross-validate honestly, and exploit the unlabeled rows
(their <i>positions</i> in feature space are information even without labels — points in the same cluster probably
share a label; that intuition is "label propagation").</p>
<p><b>The muscle:</b> the sklearn workflow — <code>fit</code> → <code>predict</code> → <code>cross_val_score</code> —
which you can run in your head. This is the Week-2 checkpoint of your 30-day plan for a reason.</p>
""",
        "gemma": chat(
            ("divider", "Chat 1 · Fast model bake-off"),
            ("user", "", "sklearn: X (labeled rows, shape (n,5)), y in {-1,1}. Write ONLY code to compare LogisticRegression, RandomForest, GradientBoosting, and SVC with 5-fold cross_val_score (accuracy), with StandardScaler in a Pipeline, printing mean±std per model. Max 25 lines."),
            ("divider", "Chat 2 · Self-training"),
            ("user", "", "Now ONLY code for sklearn SelfTrainingClassifier wrapping the best model, using X_all where unknown labels are -1... wait, my unknowns are 0 and real labels are 1/-1. Handle relabeling so sklearn's convention (-1 = unlabeled) is respected. Max 20 lines."),
            ("note", "", "That mid-prompt correction is realistic — you caught a convention clash (sklearn uses -1 for 'unlabeled', the task uses 0). Noticing such traps is exactly the code-literacy the contest tests."),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> classical ML on tiny data. Deep learning is a hammer; not everything is a nail.</li>
<li><b>Trust only cross-validation</b> on small data — single-split scores swing wildly.</li></ul>
""",
    },
}

# ------------------------------------------------ Chicken Counting (Day 2)
chicken = {
    "slug": "chicken-counting", "group": "2025c", "emoji": "🐔",
    "title": "Chicken Counting",
    "one_liner": "Count chickens via density maps — with a frozen encoder you're not allowed to touch.",
    "tags": ["CV", "Model surgery", "Density estimation"],
    "difficulty": "★★★☆ pure model surgery",
    "sections": {
        "task": """
<p>Count the chickens in farm images. The organizers hand you a <b>frozen pretrained image encoder</b> — you may
not fine-tune it. Your job is to <b>design and train the decoder</b> that turns its features into a count
(via a density map that sums to the number of chickens).</p>
<table><tr><th>Input</th><td>Images → frozen encoder features</td></tr>
<tr><th>Output</th><td>Chicken count per image (via predicted density map)</td></tr>
<tr><th>Really tests</th><td>PyTorch <b>model surgery</b>: reading someone else's module, matching shapes, building your own head</td></tr></table>
""",
        "baseline": """
<p>A trivial decoder (e.g., global pooling + linear regression on the count). Limitations: throwing away spatial
information, no density-map supervision, weak on crowded images.</p>
""",
        "solution": vs(
            """<ul><li>Pool everything → regress one number</li><li>No spatial supervision</li><li>Crowded scenes fail</li></ul>""",
            """<ul><li><b>Density-map decoder:</b> a few upsampling conv layers producing a heat map whose SUM is the count — supervise with per-pixel targets built from dot annotations</li>
<li>Count = <code>density.sum()</code>; loss = MSE on maps (optionally + count loss)</li>
<li>Freeze means freeze: <code>requires_grad=False</code> and encoder in <code>.eval()</code> — verify with a param count</li>
<li>Precompute encoder features ONCE (encoder is frozen!) → decoder training becomes lightning fast</li></ul>"""
        ),
        "beginner": """
<p><b>Why density maps?</b> Counting by detecting each chicken fails when they overlap. Instead, predict a "chicken
heat" image — each bird contributes a small blob summing to 1 — and integrate the heat. 30 blobs → sum ≈ 30.</p>
<p><b>The precompute trick</b> is the big transferable lesson: if a component is frozen, its outputs never change,
so compute them once and train only the small part on top. Turns hours into minutes — and reappears everywhere
(John Wilkins' precomputed table is the same idea in disguise).</p>
""",
        "gemma": chat(
            ("divider", "Chat 1 · Feature caching"),
            ("user", "", "PyTorch: frozen encoder `enc` maps (B,3,224,224) -> (B,512,14,14). Write ONLY code to iterate a DataLoader, run enc under torch.no_grad(), and save features+targets to features.pt. Then a TensorDataset loading them. Max 25 lines."),
            ("divider", "Chat 2 · Decoder design"),
            ("user", "", "Design ONLY an nn.Module decoder: input (B,512,14,14), output a (B,1,56,56) non-negative density map. Two ConvTranspose2d upsampling steps + final 1x1 conv + ReLU. Code only, max 25 lines."),
            ("note", "", "Shape ritual: print(decoder(torch.randn(2,512,14,14)).shape) → [2,1,56,56]. Then overfit 10 images until train loss ≈ 0 — if you can't overfit 10 images, the wiring is broken (classic debugging trick)."),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> frozen encoder + trainable head — the IOAI yearly ritual (2026 Night Watch = same skeleton).</li>
<li><b>Overfit-10-samples</b> is the fastest wiring test in deep learning. Keep it in your ritual bank.</li></ul>
""",
    },
}

# ------------------------------------------------ Restroom (Day 2)
restroom = {
    "slug": "restroom", "group": "2025c", "emoji": "🚻",
    "title": "Restroom",
    "one_liner": "Match male↔female restroom icons from the same restroom — embeddings for images.",
    "tags": ["CV", "Embeddings", "Metric learning"],
    "difficulty": "★★☆☆ embeddings, visual edition",
    "sections": {
        "task": """
<p>Given restroom door icons, match each <b>male icon to the female icon from the same restroom</b> (same design
family/style). It's a matching problem: no classes to predict, just "which of these belongs with which".</p>
<table><tr><th>Input</th><td>Two sets of icon images</td></tr><tr><th>Output</th><td>A male↔female pairing</td></tr>
<tr><th>Really tests</th><td><b>Image embeddings + similarity matching</b> — the same embed-and-compare pattern as Chameleon, but visual</td></tr></table>
""",
        "baseline": """
<p>Embed icons with a pretrained vision encoder, match greedily by cosine similarity. Limitations: greedy matching
makes locally-good globally-bad pairs; raw embeddings capture "icon-ness" more than "style".</p>
""",
        "solution": vs(
            """<ul><li>Off-the-shelf embeddings</li><li>Greedy nearest-neighbor pairing</li><li>Duplicate/conflicting matches possible</li></ul>""",
            """<ul><li><b>Global assignment instead of greedy:</b> build the full similarity matrix, solve with <code>scipy.optimize.linear_sum_assignment</code> (Hungarian algorithm) — one line, guarantees a consistent 1-to-1 pairing</li>
<li>Try several encoders (CLIP-style vs ResNet features) and layers — style lives at different depths</li>
<li>Simple preprocessing: crop/binarize icons so backgrounds don't dominate similarity</li></ul>"""
        ),
        "beginner": """
<p><b>Greedy vs global:</b> greedy matching is speed-dating where the first person picks their favorite and leaves —
by the end, the remaining people get terrible matches. The Hungarian algorithm considers all pairings at once and
maximizes total happiness. In code the upgrade is literally one function:
<code>linear_sum_assignment(-similarity_matrix)</code>. Knowing that this function exists is worth real points.</p>
""",
        "gemma": chat(
            ("divider", "Chat 1 · The one-liner that wins"),
            ("user", "", "I have sim, a (n,n) numpy array where sim[i,j] = cosine similarity between male icon i and female icon j. Give ONLY code for the optimal 1-to-1 assignment maximizing total similarity, returning list of (i,j) pairs. Max 6 lines."),
            ("gemma", "", "from scipy.optimize import linear_sum_assignment\nimport numpy as np\n\nrows, cols = linear_sum_assignment(-sim)   # negate: maximize\npairs = list(zip(rows.tolist(), cols.tolist()))"),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> embeddings + similarity, plus the matching upgrade (Hungarian algorithm).</li>
<li>Encoders are interchangeable parts: text encoder for Chameleon, vision encoder here — <i>same downstream code</i>.</li></ul>
""",
    },
}

# ------------------------------------------------ Pixel (Day 2)
pixel = {
    "slug": "pixel", "group": "2025c", "emoji": "🔲",
    "title": "Pixel",
    "one_liner": "Choose the most informative pixels under a budget — probe what models actually look at.",
    "tags": ["CV", "Creative", "Model probing"],
    "difficulty": "★★★☆ open-ended thinking",
    "sections": {
        "task": """
<p>Under a strict <b>pixel budget</b>, choose which pixels of each image to keep (masking the rest) so that
a classifier can still do its job. Score depends on how well classification survives your masking.</p>
<table><tr><th>Input</th><td>Images + a pixel budget</td></tr><tr><th>Output</th><td>A pixel mask per image</td></tr>
<tr><th>Really tests</th><td>Creative reasoning about <b>where information lives in images</b> and how to probe a model's attention</td></tr></table>
""",
        "baseline": """
<p>Naive masks: random pixels, or a fixed central crop. Limitations: ignores image content entirely.</p>
""",
        "solution": vs(
            """<ul><li>Random / central pixels for every image</li><li>Content-blind</li></ul>""",
            """<ul><li><b>Saliency-guided selection:</b> use gradients (∂output/∂pixel) or occlusion tests to find pixels the classifier relies on; spend the budget there</li>
<li>Cheap classical proxy: edges/high-contrast regions (opencv) carry most information</li>
<li>Evaluate empirically: try 3 strategies on a validation slice, keep the winner — measurement beats theory in contests</li></ul>"""
        ),
        "beginner": """
<p><b>The intuition:</b> not all pixels are equal — a blank sky pixel tells you nothing; the pixel on a cat's ear
tells you a lot. "Saliency" is asking the model: <i>if I nudge this pixel, how much does your answer change?</i>
Pixels with big answers matter. Tasks like this reward experimenters: nobody knows the best strategy in advance,
so the winner is whoever tests the most ideas cheaply.</p>
""",
        "gemma": chat(
            ("divider", "Chat 1 · Gradient saliency"),
            ("user", "", "PyTorch classifier `model`, input image x (1,3,H,W), requires_grad. Give ONLY code computing pixel saliency = abs gradient of the top logit wrt x, summed over channels, then indices of the top-k pixels. Max 15 lines."),
            ("gemma", "", "x = x.clone().requires_grad_(True)\nlogit = model(x).max()\nlogit.backward()\nsal = x.grad.abs().sum(dim=1).squeeze(0)     # (H,W)\nflat = sal.flatten()\ntopk = flat.topk(k).indices\nys, xs = topk // sal.shape[1], topk % sal.shape[1]"),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> open-ended probing task — appears each year in some form; strategy beats recipe.</li>
<li>Budgeted-resource thinking again: pixels here, LLM calls in Concepts, questions in John Wilkins.</li></ul>
""",
    },
}

TASKS_2025C = [concepts, antique, chicken, restroom, pixel]

# ------------------------------------------------ Word Segmentation (GAITE)
wordseg = {
    "slug": "word-segmentation", "group": "2025g", "emoji": "🇩🇪",
    "title": "Word Segmentation",
    "one_liner": "Split German compound words character by character — sequence labeling made friendly.",
    "tags": ["NLP", "Sequence labeling", "GAITE"],
    "difficulty": "★★☆☆ GAITE-calibrated",
    "sections": {
        "task": """
<p>German glues words together (<i>Donaudampfschiff…</i>). Given a compound word, predict <b>for each character</b>
whether a split happens there — binary label per character. 94k training examples provided.</p>
<table><tr><th>Input</th><td>A word (character sequence)</td></tr>
<tr><th>Output</th><td>0/1 per character (split boundary or not)</td></tr>
<tr><th>Really tests</th><td><b>Sequence labeling</b>: classify every position, not the whole input</td></tr></table>
<div class="callout"><div class="co-title">GAITE hint culture</div>
This was a GAITE 2025 task — and like all GAITE tasks, the statement contained hints pointing at the intended
approach. Read GAITE statements twice: the organizers TELL you the plan.</div>
""",
        "baseline": """
<p>A simple per-character classifier using local context windows (the surrounding few characters). Limitations:
fixed windows miss longer dependencies; character identity alone ignores learned patterns like common word stems.</p>
""",
        "solution": vs(
            """<ul><li>Fixed context window per character</li><li>Hand-rolled features</li></ul>""",
            """<ul><li>Character embeddings + a small <b>BiLSTM or 1-D conv</b> over the sequence, sigmoid per position — the textbook sequence-labeling recipe</li>
<li>With 94k examples, even simple models train well — don't overthink capacity</li>
<li>Clever classical alternative: a vocabulary of known word parts + dynamic-programming splitting can be shockingly strong (and CPU-fast)</li></ul>"""
        ),
        "beginner": """
<p><b>Sequence labeling vs classification:</b> classification gives one answer per input ("cat or dog?"); sequence
labeling gives one answer <i>per position</i> ("split here? here? here?"). Same training loop, one change: the
output has length = input length, and the loss averages over positions. Once you see that, this task is a Week-3
exercise, not a monster.</p>
""",
        "gemma": chat(
            ("divider", "Chat 1 · Per-position model"),
            ("user", "", "PyTorch: input padded char-id tensors (B, L), vocab 60. Write ONLY an nn.Module: Embedding(60,32) → BiLSTM(32,64) → Linear(128,1), output (B, L) logits. Code only, max 20 lines."),
            ("note", "", "Loss detail worth a follow-up chat: use BCEWithLogitsLoss with a mask so PADDING positions don't contribute. Padding bugs are the #1 sequence-task trap."),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> sequence labeling (per-position prediction).</li>
<li>Big data + simple model beats small data + fancy model at contest time scales.</li></ul>
""",
    },
}

# ------------------------------------------------ Synthetic Speech Detector (GAITE)
speech = {
    "slug": "speech-detector", "group": "2025g", "emoji": "🎙️",
    "title": "Synthetic Speech Detector",
    "one_liner": "Spot AI-generated speech from spectrograms — the statement literally tells you the solution.",
    "tags": ["Audio-as-CV", "ResNet", "GAITE"],
    "difficulty": "★☆☆☆ friendliest task on this site",
    "sections": {
        "task": """
<p>Classify speech clips as real or AI-generated. The data comes as <b>Mel spectrograms already prepared as
tensors</b> — the audio has been turned into images for you.</p>
<table><tr><th>Input</th><td>Mel spectrogram tensors</td></tr><tr><th>Output</th><td>Real vs synthetic (binary)</td></tr>
<tr><th>Really tests</th><td>Whether you read the statement: it says treat it as image classification, <b>ResNet18 is enough, ~1 epoch</b></td></tr></table>
""",
        "baseline": """
<p>A starter classification pipeline on the spectrogram tensors. The GAITE statement itself supplies the plan —
this task is the purest example of "the hints are the intended solution."</p>
""",
        "solution": vs(
            """<ul><li>Under-trained starter model</li><li>Spectrogram channels/normalization handled naively</li></ul>""",
            """<ul><li>Do what the statement says: <b>ResNet18, adapt input channels, ~1 epoch</b></li>
<li>Normalize spectrograms; check class balance; hold out a validation split</li>
<li>Time saved here goes to harder tasks — recognizing an "easy by design" task IS the skill</li></ul>"""
        ),
        "beginner": """
<p><b>Your Week-3 checkpoint task.</b> It combines everything gently: spectrograms (weird data as images),
transfer learning (ResNet18 recipe), a binary metric, and a submission file. When this takes you under two hours
end-to-end, your PyTorch literacy is contest-ready.</p>
""",
        "gemma": chat(
            ("divider", "Chat 1 · Full recipe in 3 asks"),
            ("user", "", "Ask 1: dataloaders from tensors X (N,1,128,256), y (N,) — ONLY the Dataset/DataLoader code.\nAsk 2 (fresh chat): resnet18 adapted to 1-channel input, 2 classes — ONLY the model surgery.\nAsk 3 (fresh chat): training loop, 1 epoch, AdamW, print val accuracy — ONLY the loop."),
            ("note", "", "Three fresh chats, three small pastes, assemble in your notebook. This is the chunked-prompting rhythm to make automatic before contest day."),
        ),
        "takeaways": """
<ul><li><b>Pattern family:</b> spectrograms as images + transfer learning (direct warm-up for 2026 Night Watch).</li>
<li><b>Points-per-hour triage:</b> bank easy tasks fast, spend the surplus where it pays.</li></ul>
""",
    },
}

TASKS_2025G = [wordseg, speech]
