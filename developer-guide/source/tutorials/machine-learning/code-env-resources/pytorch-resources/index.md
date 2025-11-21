# Load and re-use a PyTorch model

## Prerequisites

* [Dataiku >= 10.0.0.](https://doc.dataiku.com/dss/latest/release_notes/10.0.html#code-env-resources)
* Python >= 3.9
* A [Code Environment](https://doc.dataiku.com/dss/latest/code-envs/index.html) with the following packages:
  * `torch==2.0.1`
  * `torchvision==0.15.2`

## Introduction

Machine learning use cases can involve a lot of input data and compute-heavy thus expensive model training.
You might not want
to retrain a model from scratch for common tasks like processing images/ text or during your initial experiments.
Instead, you can load *pre-trained models* retrieved from remote repositories and use them for generating predictions. 

In this tutorial,
you will use Dataiku's [Code Environment resources](https://doc.dataiku.com/dss/latest/code-envs/operations-python.html#managed-code-environment-resources-directory) feature
to download and save a pre-trained image classification model from [PyTorch Hub](https://pytorch.org/hub/).
You will then re-use that model to predict the class of a downloaded image. 

## Loading the pre-trained model

 The first step is to download the required assets for your pre-trained model.
 To do so, in the *Resources* screen of your Code Environment,
 input the following **initialization script** then click on *Update*: 

 ``` {literalinclude} init_script.py
 ```

This script will retrieve a ResNet18 model from [PyTorch Hub](https://pytorch.org/hub/pytorch_vision_resnet/)
and store it on the Dataiku Instance. 

Note that it will only need to run once,
after that all users allowed to use the Code Environment will be able
to leverage the pre-trained model with re-downloading it again. 

## Using the pre-trained model for inference

You can now re-use this pre-trained model in your Dataiku Project's Python Recipe or notebook. Here is an example adapted from a tutorial on the PyTorch website that downloads a sample image and predicts its class from the ImageNet labels.

```{literalinclude} use_pretrained.py
```
Running this code should give you an output similar to this:

```text
Samoyed 0.8846230506896973
Arctic fox 0.0458049401640892
white wolf 0.044276054948568344
Pomeranian 0.00562133826315403
Great Pyrenees 0.004651993978768587
```

## Wrapping up

Your pre-trained model is now operational! From there you can easily reuse it, e.g. to directly classify other images stored in a Managed Folder or to fine-tune it for a more specific task.
