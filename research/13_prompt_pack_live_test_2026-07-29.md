# Prompt-pack live test — 2026-07-29

Tested `12_gemma_prompt_pack.md` against the real Gemma 4 E4B assistant on
`chat.ioai2026.kz` (account zwe104), re-solving all 3 Eastern Practice Round
problems with the pack's prompts only, then verifying every returned code cell
by actually running it locally against the practice data (A: real dataset;
C: a synthetic dataset built to the statement's exact spec; B: plan-quality
review only — no local Qwen copy).

## Verdict

**The pack works — the prompts got Gemma to produce the exact winning fixes
for all 3 problems, and the returned code ran verbatim.** But it was NOT
foolproof as written: two dangerous failure modes surfaced that the original
pack under-weighted. Both are now fixed in `12_gemma_prompt_pack.md`.

## Results by problem (fresh chat each, per the pack)

### A. Digit Recognition (vision)
| Step | Result |
|---|---|
| P1 multi-part feed | ✅ 4× "Noted.", then a correct 5-bullet summary that itself flagged rotation handling as the top risk |
| P2 plan | ❌ **#1 suggestion was "Data Augmentation: rotations, flips, zooms" — the planted trap.** A zero-knowledge user following it verbatim would tank the score |
| P3 "SVC C=10" rewrite | ✅ exact one-change cell, correct format |
| P3 "remove random rotation" (cell pasted) | ✅ rotation removed, variable names/format kept |
| P7 safety check (original wording) | ⚠️ caught the trap but replied "FAIL FAIL FAIL FAIL" on one line — no actionable info |
| Referring to "the same code" without re-pasting | ❌ **Gemma hallucinated an unrelated GPS/haversine problem** and produced garbage `load_X`, despite the code being inside the 10-message window |

**Local verification** (real practice dataset, 300 test images):
trap baseline (rotation + C=1.0) = **77.7%** → Gemma's pack-driven cells
(no rotation + SVC C=10) = **83.7%**, matching the practice-round submission
(85.6 on the hidden set).

### C. Customer Segments (clustering)
| Step | Result |
|---|---|
| P1 feed + DONE summary | ✅ perfect; summary itself said scaling is needed |
| P2 plan | ✅ **#1 suggestion was StandardScaler — unprompted, exactly right** |
| P3 "StandardScaler before KMeans" | ✅ correct cell, verbatim-runnable |

**Local verification** (synthetic data matching the statement: 3 features on
wildly different scales, 4 clusters, 250 rows): raw KMeans ARI **0.047** →
Gemma's returned cell ARI **0.979**. Same dynamic as the real problem
(0.56 → 1.00).

### B. Animal deduction (interactive oracle)
| Step | Result |
|---|---|
| P1 feed + DONE summary | ✅ correct on budget rules and the mismatch pitfall |
| P2 plan | ✅ unprompted: probabilistic inference, max-info-gain question choice, use local Qwen to precompute — the actual winning pattern |
| Step-by-step algorithm prompt | ✅ near-perfect: precompute table in `__init__`, balanced-split question selection, guess when one candidate remains, and on oracle/table disagreement invalidate only that (animal, question) entry and keep going |

(Code not run locally — no Qwen3-0.6B copy in this sandbox; on contest day
verification is the self-score cell, per the pack.)

## The two pack fixes (already applied to doc 12)

1. **P2's top suggestion can be the trap itself.** New warning under P2: check
   every P2 suggestion against the Free-wins list; the list outranks P2.
2. **Hard rule #0: always paste, never reference.** "The same code" → total
   hallucination even within the memory window. Every code-related prompt must
   contain the code.
3. (Minor) **P7 reworded** to force `"<n>) PASS/FAIL — <deciding code line>"`
   per line; the original wording produced a useless one-line "FAIL FAIL FAIL
   FAIL".

## Budget note

The whole 3-problem test used ~29 messages — comfortably inside the 60/hr
cap, consistent with the pack's "≈20 per problem" guidance.
