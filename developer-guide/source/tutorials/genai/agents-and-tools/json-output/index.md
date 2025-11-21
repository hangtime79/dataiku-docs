# Using the LLM Mesh to parse and output JSON objects

## Introduction

In this tutorial, you will process structured objects and receive JSON output
from a model via the LLM Mesh. As autoregressive text generation models, LLMs
almost often produce free-form text responses. You can ensure consistent results
using JSON for both input and output, especially by specifying an output schema.
Defined schemas are also easy to process, less error-prone and especially useful
for saving the output for data analysis or use in downstream applications. The
tutorial showcases this technique by performing sentiment analysis on product
reviews. It could be extended to other tasks that process or output text.

## Prerequisites

- Dataiku >= 13.3
- Project permissions for "Read project content" and "Write project content"
- An existing LLM Mesh connection that supports JSON output (OpenAI, Azure
  OpenAI, Vertex Gemini as of
  [13.3](https://doc.dataiku.com/dss/latest/release_notes/13.html#id16), with
  *experimental* support on Hugging Face models)

## Data extraction

This tutorial uses the [Amazon Review
Dataset](https://nijianmo.github.io/amazon/index.html). The Python script below
downloads one of the subset
[datasets](http://jmcauley.ucsd.edu/data/amazon_v2/categoryFilesSmall/Luxury_Beauty_5.json.gz),
creates a small sample of reviews and uploads it as a dataset named
`amznreviews-sample`. To use this script, you must create a Python recipe from
the Flow with an output dataset named `amznreviews-sample` and copy the code
into the recipe's editor. Pay attention to how the reviews are stored as JSON
with keys for product category and review text.

```{literalinclude} assets/extract.py
:language: python
:caption: Extracting a sample from reviews dataset
:emphasize-lines: 30-33
```

## Setting up the schema for JSON output

```{note}
Similar to the last script, you'll create another Python recipe in the Flow with `amznreviews-sample` as the input dataset and `amznreviews-sample-llm-scored` as the output. Copy the scoring script (`score`) available at the end of this tutorial into the recipe's editor. The sections below will discuss only relevant snippets of code.
```

Next, you will use the LLM Mesh to analyze product reviews and generate
structured JSON responses. The key to getting consistent, structured output is
defining the JSON schema beforehand when setting up the LLM's completion task.
It ensures that the output follows a predefined schema, making it easier to
process and validate. The goal is to direct the LLM's response to a consistent
structure, since the output will saved as a structured dataset.

```{literalinclude} assets/score.py
:language: python
:caption: Defining the JSON schema
:lines: 16-33
```

## Getting structured output

Once you define the schema of your output, you'll need to outline how you want
the LLM to process the JSON input and what keys the output should contain. This
is done using a system prompt:

```{literalinclude} assets/score.py
:language: python
:caption: Extracting a sample from reviews dataset
:lines: 35-42
```

Now, you can specify that the LLM output needs to matching the schema you
defined using the
{meth}`~dataikuapi.dss.llm.DSSLLMCompletionsQuery.with_json_output` method.
Here's what a test of this setup could look like:

```python
completion = llm.new_completion()
completion.with_json_output(schema=SCHEMA)
completion.with_message(PROMPT, role="system")
review_json = {
    "text": "This is an amazing product! It is exactly what I wanted.",
    "category": "Luxury_Beauty"
}
completion.with_message(json.dumps(review_json), role="user")

response = completion.execute()
result = response.json
print(f"Sentiment: {result['llm_sentiment']}")
print(f"Explanation: {result['llm_explanation']}")
print(f"Confidence: {result['llm_confidence']}")

# Sentiment: positive
# Explanation: The review expresses strong satisfaction with the product.
# Confidence: 0.95
```

## Processing Multiple Reviews

The `new_completions()` method sends multiple queries in a single request for
batch processing multiple reviews from the extracted sample. This approach
allows you to send multiple reviews in one batch to the LLM, which is more
efficient than sending individual requests, as in the example above.

It is also helpful in parsing or creating large datasets since each review is
processed consistently according to the schema you defined.

```{literalinclude} assets/score.py
:language: python
:caption: Extracting a sample from reviews dataset
:lines: 44-56
```

## Saving scores and other results

The results can be saved back to a Dataiku dataset. You'll define the schema for
the output dataset, ensuring that each review's scores and analysis are stored
in a structured format. The complete JSON output from the LLM is also saved.

```{literalinclude} assets/score.py
:language: python
:caption: Extracting a sample from reviews dataset
:lines: 58-66
```

## Wrapping up

Using Dataiku's LLM Mesh with structured output provides several benefits,
including built-in validation through JSON schema. You could extend this example
by trying different schema definitions and including options like strict
checking.

````{dropdown} [extract](assets/extract.py)
```{literalinclude} assets/extract.py
:language: python
:caption: Full script
```
````

````{dropdown} [score](assets/score.py)
```{literalinclude} assets/score.py
:language: python
:caption: Full script
```
````
