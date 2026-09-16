"""
01 - PyTorch Workflow

Ran locally on Apple Silicon using the MPS (GPU) backend.

Companion notes: 01_pytorch_workflow.md
"""

from typing import Any

import torch
from torch import nn # contains all of PyTorch's neural network building tools (Layers, Containers, Quantization, etc.)
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

workflow_outline = {1: " --- Data (prepare and load) --- ",
                    2: " --- Build model --- ",
                    3: " --- Fitting model to data --- ",
                    4: " --- Making predictions and evaluating a model (inference) --- ",
                    5: " --- Saving and loading a model --- ", 
                    6: " --- Combining it all together --- "}

# 1. Data (prep and load)
print(workflow_outline[1])

# create known parameters
weight = 0.8
bias = 0.2

# create 
start = 0
end = 1
step = 0.02
X = torch.arange(start, end, step).unsqueeze(dim=1)
y = weight * X + bias

print(X[:10], y[:10])

# splitting the data into training, validation, and test sets ***very important***

# create a train/test split
training_split = int(0.8 * len(X))
X_train, y_train = X[:training_split], y[:training_split]
X_test, y_test = X[training_split:], y[training_split:]

print(len(X_train), len(y_train), len(X_test), len(y_test))

def plot_predicitons(train_data=X_train,
                     train_labels=y_train,
                     test_data=X_test,
                     test_labels=y_test,
                     predictions=None):
    plt.figure(figsize=(10, 7))
    plt.scatter(train_data, train_labels, c="b", s=4, label="Training data")
    plt.scatter(test_data, test_labels, c="g", s=4, label="Testing data")

    if predictions is not None:
        plt.scatter(test_data, predictions, c="r", s=4, label="Predictions")

    plt.legend(prop={"size": 14})
    plt.show()


# 2. Creating linear regression model class
print("\n",workflow_outline[2])

class LinearRegressionModel(nn.Module): # subclasses nn.Module which contains all the tools for building neural networks
    def __init__(self):
        super().__init__()

        # init model parameters
        self.weights = nn.Parameter(torch.randn(1,
                                                requires_grad=True,     # default param, means PyTorch tracks graidents for the parameter
                                                dtype=torch.float32))
        self.bias = nn.Parameter(torch.randn(1,
                                             requires_grad=True,
                                             dtype=torch.float32))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.weights * x + self.bias     # linear regression formula


LinearRegressionModel()

# create random seed and instance of the model
torch.manual_seed(42)
model_0 = LinearRegressionModel()

# check parameters
print(f"\n{list(model_0.parameters())}")

print(f"\n{model_0.state_dict()}")

# Making predictions using `torch.inference_mode()`

with torch.inference_mode():    # makes code faster, no gradient tracking, or other background processes, also can use no_grad() for specific removal
    y_preds = model_0(X_test)


print(f"X_test: \n{X_test}\ny_preds: \n{y_preds}")
# print(plot_predicitons(predictions=y_preds))

# 3. Train model
print("\n",workflow_outline[3])

# set up a loss function
loss_fn = nn.L1Loss()

# set up an optimizer
optimizer = torch.optim.SGD(params=model_0.parameters(),    # stocastic gradient descent (random) for the parameters we want to optimize
                            lr=0.01)        # learning rate, very important hyperparameter you can set

# Building a training & testing loops in PyTorch

epochs = 230       # count of loops through the data... hyperparameter

# track different values to compare future experiements to past
epoch_count = []
loss_values = []
test_loss_values = []

for epoch in range(epochs):    # 0. loop through the data

    model_0.train()            # training mode for model, sets requires_grad = True
    y_pred = model_0(X_train)  # 1. forward pass
    
    # 2. calculate the loss
    loss = loss_fn(y_pred, y_train)# MAE or difference between model's predictions and labels (input, target)
    
    # 3. optimizer zero grad
    optimizer.zero_grad()
    
    # 4. perform backpropigation on the loss w/ respect to the params of the model
    loss.backward()
    
    # 5. step the optimizer aka gradient descent
    optimizer.step()       # how it changes will accumulate w/o zero_grad so it needs to happen above in step 3
    
    
    model_0.eval()             # evaluation mode, sets requires_grad = False
    with torch.inference_mode():    # turns off gradient tracking
        # 1. forward pass
        test_pred = model_0(X_test)
        
        # 2. calculate the loss
        test_loss = loss_fn(test_pred, y_test)
        
    if epoch % 10 == 0 or epoch % 229 == 0:
        epoch_count.append(epoch)
        loss_values.append(loss.item())
        test_loss_values.append(test_loss.item())
        print(f"Epoch: {epoch} | Loss: {loss:.6f} | Test loss: {test_loss:.6f}")

with torch.inference_mode():
    y_preds_new = model_0(X_test)

print(model_0.state_dict())
# plot_predicitons(predictions=y_preds)   # old predictions
# plot_predicitons(predictions=y_preds_new)   # new after training

plt.plot(epoch_count, loss_values, label="Train loss")
plt.plot(epoch_count, test_loss_values, label="Test loss")
plt.title("training and test loss curves")
plt.ylabel("Loss")
plt.xlabel("Epochs")
plt.legend()
# plt.show()


# 5. Saving a model
print("\n",workflow_outline[5])

# create model dir
MODEL_PATH = Path("models")
MODEL_PATH.mkdir(parents=True, exist_ok=True)

# create model save path
MODEL_NAME = "01_pytorch_workflow_model_0.pth"
MODEL_SAVE_PATH = MODEL_PATH / MODEL_NAME

# save the model state dict
print(f"Saving model to: {MODEL_SAVE_PATH}")
torch.save(obj=model_0.state_dict(), f=MODEL_SAVE_PATH)



# one manual SGD step (predict before running each print) 

w = torch.tensor([2.0], requires_grad=True)   # a single parameter
optimizer = torch.optim.SGD([w], lr=0.1)

loss = w ** 2          # our "loss" as a function of w

optimizer.zero_grad()
loss.backward()
print("grad:", w.grad)   # <-- PREDICT this first

optimizer.step()
print("w:", w)           # <-- PREDICT this before running

# Loading a PyTorch model

loaded_model_0 = LinearRegressionModel()

loaded_model_0.load_state_dict(torch.load(f=MODEL_SAVE_PATH))

print(loaded_model_0.state_dict())
print(model_0.state_dict())   # match parameters

# make some predictions of loaded vs original
loaded_model_0.eval()
with torch.inference_mode():
    loaded_model_0_preds = loaded_model_0(X_test)

model_0.eval()
with torch.inference_mode():
    y_pred = model_0(X_test)
    
print(f"Loaded model vs Original model: \n{y_pred == loaded_model_0_preds}")

# FULL WORKFLOW DONE BELOW

print("\n",workflow_outline[6])

# Data

if torch.cuda.is_available():
    device = "cuda"          # NVIDIA GPU 
elif torch.backends.mps.is_available():
    device = "mps"           # Apple Silicon GPU
else:
    device = "cpu"           # fallback
print(f"\nUsing device: {device}")

# create some data using linear regression formula of y = weight * (feat + bias)

weight, bias = 0.7, 0.3
print(f"\nWeight: {weight} \nBias: {bias}")

# create range values
start = 0
end = 1
step = 0.02
print(f"\nRange: {start} -> {end} \nStep Distance: {step}")

# create X and y (features and labels)
X = torch.arange(start, end, step).unsqueeze(dim=1)
y = weight * X + bias
print(f"\nFeatures: X={len(X)} \nLabels: y={len(y)}")

# split data
training_split = int(0.8 * len(X))
X_train, y_train = X[:training_split], y[:training_split]
X_test, y_test = X[training_split:], y[training_split:]
print(f"\nX_train: {len(X_train)} \ny_train: {len(y_train)} \nX_test: {len(X_test)} \ny_test: {len(y_test)}")

# Building a PyTorch linear model

class LinearRegressionModelV2(nn.Module):
    def __init__(self):
        super().__init__()
        # use nn.Linear()
        self.linear_layer = nn.Linear(in_features=1,
                                      out_features=1) # within this one layer, an input x is one value, outputs y at one value
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear_layer(x)
    
# set the manual seed and make model istance
torch.manual_seed(42)
model_1 = LinearRegressionModelV2()
model_1.to(device="mps")
print(f"\nmodel_1: {model_1} \nmodel_1 dict: {model_1.state_dict()}")

# Training & Testing

# setup loss function
loss_fn = nn.L1Loss() # same as MAE

# set up optimizer
optimizer = torch.optim.SGD(params=model_1.parameters(),
                            lr=0.01)

