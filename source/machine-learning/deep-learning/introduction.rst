Introduction
#############

You can build powerful deep learning models within the DSS visual machine learning component.

.. note::
    Step-by-step instructions for `defining Deep Learning architectures with Keras and Tensorflow in Dataiku DSS
    <https://knowledge.dataiku.com/latest/ml-analytics/deep-learning/code-within-visual-ml/tutorial-index.html>`_ are available in this How-To.


Deep learning in DSS is "semi-visual":

* You write the code that defines the architecture of your deep learning model
* DSS handles all the rest:

  * Preprocessing your data (Handling missing values, categorical data, rescaling, ...)
  * Feeding the model
  * Handling the training process, including epochs, generators, early stopping
  * Showing per-epoch training charts and giving early stopping capabilities
  * Integrating with Tensorboard
  * Building all results metrics and charts
  * Giving ability to score
  * Deploying deep learning models to API nodes for production deployments

DSS Deep Learning is based on the Keras + TensorFlow couple. You will mostly write Keras code to define your deep learning models.

DSS Deep Learning supports training on CPU and GPU, including multiple GPUs. Through container deployment capabilities, you can train and deploy models on cloud-enabled dynamic GPUs clusters.

.. note::
    To create a model using a "fully-visual" task, check out :doc:`../computer-vision/index` feature instead.