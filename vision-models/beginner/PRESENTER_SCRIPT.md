# Presenter script — "How machines learn to see"

For the presenter. Audience: 14–18, zero coding/AI background. ~60–75 min with quizzes.
Rules that make this work: **never say a term before its Name Box appears**, do the
slide-6 multiplication WITH the room (it's the heart of the whole deck), and run the
three quick-checks out loud — no grades, just answers.

---

## 01 — Cover
"Today, in about an hour, you'll understand how a computer recognizes a cat, finds it in a photo, and even draws one from scratch. The only math you need is multiplying small numbers. Everything on these slides actually ran on a normal laptop — every number is real."

## 02 — The plan
Walk the five parts in one breath each. Promise: "Maximum ONE new word per slide, and every word lands in a cheat sheet at the end."

## 03 — Five starter words
Read all five out loud. "These are the only words I'll use without warning. Everything else gets introduced properly when we reach it." Don't rush — these five carry the day.

## 04 — (dark) A computer has never seen a cat
Pause here. "It has no eyes. So what DOES it get?" Let someone guess, then advance.

## 05 — A photo is a grid of numbers
Point at the marked square on Chelsea's eye, then the real numbers below. Ask the room: where are the big numbers — bright fur or dark pupil? (Bright fur; 255 = white.) Key sentence: "Three stacked grids of numbers. That is ALL the computer ever gets."

## 06 — Convolution by hand ★ THE CENTERPIECE
Slow down. Do the nine multiplications out loud with the room before showing the total. "Bright stripe next to dark area = an edge. The stencil multiplied and added... and got a BIG number exactly where the edge is, and 0 where nothing happens." Then the reveal: "Congratulations — you just did a convolution. That word scares people. It's times tables."

## 07 — Slide it everywhere
"Same stencil, every position, write down every answer — you get a map of where the pattern lives." Point at the whisker glow in the real feature map: "This is real output of that exact stencil on Chelsea."

## 08 — Stride & padding
Quick slide. "Two boring rules about HOW the stencil walks: step size, and zeros glued on the border so edges aren't ignored." Don't linger.

## 09 — Pooling
"Keep each window's winner. Map shrinks, and a pattern that shifts one pixel still wins its window — small shifts stop mattering." Verify one quadrant with the room (top-left: 1,3,4,8 → 8).

## 10 — ReLU
The one abstract slide in Part 1. Anchor sentence: "Negatives become zero. Without that little bend, stacking 50 layers collapses into the power of ONE layer — depth would be fake."

## 11 — The full CNN stack
The payoff: "Stencils on stencils. Layer 1 finds edges; layer 2 looks at edge-maps and finds corners and textures; layer 3 finds eyes and wheels. Nobody told it to — that ladder appears on its own."

## 12 — Code card 1
"Every line is a thing you already know." Read the lines mapping words to code. Then the knob box: this is exam material — what happens if I remove ReLU? Make the kernel 7×7?

## 13 — QUICK CHECK 1
Out loud, popcorn style. If the room struggles on ReLU, re-anchor: "the bend that makes depth real."

## 14 — (dark) Nobody programs the filters
"On slide 6, WE chose the nine numbers. In a real network there are millions. Nobody picks them. They're learned. How?"

## 15 — The learning loop
"Guess → compare to the label → nudge every number so the same mistake shrinks → repeat." That's training. The wrongness score has a name: loss.

## 16 — Gradient descent
"Imagine every possible setting of all the stencil numbers as a hilly landscape; height = wrongness. Training = rolling a ball downhill." Right panel: step too big = bouncing across the valley forever. Learning rate = THE most important knob.

## 17 — Overfitting
The student-who-memorized-past-papers analogy. Point at the two curves: train score keeps climbing, exam score peaks then falls. "Never grade on the study set."

## 18 — Augmentation
"A flipped cat is still a cat — free extra photos." The code lines shown are the real ones from our training run.

## 19 — What the network learned by itself
"Nobody drew these filters. They started as random noise and became edge detectors — the same kind we hand-built on slide 6."

## 20 — RECEIPTS ★ remember these three numbers
50.0% from scratch with 4,000 photos. 74.2% with only 1,000 photos. 88.5% with ZERO photos. "Chance is 10%. The two bigger bars are the rest of this talk."

## 21 — (dark) Never start from scratch
One breath, advance.

## 22 — Transfer learning
Chef analogy: switching from Italian to Japanese, you don't relearn chopping. "Keep the trained eyes, swap the final decision layer. That's how 1,000 beat 4,000."

## 23 — ResNet skips
Tell the 2015 surprise: 56 layers scored WORSE than 20. "The fix is one arrow: an express lane that adds the input back. Each block only learns the small CHANGE. Signals stop fading; 152 layers train fine."

## 24 — Code card 2
"Four honest lines. Borrow, freeze, swap, train." Knob box again = exam material.

## 25 — Detection
Point at the real outputs: cat 97%, person 91%. "Box + label + confidence, all in one pass." Then IoU (overlap ÷ union grades a box) and NMS (delete duplicate boxes).

## 26 — YOLO / SSD / DETR
"Know the names and characters: YOLO = speed king for live video, SSD = light for phones (it made the cat slide), DETR = transformer asking ~100 questions, no cleanup needed." Internals NOT needed.

## 27 — Segmentation
"Cats aren't rectangles. A class for EVERY pixel." U shape: shrink to understand what, grow back to say where — and skip connections carry the crisp edges across. "Skip connections again!"

## 28 — QUICK CHECK 2
The myth matters most: "you need millions of photos" — no, our 74.2% ran on a CPU with 1,000 photos.

## 29 — Self-supervised
"Labels are the expensive part. Trick: two augmented views of the same photo must land close together in embedding space. To manage that, the network must learn what MATTERS in images. No human labels anywhere."

## 30 — CLIP
"Two encoders — photos and SENTENCES — into the same space, trained on 400M internet photo-caption pairs. To classify: pick the closest sentence. New classes = new sentences, zero retraining. That's the 88.5% bar."

## 31 — Code card 3
Walk it slowly; this is the full zero-shot recipe. Real output: cat 97.9%, tiger 1.6%.

## 32 — GANs
Counterfeiter vs detective arms race. The honest subtlety students love: "the counterfeiter NEVER sees a real photo — only the detective's feedback." Mode collapse = the one-trick forger.

## 33 — Diffusion
Read the strip RIGHT to LEFT: pure noise → cat. "Its only skill is removing a little noise. Generation = that skill ~50 times, with a text prompt steering each step. This is DALL·E / Stable Diffusion / Midjourney."

## 34 — QUICK CHECK 3 → 35 syllabus map → 36 glossary → 37 knob table
"These three slides ARE your revision. Screenshot them." The knob table is the practical-round drill: predict what a change does BEFORE running it.

## 38–39 — Close
"It was never magic. Multiply, add, and practice. The notebooks to re-run every number are in our repo."

---

## Q&A cards — likely questions

**"How does the network know what to nudge?"**
The loss landscape has a slope at every point; calculus gives the downhill direction for every number at once. You don't compute it by hand — `loss.backward()` does. (Name if pressed: backpropagation.)

**"Who decided the filter numbers in slide 6?"**
We did, for teaching. In real networks they start random and training nudges them — slide 19 shows the result.

**"Is this how my brain works?"**
Loosely inspired, not a copy. Neurons don't do backpropagation as far as we know.

**"Why 0–255?"**
One byte holds 256 values. Pure convention.

**"What's a tensor really?"**
A grid of numbers, possibly stacked. A photo is a 3×height×width tensor. Nothing scarier.

**"Can CLIP be wrong?"**
Yes — it inherits internet biases and can be fooled by text in the image (a pear with "iPod" written on it). Good honest answer to volunteer.

**"GAN vs diffusion — who wins?"**
Diffusion won the quality war (stable training, better variety); GANs are still faster at generation time.

**"Could we run this?"**
Yes — every number in the deck came from notebooks in this repo, CPU only.

**If asked anything you don't know:** "Good question — not on our syllabus, but let's look it up after." Never bluff.
