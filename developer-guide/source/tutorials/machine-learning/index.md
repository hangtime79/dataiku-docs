(machine-learning-tutos/index)=

# Machine Learning

This tutorial section contains learning material on programmatically training, managing and deploying machine learning models in Dataiku.

## Local Interpretable Model-agnostic Explanations

* [This tutorial](./models/lime/index.md) explains using LIME (Local Interpretable Model-agnostic Explanations) 
  to provide human-readable explanations for machine learning model predictions.

## Predictive maintenance

* [This tutorial](./models/predictive-maintenance/index) explains how can you predict performance before getting the ground truth.

## Reinforcement learning

* [This tutorial](./others/reinforcement-learning/index) uses reinforcement learning (RL)
  to tune a random forest classifier's hyperparameters automatically.
  The Q-learning algorithm explores and exploits hyperparameter combinations to find the best combination,
  using validation accuracy as the reward.

(machine-learning-tutos/experiment-tracking)=
## Experiment Tracking

* [With XGBoost and custom pre-processing](experiment-tracking/xgboost-pyfunc/index)
* [With Keras/Tensorflow for sentiment analysis](experiment-tracking/keras-nlp/index)
* [With Catboost](experiment-tracking/catboost/index)
* [With LightGBM](experiment-tracking/lightgbm/index)
* [With scikit-learn](experiment-tracking/scikit-learn/index)

(machine-learning-tutos/pretrained-models)=
## Pre-trained Models

* [Tensorflow](code-env-resources/tf-resources/index)
* [PyTorch](code-env-resources/pytorch-resources/index)
* [Hugging Face](code-env-resources/hf-resources/index)
* [SentenceTransformers](code-env-resources/sentence-transformers-resources/index)
* [spaCy](code-env-resources/spacy-resources/index)
* [NLTK](code-env-resources/nltk-resources/index)

(machine-learning-tutos/model-import)=
## Model Import

* [](model-import/scikit-pipeline/index)

(machine-learning-tutos/model-export)=
## Model Export

* [](model-export/python-export-cli/index)
* [](model-export/python-export-edge-deployment-aws-greengrass/index)

## Distributed training

* [](./others/distributed-training/index)

## Vulnerability and Bias Scanning with Protect AI Guardian
This tutorial will guide you through the process of scanning a model for vulnerabilities,
biases, and security concerns using Protect AI Guardian's Python SDK.

```{toctree}
:maxdepth: 1
:hidden:

quickstart-tutorial/index
models/lime/index
models/predictive-maintenance/index
others/reinforcement-learning/index

experiment-tracking/index
code-env-resources/index
model-import/index
model-export/index
others/distributed-training/index
others/protect-ai-guardian/index
```
