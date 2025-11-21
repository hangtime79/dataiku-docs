# Load and re-use a SentenceTransformers word embedding model

## Prerequisites
* [Dataiku version >= 10.0.0.](https://doc.dataiku.com/dss/latest/release_notes/10.0.html#code-env-resources)
* A Python>=3.9 [Code Environment](https://doc.dataiku.com/dss/latest/code-envs/index.html) with the following package:

  * `sentence-transformers==2.2.2`

## Introduction

 Natural Language Processing (NLP) use cases typically involve converting text to word embeddings. Training your word embeddings on large corpora of texts is costly. As a result, downloading *pre-trained word embeddings models* and re-training them as needed is a popular option. [SentenceTransformers](https://www.sbert.net/) is a Python framework for state-of-the-art sentence, text and image embeddings. The framework is based on [Pytorch](https://pytorch.org/) and [Transformers](https://huggingface.co/docs/transformers/index) and offers a large collection of pre-trained models. In this tutorial, you will use Dataiku's [Code Environment resources](https://doc.dataiku.com/dss/latest/code-envs/operations-python.html#managed-code-environment-resources-directory) feature to download and save pre-trained word embedding models from SentenceTransformers. You will then use one of those models to map a few sentences to embeddings.

## Downloading the pre-trained word embedding model

 The first step is to download the required assets for your pre-trained models. To do so, in the *Resources* screen of your Code Environment, input the following **initialization script** then click on *Update*:

 ``` {literalinclude} init_script.py
 ```

This script retrieves a pre-trained model from [SentenceTransformers](https://www.sbert.net/) and stores them in the Dataiku Instance. To download more of them, you'll need to add them to the list and includes their `revision`, which is the model repository's way of [versioning these models](https://huggingface.co/docs/transformers/model_sharing#repository-features).

Note that the script will only need to run once. After that, all users allowed to use the Code Environment will be able to leverage the pre-trained models without having to re-download them.

## Converting sentences to embeddings using your pre-trained model 

You can now use those pre-trained models in your Dataiku Project's Python Recipe or notebook. Here is an example using the word `average_word_embeddings_glove.6B.300d` model to map each sentence in a list to a 300-dimensional dense vector space.

```{literalinclude} use_pretrained.py
```
Running this code should output a numpy array of shape (2,300) containing numerical values. 

