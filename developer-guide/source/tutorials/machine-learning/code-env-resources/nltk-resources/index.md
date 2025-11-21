# Load and re-use an NLTK tokenizer 

```{caution}
Usage of the NLTK package is now deprecated in favor of other packages.  
A good replacement could be the transformers package as used in {doc}`/tutorials/machine-learning/code-env-resources/hf-resources/index`.
```

## Prerequisites

* [Dataiku >= 10.0.0](https://doc.dataiku.com/dss/latest/release_notes/10.0.html#code-env-resources)
* A Python>=3.7 [code environment](https://doc.dataiku.com/dss/latest/code-envs/index.html) with the following package:
  * `nltk == 3.8.1`


## Introduction
[Natural Language Toolkit (NLTK)](https://www.nltk.org/index.html) is a Python package to execute a variety of operations on text data. It relies on several pre-trained artifacts like word embeddings or tokenizers that are not available out-of-the-box when you install the package: by default you have to manually download them in your code.

In this tutorial, you will use Dataiku's [code environment resources](https://doc.dataiku.com/dss/latest/code-envs/operations-python.html#managed-code-environment-resources-directory) to create a code environment and add the [punkt](https://www.nltk.org/api/nltk.tokenize.punkt.html) sentence tokenizer to it.

## Loading the tokenizer

 After creating your Python code environment with the required NLTK package (see the beginning of the tutorial), in the *Resources* screen of your Code Environment, input the following **initialization script** then click on *Update*:

 ``` {literalinclude} init_script.py
 ```

This script will download the `punkt` tokenizer and store it on the Dataiku instance. 
Note that the script will only need to run once. Once run successfully, all users allowed to use the code environment will be able to leverage the tokenizer without having to re-download it.

## Using the tokenizer in your code

You can now use your tokenizer in your Dataiku project's Python recipe or notebook. Here is an example:

```{literalinclude} use_pretrained.py
```
Running this code should give you an output similar to this:

```text
Dataiku integrates with your existing infrastructure — on-premises or in the cloud.
-----
It takes advantage of  each technology’s native storage and computational layers.
-----
Additionally, Dataiku provides  a fully hosted SaaS option built for the modern cloud data stack.
-----
With fully  managed elastic AI powered by Spark and Kubernetes, you can achieve maximum performance  and efficiency on large workloads.
```

Using the same process, you can easily fetch and reuse any other kind of artifact required by NLTK for your text-processing tasks.
