# Presenter Guide — "How a Computer Sees"

One-hour Google Meet session · 19 slides · ~42 min slides + ~10 min live notebook demo + Q&A.
Companion files: `vision_from_scratch_deck.pdf` (present this), `vision_from_scratch_deck.pptx` (same deck with these notes embedded), `LESSON_CONTENT.md` (full script per slide).

---

## Minute-by-minute plan

| Time | Slides | What happens |
|---|---|---|
| 0:00–0:02 | 1–2 | Hello + the promise + the 3-act plan. Energy up, no biography. |
| 0:02–0:04 | 3 | "A computer has never seen a cat." Let it sit for 2 seconds before talking. |
| 0:04–0:09 | 4 | Pixel grid. **INTERACTION 1** (chat: fur or pupil?). Don't rush — this slide is the foundation. |
| 0:09–0:16 | 5 | **THE centerpiece.** Hand convolution, **INTERACTION 2** (compute out loud). Budget 6–7 min. |
| 0:16–0:19 | 6 | Feature maps: "the filter you just ran, on the whole photo." |
| 0:19–0:22 | 7 | Stack layers; point at the real ResNet18 filters: "nobody drew these." |
| 0:22–0:24 | 8 | Code card 1. Keep it light: "that's the whole eye." → ACT 2 |
| 0:24–0:26 | 9–10 | Dark divider + learning loop. Hot-and-cold game analogy. |
| 0:26–0:29 | 11 | Augmentation: five cats, five lessons. |
| 0:29–0:34 | 12 | Results. **INTERACTION 3** (guess my accuracy). Walk the bars left to right. |
| 0:34–0:36 | 13 | Code card 3: the four-line giant-shoulders trick. → ACT 3 |
| 0:36–0:37 | 14 | Dark divider. "Four quick trailers — no depth, just wow." |
| 0:37–0:44 | 15–18 | Detection → segmentation → CLIP → diffusion. ~1.5–2 min each, strict. |
| 0:44–0:46 | 19 | Close: IOAI syllabus + notebooks offer. Ask for questions. |
| 0:46–0:50 | — | Q&A round 1 (take 2–3 questions). |
| 0:50–0:58 | — | **Live notebook demo** (see below). |
| 0:58–1:00 | — | Final questions, share notebook links in chat, thank everyone. |

**Running late?** Cut from Act 3 only — slide 16 (segmentation) and slide 18 (diffusion) compress to one sentence each. Never cut slides 4, 5, or 12.

**Live demo plan (8 min):** open the finished notebook (everything pre-run, do NOT retrain live). Show: (1) the CIFAR-10 grid of tiny images, (2) the training-loss curve going down — "watch the loss get colder," (3) the 50.0% evaluation cell, (4) the CLIP cell — change one prompt live (e.g. add "a photo of a hamster") and rerun just that cell; it takes seconds on CPU and always lands.

---

## The hand-convolution walkthrough (slide 5) — full script

This is the moment the talk lives or dies. Slow down. Script:

1. **Set the scene.** "Everything in computer vision — your phone unlocking, self-driving cars, image generators — is built on ONE operation. We're going to do it by hand right now. It's just times tables."
2. **Read the image.** "Left grid is a tiny image: a bright stripe of 2s next to a dark area of 0s. Right where they meet — that's an edge, right? Let's see if math can FIND that edge."
3. **Read the filter.** "This 3×3 box of nine numbers is called a filter. Think of it as a stencil: 1s on the left column, 0s in the middle, −1s on the right."
4. **Lay it down.** "I place the stencil on the highlighted 3×3 patch — right on the edge. Now the rule: multiply each pair of overlapping cells, then add all nine."
5. **Compute together (INTERACTION 2).** Go row by row, ask the chat: "Top row: 2 times 1 is…? 2 times 0…? 0 times minus 1…? So the row gives 2." Same for rows two and three. "Add them up: 2+2+2 = **6**."
6. **The reveal.** "Six. Big number. The filter is SHOUTING: 'there's a vertical edge here!'"
7. **The control test.** "Now slide the stencil to the flat dark area. Every cell is 0, so every product is 0, sum is **0**. Silence. The filter only speaks on its own pattern."
8. **Land it.** "That's a convolution. You just did, by hand, the exact computation that runs billions of times inside every vision AI. Everything else today is just this, repeated and stacked."

