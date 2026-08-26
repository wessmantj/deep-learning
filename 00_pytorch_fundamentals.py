import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(torch.__version__)

if torch.backends.mps.is_available():
    mps_device = torch.device("mps")
    x = torch.ones(1, device=mps_device)
    print (x)
else:
    print ("MPS device not found.")

## Introduction to Tensors

### Creating Tensors

# scalar
scalar = torch.tensor(7)
print(scalar)

# check dimensions
print(scalar.ndim)

# get back as Python int
print(scalar.item())

# vector
vector = torch.tensor([7, 6, 7, 1])
print(vector)

print(vector.shape)

print(vector.ndim)

# MATRIX
MATRIX = torch.tensor([[7, 6],
                       [5, 6]])
print(MATRIX)

print(MATRIX.ndim)
print(MATRIX.shape)

# TENSOR
TENSOR = torch.tensor([[[1, 2, 3, 4],
                        [2, 3, 4, 2],
                        [2, 3, 1, 0]]])
print(TENSOR)
print(TENSOR.ndim)
print(TENSOR.shape)

### Random Tensors

random_tensor = torch.rand(3, 4, 2)
print(random_tensor)
print(random_tensor.ndim)
print(random_tensor.shape)

random_image_size_tensor = torch.rand(size=(224, 224, 3)) # height, width, color channel (R, G, B)

print(random_image_size_tensor.shape)
print(random_image_size_tensor.ndim)

# Create a tensor of all zeros
zeros = torch.zeros(size=(3, 4, 2))
print(zeros)
print(zeros*random_tensor)

# all ones
ones = torch.ones(size=(3, 4, 2))
print(ones)

### Create range of tensors and tensors-like

one_to_ten = torch.arange(start=0,end=11, step=1)
print(one_to_ten)

# gives same shape as input, but zeros _like
ten_zeros = torch.zeros_like(input=one_to_ten)

### Tensor datatypes

float_32_tensor = torch.tensor([3.0, 6.0, 9.0],
                                dtype=None, # what datatype all in docs
                                device=None, # either cpu, gpu, cuda, what device the tensor lives on
                                requires_grad=False) # want pytorch to track gradient
print(float_32_tensor) # default type float32

float_16_tensor = float_32_tensor.type(torch.half) # or torch.float16
print(float_16_tensor)