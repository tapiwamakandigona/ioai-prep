# LESSON_CONTENT — "How a Computer Sees"

One-hour lesson for high schoolers with zero AI background, presented over Google Meet
by a fellow student (IOAI/GAITE contestant). ~40–45 min slides + ~10 min live notebook
demo + Q&A. Strategy: **teach ONE story deeply (pixels → convolution → learning →
my own results), then tour the rest as trailers.**

All numbers are real and verified:
- SmallCNN from scratch: **50.0%** test accuracy (4,000 training photos, 3 epochs, CPU) — notebook 01
- Finetuned pretrained ResNet18: **74.2%** (only 1,000 training photos, 2 epochs) — notebook 02
- CLIP zero-shot: **88.5%** (0 training photos, evaluated on 200 test images) — notebook 02
- Live asset numbers (generated for this deck, real model outputs): SSDLite detector — "cat 97%" on the cat photo, "person 91%" on the astronaut; CLIP on the cat photo — "a photo of a cat" 97.9%, tiger 1.6%, dog 0.5%, pizza 0.0%.

All photos are real: `chelsea` (cat) and `astronaut` from the scikit-image sample
gallery; every derived image (pixel grid, feature maps, augmentations, detection boxes,
segmentation mask, noise chain) was computed from them with real code in `gen_assets.py`.

---

## Slide 1 — Cover

- **Title:** How a computer sees
- **Eyebrow:** A LESSON · COMPUTER VISION · BY A STUDENT, FOR STUDENTS
- **Visual:** Title only, whitespace.
- **Speaker note:** Hey everyone! Quick intro: I'm a high school student like you — I'm training for the International Olympiad in AI, and today I want to show you the single coolest thing I've learned: how a computer actually sees a picture. No background needed. If you can multiply small numbers, you can follow every step of this. By the end, you'll be able to explain how a photo becomes the word "cat" — and I'll show you models I trained myself.

## Slide 2 — One hour, one story

- **Bullets:**
  - Act 1 — How a computer sees: we compute what a network computes, by hand.
  - Act 2 — How it learns: nobody programs it; it practices. I'll show my own results.
  - Act 3 — What this unlocks: finding objects, cutting them out, words, image generation.
- **Dek:** The promise: in one hour you can explain how a photo becomes the word "cat."
- **Visual:** Plain numbered list at body size (no agenda theatrics).
- **Speaker note:** Here's the plan. Instead of racing through fifty terms, we'll learn ONE idea properly — the trick at the heart of all computer vision — and we'll actually compute it together by hand, on screen. Then I'll show you how a network learns that trick by itself, including real numbers from models I trained on my own computer. And at the end, quick trailers: the same trick powering face filters, self-driving cars, and AI image generators. Sound good? Let's go.

## Slide 3 — ACT 1 divider (dark statement slide)

- **Statement:** A computer has never seen a cat.
- **Eyebrow:** ACT 1 · HOW A COMPUTER SEES
- **Speaker note:** Let's start with something that sounds obvious but isn't: a computer has never seen anything. No screen inside, no little person watching. When your phone unlocks by recognizing your face, there is no picture anywhere inside the chip — there are only numbers. So the real question of this whole talk is: how do you get from a pile of numbers to the idea "cat"? Let me show you exactly what the computer gets.

## Slide 4 — A photo is just a grid of numbers  [INTERACTION 1]

- **Bullets:**
  - Zoom far enough in and a photo becomes a grid; each square is a pixel.
  - Each pixel is just a brightness number: 0 = black, 255 = white.
  - Color photos have three grids — red, green, blue. That's ALL the computer gets.
