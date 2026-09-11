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
his own, then returning here to be tested + have it expanded.

**Session note (latest):** he blew past the old edge on his own — built a full
linear-regression training loop in `01_pytorch_workflow.py` (nn.Module, custom
nn.Parameter, forward, L1Loss, SGD, full train loop, inference_mode, save).
Consolidation session run on the loop. **Next milestone (his choice):** real
data loading — Datasets/DataLoaders/batching — *then* change learning type
(nonlinearity + classification). Still has some course left but fine leaving it.

TERMINAL NOTE: keep quiz options SHORT — his terminal truncates long options
(caused several false-miss answers early this session).

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
| autograd | `requires_grad`=tensor property; `inference_mode` temporarily overrides tracking (both confirmed live) | graph internals unprobed | confirmed |
| `.backward()` / `.grad` | `.grad` holds ∂loss/∂p; backward ACCUMULATES (both confirmed) | — solid | confirmed |
| nn.Module / layers | built subclass, custom nn.Parameter, forward; `train/eval`=mode flag (fixed this session) | only ever hand-written linear; `nn.Linear`/dropout/batchnorm unseen | confirmed |
| Loss functions | uses `nn.L1Loss` in a working loop | why/which loss when — unprobed | seeded |
| Optimizers | `SGD` wired correctly; NOW knows update rule `p←p-lr·grad` (taught, fragile) | momentum/Adam/other optimizers absent | confirmed |
| Training loop | can build+run full loop AND now explains why each line/order | independent recall of chain unconfirmed; only 1 model type | confirmed |
| Dataset / DataLoader | — | **absent** — NEXT MILESTONE | seeded |

**The edge, in one line:** *builds & now understands a full linear-regression
training loop; has never fed it real data.* Teaching starts at Datasets/DataLoaders.
Also: `torch.save` bug in his code — passed `model_0.state_dict` (method) not
`state_dict()` (call); flagged, not yet fixed by him.

---

## Misconceptions

Log as: `- [date] <belief> — dislodged | STILL LIVE — <note>`.

- [2026-08-27] "reshape returns an independent copy of the data" — **STILL LIVE** — missed on live probe; no concept yet that a tensor = flat storage + shape/stride metadata, so reshape/view usually *share* storage. Not revisited this session.
- [latest] "model.train()/eval() toggle requires_grad / gradient tracking" (was written into his code comments) — **DISLODGED** this session. Confirmed he now knows they only flip self.training for dropout/batchnorm, are no-ops in his linear model, and that grad tracking is requires_grad + inference_mode/no_grad. Recheck once next session.

---

## Nodes taught

Log as: `- [date] <node> — landed? held on recheck [date]? | needs rebuild`.

- [latest] train()/eval() = mode flag, not grad tracking — landed (dislodged prior misconception). due recheck ~+3d
- [latest] SGD update rule `p ← p - lr·∂loss/∂p`; step size scales with gradient magnitude — landed after a struggle, THEN confirmed solid via hands-on prediction on real optimizer (predicted grad=4.0 and post-step w=1.6 correctly). due recheck +3d.
- [latest] full loop as causal chain + WHY the order — confirmed via hands-on: correctly predicted that skipping zero_grad makes backward accumulate 4.0→8.0 (united accumulation node with update-rule node). solid. due recheck +3d.

---

## Review schedule (spaced)

For computing intervals, not guessing. A node that **held** lengthens its
interval (e.g. 1d → 3d → 7d → 16d → 35d); a node that **needed rebuilding**
resets to ~1d. Log as: `- <node> — last reviewed <date>, held ×N, due <date>`.

- train/eval mode flag — last reviewed [latest], held ×1, due +3d
- SGD update rule — last reviewed [latest], held ×1 (confirmed via hands-on), due +3d
- full-loop chain — last reviewed [latest], held ×1 (confirmed via hands-on), due +3d
