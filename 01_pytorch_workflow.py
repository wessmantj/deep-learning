import torch
from torch import nn # contains all of PyTorch's neural network building tools (Layers, Containers, Quantization, etc.)
import matplotlib.pyplot as plt

workflow_outline = {1: "data (prep and load)",
                    2: "build model",
                    3: "fitting model to data",
                    4: "making predictions and evaluating a model (inference)",
                    5: "saving and loading a model", 
                    6: "combining it all together"}

# 1. Data (prep and load)

# create known parameters
weight = 0.7
bias = 0.3

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

plot_predicitons()

