# Load and re-use a Hugging Face model

 Machine learning use cases can involve a lot of input data and compute-heavy thus expensive model training. It is common to download *pre-trained models* from remote repositories and use them instead. Hugging Face hosts a well-known [one](https://huggingface.co/models) with models ranging from text generation to image embedding passing by reasonning. In this tutorial you will see how you can leverage Dataiku functionnality to download and save a pre-trained text classification model. You will then re-use that model to predict a masked string in a sentence.

## Loading a model leveraging the model cache (recommended)

In this section, you will use Dataiku's {ref}`Model Cache<refdoc:hugging-face-model-cache>` to download, save, and retrieve your Hugging model.


### Downloading the pre-trained model

 The first step is to download the required assets for your pre-trained model. Run this snippet of code anywhere in DSS (for example in a Python recipe, in a Notebook, or even in an initialization script of a code environment):

 ``` {literalinclude} init_script_model_cache.py
 ```

This script retrieves a DistilBERT model from [Hugging Face](https://huggingface.co/distilbert-base-uncased) and stores it in the Dataiku Instance model cache.

Note that the model must have been enabled by your Dataiku admin in an {doc}`HuggingFace connection<refdoc:generative-ai/huggingface-models>`. For gated models, you must pass a connection name to use the HuggingFace authentication token.

### Using the pre-trained model for inference

#### Prerequisites

* Dataiku >= 14.2.0
* Python >= 3.9
* A {doc}`Code Environment<refdoc:code-envs/index>` with the following packages:
  ```python
  transformers  # tested with 4.51.3
  torch         # tested with 2.7.0
  ```

You can now re-use this pre-trained model in your Dataiku Project's Python Recipe or notebook. Here is an example adapted from a sample in the [model repository](https://huggingface.co/distilbert-base-uncased/tree/main) that fills the masked parts of a sentence with the appropriate word:


```{literalinclude} use_pretrained_model_cache.py
```

Running this code should give you an output similar to this:

```text
lend me your ears and i ' ll sing you a lullaby (0.29884061217308044)
lend me your ears and i ' ll sing you a tune (0.10296323150396347)
lend me your ears and i ' ll sing you a song (0.10061406344175339)
lend me your ears and i ' ll sing you a hymn (0.09704922884702682)
lend me your ears and i ' ll sing you a cappella (0.034581173211336136)
```

## Loading a model using code environment ressources


  In this section, you will use Dataiku's {ref}`Code Environment Resources<code-env-resources-directory>` feature to download and save a pre-trained text classification model from Hugging Face.
  Be careful when using large model in code environment ressources since the full models will be packed up with your environment which can easily represents dozens of GB.

### Prerequisites

* {ref}`Dataiku >= 10.0.0<code-env-resources-v-10.0>`
* Python >= 3.9
* A {doc}`Code Environment<refdoc:code-envs/index>` with the following packages:
  ```python
  transformers  # tested with 4.54.1
  torch         # tested with 2.7.1
  ```

### Downloading the pre-trained model

 The first step is to download the required assets for your pre-trained model. To do so, in the *Resources* screen of your Code Environment, input the following **initialization script** then click on *Update*:

 ``` {literalinclude} init_script_code_env.py
 ```

This script retrieves a DistilBERT model from [Hugging Face](https://huggingface.co/distilbert-base-uncased) and stores it in the Dataiku Instance.

Note that it will only need to run once, after that all users allowed to use the Code Environment will be able to leverage the pre-trained model without re-downloading it again.

### Using the pre-trained model for inference

You can now re-use this pre-trained model in your Dataiku Project's Python Recipe or notebook. Here is an example adapted from a sample in the [model repository](https://huggingface.co/distilbert-base-uncased/tree/main) that fills the masked parts of a sentence with the appropriate word:

```{literalinclude} use_pretrained_code_env.py
```

Running this code should give you an output similar to this:

```text
lend me your ears and i'll sing you a lullaby (0.29883989691734314)
lend me your ears and i'll sing you a tune (0.10296259075403214)
lend me your ears and i'll sing you a song (0.10061296075582504)
lend me your ears and i'll sing you a hymn (0.09704853594303131)
lend me your ears and i'll sing you a cappella (0.034581124782562256)
```


## Wrapping up

Your pre-trained model is now operational! From there you can easily reuse it, e.g. to process multiple text records stored in a Managed Folder or within a text column of a Dataset.
