# pytorch-fundamentals

Notes taken

What Deep Learning is actually good for?
- Problems with long lists of rules. An example of this could be, say you are playing basketball and you know how to shoot from one spot, how to dribble, etc. That is a rule. For you to now go and learn
how to do the same with the other hand, from the other side of the court, another. For the entire court floor there is millions of places where you can dribble shoot, can't dribble or shoot, and these all
make up rules which to us, are subconcious. To automate something like this, you would need Deep Learning.

- Continually changing environments. Continuing with the basketball analogy, say you are now moved to a different court, or even a different sport, you would, with your knew gained athleticism, be able to
comprehend some of whats going on. Deep Learning allows the models to adapt or learn in new scenarios, based on past experience, just like us.

- Discovering insights within large collections of data. Again, basketball. Say you want to make an app that shows what a good shot is versus a bad one. You would need a set of rules. These rules would
need to span not only what a good shot looks like from every spot on the court, but also a bad shot. Deep Learning is a feasable solution to this.

What Deep Learning is not great for?
- When you need explainability. Since the patterns learned by a deep learning model are typically converted to data, floats and integers, they become uninterpretable by humans.

- When the traditional approach is a better option or can accomplish what you need with a simple rule-based system.

- When errors are unacceptable. Since its output is not always predictable and may hallucinate, you need margin for mistake.

- Data pool isn't large enough. Deep Learning models usually require large amounts of data to produce great result, so the more it can be trained on and see possibilities, the more it can get better 
results on unseen data.

Machine Learning:
- Structured data
- XGBoost algorithm
- Random forest
- Gradiant boosted models
- Naive Bayes
- Nearest neighbor
- Support vector machine
- ...

Deep Learning:
- Typically better with unstructured
- Image & audio data
- Brings order to mess
- Neural networks
- Fully connected neural network
- Convolutional neural network
- Recurrent neural network
- Transformer
- ...


Neural Networks. Input data, unstructured, like images, audio, unformatted text. This data needs to be turned numerical and is collected in matrices or tensors. Then, the tensor/matrix is passed through a Neural Networks (many layers, nodes, types of networks) all following a system of input, manipulated and learns features, represents it how it best understands, and is converted back into human understood output.

