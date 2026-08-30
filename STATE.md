# STATE — learner model & session memory

Data file for the `teach` skill. Phase 1 step 0 **reads** this before probing;
Phase 4 **updates** it at session end. Keep entries terse and truthful — an
over-optimistic entry (claiming a shaky node held) is worse than a missing one.
Dates are absolute (`YYYY-MM-DD`).

---

## Current goal


Get from **tensor mechanics → a working training loop**: the smallest program
that actually *learns*. Planned spine, in dependency order:

1. **autograd** — `requires_grad`, `.backward()`, `.grad`, the graph, `no_grad`.
2. **nn.Module** — parameters, `forward`, a hand-built linear layer, then `nn.Linear`.
3. **loss + optimizer** — a loss function (e.g. MSE), `torch.optim` (SGD), `.step()` / `.zero_grad()`.
4. **the training loop** — forward → loss → `backward` → step, iterated, on toy data that visibly converges.

Simply put...
Long-term: ML/DL/NLP/LLM
Current: tensors → a working training loop

**Session note (2026-08-27):** he's continuing the video course to finish the
tensor-fundamentals material (reshaping/stacking/squeezing/permute/indexing) on
his own, then returning here to be tested + have it expanded. Next session:
probe what stuck from the course, patch gaps, then teach the storage/view model
and the rest of the shaping toolkit before moving on to autograd.

---

## Strand edges

Per strand: **have** (floor, reliably known) → **edge** (where it runs out).
Seeded from the assessment of `00_pytorch_fundamentals.py` on 2026-08-27; not yet
confirmed by live probing (do a short confirmation probe, not a remap).

| Strand | Have (floor) | Edge (ceiling — starts here) | Confidence |
|---|---|---|---|
| Tensor construction | ranks/shapes; `torch.rand`, `arange`, `zeros_like` | — solid | seeded |
| Tensor attributes | `.ndim` `.shape` `.dtype` `.device` `.item()` | — solid | seeded |
| Dtypes | float32 default; `.type(torch.half)`; mean needs float | — solid | seeded |
| Device | autodetect `cuda→mps→cpu` (adapted from course CUDA) | — solid | seeded |
| Element-wise ops | add/sub/mul/div, broadcasting basics | — solid | seeded |
| Matmul | `torch.matmul`, `@`, `.T` | — solid | seeded |
| Aggregation | `min/max/mean/sum/argmin/argmax` (+ float-for-mean gotcha) | — solid | seeded |
| Reshaping | reshape **element-count invariant** confirmed (live probe 08-27) | **storage/view model absent** — thinks reshape copies; `view`/`stack`/`squeeze`/`permute` unseen | confirmed |
| Indexing / slicing | — | **absent** — never exercised | seeded |
| `.cpu()` / `.numpy()` round-trips | — | **absent** | seeded |
| autograd | — | **absent** — `requires_grad` appears once, never run | seeded |
| `.backward()` / `.grad` | — | **absent** | seeded |
| nn.Module / layers | — | **absent** | seeded |
| Loss functions | — | **absent** | seeded |
| Optimizers | — | **absent** | seeded |
| Training loop | — | **absent** | seeded |
| Dataset / DataLoader | — | **absent** | seeded |

**The edge, in one line:** *can manipulate tensors fluently; has never built
anything that learns.* Teaching starts at autograd.

---

## Misconceptions

Log as: `- [date] <belief> — dislodged | STILL LIVE — <note>`.

- [2026-08-27] "reshape returns an independent copy of the data" — **STILL LIVE** — missed on live probe; no concept yet that a tensor = flat storage + shape/stride metadata, so reshape/view usually *share* storage. Teach this first next session.

---

## Nodes taught

Log as: `- [date] <node> — landed? held on recheck [date]? | needs rebuild`.

_(none yet — first teaching session pending)_

---

## Review schedule (spaced)

For computing intervals, not guessing. A node that **held** lengthens its
interval (e.g. 1d → 3d → 7d → 16d → 35d); a node that **needed rebuilding**
resets to ~1d. Log as: `- <node> — last reviewed <date>, held ×N, due <date>`.

_(empty — populates once teaching begins)_
