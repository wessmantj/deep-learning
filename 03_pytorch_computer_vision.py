
# %% Imports Cell
import torch
from torch import nn
import torchvision
from torchvision import datasets
from torchvision import transforms
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
import pandas as pd
import requests
import numpy as np 
from pathlib import Path


# device agnostic 
if torch.cuda.is_available():
    device = "cuda"          # NVIDIA GPU 
elif torch.backends.mps.is_available():
    device = "mps"           # Apple Silicon GPU
else:
    device = "cpu"           # fallback
print(f"\nUsing device: {device}")

if Path("helper_functions.py").is_file():
    print("helper_functions.py already exists, skipping download.")
else:
    print("Downloading helper_functions.py")
    request = requests.get("https://raw.githubusercontent.com/mrdbourke/pytorch-deep-learning/refs/heads/main/helper_functions.py")
    with open("helper_functions.py", "wb") as f:
        f.write(request.content)
        
from helper_functions import plot_predictions, plot_decision_boundary

# %% Computer Vision

# Getting a dataset
train_data = datasets.FashionMNIST(
    root ="data",   # where to download data to?
    train=True,     # do we want the training dataset (False = testing set)
    download=True,  # do we want to download yes/no?
    transform=torchvision.transforms.ToTensor(),# how do we want to transform the data
    target_transform=None  # how do we want to transform the label/targets?
)

test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
    target_transform=None
)
# 60000 train, 10000 test

# See the first training example
image, label = train_data[0]
class_names = train_data.classes
print(f"Class names: {class_names}")

class_idx = train_data.class_to_idx
print(f"Class indexes: {class_idx}")

print(f"Image shape: {image.shape} -> [color_channels, height, width]")
print(f"Image label: {label}") 