- **Visual:** Real cat photo (chelsea) with a small white box marked on the eye → arrow → that 10×10 crop blown up into a literal grid with the REAL brightness values printed in every cell (values from `pixel_grid.json`, e.g. 67, 59, 53… down to 6–10 in the dark pupil).
- **[INTERACTION 1]:** Before revealing values: "Look at the crop — which corner do you think has the BIG numbers, the bright fur or the dark pupil? Type your guess in the chat." Then reveal: bright fur ≈ 60–70s, pupil drops to single digits.
- **Speaker note:** This is a real photo — meet Chelsea, the most famous cat in computer science. I marked a tiny 10-by-10 square on her eye and zoomed all the way in. Quick game: bright pixels get big numbers, 255 is pure white, 0 is pure black. Which corner of this crop has the big numbers? Type it in the chat… Right — the fur side! Around 60–70. And the pupil crashes to 6, 7, 9. This grid of numbers is literally ALL the computer receives. Everything else today is: what do you DO with these numbers?

## Slide 5 — The one trick: convolution, by hand  [INTERACTION 2]

- **Bullets:**
  - Take a tiny 3×3 stencil of numbers — called a filter.
  - Slide it over the image; at each stop: multiply matching cells, add everything up.
  - One big answer = "my pattern is here." Zero = "nothing here."
- **Visual:** Three HTML grids. Left: 5×5 input with a vertical bright/dark edge (columns of 2s then 0s), the left 3×3 window highlighted. Middle: the 3×3 filter (1 0 −1 / 1 0 −1 / 1 0 −1). Right: the multiply-and-add written out in nine small products, sum revealed as **6**. Below: the same filter on the flat dark region → **0**.
- **[INTERACTION 2]:** The centerpiece. Audience computes the nine products out loud / in chat before the answer is revealed. Then the second window ("now all zeros — what do we get?").
- **Speaker note:** This is the heart of ALL computer vision, and we're going to compute it together — it's just times tables. The image has a bright stripe (2s) next to a dark area (0s). The filter is nine numbers. Lay it on the image, multiply each pair of cells, add the nine results. Let's do it in chat: two times one is…? Keep going… total: six! Now slide it onto the flat dark area: everything is zero. So this filter outputs LOUD where there's a vertical edge and SILENT where there isn't. Congratulations — you just ran a convolution, the exact operation inside every vision AI.

## Slide 6 — A filter is a pattern detector

- **Bullets:**
  - Run one filter across the WHOLE photo → a map of where its pattern lives.
  - The vertical-edge filter lights up on whiskers and eye outlines.
  - Rotate the filter → it finds horizontal edges instead. Different stencil, different pattern.
- **Visual:** Real computation on the real cat photo: grayscale chelsea, then the actual conv2d output of the vertical-edge filter (whiskers glow), then the horizontal-edge filter. Generated by `gen_assets.py` with torch.nn.functional.conv2d — same math as slide 5, just repeated everywhere.
- **Speaker note:** Now take the exact filter we just computed by hand and slide it across the entire cat photo — thousands of little multiply-and-adds. The result is this glowing map: white means "my pattern is HERE." Look — the whiskers and the eye outlines light up, because those are vertical-ish edges. Flip the filter on its side and suddenly it finds horizontal edges instead. This is real output, by the way — I ran this exact code on this exact photo. One filter, one pattern. So… what if we used lots of filters, in layers?

## Slide 7 — Stack layers: edges → textures → parts → objects

- **Bullets:**
  - Layer 1 filters find edges and color blobs.
  - Layer 2 looks at edge-maps and finds textures — fur, stripes, mesh.
  - Higher layers combine textures into parts (ear, eye, wheel), then whole objects.
  - This stack is a convolutional neural network — a CNN.
- **Visual:** Real first-layer filters of ResNet18 (all 64, trained on 1.28M ImageNet photos) shown as a grid — visible edge stripes and color blobs that the network discovered BY ITSELF. Plus a small edges→textures→parts→objects ladder.
- **Speaker note:** Here's the beautiful part. Stack filters in layers: the first layer finds edges, the next layer looks at the EDGE MAPS and finds combinations — textures like fur or stripes — then parts like an ear, then "cat." That whole stack is called a convolutional neural network, a CNN. And these tiles? The actual first-layer filters from a famous network trained on 1.28 million photos. Nobody drew these. They look like edge and color detectors because the network DISCOVERED that edges are the right place to start. Which raises the big question: how?

