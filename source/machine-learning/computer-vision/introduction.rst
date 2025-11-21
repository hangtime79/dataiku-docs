Introduction
#############

Computer vision in DSS is "fully-visual": You don't need to write code, you can configure training using the
interface. It includes for both Object detection and Image classification :

  * Preparing the requisite environment
  * Visually configuring the training task (including interactive data augmentation)
  * Handling the training process (with or without GPU) with early stopping capabilities
  * Interactive results & performance visualisation
  * Ability to deploy and score images in batch or realtime

Checkout this `Sample project <https://www.dataiku.com/learn/samples/object-detection/>`_  to get an overview of the object detection native capabilities or
start creating your own using the next sections.

DSS Computer vision is based on PyTorch. Through container deployment capabilities, you can train and deploy models
on cloud-enabled dynamic GPUs clusters.

.. note::
    To create a model from scratch with a custom architecture and full parametrization, you can write your model in Keras using our :doc:`../deep-learning/index` feature instead.
