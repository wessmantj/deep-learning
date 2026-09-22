"""
02 - PyTorch Neural Network Classification

Ran locally on Apple Silicon using the MPS (GPU) backend.

Companion notes: 02_pytorch_nn_classification.md
"""

from typing import Any

import sklearn
from sklearn.datasets import make_circles
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
import torch
from torch import nn
import requests
import numpy as np 
from pathlib import Path

# Make classification data and get ready
n_samples = 1000

# create circles
X, y = make_circles(n_samples,
                    noise=0.03,
                    random_state=42)    # random seed

print(f"X length: {len(X)} \ny length: {len(y)}")
print(f"\nFirst 5 samples of X: \n{X[:5]}")
print(f"First 5 samples of y: \n{y[:5]}") # 0 or 1; binary classification

# make a DataFrame of circle data
circles = pd.DataFrame({"X1" : X[:, 0],
                        "X2" : X[:, 1],
                        "label" : y})

print("\n", circles.head(10))

# visualize
plt.scatter(x=X[:, 0],
            y=X[:, 1],
            c=y,
            cmap=plt.cm.RdYlBu)

# plt.show()  # shows two circles, given an input we are trying to have it predict if it will be on the red area or blue area (seperating the two)

# Check input and output shapes
print(f"X.shape: {X.shape} \ny.shape: {y.shape}")

# view the first example of features and labels
X_sample = X[0]
y_sample = y[0]

print(f"Values for one same of X: {X_sample} and the same for y: {y_sample}")
print(f"Shapes for one sample of X: {X_sample.shape} and the same for y: {y_sample.shape}")

# Turn data into tensors and create train and test splits

X = torch.from_numpy(X).type(torch.float32) # turned to tensor
y = torch.from_numpy(y).type(torch.float) # turned to tensor

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,  # 0.2 = 20% of data will be test, 80% will be train
                                                    random_state=42)    # random seed

print(f"\nTotal samples: {n_samples} \nX_train samples: {len(X_train)} \nX_test samples: {len(X_test)} \ny_train samples: {len(y_train)}  \ny_test samples: {len(y_test)}")  # 80/20 split

# Building a model to classify blue and red dots

# device agnostic 
if torch.cuda.is_available():
    device = "cuda"          # NVIDIA GPU 
elif torch.backends.mps.is_available():
    device = "mps"           # Apple Silicon GPU
else:
    device = "cpu"           # fallback
print(f"\nUsing device: {device}")



