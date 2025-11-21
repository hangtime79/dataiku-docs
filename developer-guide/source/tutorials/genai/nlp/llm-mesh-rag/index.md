# Programmatic RAG with Dataiku's LLM Mesh and Langchain

While large language models (LLM) perform text generation well, they can only
leverage the information on which they have been trained. However, many use
cases might rely on data the model has not seen. This inability of LLMs to
perform tasks outside their training data is a well-known shortcoming--for
example, with recent or domain-specific information. This tutorial covers a
technique that overcomes this common pitfall.

This tutorial implements this process known as *retrieval-augmented generation*
(RAG). To perform this task, you will use OpenAI's GPTx model over a custom
source of information, namely a PDF file. In the process, you will use Dataiku's
LLM mesh features, namely:

1. LLM connections
2. Knowledge Banks
3. Dataiku's Langchain integrations for vector stores and LLMs

## Prerequisites

- Dataiku >= 12.4
- permission to use a Python code environment with the **Retrieval augmented
generation models** package set installed, plus the `tiktoken`, `pypdf`
packages
- OpenAI LLM connection for a GPT model enabled (preferably GPT-4)

```{note}
You will *index* a document so it can be queried by an LLM. From version 12.3, Dataiku provides a native Flow item called [Knowledge Bank](https://doc.dataiku.com/dss/latest/generative-ai/rag.html#concepts) that points to a vector databases where its embeddings are stored.
```

## Converting a downloaded document into chunks

Create a Python recipe and create an output dataset named `document_splits`.
Within it, run the following script that downloads a PDF document:

```{dropdown} [Python script - split document](./assets/recipe_split.py)
```{literalinclude} assets/recipe_split.py
:language: python
:caption: recipe_split.py
```

```{caution}
This tutorial uses the World Bank's Global Economic Prospects (GEP) report. 
If the referenced publication is no longer available, look for the latest report's 
PDF version on [this page](https://www.worldbank.org/en/publication/global-economic-prospects) 
```

The next step will be to extract the document text, transform it into
*embeddings* and store them in a *vector database*. Before indexing a document
into a vector database this way, it is a common practice to split the text into
smaller chunks first. Searching across multiple smaller chunks instead of a
single large document allows for a more granular match between the input prompt
and the document's content.

Once built, each row from `document_splits` will contain a distinct chunk with:
1. an ID
1. text
1. origin page number
1. length measured by the number of tokens, which allows us to quantify how much
of the LLM's context window will be consumed and the cost of computing
embeddings via services like the OpenAI API

## Storing embeddings in a vector database

Embeddings capture the semantic meaning and context of the encoded text.
Querying the vector database with a text input will return the most similar
elements (in the semantic sense) in that database. These results from that
vector database are used to *enrich* your prompt by adding relevant text from
the document. This allows the LLM to leverage the document's data directly when
asked about its content.

In Dataiku, a knowledge bank (KB) flow item represents the vector database. It
is created using a visual *[embedding
recipe](https://knowledge.dataiku.com/latest/ml-analytics/gen-ai/concept-rag.html#embed-recipe-settings)*.

Implement and run a new embedding recipe (**+RECIPE > LLM Recipes > Embed**)
with `document_splits` as the input dataset and a KB called `document_embedded`
with the following settings:

1. embedding model: "Embedding (Ada 002)"
1. knowledge column -> `text`
1. metadata columns (optional): page, split_id, nb_tokens
1. document splitting method: “Do not split”

```{note}
When accessing a KB from the Dataiku UI, its URL is of the form:

`https://dss.example/projects/YOUR_PROJECT_KEY/knowledge-bank/<KB_ID>`
```

Take note of the KB ID. You can also retrieve this identifier later on with the
{meth}`~dataikuapi.dss.project.DSSProject.list_knowledge_banks()` method.

By handling it as  *Langchain vector stores*, you can query a KB
programmatically. To test, run the following code from a notebook:

```{dropdown} [Python notebook - test kb](./assets/recipe_split.py)
```{literalinclude} assets/sample_simsearch.py
:language: python
:caption: sample_simsearch.py
```

## Running an enriched LLM query

 Now that the KB is ready to query, you can use it with an LLM. In practice, you
 will use your prompt as a query for similarity search to retrieve additional
 data as context. Before running inference on the LLM, this context can be added
 to the initial prompt.

 Run the following code from a notebook:

 ```{literalinclude} assets/sample_rag.py
 :language: python
 :caption: sample_rag.py
 ```

If you don't have your LLM ID at hand you can use the
{meth}`~dataikuapi.dss.project.DSSProject.list_llms()` method to list all
available LLMs for this project.

The Dataiku-native knowledge base and the LLM objects are translated into
Langchain-compatible items, which are then used to build and run the
question-answering chain. This allows you to extend the capabilities of
Dataiku-managed LLMs for more complex cases.

## Wrapping up

Congratulations, now you can perform RAG using Dataiku's programmatic LLM mesh
features! To go further, you can:

- query from multiple documents
- retrieve more results from the knowledge bank to feed the LLM
- reinforce the retrieved context's importance in the prompt