## Slide 8 — CODE CARD 1: the whole "eye" is one line

- **Code:**
  ```python
  import torch.nn as nn

  layer = nn.Conv2d(in_channels=3,    # red, green, blue
                    out_channels=32,  # learn 32 different stencils
                    kernel_size=3)    # each stencil is 3x3
  ```
- **Caption:** One line of Python = 32 sliding stencils, exactly the operation you did by hand.
- **Speaker note:** Before we move on — I want to demystify the code, because it's shockingly short. This single line creates a convolution layer: 32 different 3-by-3 stencils that slide over a color image. That's it. What you computed by hand on slide five is exactly what this line does, just 32 filters at once and very fast. When people say "I built a neural network," they're stacking a handful of lines like this one. You could type this tonight.

## Slide 9 — ACT 2 divider (dark statement slide)

- **Statement:** Nobody programs the filters. The network finds them.
- **Eyebrow:** ACT 2 · HOW IT LEARNS
- **Speaker note:** So here's the twist that makes this AI and not just clever programming. On slide five, I chose the filter numbers. But in a real network, NOBODY chooses them. All 32 stencils — millions of numbers in the full stack — start as pure random noise. And then the network learns them. By itself. From examples. Act two is about how that works, and I promise: no equations. It's basically a game you already know.

## Slide 10 — Learning = guess, get told how wrong, adjust

- **Bullets:**
  - Show the network a photo; it guesses: "70% dog, 20% cat…"
  - The loss is one number scoring how wrong the guess was — that's all "loss" means.
  - Nudge every filter a tiny step that shrinks the loss. Repeat a million times.
