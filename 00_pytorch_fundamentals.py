"""
00 - PyTorch Fundamentals
=========================
Follow-along code for the PyTorch fundamentals section.
Run locally on Apple Silicon using the MPS (GPU) backend.

Companion notes: pytorch-fundamentals.md
"""

import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"PyTorch version: {torch.__version__}")


# =============================================================================
# 0. Device setup (CPU / GPU)
# =============================================================================
# The course uses "cuda" (NVIDIA GPUs). On a Mac we use "mps" (Apple GPU).
# This block picks the best available device and stores it in `device` so we
# can send tensors to the GPU later with `.to(device)`.
if torch.cuda.is_available():
    device = "cuda"          # NVIDIA GPU (e.g. Google Colab)
elif torch.backends.mps.is_available():
    device = "mps"           # Apple Silicon GPU
else:
    device = "cpu"           # fallback
print(f"Using device: {device}")

# quick sanity check that the GPU works
x = torch.ones(1, device=device)
print(x)


# =============================================================================
# 1. Introduction to Tensors
# =============================================================================

# -----------------------------------------------------------------------------
# 1.1 Creating tensors
# -----------------------------------------------------------------------------

# scalar - a single number, 0-dimensional
scalar = torch.tensor(7)
print(scalar)
print(scalar.ndim)        # number of dimensions
print(scalar.item())      # get back as a Python int

# vector - 1-dimensional
vector = torch.tensor([7, 6, 7, 1])
print(vector)
print(vector.shape)
print(vector.ndim)

# MATRIX - 2-dimensional (convention: uppercase name)
MATRIX = torch.tensor([[7, 6],
                       [5, 6]])
print(MATRIX)
print(MATRIX.ndim)
print(MATRIX.shape)

# TENSOR - n-dimensional (convention: uppercase name)
TENSOR = torch.tensor([[[1, 2, 3, 4],
                        [2, 3, 4, 2],
                        [2, 3, 1, 0]]])
print(TENSOR)
print(TENSOR.ndim)
print(TENSOR.shape)

# -----------------------------------------------------------------------------
# 1.2 Random tensors
# -----------------------------------------------------------------------------
# Neural networks often start with random numbers and adjust them to fit data.

random_tensor = torch.rand(3, 4, 2)
print(random_tensor)
print(random_tensor.ndim)
print(random_tensor.shape)

# a random tensor shaped like an image: height, width, color channels (R, G, B)
random_image_size_tensor = torch.rand(size=(224, 224, 3))
print(random_image_size_tensor.shape)
print(random_image_size_tensor.ndim)

# -----------------------------------------------------------------------------
# 1.3 Zeros, ones, and ranges
# -----------------------------------------------------------------------------

# a tensor of all zeros
zeros = torch.zeros(size=(3, 4, 2))
print(zeros)
print(zeros * random_tensor)

# a tensor of all ones
ones = torch.ones(size=(3, 4, 2))
print(ones)

# a range of values
one_to_ten = torch.arange(start=0, end=11, step=1)
print(one_to_ten)

# match the shape of an input, filled with zeros (also see torch.ones_like)
ten_zeros = torch.zeros_like(input=one_to_ten)
print(ten_zeros)

# -----------------------------------------------------------------------------
# 1.4 Tensor datatypes
# -----------------------------------------------------------------------------

float_32_tensor = torch.tensor([3.0, 6.0, 9.0],
                               dtype=None,          # datatype (default float32); see docs for options
                               device=None,         # device the tensor lives on: cpu, cuda, mps
                               requires_grad=False)  # whether PyTorch tracks gradients on it
print(float_32_tensor)                              # default type is float32

float_16_tensor = float_32_tensor.type(torch.half)  # torch.half == torch.float16
print(float_16_tensor)

print(float_16_tensor * float_32_tensor)

# -----------------------------------------------------------------------------
# 1.5 Getting information from tensors (attributes)
# -----------------------------------------------------------------------------
# Three you'll reach for constantly: .dtype, .shape, .device

some_tensor = torch.rand(4, 4)
print(f"Datatype of tensor: {some_tensor.dtype}")
print(f"Shape of tensor: {some_tensor.shape}")
print(f"Device tensor lives on: {some_tensor.device}")


# =============================================================================
# 2. Manipulating Tensors
# =============================================================================
# TODO: tensor operations - addition, subtraction, element-wise multiplication,
#       division, and matrix multiplication.
