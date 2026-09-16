# PyTorch Workflow - Notes

Companion code: [`01_pytorch_workflow.py`](./01_pytorch_workflow.py)

## Table of contents
- [What does the model do?](#what-does-the-model-do)
- [Main classes used in PyTorch model building](#main-classes-used-in-pytorch-model-building)
- [Loss function and optimizer](#loss-function-and-optimizer)
- [The training loop](#the-training-loop)
- [The testing loop](#the-testing-loop)
- [Saving and loading models](#saving-and-loading-models)

---

## What does the model do?
- Start with random values (weight & bias)
- Look at the training data and adjust the random values to better represent (get closer to global min) the ideal values (the weight & bias used to create data)

It does this by two algorithms: gradient descent and backpropagation.

The whole idea of training is for a model to move from some *unknown* parameters (in this case random) to some *known* parameters. This could also be called moving from a poor representation of the data to a better one.

## Main classes used in PyTorch model building

- **torch.nn** - contains all of the building blocks for computational graphs (another word for a neural network; it can be considered a computational graph)
- **torch.nn.Parameter** - what parameters should our model learn; often a PyTorch layer from `torch.nn` will set these
- **torch.nn.Module** - the base class for all neural network modules. If subclassed, you overwrite `forward`
- **torch.optim** - this is where PyTorch optimizers live; they help with gradient descent
- **def forward()** - all `nn.Module` subclasses require the dev to overwrite `forward()`; this method defines what happens in the forward computation

## Loss function and optimizer

Use a loss function (also called a cost function or criterion, depending on the area) to measure how wrong the model's predictions are compared to the ideal outputs. A lower difference is better.

- **Loss function**: measures the difference between model output and ideal outputs
- **Optimizer**: takes into account the loss of a model and adjusts the model's parameters (e.g. weight & bias) to improve the loss

## The training loop

0. Loop through the data
1. Forward pass (data moving through the model's `forward()` method), also called forward propagation
2. Calculate the loss by comparing the forward pass predictions with the ground truth labels
3. Optimizer zero grad
4. Loss backward — move backwards through the network to calculate the gradients of each parameter in the model with respect to the loss (**backpropagation**)
5. Optimizer step — use the optimizer to adjust the model's parameters to improve the loss (**gradient descent**)

## The testing loop

1. Set the model to evaluation mode with `model.eval()` (sets `requires_grad = False`)
2. Wrap the forward pass in `torch.inference_mode()` to turn off gradient tracking
3. Forward pass on the test data
4. Calculate the test loss by comparing predictions with the test labels
5. Track/print the loss so you can watch the training and test loss curves over the epochs

## Saving and loading models

Three methods for saving and loading models in PyTorch:

1. `torch.save()` - allows you to save a PyTorch object in Python's pickle format
2. `torch.load()` - allows you to load a saved PyTorch object
3. `torch.nn.Module.load_state_dict()` - this lets you load a model's saved state dictionary
