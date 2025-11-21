Troubleshooting
################

Here is a list of known issues and limitations of the Visual Deep Learning.

.. contents::
    :local:

Using pre-trained models from Keras
====================================

Keras provides `"applications" <https://www.tensorflow.org/api_docs/python/tf/keras/applications/>`_, which are state-of-the-art architectures trained on millions of data points that can be reused, for example, to do transfer learning.

For example, you can use `ResNet 50 <https://www.tensorflow.org/api_docs/python/tf/keras/applications/resnet50/ResNet50/>`_ as follows:

.. code-block:: python

    from tensorflow.keras.applications import ResNet50
    model = ResNet50(weights="imagenet")


where `weights` can be `"imagenet"` (or `None`), and it means that they are weights on the architecture trained on `Imagenet <https://fr.wikipedia.org/wiki/ImageNet>`_. It is the most interesting use case because these applications are big networks that require a lot of training data. In that case, it needs to download the weights of the model, which is only possible if you have access to the internet.

If you don't have access to the internet, the code throws `Exception: URL fetch failure`.

To work around this issue, you need to have the file containing the weights of your model available locally on the server.

Each application has the possibility to load the model with a top (i.e. last fully connected layers for the classification and the corresponding weights) or without these last layers. It corresponds to the `include_top` parameter for each application. It means that for each application, there are two possible sets of weights: one for architecture with top and one without.

All weights files are available `here <https://github.com/fchollet/deep-learning-models/releases>`_

Once you have downloaded the appropriate files, you have two options:

* manually put them at `~/.keras/models/`. In that case, be sure to respect Keras naming for files.
* put them inside a managed folder and then load them in the model with code like:

    .. code-block:: python

       import dataiku
       import os
       from tensorflow.keras.applications import ResNet50

       model = ResNet50(weights=None)

       weights_mf_path = dataiku.Folder("folder_containing_weights").get_path()
       weights_path = os.path.join(weights_mf_path, "resnet_weights.h5")

       model.load_weights(weights_path)


Code environment lineage
=========================

The code environment used to train a model is attached to every action performed with that model afterwards.

If the model is trained in a GPU-aware code environment, all the following operations will have access to GPU(s):

* the Retrain recipe - which will reuse training options
* the Scoring/Evaluation recipes - you can choose in the recipe settings whether to use a GPU to run the recipe
* on the API node, the DSS server needs to have access to a GPU, otherwise the code environment will fail to install. Then, for scoring, the model will be loaded on GPU (not possible to run it on CPU).

If you're using TensorFlow 1.X and training a model in a code environment without GPU (not using the `tensorflow-gpu` package), it will not be possible to use a GPU for those operations.

Code environments using TensorFlow 2.0 or later are always GPU-aware and can run on CPU or GPU.

TensorFlow session
===================

TensorFlow provides `sessions <https://www.tensorflow.org/api_docs/python/tf/compat/v1/Session>`_ to manage the environment on which the operations are performed. In particular, when we use GPU(s), we can define in these Sessions how we want to handle the computation and split into our different devices (CPU, GPU #0, GPU #1, ...).

In the context of Visual Deep Learning, it is DSS that handles the session, so you should not use it inside its architecture. Otherwise, it could result in unwanted behaviors.

You can "modify" the session in the UI, when selecting the GPU(s). If you modify the "Memory allocation rate per GPU", it will impact the `config.gpu_options.per_process_gpu_memory_fraction` of the session.

We also set the `allow_soft_placement` parameter to `True`. As per TensorFlow `documentation <https://www.tensorflow.org/guide/gpu>`_:

    If you would like TensorFlow to automatically choose an existing and supported device to run the operations in case the specified one doesn't exist, you can call `tf.config.set_soft_device_placement(True)`.

In DSS this is useful when training on multiple GPUs.

ML API
=======

DSS provides an :doc:`devguide:api-reference/python/ml` API to interact with models created in the visual machine learning part of the software. However, it is currently not available for  Deep Learning.

Number of outputs in the model
===============================

Keras allows you to build multi output architectures. For example, to perform object detection inside images or videos, you want to be able to predict the type of object and its position in the image.

Currently, the Deep Learning is only available in the *Prediction* part of the Visual Machine Learning, which can treat various problems: Regression, Binary Classification and Multiclass Classification. All those types of problems require one output. Therefore it is currently not possible to have several outputs in an architecture.

Enforced code environment for Project
==========================================

DSS allows you to select a preferred code environment for a Project, and even allows you to enforce this code environment to be used in every code recipe/Visual ML. However, it currently conflicts with the process of pre-selecting a code environment when creating a new Deep Learning analysis, that will always override this behaviour by selecting a code environment with the appropriate packages.

If you want to enforce the usage of a code environment in your project, you would need to install the appropriate packages on it for being able to run deep-learning (see :doc:`runtime-gpu`). Then, when creating a new analysis, you should go to the *Python Environment* tab, and select *Inherit project default* (and ignore the warning that is displayed).
