import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print(torch.__version__)

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