class CircleModelV0(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        
        # create two layers capable of handling shapes of data
        self.layer_1 = nn.Linear(in_features=2,
                                 out_features=5)    # takes in two features and upscales to 5 (or x) features
        
        self.layer_2 = nn.Linear(in_features=5,
                                 out_features=1)    # takes in 5 features from prev layer and outputs single feature
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layer_2(self.layer_1(x))
    
model_0 = CircleModelV0().to(device)

model_0 = nn.Sequential(
    nn.Linear(in_features=2, out_features=5),
    nn.Linear(in_features=5, out_features=1)
).to(device)

print(model_0.state_dict())  # Same model as before, sequences layers and makes forward method for us in descending order. Good for quick test but when there are more complex operations and forward pass, its secondary to subclassing nn.Module.

# Make predictions
with torch.inference_mode():
    untrained_preds = model_0(X_test.to(device))
print(f"Length preds: {len(untrained_preds)} \nShape preds: {untrained_preds.shape}")
print(f"Length test samples: {len(X_test)} \nShape test: {X_test.shape}")

loss_fn = torch.nn.BCEWithLogitsLoss()  # BCEWithLogitsLoss = signmoid activation function built-in
optimizer = torch.optim.SGD(params=model_0.parameters(),
                            lr=0.1)

# Calculate accuracy - so out of 100 examples, what percentage does our model get right?
def accuracy_fn(y_true, y_pred):
    correct = torch.eq(y_true, y_pred).sum().item()
    acc = (correct/len(y_pred) * 100)
    
    return acc


# Train model

X_train = X_train.to(device)
y_train = y_train.to(device)
X_test = X_test.to(device)
y_test = y_test.to(device)

epochs = 201

for epoch in range(epochs):
    model_0.train()
    
    y_logits = model_0(X_train).squeeze()
    y_pred = torch.round(torch.sigmoid(y_logits)) # turn logits -> pred probs -> pred labels
    loss = loss_fn(y_logits, y_train)
    
    acc = accuracy_fn(y_true=y_train,
                      y_pred=y_pred)
    
    optimizer.zero_grad()
    
    loss.backward()
    
    optimizer.step()    


    model_0.eval()
    with torch.inference_mode():
        test_logits = model_0(X_test).squeeze()
        test_pred = torch.round(torch.sigmoid(test_logits))
        test_loss = loss_fn(test_logits, y_test)
        test_acc = accuracy_fn(y_true=y_test,
                                y_pred=test_pred)
            
    if epoch % 10 == 0:
        print(f"EPOCH: {epoch} | LOSS: {loss:.6f} | TEST LOSS: {test_loss:.6f} | TEST ACC: {test_acc:.2f}")
            
# Make predictions and evaluate why model isn't learning
    
if Path("helper_functions.py").is_file():
    print("helper_functions.py already exists, skipping download.")
else:
    print("Downloading helper_functions.py")
    request = requests.get("https://raw.githubusercontent.com/mrdbourke/pytorch-deep-learning/refs/heads/main/helper_functions.py")
    with open("helper_functions.py", "wb") as f:
        f.write(request.content)
        
from helper_functions import plot_predictions, plot_decision_boundary

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("Train")
plot_decision_boundary(model_0, X_train, y_train)
plt.subplot(1, 2, 2)
plt.title("Test")
plot_decision_boundary(model_0, X_test, y_test)
# plt.show()  # linear layer is trying to split the whole dataset in half since two classes, red or blue

# Improving the model
class CircleModelV1(nn.Module):
    def __init__(self) -> None:
        super().__init__()
    
        self.layer_1 = nn.Linear(in_features=2,
                                 out_features=10)
        self.layer_2 = nn.Linear(in_features=10,
                                 out_features=10)
        self.layer_3 = nn.Linear(in_features=10,
                                 out_features=1)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # z = self.layer_1(x)
        # z = self.layer_2(z)
        #z = self.layer_3(z)
        return self.layer_3(self.layer_2(self.layer_1(x)))
    
model_1 = CircleModelV1().to(device)
    
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.SGD(params=model_1.parameters(),
                                 lr=0.01)
    
torch.manual_seed(42)
torch.mps.manual_seed(42)
    
epochs = 1001   
    
X_train, y_train = X_train.to(device), y_train.to(device)
X_test, y_test = X_test.to(device), y_test.to(device)
    
for epoch in range(epochs):
    model_1.train()
        
    y_logits = model_1(X_train).squeeze()
    y_pred = torch.round(torch.sigmoid(y_logits)) # logits -> pred probabilities -> prediction labels
        
    loss = loss_fn(y_logits, y_train)
    acc = accuracy_fn(y_true=y_train, y_pred=y_pred)

    optimizer.zero_grad()
    loss.backward()
        
    optimizer.step()
        
        
    model_1.eval()
    with torch.inference_mode():
        test_logits = model_1(X_test).squeeze()
        test_pred = torch.round(torch.sigmoid(test_logits))
            
        test_loss = loss_fn(test_logits, y_test)
        test_acc = accuracy_fn(y_true=y_test,
                                   y_pred=test_pred)
            
    if epoch % 50 == 0:
        print(f"EPOCH: {epoch} | LOSS: {loss:.6f} | TEST LOSS: {test_loss:.6f} | TEST ACC: {test_acc:.2f}")
