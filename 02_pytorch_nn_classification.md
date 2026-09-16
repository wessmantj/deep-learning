# PyTorch Neural Network Classification - Notes

Companion code: [`02_pytorch_nn_classification.py`](./02_pytorch_nn_classification.py)

## Table of contents
- [What is a classification problem?](#what-is-a-classification-problem)
- [Architecture of a classification model](#architecture-of-a-classification-model)
- [Making classification data](#making-classification-data)
- [Building the model](#building-the-model)

---

## What is a classification problem?

- **Binary classification** — is an email spam or not spam. Either yes or no.
- **Multiclass classification** — is a photo sushi, steak, or pizza. More than one option, but the model assigns exactly one class to the given photo.
- **Multilabel classification** — what tags should this article have. Multiple options can apply per sample.

## Architecture of a classification model

(Binary first, then multiclass.)

- **Input layer shape (in_features):** Same as the number of features (e.g. 5 for age, sex, weight, smoking status in a heart disease prediction). Same for multiclass.
- **Hidden layer(s):** Problem specific. Minimum is 1, max is unlimited. Same for multiclass.
- **Neurons per hidden layer:** Problem specific, generally 10 to 512. Same for multiclass.
- **Output layer shape (out_features):** 1 (one class or the other), while for multiclass there is 1 per class (e.g. 3 for food, person, or dog photo identification).
- **Hidden layer activation:** Usually ReLU (rectified linear unit), but can be many others. Same for multiclass.
- **Output activation:** Sigmoid for binary and Softmax for multiclass.
- **Loss function:** Binary cross entropy for binary and cross entropy for multiclass.
- **Optimizer:** SGD (stochastic gradient descent) or Adam for both binary and multiclass, but many others exist.

## 
