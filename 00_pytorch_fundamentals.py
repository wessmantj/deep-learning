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

# matrix
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