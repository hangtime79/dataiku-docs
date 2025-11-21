# Load and re-use a spaCy named-entity recognition model

## Prerequisites

* [Dataiku >= 10.0.0](https://doc.dataiku.com/dss/latest/release_notes/10.0.html#code-env-resources)
* A Python>=3.9 [Code Environment](https://doc.dataiku.com/dss/latest/code-envs/index.html) with the following package:
  * `spacy==3.4.4`

## Introduction

[Named-entity recognition](https://en.wikipedia.org/wiki/Named-entity_recognition) (NER) is concerned with locating and classifying named entities mentioned in unstructured text into pre-defined categories such as person names, organizations, locations etc. The training of a NER model might be costly. Fortunately, you could rely on pre-trained models to perform that recognition task.

In this tutorial, you will use Dataiku's [Code Environment resources](https://doc.dataiku.com/dss/latest/code-envs/operations-python.html#managed-code-environment-resources-directory) to create a code environment with a [spaCy](https://spacy.io/) pre-trained NER model. 


## Loading the pre-trained NER model

 After creating your Python code environment with the required spaCy package (see beginning of tutorial), you will download the required assets for your pre-trained model. To do so, in the *Resources* screen of your Code Environment, input the following **initialization script** then click on *Update*:

 ``` {literalinclude} init_script.py
 ```

This script will download the spaCy English pipeline [en_core_web_sm](https://spacy.io/models/en) and store it on the Dataiku Instance. This pipeline contains the pre-trained NER model, among other NLP tools.

Note that the script will only need to run once. After that all users allowed to use the Code Environment will be able to leverage the NER model without having to re-download it.

## Performing NER using your pre-trained model

You can now use your pre-trained model in your Dataiku Project's Python Recipe or notebook to perform NER on some text. Here is an example:

```{literalinclude} use_pretrained.py
```
Running this code should give you an output similar to this:

```text
American --> NORP
Britain --> GPE
the Virginia Declaration of Rights --> ORG
George Mason --> PERSON
May 1776 --> DATE
```
