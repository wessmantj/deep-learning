What the model does:
 * Start with random values (weight & bias)
 * Look at the training data and adjust the random values to better represent (get closer to global min) the ideal values (the weight & bias used to create data)

It does this by two algos. Gradient descent and backpropigation. 

Some of the main classes being used in PyTorch model building:

 * torch.nn - contains all of the building blocks for computational graphs (another word for neural network can be considered a computational graph)
 * torch.nn.Parameter -  what paramenters should our model learn, often a PyTorch layer from torch.nn will set these 
 * torch.nn.Module - the base class for all neural network modules. If subclassed, you overwrite forward
 * torch.optim - this is where PyTorch optimizers live, they help with gradient descent 
 * def forward() - all nn.Modules subclasses require dev to overwrite forward(), this methods defines what happens in the forward computation

The whole idea of training is for a model to move from some *unknown* parameters (in this case random) to some *known* parameters. Also could be called moving from poor representation of the data to better.

Use loss-function or cost-function or criterion, depending on area, measure how wrong the model's predictions are to the ideal outputs, lower difference is better.

In PyTorch, and generally Machine Learning, is...
- Loss-function: measures difference between model output and ideal outputs
- Optimizer: takes into account the loss of a model and adjusts the model's parameters (e.g. weight & bias) to improve the loss
- A training loop:
- A testing loop:

