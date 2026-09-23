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

**Session note (2026-08-27, prior):** he blew past the old edge on his own — built a full
linear-regression training loop in `01_pytorch_workflow.py` (nn.Module, custom
nn.Parameter, forward, L1Loss, SGD, full train loop, inference_mode, save).
Consolidation session run on the loop. Old planned next milestone was DataLoaders.

**Session note (2026-09-22):** first session on Claude Code (migrated off pi, no
more API credits — launch via `./start-learning-cc.sh` then `/learn`). He SKIPPED
the DataLoaders milestone and went straight to **binary classification** in
`02_pytorch_nn_classification.py`: make_circles data, train/test split, CircleModelV0
(2 Linear) and V1 (3 Linear), BCEWithLogitsLoss, SGD, logits→sigmoid→round pipeline,
accuracy_fn, decision-boundary plots. **This session was a full ASSESSMENT** (his
request) across 01+02 — 12 graded questions, 3 waves. Results reconciled below.
DataLoaders never happened and is not currently his focus. **Next milestone (2026-09-23):
wire nn.ReLU into CircleModelV1** (code-first, predict-before-run) and watch test acc
jump ~50%→~99% — the logit/sigmoid node is now taught & landed. Open with a light recheck
of the exact-0 decision boundary (see misconceptions) before starting ReLU.

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
| Training loop | can build+run full loop AND now explains why each line/order; loop chain (zero_grad accumulation, backward fills .grad, step) all held at HARD difficulty (live 09-22) | — solid | confirmed 09-22 |
| eval / inference_mode | eval=mode flags, inference_mode=stops grad tracking — cleanly separated (live 09-22) | — solid | confirmed 09-22 |
| nn.Parameter | registers tensor in parameters()/state_dict so optimizer sees it + it saves (live 09-22) | — solid | confirmed 09-22 |
| Shape reasoning | `.squeeze()` [N,1]→[N]; `nn.Linear` in/out wiring (out of layer N = in of layer N+1) (live 09-22) | — solid | confirmed 09-22 |
| Device-agnostic | model AND data must both be `.to(device)`; ops error across devices (live 09-22) | — solid | confirmed 09-22 |
| Linear collapse / nonlinearity | stacked Linear = one linear map → circles stall ~50%; THE fix is a nonlinear activation, not depth/epochs/lr (live 09-22, twice) | has NOT yet coded ReLU in — knows the fix, hasn't applied it | confirmed 09-22 |
| **Logits / sigmoid / probs / labels** | **TAUGHT & LANDED 09-22.** logit = raw pre-sigmoid score; sigmoid squashes ℝ→(0,1)=prob; round@0.5→label; `logit>0 ⇔ class1` shortcut; BCEWithLogitsLoss fuses sigmoid for stability (explains loop's logits-to-loss vs sigmoid-to-preds split); accuracy_fn compares labels. Predicted full pipeline correctly hands-on. | **fragile edge: the exact-0 boundary** — used `≥` not strict `>` (put logit 0.0 → class1; correct is class0, matches torch round-half-to-even `round(0.5)=0`). Narrow convention slip, recheck once. | taught 09-22 |
| Classification data pipeline | make_circles, train/test split, numpy→tensor `.type(torch.float32)` — all in working code | not probed deeply; assume floor-solid from working code | seeded |
| Dataset / DataLoader | — | **absent** — SKIPPED, not current focus | seeded |

**The edge, in one line (updated 09-22):** *training-loop mechanics and the
linear-collapse insight are rock-solid; the frontier is the logit→sigmoid→probability→label
chain — he runs the pipeline without seeing through it.* Teaching starts at "what
is a logit / why sigmoid," then code ReLU into V1.
Still open from before (not re-probed 09-22): `torch.save` bug — passed
`model_0.state_dict` (method) not `state_dict()` (call); flagged, not yet fixed.

---

## Misconceptions

Log as: `- [date] <belief> — dislodged | STILL LIVE — <note>`.

- [2026-08-27] "reshape returns an independent copy of the data" — **STILL LIVE** — no concept yet that a tensor = flat storage + shape/stride metadata, so reshape/view usually *share* storage. NOT re-probed 09-22 (assessment focused on 01/02, not tensor mechanics).
- [2026-08-27] "model.train()/eval() toggle requires_grad / gradient tracking" — **DISLODGED**, and **HELD on recheck 09-22** (cleanly picked eval=mode-flags / inference_mode=stops-tracking at hard difficulty). Considered solid now.
- [2026-09-22] "you can round the raw logits directly to get the class label" — **DISLODGED same session** — after concrete side-by-side (round(logit) gives 2,-2,… vs round(sigmoid)∈{0,1}) + hands-on predict-before-run, he predicted the full logit→prob→label pipeline correctly. Solid. Recheck ~+3d.
- [2026-09-22] "accuracy_fn's `eq(...).sum()` sums predicted probabilities" — **RESOLVED** — was downstream of the logit/sigmoid gap; once that landed he saw `y_pred` is already labels by that point. Treat as cleared (was not a real separate misconception).
- [2026-09-22] NEW, minor: uses `≥` at the decision boundary (thinks logit `0.0`/prob `0.5` → class 1). Real convention is strict `logit > 0`, and `torch.round` is half-to-even so `round(0.5)=0` → class 0. Narrow slip on a rare edge case; recheck once, don't over-invest.

---

## Nodes taught

Log as: `- [date] <node> — landed? held on recheck [date]? | needs rebuild`.

- [2026-08-27] train()/eval() = mode flag, not grad tracking — landed; **held on recheck 09-22**.
- [2026-08-27] SGD update rule `p ← p - lr·∂loss/∂p`; step size scales with gradient magnitude — landed after a struggle, confirmed via hands-on. NOT re-probed 09-22.
- [2026-08-27] full loop as causal chain + WHY the order — confirmed via hands-on. **Held on recheck 09-22** (zero_grad-accumulation + backward-fills-.grad both hard-correct).

**Assessment 09-22 (mapping):** confirmed HELD at hard difficulty — training-loop chain, eval/inference_mode, nn.Parameter, shape/squeeze, nn.Linear wiring, device placement, linear-collapse→nonlinearity. Found the edge at logits/sigmoid.

- [2026-09-22] logit/sigmoid/prob/label chain (what a logit is, sigmoid as ℝ→(0,1) bridge, round→label, why sigmoid-before-round) — **landed** after 2 misses → de-escalated to concrete numbers + hands-on predict-before-run (predicted pipeline perfectly). Ref written: `lessons/logits_sigmoid.md`. due recheck ~+3d.
- [2026-09-22] `logit > 0 ⇔ class 1` shortcut (sigmoid monotonic, σ(0)=0.5) — landed; boundary case (exact 0) still fragile. due recheck ~+2d.
- [2026-09-22] BCEWithLogitsLoss fuses sigmoid for numerical stability; explains loop feeding raw logits to loss but sigmoid to predictions — landed (expository payoff, not independently quizzed). recheck +3d.

---

## Review schedule (spaced)

For computing intervals, not guessing. A node that **held** lengthens its
interval (e.g. 1d → 3d → 7d → 16d → 35d); a node that **needed rebuilding**
resets to ~1d. Log as: `- <node> — last reviewed <date>, held ×N, due <date>`.

- train/eval mode flag — last reviewed 2026-09-22, held ×2, due 2026-09-29
- SGD update rule — last reviewed 2026-08-27, held ×1 (not re-probed 09-22), due 2026-09-23 (overdue — recheck next session)
- full-loop chain — last reviewed 2026-09-22, held ×2, due 2026-09-29
- shape/squeeze + nn.Linear wiring — last reviewed 2026-09-22, held ×1, due 2026-09-25
- linear-collapse → nonlinearity — last reviewed 2026-09-22, held ×1, due 2026-09-25
- logit/sigmoid/prob/label chain — last reviewed 2026-09-22, held ×1 (landed after rebuild), due 2026-09-25
- logit>0 shortcut (+ exact-0 boundary) — last reviewed 2026-09-22, held ×1 w/ boundary slip, due 2026-09-24 (recheck boundary)
- BCEWithLogitsLoss = fused sigmoid+BCE for stability — last reviewed 2026-09-22, held ×1 (not independently quizzed), due 2026-09-25
