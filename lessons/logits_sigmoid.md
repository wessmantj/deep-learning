# Logits → Sigmoid → Probability → Label

The chain that turns a model's raw output into a binary class prediction.

---

## 1. The problem

A `nn.Linear` layer computes $z = Wx + b$. That output $z$ is a **raw real number** — it can be anything in $(-\infty, +\infty)$.

But for binary classification we want to answer: *"how likely is this class 1?"* — a **probability**, which by definition must live in $[0, 1]$.

So there's a gap:

$$\text{model output } z \in (-\infty, \infty) \qquad\longrightarrow\qquad \text{probability } p \in [0, 1]$$

We need a **bridge**: a function that squashes any real number into $(0,1)$.

## 2. Discovering the bridge — what must it do?

Before naming anything, list what this squashing function *has* to satisfy:

- Takes any real input, outputs a value in $(0, 1)$.
- **Monotonic increasing** — a bigger raw score should mean a higher probability (order preserved).
- Maps $0 \mapsto 0.5$ — a raw score of zero is "undecided," a coin flip.
- Large positive $\mapsto$ near $1$; large negative $\mapsto$ near $0$.
- Smooth (differentiable), so backprop can flow through it.

The function that does exactly this is the **sigmoid**:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

Check it against the wishlist:

| $z$ | $e^{-z}$ | $\sigma(z)$ |
|---|---|---|
| $\to +\infty$ | $\to 0$ | $\to 1$ |
| $0$ | $1$ | $0.5$ |
| $\to -\infty$ | $\to +\infty$ | $\to 0$ |

```
 σ(z)
 1.0 |                       . - - ─────
     |                  .
 0.5 |- - - - - - - - •
     |          .
 0.0 |___ ─────. ______________________
     -6      0                      +6   z
```

## 3. So what *is* a "logit"?

A **logit** is just the model's **raw, pre-sigmoid output** $z$ — the real number in $(-\infty, \infty)$.

The name comes from it being the *inverse* of the sigmoid, the **log-odds**:

$$\text{logit}(p) = \log\!\left(\frac{p}{1-p}\right), \qquad \sigma\big(\text{logit}(p)\big) = p$$

You don't need the log-odds algebra day to day. The one-liner to keep: **a logit is the raw score sigmoid turns into a probability.**

## 4. From probability to a 0/1 label

Once you have $p = \sigma(z)$, decide the class by thresholding at $0.5$:

$$\hat{y} = \begin{cases} 1 & p > 0.5 \\ 0 & p < 0.5 \end{cases}$$

That's what `torch.round(p)` does. **Gotcha:** at exactly $p = 0.5$, `torch.round` breaks the tie toward the **even** integer (round-half-to-even), so `round(0.5) = 0`, `round(1.5) = 2`, `round(2.5) = 2`. A logit of exactly $0.0$ therefore lands in class $0$. Rare in practice (real logits are almost never exactly $0$), but real.

Hence the pipeline in your code:

```python
y_pred = torch.round(torch.sigmoid(y_logits))   # logits → probs → labels
```

### Why you can't round the raw logit

`torch.round(logit)` rounds the raw score to the nearest **integer**:

- logit $= 2.3 \to$ rounds to $2$
- logit $= -1.6 \to$ rounds to $-2$
- logit $= 0.4 \to$ rounds to $0$

You'd get labels like $2$, $-2$, $7$ — nonsense for a two-class problem. Sigmoid **first** guarantees the value is in $(0,1)$, so rounding can only ever give $0$ or $1$. That's the whole reason sigmoid sits before round.

---

## 5. The shortcut — skip sigmoid for the prediction

Sigmoid is monotonic and $\sigma(0) = 0.5$, so:

$$p > 0.5 \iff \sigma(z) > 0.5 \iff z > 0$$

All three are the same statement. To pick the **label** you only need the **sign of the logit**: $z > 0 \Rightarrow$ class 1, else class 0. No sigmoid required. (Sigmoid is still needed for the loss and for a readable probability.)

## 6. Why `BCEWithLogitsLoss` takes raw logits

BCE needs a probability, so it must sigmoid the logits first. `BCEWithLogitsLoss` **fuses** sigmoid + BCE into one op that is **numerically stable** — computing $\log \sigma(z)$ naively overflows for large $|z|$; the fused version uses the log-sum-exp trick to avoid it. Prefer it over `sigmoid` + `BCELoss`.

This is why the training loop is asymmetric:

```python
loss   = loss_fn(y_logits, y_train)              # RAW logits — BCEWithLogitsLoss sigmoids inside
y_pred = torch.round(torch.sigmoid(y_logits))    # sigmoid yourself for the LABEL (or: y_logits > 0)
```

- **Loss** → feed raw logits.
- **Prediction** → sigmoid + round yourself, or just `logit > 0`.
- By the time `y_pred` reaches `accuracy_fn`, it's already labels (0/1), so `eq(y_true, y_pred).sum()` counts matching **labels**, not probabilities.
