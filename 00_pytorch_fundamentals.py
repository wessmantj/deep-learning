"""
00 - PyTorch Fundamentals

Ran locally on Apple Silicon using the MPS (GPU) backend.

Companion notes: pytorch-fundamentals.md
"""

import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"PyTorch version: {torch.__version__}")


# Device setup (CPU / GPU)

"""
The course uses "cuda" (NVIDIA GPUs). On a Mac we use "mps" (Apple GPU).
This block picks the best available device and stores it in `device` so we can send tensors to the GPU later with `.to(device)`.
"""

if torch.cuda.is_available():
    device = "cuda"          # NVIDIA GPU 
elif torch.backends.mps.is_available():
    device = "mps"           # Apple Silicon GPU
else:
    device = "cpu"           # fallback
print(f"Using device: {device}")

# quick sanity check that the GPU works
x = torch.ones(1, device=device)
print(x)


# Introduction to Tensors

# Creating tensors

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


# Random tensors

# Neural networks often start with random numbers and adjust them to fit data.

random_tensor = torch.rand(3, 4, 2)
print(random_tensor)
print(random_tensor.ndim)
print(random_tensor.shape)

# a random tensor shaped like an image: height, width, color channels (R, G, B)
random_image_size_tensor = torch.rand(size=(224, 224, 3))
print(random_image_size_tensor.shape)
print(random_image_size_tensor.ndim)


# Zeros, ones, and ranges

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


# Tensor datatypes

float_32_tensor = torch.tensor([3.0, 6.0, 9.0],
                               dtype=None,          # datatype (default float32); see docs for options
                               device=None,         # device the tensor lives on: cpu, cuda, mps
                               requires_grad=False)  # whether PyTorch tracks gradients on it
print(float_32_tensor) # default type is float32

float_16_tensor = float_32_tensor.type(torch.half) # torch.half == torch.float16
print(float_16_tensor)

print(float_16_tensor * float_32_tensor)


# Getting information from tensors (attributes)
# Three constantly used: .dtype, .shape, .device

some_tensor = torch.rand(4, 4)
print(f"Datatype of tensor: {some_tensor.dtype}")
print(f"Shape of tensor: {some_tensor.shape}")
print(f"Device tensor lives on: {some_tensor.device}")


# Manipulating Tensors

tensor = torch.tensor([1, 2, 3])

# addition with tensors
print(tensor + 10)
print(tensor + 100)
print(torch.add(tensor, 10))

# subtraction with tensors
print(tensor - 10)
print(tensor - 5)
print(torch.subtract(tensor, 5))

# multiplication with tensors (element-wise)
print(tensor * 10)
print(tensor * 15)
print(torch.mul(tensor, 10))

# Matrix Multiplication

# this just flips it to work, but isn't real world application
tensor = torch.tensor([[12, 1, 20, 4],
                      [2, 13, 1, 7],
                      [5, 40, 2, 1]])
print(torch.matmul(tensor, torch.rot90(tensor, k=1)))
print(tensor @ torch.rot90(tensor))

# or instead of rot90, we can use .T to flix the axis; this is actually used
print(f"Original: \n{tensor} \nRotated: \n{tensor.T}")
print(f"Gram Matrix (normal method): \n{torch.matmul(tensor, tensor.T)}")


# Finding the min, max, mean, sum, etc. (tensor aggregation)

x = torch.arange(1, 100.0, 12) 
print(f"Tensor: \n{x}")
print(f"Min: {torch.min(x)}")
print(f"Max: {torch.max(x)}")
print(f"Mean: {torch.mean(x)}") # will cause TypeError if not float32

print(f"Sum: {torch.sum(x)}") # the normal x.sum() python function works too

# positional min & max
print(f"Positional/Index Min: {torch.argmin(x)}")
print(f"Positional/Index Max: {torch.argmax(x)}")


# Reshaping, stacking, squeezing and unsqueezing tensors

x = torch.arange(1., 10.)
print("")
print(f"Original x: {x} \nx.shape: {x.shape}")

# add an extra dimension
x_reshaped = x.reshape(1, 9), # As long as the reshape sums  to the original size, it will work
x_reshaped = x.reshape(1, 3, 3)
print(f"Reshaped x: {x_reshaped} \nNew x.shape: {x_reshaped.shape}")

# change the view
z = x.view(1, 9) # shares the same memory as x, so changing it changes the original tensor
z[:, 0] = 5
print(z)
print(x)

# stack tensors

x_stacked = torch.stack([x, x, x, x], dim=0)
print(x_stacked)

 # squeeze tensors

# removes all singel dimensions from a single tensor e.g. if shape (A x 1 x B x 1) out tensor shape is (A x B)

print()
x_squeezed = x_reshaped.squeeze()
print(f"Pre-squeeze Shape: {x_reshaped.shape} \nPost-squeeze: {x_squeezed.shape}")

x_unsqueezed = x_squeezed.unsqueeze(dim=1) # dim changes which one so if orgininal [3, 3] and dim = 0, [1, 3, 3] or dim = 2 [3, 3, 1]
print(f"Pre-squeeze Shape: {x_reshaped.shape} \nSqueeze: {x_squeezed.shape} \nUnsqueezed Shape: {x_unsqueezed.shape}")

# rearrange dimensions of target tensor in specified order

x_permuited = x_unsqueezed.permute(2, 0, 1) # moves 2nd dim first, then 0th, then 1st. [3, 1, 3] -> [3, 3, 1]
print(f"Permuited/Rearranged Shape: {x_permuited.shape}")

# indexing within tensors (similar to NumPy)

x = torch.arange(1., 10., 1).reshape(1, 3, 3)
print()
print(f"Orginal x: {x} \nOriginal x.shape: {x.shape}")
print(f"First dimension: {x[0]}\nSecond dimension: {x[0][2]}\nLast dimension: {x[0][1][1]}")

print(x[0][2][2]) # dim 0, dim 2, dim[2]
print(x[:, :, 2]) # dim 1 & 2, dim[2]

# Some numpy tensor conversion
tensor = torch.ones(7)
numpy_tensor = tensor.numpy()
print(tensor.dtype, numpy_tensor.dtype)

rand_tensor_1 = torch.rand(3, 4)
rand_tensor_2 = torch.rand(3, 4)

print(rand_tensor_1 == rand_tensor_2)

# set random seed, still random but reproducable
RANDOM_SEED = 324234

torch.manual_seed(RANDOM_SEED) # need to use this format, manual seed in cell, then definition.
rand_tensor_3 = torch.rand(3, 4)

torch.manual_seed(RANDOM_SEED)
rand_tensor_4 = torch.rand(3, 4)

print(rand_tensor_3 == rand_tensor_4)

# Moving a tensor to GPU, on mac is MPS
tensor_on_mps = tensor.to(device)
print(tensor_on_mps)

# Move back to CPU (for NumPy or other)
tensor_on_cpu = tensor_on_mps.cpu().numpy()
print(tensor_on_cpu, tensor_on_cpu.device)