# Gemma 4 Playbook — Turning Your Chatbot Into a Superpower

Your GAITE setup: **Gemma 4, max 2000 output tokens per query, unlimited new chats, no external internet except docs sites.**
Gemma 4 is Google's 2026 open-model family (released March–June 2026; sizes incl. E2B, E4B, 26B-A4B, 31B, 12B-Unified) — very strong at code, reasoning and instruction-following. Which exact variant IOAI deploys will be announced pre-contest; assume "capable but not a genius" and verify everything it gives you.

## The two constraints and what they mean
1. **2000 output tokens ≈ ~120 lines of code or ~1200 words.** Long answers get cut off mid-sentence. So: never ask for "the whole solution" — ask for *pieces*.
2. **Unlimited new chats** = unlimited retries and no context pollution. Fresh chats are free; use them aggressively.

## Core strategies

### 1. Chunk everything (beat the 2000-token cap)
- ❌ "Write a full training pipeline for this task"
- ✅ Ask in stages: (1) "Give me ONLY the Dataset class", (2) "Now ONLY the training loop", (3) "Now ONLY the inference + CSV writing code".
- Magic phrases: *"Code only, no explanation."* / *"Be concise."* / *"Continue exactly from this line: …"* (if cut off, paste the last line and ask it to continue).
- Ask for functions one at a time and assemble them yourself in Jupyter.

### 2. One chat = one job
Start a fresh chat per subproblem. Long conversations make models drift and waste your reading time. Good chat types:
- **Explainer chat:** "Explain what this code does, line by line, for a beginner: `<paste baseline chunk>`"
- **Bug-fixer chat:** "This code raises this error. Here is the code + full traceback. Give the minimal fix only."
- **Strategy chat:** "Task: <2-3 sentence summary>. Baseline does X and scores Y. List 5 improvements ordered by (impact ÷ implementation time) for a 6-hour contest."
- **API-lookup chat:** "What are the arguments of `sklearn.model_selection.train_test_split`? Short answer." (faster than browsing docs)

### 3. Paste context, always
Gemma can't see your screen or files. Every prompt should include: the error message, the relevant code snippet, tensor shapes, and what you already tried. Template:
```
Task: [1-2 sentences]
Code: [paste the smallest relevant chunk]
Error/problem: [paste full traceback or wrong behavior]
Data shapes: X_train (500, 5), y in {-1, 0, 1}
Question: [one specific question]
Answer with code only, max 40 lines.
```

### 4. Make it your teacher during prep AND your intern during the contest
- **Before the contest** (use any chatbot): "Explain like I'm 15", "Quiz me on train/val/test splits", "Show me the simplest possible PyTorch training loop and explain each line."
- **During the contest:** you are the manager. You decide the plan; Gemma writes boilerplate, fixes bugs, explains baseline code, recalls API signatures. Never paste-and-pray: run every snippet on a tiny slice of data first.

### 5. Verification ritual (LLMs lie confidently)
1. Read the code before running — does it use variables that exist?
2. Run on a tiny subset (e.g., first 100 rows / 2 batches) before full training.
3. `print(x.shape)` liberally; shape mismatches are 80% of deep-learning bugs.
4. If Gemma's fix fails twice, open a **fresh chat** and re-ask with the new traceback — don't argue with a confused model in a long thread.

### 6. Contest-day prompt bank (memorize these patterns)
- "Summarize this task statement in 5 bullet points: what is the input, output, metric, and submission format? `<paste>`"
- "Given metric = F1 on binary labels, what naive baseline should I try first?"
- "Rewrite this training loop to add early stopping on validation loss. Change nothing else."
- "My model overfits (train acc 0.99, val acc 0.70). List the 3 fastest fixes for a CNN in torch."
- "Write code to save predictions as a CSV with one 0/1 per line, no header, from tensor `preds`."
- "How do I load a pre-cached Hugging Face model from a local path with transformers, no internet?"

### 7. Time economics (6-hour day, 3 tasks)
- ~5 min: read all 3 statements; rank by expected points/hour. GAITE hints often reveal the intended difficulty.
- First 30 min per task: get the **baseline running and submitted**. Points on the board beat perfection.
- Use Gemma in parallel: while a model trains, have a chat open planning the next improvement.
- Last 45 min: freeze experiments, make sure your best 2 submissions are selected, verify file formats.

## Practice this skill NOW
During the 30-day prep, do all your studying with a free chatbot (Gemini/ChatGPT/AI Studio) **but impose the contest rules on yourself**: pretend answers are capped, ask in chunks, start fresh chats per topic, and always verify by running code. By contest day, driving an LLM under constraints will be muscle memory. If you want the real thing, Gemma 3 (and Gemma 4 where available) can be tried free at aistudio.google.com or via Hugging Face — practicing against the actual model family is a bonus, not a requirement.
