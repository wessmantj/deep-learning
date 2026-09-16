What is a classification problem?
- Is an email spam or not spam makes an example of binary classification, either yes or no.
- Is a photo sushi, steak, or pizza is an example of multiclass classification, more than one thing or another but will assign one to the photo given.
- What tags should this article have is an example of multilabel classification since multiple options per sample.

Architecture of a Classification Model (Binary first, then Multiclass).

- Input layer shape (in_features): Same as number of features (e.g. 5 for age, sex, weight, smoking status in heart disease pred), same for multiclass.
- Hiden layer(s): Problem specific, minimum is 1, and max is unlimited. Same for multiclass.
- Neurons per hidden layer: Problem specific, generally 10 to 512. Same for multiclass.
- Output layer shape (out_features): 1 (one class or the other), while for multiclass there is 1 per class (e.g. 3 for food, person, or dog photo identification).
- Hidden layer activiation: usually ReLU (rectified linear unit) but can be many others, same for multiclass classification.
- Output activation: Sigmoid for binary and Softmax for multiclass.
- Loss function: Binary crossentropy for binary and cross entropy for multiclass.
- Optimizer: SGD (stocastic gradient descent), Adam for binary and multiclass, but many others.