# writing training loop
torch.manual_seed(42)
epochs = 116

# put data on target device
X_train = X_train.to(device)
y_train = y_train.to(device)
X_test = X_test.to(device)
y_test = y_test.to(device)

for epoch in range(epochs):
    # set to training mode
    model_1.train()
    
    # do the forward pass
    y_pred = model_1(X_train)
    
    # calculate the loss
    loss = loss_fn(y_pred, y_train)
    
    # zero the optimizer
    optimizer.zero_grad()
    
    # perform backpropagation
    loss.backward()
    
    # optimizer step
    optimizer.step()

    # Testing
    
    model_1.eval()
    with torch.inference_mode():
        test_pred = model_1(X_test)
        test_loss = loss_fn(test_pred, y_test)

    if epoch % 5 == 0:
        print(f"Epoch: {epoch} | Loss: {loss:.6f} | Test loss: {test_loss:.6f}")
    

# plot_predicitons(predictions=test_pred.cpu())


# Exercises for Part 2
print("---------------------------------------------")

# create a straight line dataset using the linear regression formula
start = 0
end = 10
step = 0.1

X = torch.arange(start, end, step).unsqueeze(dim=1)

# set weight and bias to 0.3 and 0.8
weight, bias = 0.3, 0.9
y = weight * X + bias

# split the data into 80% training and 20% testing
training_split = int(0.8 * len(X))
X_train, y_train = X[:training_split], y[:training_split]
X_test, y_test = X[training_split:], y[training_split:]

# plot training data (default args used above)
plot_predicitons(X_train, y_train, X_test, y_test)

# build a PyTorch model by subclassing nn.Module
class ExerciseLinearModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.weights = nn.Parameter(torch.randn(1,
                                    requires_grad=True,     
                                    dtype=torch.float32)) # random nn.Parameter w/ requires_grad = True
        self.bias = nn.Parameter(torch.randn(1,
                                requires_grad=True,
                                dtype=torch.float32)) # one for both
    
    # impliment the forward() method to compute th elinear regression function you used to create the dataset in 1
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.weights * x + self.bias

# instanciate model and check state dict
model_exercise = ExerciseLinearModel()
print(f"Exercise Model State Dict: \n{model_exercise.state_dict()}")

# create a loss function and optimizer
loss_fn = nn.L1Loss()
optimizer = torch.optim.SGD(params=model_exercise.parameters(),
                            lr=0.01)

# write a training loop to perform the appropriate training steps for 300 epochs
epochs = 300

for epoch in range(epochs):
    model_exercise.train()
    
    y_pred = model_exercise(X_train)
    
    loss = loss_fn(y_pred, y_train)
    
    optimizer.zero_grad()
    
    loss.backward()
    
    optimizer.step()
    
    if epoch % 20 == 0:
        model_exercise.eval()
        with torch.inference_mode():
            test_pred = model_exercise(X_test)
            test_loss = loss_fn(test_pred, y_test)
            print(f"Epoch: {epoch} | Loss: {loss:.6f} | Test loss: {test_loss:.6f}")
            
print(model_exercise.state_dict())

model_exercise.eval()
with torch.inference_mode():
    y_preds_new = model_exercise(X_test)
    
plot_predicitons(train_data=X_train, train_labels=y_train,
                 test_data=X_test, test_labels=y_test, predictions=y_preds_new)

# save the trained model's state dict to file
MODEL_NAME = "01_pytorch_workflow_exercise_model.pth"
MODEL_SAVE_PATH = MODEL_PATH / MODEL_NAME

print(f"Saving model to: {MODEL_SAVE_PATH}")
torch.save(obj=model_exercise.state_dict(), f=MODEL_SAVE_PATH)

# create a new instance of the model and load in the saved state dict
loaded_model_exercise = ExerciseLinearModel()

loaded_model_exercise.load_state_dict(torch.load(f=MODEL_SAVE_PATH))

print(loaded_model_exercise.state_dict())
print(model_exercise.state_dict())   # match parameters

# make predictions with the loaded model and confirm they match the original
loaded_model_exercise.eval()
with torch.inference_mode():
    loaded_model_exercise_preds = loaded_model_exercise(X_test)

print(f"Loaded model vs Original model: \n{y_preds_new == loaded_model_exercise_preds}")


