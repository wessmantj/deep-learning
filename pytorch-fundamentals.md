# PyTorch Fundamentals — Notes

Companion code: [`00_pytorch_fundamentals.py`](./00_pytorch_fundamentals.py)

## Table of contents
- [What is Deep Learning good for?](#what-is-deep-learning-good-for)
- [What is Deep Learning *not* great for?](#what-is-deep-learning-not-great-for)
- [Machine Learning vs Deep Learning](#machine-learning-vs-deep-learning)
- [Neural Networks](#neural-networks)
- [Tensors: scalar, vector, matrix, tensor](#tensors-scalar-vector-matrix-tensor)
- [Random tensors](#random-tensors)
- [Getting information from tensors](#getting-information-from-tensors)
- [Tensor operations](#tensor-operations)

---

## What is Deep Learning good for?

- **Problems with long lists of rules.** An example of this could be, say you are
  playing basketball and you know how to shoot from one spot, how to dribble, etc.
  That is a rule. For you to now go and learn how to do the same with the other hand,
  from the other side of the court, another. For the entire court floor there is
  millions of places where you can dribble shoot, can't dribble or shoot, and these
  all make up rules which to us, are subconscious. To automate something like this,
  you would need Deep Learning.

- **Continually changing environments.** Continuing with the basketball analogy, say
  you are now moved to a different court, or even a different sport, you would, with
  your new gained athleticism, be able to comprehend some of what's going on. Deep
  Learning allows the models to adapt or learn in new scenarios, based on past
  experience, just like us.

- **Discovering insights within large collections of data.** Again, basketball. Say
  you want to make an app that shows what a good shot is versus a bad one. You would
  need a set of rules. These rules would need to span not only what a good shot looks
  like from every spot on the court, but also a bad shot. Deep Learning is a feasible
  solution to this.

## What is Deep Learning *not* great for?

- **When you need explainability.** Since the patterns learned by a deep learning
  model are typically converted to data, floats and integers, they become
  uninterpretable by humans.

- **When the traditional approach is a better option** or can accomplish what you need
  with a simple rule-based system.

- **When errors are unacceptable.** Since its output is not always predictable and may
  hallucinate, you need margin for mistake.

- **When the data pool isn't large enough.** Deep Learning models usually require large
  amounts of data to produce great results, so the more it can be trained on and see
  possibilities, the more it can get better results on unseen data.

## Machine Learning vs Deep Learning

| Machine Learning (typically structured data) | Deep Learning (typically unstructured data) |
| --- | --- |
| XGBoost algorithm | Neural networks |
| Random forest | Fully connected neural network |
| Gradient boosted models | Convolutional neural network |
| Naive Bayes | Recurrent neural network |
| Nearest neighbor | Transformer |
| Support vector machine | (image & audio data — "brings order to mess") |
| ... | ... |

## Neural Networks

Input data — unstructured, like images, audio, unformatted text. This data needs to be
turned numerical and is collected in matrices or tensors. Then, the tensor/matrix is
passed through a neural network (many layers, nodes, types of networks) all following a
system of: input → manipulated and learns features → represents it how it best
understands → converted back into human-understood output.

## Tensors: scalar, vector, matrix, tensor

| Term | Definition | Dimensions | Naming convention |
| --- | --- | --- | --- |
| **Scalar** | a single number | 0-D | lowercase |
| **Vector** | a number with direction, can contain many numbers | 1-D | lowercase |
| **Matrix** | a 2-dimensional array of numbers | 2-D | UPPERCASE |
| **Tensor** | an n-dimensional array of numbers | n-D | UPPERCASE |

> A 0-dimensional tensor is a scalar, and a 1-dimensional tensor is a vector.

## Random tensors

Random tensors are a big part of PyTorch because the way many neural networks learn is
that they **start with tensors full of random numbers and adjust those numbers** to
better represent the data.

## Getting information from tensors

Three attributes you'll reach for constantly:

1. `tensor.dtype` — the datatype
2. `tensor.shape` — the shape
3. `tensor.device` — the device it lives on (cpu / cuda / mps)

## Tensor operations

Tensor operations include:
- addition
- subtraction
- multiplication (element-wise)
- division
- matrix multiplication