Common stumble: someone asks why −1 and not another number. Answer: "Great question — any numbers work; THESE numbers happen to detect bright-left/dark-right. In Act 2 you'll see the network picks the numbers itself."

---

## The three interaction moments

1. **Slide 4 — pixel guess.** "Bright = big number. Which side of the grid has big numbers — the fur or the pupil?" Wait for chat answers, then point at real values: fur ≈ 60–70, pupil 6–10. Purpose: everyone internalizes image = numbers.
2. **Slide 5 — convolution out loud.** See script above. Purpose: everyone has personally computed a convolution.
3. **Slide 12 — accuracy bet.** Before showing the slide content, ask: "I trained a small CNN from scratch on 4,000 tiny photos, 10 categories. Random guessing gets 10%. What did mine score? Closest in chat wins eternal glory." Then reveal: 50.0%. Then ride the surprise of 74.2% with less data, then 88.5% with none.

---

## Transition lines between acts

- **Into Act 1 (slide 2→3):** "So let's start at absolute zero — with the uncomfortable fact that a computer has never seen anything."
- **Act 1 → Act 2 (slide 8→9):** "You now know what a network computes. But here's the twist that makes it AI: nobody types in those filter numbers. The network finds them by itself — and that's Act 2."
- **Act 2 → Act 3 (slide 13→14):** "So that's the engine: filters, learned by guess-and-nudge, ideally borrowed from a giant. Act 3 is the joyride — four things this one trick unlocks."
- **Act 3 → Close (slide 18→19):** "Detection, cutting things out, talking to images, generating them from static — same convolutions every time. Which brings me to my last point: none of this is magic."

---

## Six likely audience questions, with simple answers

1. **"How long did training take? Do you need a supercomputer?"**
   "My small CNN trained in about a minute on a normal laptop CPU — no GPU. The giant models took someone else's supercomputer, but that's the point of transfer learning: they paid, we borrow."

2. **"Why did your CNN only get 50%? That sounds bad."**
   "Random guessing is 10%, so 50% means it genuinely learned a lot — from just 4,000 thumbnail-sized photos and one minute of practice. State of the art on this dataset is around 99%, but those models are bigger, see far more data, and train far longer. Mine is the bicycle version, built so we can understand every part."

3. **"Is this how face unlock / Snapchat filters work?"**
   "Yes — the same building blocks. Detection finds your face, a network maps facial landmarks, and segmentation-like masks let filters stick to the right pixels. Different last layers, same convolutions underneath."

4. **"What's the difference between this and ChatGPT?"**
   "ChatGPT works on text and predicts the next word; today's models work on pixels. Different data, same big recipe: a deep network learning from huge amounts of examples by guess-and-nudge. CLIP is literally the bridge — half of it reads text, half reads images."

5. **"Can the model be fooled?"**
   "Yes, surprisingly easily — and remember CLIP gave 'tiger' 1.6% on a stripy cat, so you can see WHY: it matches patterns, it doesn't 'know' anything. There are even adversarial images: tiny pixel changes, invisible to us, that flip the answer. Making models robust is a whole research field — and it's on the olympiad syllabus too."

6. **"How do I start? Do I need to be great at math?"**
   "If you followed the multiply-and-add today, you have the core math. Start with Python basics, then PyTorch tutorials, then my notebooks — they run on a free Google Colab or any laptop. The whole path is on the IOAI 2026 syllabus; that's the map I'm following myself."

---

## Numbers cheat-sheet (everything quotable on the slides — all verified)

- Small CNN, from scratch: **50.0%** test accuracy · 4,000 training photos · ~1 min CPU training.
- ResNet18, finetuned: **74.2%** · only 1,000 photos (4× less) · pretrained on **1.28M** ImageNet photos.
- CLIP zero-shot: **88.5%** on a 200-image CIFAR-10 test sample · **0** training photos · trained on **400M** image–caption pairs.
- Random-guessing baseline: **10%** (10 classes).
- Detection demo: cat **97%**, person (astronaut) **91%** — pretrained SSDLite, run on CPU.
- CLIP on the cat photo: cat **97.9%**, tiger **1.6%**, dog **0.5%**, pizza **0.0%**.
- Pixel values: 0 = black, 255 = white; the eye crop reads fur ≈ 60–70, pupil 6–10.

Tech check before the call: share-screen the PDF at full screen, have the notebook already open in a second tab, chat visible on a second window/phone so you can read interaction answers.
