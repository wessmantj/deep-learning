import torch
from torch import nn # contains all of PyTorch's neural network building tools (Layers, Containers, Quantization, etc.)
import matplotlib.pyplot as plt
import numpy as np

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
plt.show()
