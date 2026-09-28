
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
from torch.utils.data import DataLoader


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

# Visualize
plt.imshow(image.squeeze())
plt.title(label)
plt.imshow(image.squeeze(), cmap="gray")
plt.title(class_names[label])
plt.axis(False)
plt.show()

# plot more images
torch.manual_seed(42)
fig = plt.figure(figsize=(9, 9))
rows, cols = 4, 4
for i in range(1, rows*cols+1):
    random_idx = torch.randint(0, len(train_data), size=[1]).item()
    img, label = train_data[random_idx]
    fig.add_subplot(rows, cols, i)
    plt.imshow(img.squeeze(), cmap="gray")
    plt.title(class_names[label])
    plt.axis(False)
    plt.show()
    
# Prepare DataLoader; turns dataset into Python iterable or batches/mini-batches

# batchsize hyperparameter
BATCH_SIZE = 32

train_dataloader = DataLoader(dataset=train_data,
                              batch_size=BATCH_SIZE,
                              shuffle=True) # good to shuffle data so model doesn't learn order
test_dataloader = DataLoader(dataset=test_data,
                             batch_size=BATCH_SIZE,
                             shuffle=False) # can shuffle, but easier to evaluate when in same order; just eval so it can't learn here

print(f"Dataloaders: \n{train_dataloader} \n{test_dataloader}")
print(f"Length train_dataloader: \n{len(train_dataloader)} batches of {BATCH_SIZE}...") # 60000 // 32
print(f"Length test_dataloader: \n{len(test_dataloader)} batches of {BATCH_SIZE}...") # 1000 // 32

# see whats inside the training dataloader
train_features_batch, train_labels_batch = next(iter(train_dataloader))

# show a sample
torch.manual_seed(42)
random_idx = torch.randint(0, len(train_features_batch), size=[1]).item()
img, label = train_features_batch[random_idx], train_labels_batch[random_idx]
plt.imshow(img.squeeze(), cmap="gray")
plt.title(class_names[label])
plt.axis(False)
print(f"Image size: {img.shape}")
print(f"Label: {label}, label size: {label.shape}")
plt.show()
