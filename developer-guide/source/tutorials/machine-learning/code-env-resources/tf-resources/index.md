# Load and re-use a TensorFlow Hub model

## Prerequisites

* [Dataiku >= 10.0.0.](https://doc.dataiku.com/dss/latest/release_notes/10.0.html#code-env-resources)
* A [Code Environment](https://doc.dataiku.com/dss/latest/code-envs/index.html) with the following packages:
  * `tensorflow==2.8.0`
  * `tensorflow-estimator==2.6.0`
  * `tensorflow-hub==0.12.0`
  * `protobuf>=3.20,<3.21`
  * `requests==2.28.1`
  * `Pillow==9.3.0`


## Introduction

Machine learning use cases can involve a lot of input data and compute-heavy thus expensive model training. Instead, you might want to reuse artifacts for common tasks like pre-processing images or text for model training. You can load *pre-trained models* from remote repositories and embed them in your code.

In this tutorial, you will use Dataiku's [Code Environment resources](https://doc.dataiku.com/dss/latest/code-envs/operations-python.html#managed-code-environment-resources-directory) feature to download and save a pre-trained image classification model from the [TensorFlow Hub](https://www.tensorflow.org/hub). You will then reuse it to classify a picture downloaded from the Internet.

## Loading the pre-trained model

The first step is to download the required assets for your pre-trained model. To do so, in the *Resources* screen of your Code Environment, input the following **initialization script** then click on *Update*:

```{literalinclude} init_script.py
```

This script will retrieve a MobileNet v2 model from [Tensorflow Hub](https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4) and store it on the Dataiku Instance.

Note that it will only need to run once, after that all users allowed to use the Code Environment will be able to leverage the pre-trained model with re-downloading it again.

## Using the pre-trained model for inference

You can now re-use this pre-trained model in your Dataiku Project's Python Recipe or notebook. Here is an example adapted from a [tutorial on the Tensorflow website](https://www.tensorflow.org/tutorials/images/transfer_learning_with_hub) that downloads a sample image and predicts its class from the ImageNet labels.

```{literalinclude} use_pretrained.py
```
Running this code should give you the following output:

```text
Predicted class name: tiger
```

## Wrapping up

Your pre-trained model is now operational! From there you can easily reuse it, e.g. to directly classify other images stored in a Managed Folder or to fine-tune it for a more specific task.
