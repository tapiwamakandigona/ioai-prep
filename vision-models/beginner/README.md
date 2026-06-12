# Beginner vision deck — "How machines learn to see"

Materials for presenting the IOAI Section 3 (computer vision) syllabus to a
zero-background 14–18 audience.

```
beginner/
├── presentation/
│   ├── how_machines_learn_to_see.pdf    ← present this (fullscreen in any PDF viewer)
│   └── how_machines_learn_to_see.pptx   ← same deck, Google Slides–ready (upload to Drive)
├── teacher/
│   ├── teacher_guide.pdf                ← READ THIS FIRST — every slide explained in simple English
│   └── PRESENTER_SCRIPT.md              ← compact per-slide talking points + Q&A cards
├── build/                               ← scripts that generate everything
│   ├── build_beginner_deck.py           ← deck PDF      (uv run --with weasyprint python build_beginner_deck.py)
│   ├── build_pptx.py                    ← PPTX          (uv run --with pymupdf --with python-pptx python build_pptx.py)
│   ├── build_teacher_guide.py           ← teacher guide (uv run --with weasyprint --with pymupdf python build_teacher_guide.py)
│   ├── guide_content.py                 ← the teacher guide text lives here
│   └── CONTENT_DRAFT.md                 ← original content outline
└── assets/                              ← real outputs from the repo notebooks used in the deck
```

Suggested prep order: teacher_guide.pdf once (≈45 min) → skim PRESENTER_SCRIPT.md →
practice slide 6 (the hand convolution) → present from presentation/.
