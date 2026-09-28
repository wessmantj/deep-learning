
Why do we turn our datasets into batches and/or mini-batches?

1. Its more computationally efficient. Your computing hardware may not be able to look (store in memory) at 60000 images in one hit. So we break it down to 32 images at a time (batch size of 32, just common beginner size). 
2. It gives the neural network more chances to update its gradients per epoch. If we looked at all images per epoch we would only get an update after the interation completes, while with batches the nn updates it every batch (32 in this instance).

