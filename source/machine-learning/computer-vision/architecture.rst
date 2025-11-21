Model architectures & training parameters
##########################################

You can train a computer vision model without any code; tailor the training regime to your needs in the "Design >> training" tab of the analysis, or accept the default configuration.

Pre-trained models available
=============================

* Object detection uses a `Faster R-CNN model <https://arxiv.org/abs/1506.01497>`_ with a ResNet-50-FPN backbone. See `PyTorch tutorial <https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html>`_ for more details on how Faster R-CNN model is implemented in PyTorch.
* For Image classification you can choose between several `EfficientNet models (B0, B4 and B7) <https://arxiv.org/abs/1905.11946>`_. B0 is the smallest model (fewest parameters, size on disk), while B7 is the largest. Smaller models will yield faster training times, whilst larger models may result in better performance. B4 is a good balance between the two other models, it is selected by default.

Training parameters
===================

The **number of retrained layers**: this indicates how many backbone layers will be finetuned on your images while the
other layers are frozen. Increasing the number of finetuned layers can lead to overfitting if the training dataset is insufficiently large.

An **optimizer** is used during training to update the weights of the network based on the loss. You can choose
one of the following optimizers: ADAM, SGD, RMSprop, Adamax, Adagrad and Adadelta. A **learning rate schedule** is used to adapt the learning rate at the end of each epoch. Available methods are: On
plateau, step and exponential methods. See `Pytorch documentation <https://pytorch.org/docs/stable/optim.html>`_ for
more details on the optimizers and learning rate schedules.
Note that in addition to the learning rate schedules applied at the end of each epochs, we use a **warmup learning rate
schedule** during the first epoch to start with a smaller learning rate and increase its value quickly to match the
initial learning rate value specified by the end of the first epoch.

You may specify the upper limit for training with the **number of epochs** parameter, and optionally an **early
stopping** configuration to conclude training early if the performance metric on the test set does not improve by at
least the **early stopping delta**, within the number of epochs set as **early stopping patience**.

The **batch size** defines the number of images used in each training step. It is defined per device meaning that if you train on 2 GPUs, each will
receive batch size images per training-step. Increasing the batch size will accelerate
training, however it will be limited by the available GPU/CPU memory of your infrastructure.
