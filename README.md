# pytorch-deep-learning

Follow-along work for a PyTorch deep learning course, run **locally on a Mac**
(Apple Silicon / MPS GPU backend) instead of Google Colab.

## Contents

| File | Description |
| --- | --- |
| [`00_pytorch_fundamentals.py`](./00_pytorch_fundamentals.py) | Code: tensors, datatypes, tensor attributes |
| [`00_pytorch_fundamentals.md`](./00_pytorch_fundamentals.md) | Notes: deep learning concepts & tensor theory |
| [`01_pytorch_workflow.py`](./01_pytorch_workflow.py) | Code: the end-to-end PyTorch workflow (data → model → train → save/load) |
| [`01_pytorch_workflow.md`](./01_pytorch_workflow.md) | Notes: the PyTorch workflow |
| [`02_pytorch_nn_classification.py`](./02_pytorch_nn_classification.py) | Code: neural network classification (in progress) |
| [`02_pytorch_nn_classification.md`](./02_pytorch_nn_classification.md) | Notes: neural network classification (in progress) |
| [`requirements.txt`](./requirements.txt) | Python dependencies |

## Setup

Using a conda environment (Python 3.11):

```bash
conda activate deep-learning
pip install -r requirements.txt
```

## Running on GPU (Mac)

The course uses NVIDIA's CUDA (`device = "cuda"`). On Apple Silicon there is no
NVIDIA GPU, so we use Apple's **MPS** backend instead. The code auto-detects the
best available device:

```python
if torch.cuda.is_available():
    device = "cuda"   # NVIDIA GPU (e.g. Colab)
elif torch.backends.mps.is_available():
    device = "mps"    # Apple Silicon GPU
else:
    device = "cpu"
```

Send tensors to it with `tensor.to(device)`.
