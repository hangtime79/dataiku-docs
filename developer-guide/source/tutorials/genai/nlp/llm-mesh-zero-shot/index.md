# Using LLM Mesh to benchmark zero-shot classification models


## Prerequisites

* Dataiku >= 12.4
* Access to at least 2 LLM connections (see the 
{doc}`reference documentation <refdoc:generative-ai/llm-connections>`
for configuration details). This tutorial uses OpenAI's GPT-3.5-turbo and
GPT-4, but you can easily swap them with other providers/models.
* Access to an existing project with the following permissions:
    * "Read project content"
    * "Write project content"

## LLM mesh API basics: prompting a model


With Dataiku's LLM mesh capabilities, you can
leverage the power of various LLM types using a unified programmatic interface
provided by the public API. More specifically, the Python API client allows you
to easily manipulate query and response objects you send to/get from your LLM.

Authentication is fully handled by the LLM connection settings under the hood
so that you can focus solely on the essentials parts of your code.

As a first example, let's see how to query a GPT-3.5-Turbo model. Run the
following code from a notebook:

```{literalinclude} assets/basic_query.py
:language: python
:caption: basic_query.py
```

Here is what happens under the hood with this code snippet:

1. A `DSSLLM` object is instantiated using the LLM connection mapped associated
with the specified LLM id. If you don't have your LLM ID at hand, you can use the 
{meth}`~dataikuapi.dss.project.DSSProject.list_llms()` method to list all available LLMs within
the project.
2. From this `DSSLLM` object, a `DSSLLMCompletionQuery` object is created to serve
as the building ground for the user prompt. This prompt is built by adding one
(or more) messages with the `with_message()` method.
3. Once the prompt is built, the query is executed. It returns a `DSSLLMCompletionResponse` object
that you can use to check if the model inference was run successfully and retrieve
the model's output.

Note also that your code doesn't call any external dependency: for this simple
use-case, everything you need is the Python API client.

Now for the interesting part: if you want to swap the GPT-3.5-turbo model with
another LLM, *you only need to change the LLM id. The rest of the code remains
exactly the same*. This is one of the main strengths of the LLM mesh: 
allowing developers to write provider-agnostic code when prompting models.


## Classifying movie reviews
Let's look at a more elaborate use-case: movie review classification. To perform
this task, you will need to build a more elaborate prompt that will:

* align with the task at hand,
* generate standardized outputs.

To do so, you can rely on *system messages* whose role is to define the model's behavior.
In practice, you describe this behavior in the `with_message()`
method by passing the `role='system'` parameter. Here is an example:

```{literalinclude} assets/basic_review.py
:language: python
:caption: basic_review.py
```

To make it more composable, you can wrap this code into a function and place it
in your project Libraries. Go to your project library and, under `python/`, create
a new directory called `review_code`. Inside that directory, create two files:

* `__init__.py` that should be left empty,
* `models.py` that will contain our helper functions.

Add the following code to `models.py`:

```{literalinclude} assets/models.py
:language: python
:caption: models.py
```

Your next task is to gather the input dataset containing the movie reviews.
The dataset you will work on is an extract from the
[Large Movie Review Dataset](https://ai.stanford.edu/~amaas/data/sentiment/).
Download the file [here](https://cdn.downloads.dataiku.com/public/website-additional-assets/data/IMDB_train.csv.gz) and use it to create a dataset in your project called `reviews`. In this dataset,
there are two columns of interest:

- `text` contains the reviews to be analyzed,
- `polarity` reflects the review sentiment: 0 for negative, 1 for positive.

Next, from the `reviews` dataset, create a Python recipe with a single output dataset called `reviews_scored`
with the following code:

```{literalinclude} assets/recipe_zshot.py
:language: python
:caption: recipe_zshot.py
```

After running this recipe, your `reviews_scored` dataset should be populated
with the predicted sentiments. The final step is to compute the performance of
your zero-shot classifier since you have the ground truth at your disposal.

To compute the *accuracy* of your model, run the following code:

```{literalinclude} assets/acc_single_model.py
:language: python
:caption: acc_single_model.py
```

You should get a decent accuracy value, but what if you wanted to see how good
the model is *compared to another one*?

## Benchmarking multiple LLMs

In this section, you will see how to easily run the same operation as before over
two different models. In practice, you will compare the performance of
GPT-3.5-turbo with GPT-4.

Create a new Python recipe with:
* `reviews` as input dataset,
* `reviews_2_models_scored` as a new output dataset.

Add the following code:

```{literalinclude} assets/recipe_2_models_zshot.py
:language: python
:caption: recipe_2_models_zshot.py
```

Note that the code barely changes even if you introduce a new model. You just had
to create a new handle and call the scoring function a second time, but nothing
more! 

To compare how both models are doing in terms of performance, you can run the
following code:

```{literalinclude} assets/acc_2_models.py
:language: python
:caption: acc_2_models.py
```

You will get relatively similar performances for a small value of `N_MAX_OUTPUT_ROWS`.
But as you increase the number of scored records, you should see 
GPT-4 performing a bit better. Do not hesitate to try different models among
the ones at your disposal, as you can now see it only mandates very few changes
in the code!

## Wrapping up

Congratulations on finishing this tutorial! You now have a good overview of the
LLM mesh completion query capabilities in Dataiku! If you want to go further,
you can try:
- tweaking the prompt,
- running comparisons with more than two models,
- leveraging Dataiku's experiment tracking abilities to better log parameters,
prompt variations, and resulting performances.

Here are the complete versions of the code presented in this tutorial:

:::{dropdown} [basic_query.py](./assets/basic_query.py)

```{literalinclude} assets/basic_query.py
:language: python
```
:::

:::{dropdown} [basic_review.py](./assets/basic_review.py)

```{literalinclude} assets/basic_review.py
:language: python
```
:::

:::{dropdown} [models.py](./assets/models.py)

```{literalinclude} assets/models.py
:language: python
```
:::

:::{dropdown} [recipe_zshot.py](./assets/recipe_zshot.py)

```{literalinclude} assets/recipe_zshot.py
:language: python
```
:::

:::{dropdown} [acc_single_model.py](./assets/acc_single_model.py)

```{literalinclude} assets/acc_single_model.py
:language: python
```
:::

:::{dropdown} [recipe_2_models_zshot.py](./assets/recipe_2_models_zshot.py)

```{literalinclude} assets/recipe_2_models_zshot.py
:language: python
```
:::

:::{dropdown} [acc_2_models.py](./assets/acc_2_models.py)

```{literalinclude} assets/acc_2_models.py
:language: python
```
:::