- **Visual:** Simple monochrome loop diagram: photo → network (random stencils) → guess → compared to true label "cat" → wrongness score → arrow looping back "nudge all the numbers".
- **Speaker note:** Learning is the hot-and-cold game. Remember hiding something and shouting "warmer… colder…"? Same thing. The network guesses "dog." We know it's a cat, so we hand it one number — the loss — which just means "how wrong were you." Big loss: ice cold. Then the magic step: there's a recipe (it's called backpropagation, that's the only name I'll drop) that tells every single filter number which direction to nudge to be slightly less wrong. One photo, tiny nudge. A million photos later, those random stencils have turned into the edge detectors you saw — nobody put them there.

## Slide 11 — Free extra photos: augmentation  +  CODE CARD 2

- **Bullets:**
  - Networks memorize if you keep showing the same photos — like cramming answers, not understanding.
  - A flipped cat is still a cat: flip, crop, recolor, add noise → free new examples.
- **Visual:** Five REAL images in a row: original cat → mirrored → zoomed crop → brightness/color shifted → noisy. All generated with torchvision/PIL from the same photo.
- **Code:**
  ```python
  train_tf = transforms.Compose([
      transforms.RandomCrop(32, padding=4),
      transforms.RandomHorizontalFlip(),
      transforms.ToTensor(),
  ])
  ```
- **Caption:** Every epoch, every photo arrives slightly different — the network can't just memorize.
- **Speaker note:** One practical trick before my results, because I use it in my own training. If you show a network the same photos over and over, it cheats — it memorizes them, like memorizing answer keys instead of understanding the subject. The fix is delightfully dumb: a mirrored cat is still a cat. So every time a photo is used, we randomly flip it, crop it, shift the colors, sprinkle noise. Same five lines in my actual training code, shown here on the same cat. Free infinite-ish data, and the network is forced to learn what cats LOOK like.

## Slide 12 — I trained this. Here's what actually happened.  [INTERACTION 3]

- **Bullets:**
  - Same task: 10 categories of small photos (CIFAR-10). Random guessing = 10%.
  - All three results are mine, run on an ordinary CPU — you can rerun the notebooks.
- **Visual:** Ascending bar chart (inline SVG, real numbers): **50.0%** my small CNN, from scratch, 4,000 photos → **74.2%** pretrained ResNet18, finetuned on just 1,000 photos → **88.5%** CLIP, zero training photos (zero-shot, measured on 200 test images). Title grammar: "from scratch vs standing on giants' shoulders."
- **[INTERACTION 3]:** Before reveal: "My little CNN trained for three rounds on 4,000 tiny photos. Random guessing gets 10%. What accuracy do you think it reached? Closest guess in chat wins bragging rights."
- **Speaker note:** Time for receipts. The task: tiny photos, ten categories — cat, ship, truck… Random guessing scores 10%. I built the small CNN from act one and trained it myself. Guess what it scored — closest in chat wins… 50%! Five times better than chance, from scratch, in about a minute of training. Then the plot twist: I took ResNet18, already trained on 1.28 million photos, swapped its last layer, fed it only a QUARTER of the data — 74.2%. And CLIP, which I'll show you soon, got 88.5% with ZERO training photos. Lesson: in modern AI you stand on giants' shoulders.

## Slide 13 — CODE CARD 3: borrowing a giant's eyes

- **Code:**
  ```python
  from torchvision.models import resnet18, ResNet18_Weights

  model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
  model.fc = nn.Linear(512, 10)   # swap the last layer: my 10 classes
  ```
- **Caption:** Keep every learned filter; replace only the final layer. This is transfer learning — the 74.2% recipe.
- **Speaker note:** And here is the entire giant-shoulders trick — four lines. Line one: download ResNet18 WITH the filters it learned from a million photos. Those filters already know edges, fur, wheels. Line two: its last layer answers the wrong question — it predicts a thousand ImageNet categories, but I have ten. So I rip off just that final layer and bolt on a fresh one for my classes. Then train briefly. That's "transfer learning," and it's how almost everyone uses vision AI in the real world — nobody starts from scratch if they can help it.

## Slide 14 — ACT 3 divider (dark statement slide)

- **Statement:** Same trick. Four superpowers.
- **Eyebrow:** ACT 3 · WHAT THIS UNLOCKS
- **Speaker note:** You now own the core: images are numbers, filters find patterns, stacks find objects, and it all learns by guess-and-nudge. Act three is the fun part — four quick trailers of what that one trick unlocks. I'm not going deep on any of these; I just want you to see that none of them is magic anymore. Each one is the same CNN idea wearing a different costume. And yes — every output you're about to see, I generated myself while building these slides.

## Slide 15 — Trailer 1: object detection — find it AND box it

- **Bullets:**
  - Classification says "there's a cat somewhere." Detection says WHERE — with a box.
  - One network pass predicts boxes + labels + confidence, fast enough for live video.
- **Visual:** REAL detector output (SSDLite, pretrained): the cat photo with its actual predicted box, labeled "CAT · 97%", and the astronaut photo labeled "PERSON · 91%". Generated in `gen_assets.py` on CPU.
- **Speaker note:** Trailer one: detection. Our CNN said "this photo is a cat." Detection answers the harder question — WHERE is the cat? — by drawing a box. I downloaded a small pretrained detector and ran it on our two photos while making these slides: it boxed the cat with 97% confidence and the astronaut as a person at 91%. No training by me, ran in seconds on a normal CPU. This is the tech inside self-driving car cameras and the thing that finds faces before your phone focuses on them.

## Slide 16 — Trailer 2: segmentation — cut out the exact shape

- **Bullets:**
  - Boxes are rough. Segmentation labels EVERY pixel: cat or not-cat.
  - That pixel mask is how portrait mode blurs behind you and meet apps swap backgrounds.
- **Visual:** REAL segmentation output (LR-ASPP, pretrained), three panels: photo → predicted black/white cat mask → cat cut out cleanly on white. Generated in `gen_assets.py`.
- **Speaker note:** Trailer two: sometimes a box isn't enough — you want the exact outline. Segmentation asks the network to decide for EVERY single pixel: cat, or not cat? Middle image: the real mask a pretrained model produced for me — white means "cat pixel." Right: use the mask as scissors and the cat lifts cleanly off the background. Sound familiar? It's exactly how this very video call can blur or replace my background in real time, and how doctors' software outlines organs in scans. Every pixel, classified.

## Slide 17 — Trailer 3: CLIP — a model that speaks image AND text  +  CODE CARD 4

- **Bullets:**
  - CLIP learned from 400 million internet photos with their captions.
  - It scores how well a sentence matches an image — so you classify with SENTENCES, no training.
  - That's "zero-shot": describe the classes in words; the model does the rest.
- **Visual:** The real cat photo + REAL CLIP scores computed for this deck: "a photo of a cat" 97.9% · "a photo of a tiger" 1.6% · "a photo of a dog" 0.5% · "a photo of a pizza" 0.0% — drawn as a clean bar row.
- **Code:**
  ```python
  inputs = processor(text=["a cat", "a dog", "a pizza"],
                     images=photo, return_tensors="pt")
  probs  = model(**inputs).logits_per_image.softmax(dim=1)
  ```
- **Caption:** Classify with sentences instead of training — this is the 88.5% zero-shot model.
- **Speaker note:** Trailer three is my favorite. CLIP read 400 million internet images WITH their captions, and learned to score how well a sentence matches a picture. So instead of training anything, you just… ask. I gave it our cat photo and four sentences. Real output: "a photo of a cat" — 97.9%. Tiger gets 1.6% — fair, she's stripy! Pizza: zero. Three lines of code, no training, and remember the bar chart: this is the model that beat my hand-trained CNN with zero training photos. Words plus images in one brain.

## Slide 18 — Trailer 4: image generation — start from static

- **Bullets:**
  - Train by RUINING photos: add a little noise, then more, until pure static.
  - The network learns one skill — undo a bit of noise.
  - Generate: start from fresh static and de-noise step by step. That's diffusion.
- **Visual:** Five REAL frames: the cat photo progressively drowned in real Gaussian noise until pure static, with the arrow pointing BACKWARD (static → cat) labeled "generation runs this way." (Forward noising computed for real; the reverse direction is the learned part.)
- **Speaker note:** Last trailer: how do AI image generators work? Weirdly, you train them by DESTROYING photos. Take the cat, add a pinch of noise, again, again — until it's pure TV static. I did the forward part for real, that's these frames. The network practices one humble skill: look at a slightly noisy image and clean it up a little. Now the magic: hand it PURE STATIC and apply that cleanup over and over. An image crystallizes out of noise. That's diffusion — the engine behind the famous image generators. Same convolutions underneath, by the way.

## Slide 19 — Close: this is a syllabus, not magic

- **Bullets:**
  - Everything today is on the official IOAI 2026 syllabus — the olympiad I'm training for.
  - My two notebooks rerun everything: the CNN, the 50.0 → 74.2 → 88.5 ladder. Take them.
  - You can multiply small numbers. So you can do this.
- **Eyebrow:** RECAP · PIXELS → FILTERS → LEARNING → SUPERPOWERS
- **Visual:** Mirror of the cover; restate thesis, then Q&A prompt. No "thank you" slide.
- **Speaker note:** Quick recap of the one story: a photo is a grid of numbers; a filter is a stencil we slid by hand; stacked filters see edges, then fur, then cat; and it all learns by guess-and-nudge. Here's the thing — none of today was magic, and none of it was university material. It's all literally on the official syllabus of the International Olympiad in AI, which high schoolers like us compete in. The two notebooks with everything I showed — the 50%, the 74.2%, the 88.5% — are yours; rerun them tonight on a normal laptop. Now: questions! And then I'll show you the notebooks live.

---

## Code cards used (4 total)
1. Slide 8 — `nn.Conv2d` (the eye)
2. Slide 11 — `transforms.Compose` (augmentation)
3. Slide 13 — ResNet18 head swap (transfer learning)
4. Slide 17 — CLIP zero-shot (3 lines)

## Interaction moments (3 total)
1. Slide 4 — guess which corner of the pixel grid has big numbers (chat)
2. Slide 5 — compute the convolution together out loud / in chat (centerpiece)
3. Slide 12 — guess my model's accuracy before the reveal (chat, "closest wins")
