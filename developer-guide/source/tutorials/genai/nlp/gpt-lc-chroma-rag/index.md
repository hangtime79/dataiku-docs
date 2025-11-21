# Using Langchain, Chroma, and GPT for document-based retrieval-augmented generation 

```{tip}
As of version 12.3, Dataiku's {doc}`LLM mesh features <refdoc:generative-ai/index>`
enhance the user experience by providing oversight, governance and centralization of LLM-powered capabilities.
Please refer to {doc}`this tutorial <../llm-mesh-rag/index>` for a
LLM-mesh-oriented example of zero-shot classification problem.
```

While large language models (LLM) can perform well on text generation, they can only do so by leveraging 
the information gathered from the data they have been trained on. However, in several use-cases, you may need
to rely on data that the model hasn't seen (e.g., recent or domain-specific data).

In this tutorial you will leverage OpenAI's GPT model with a custom source of information, 
namely a PDF file. This process is often called *retrieval-augmented generation* (RAG) and will also bring
in new tools such as *vector databases* and the *Langchain* library.

## Prerequisites

* Dataiku >= 11.4
* “Use” permission on a code environment using Python >= 3.9 with the following packages:
    * In the code environment screen, for core package versions select "Pandas 1.3 (Python 3.9 and above)"
    * `openai` (tested with version 0.27.8)
    * `langchain` (tested with version 0.0.200)
    * `chromadb` (tested with version 0.3.26)
    * `pypdf` (tested with version 3.9.1)
    * `sentence-transformers` (tested with version 2.2.2) with the following resource initialization script:
      
      :::{dropdown} [code_env_init_script.py](./assets/code_env_init_script.py)

        ```{literalinclude} assets/code_env_init_script.py
        :language: python
        ```
        :::

## Creating the vector database 

In this section, you will retrieve an external document and *index* it to be queried. In your project,
create a new empty local managed folder called `documents` and write down its id.

### Getting the data

The examples covered in this tutorial will be based on the World Bank's Global Economic Prospects (GEP) 2023 report.
Download its PDF version from [this page](https://www.worldbank.org/en/publication/global-economic-prospects) (Downloads
-> Full report) into the managed folder. Then, rename the file as `world_bank_2023.pdf`. 

### Indexing and persisting the database 

The first step of your Flow will extract the text from your document, transform it into *embeddings* then store them 
inside a *vector database*. Simply put, those embeddings capture the semantic meaning and context of the encoded 
text: querying the vector database with a text input will return the most similar elements in that database (in 
the semantic sense).

In practice, you will use that vector database to *enrich your prompt* by adding relevant text from the document. 
This will allow the LLM to directly leverage the document's data when asked about its content. 

Create a new Python recipe using `documents` as input and a new local managed folder called `vector_db` as output
with the code below. The highlighted lines indicate where you should put your folder ids:

:::{dropdown} compute_vector_db.py
:open:

```{literalinclude} assets/compute_vector_db.py 
:language: python 
:emphasize-lines: 10,26
```
:::

The 3 key ingredients used in this recipe are:

* **The document loader** (here `PyPDFLoader`): one of Langchain's tools to easily load data from various files 
and sources. 

* **The embedding function**: which kind of text embedding to use for encoding the document's text. The recipe
leverages a variant of the [sentence transformer embeddings](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) 
that maps paragraphs and sentences to a 384-dimensional dense vector space. 

* **The vector database**: there are many options available to store the embeddings. In this tutorial, you will use 
[Chroma](https://www.trychroma.com/), a simple yet powerful open-source vector store that can efficiently be persisted 
in the form of Parquet files. 

Note that the original document was split into smaller chunks before being indexed. This will allow you to find the 
most relevant pieces of the document for a given query and pass only those into your LLM's prompt.

## Running an enriched LLM query

Now that the vector database is ready, you can combine it with a call to your LLM. To do so, you will take advantage 
of several main assets of the Langchain library: *prompt templates*, *chains*, *loaders*, and *output parsers*.

### Creating the LLM object 

The first object to define when working with Langchain is the *LLM*. Langchain's LLM API allows users to easily swap 
models without refactoring much code. Since this tutorial relies on OpenAI's GPT, you will leverage the corresponding 
[chat model](https://python.langchain.com/docs/modules/model_io/models/chat/) called `ChatOpenAI`.

In your Python project library, create a new directory called `gpt_utils`, and inside that directory, create two files:

* an empty `__init__.py` file 
* an `auth.py` file with the following code: 

    :::{dropdown} auth.py
    :open:

    ```{literalinclude} assets/auth.py
    :language: python 
    ```
    :::

* a `models.py` file with the following code: 

    :::{dropdown} models.py
    :open:

    ```{literalinclude} assets/models.py
    :language: python 
    ```
    :::

From there you can easily test your LLM. Try running this code from a notebook: 

```{literalinclude} assets/notebook.py
    :language: python 
    :lines: 2-5
```

```
The World Bank is an international financial institution that provides loans and grants to 
developing countries for the purpose of reducing poverty and promoting sustainable economic growth.
```

You will use more elaborate ways to call the model later on. Next comes the notion of the chain. 

### Creating the question-answering chain 

The main objective of the Langchain library is to enable users to chain together different components (models,
prompts, vector databases, etc.). In the API, the `Chain` interface is a sequence of calls to these components taking 
a given input, and returning a given output. 

In this section, you will create a specific type of chain called *stuff document chain* which will insert parts of a 
document into a prompt and then pass that prompt into a LLM.

Let's see a usage example: in your notebook, run the code below. The highlighted lines indicate where you should put 
your output folder id:

```{literalinclude}  assets/notebook.py
:language: python 
:lines: 9-37
:emphasize-lines: 16
```

```
Based on the given context, the three main perspectives regarding inflation are:

1. Favorable Base Effects: The deceleration of global inflation is largely attributed to favorable base effects 
from commodity prices falling below their peak levels in 2022. This suggests that the recent decrease in inflation 
is temporary and influenced by the fluctuations in commodity prices.

2. Excess Demand: In advanced economies, high inflation is primarily driven by excess demand, even as supply chain 
pressures ease and energy prices decline. The absence of economic slack and the ability of firms and workers to 
exercise pricing power contribute to the persistence of inflation.

3. Negative Supply Shocks: Negative supply shocks, such as significant disruptions to oil supplies caused by 
geopolitical disturbances or stronger-than-expected demand for commodities, can raise commodity prices and 
pass through to core consumer prices. This can lead to unanchored inflation expectations and prompt central banks 
to tighten monetary policy.
```

Let's decompose this code snippet:

* First, it loads the embedding function that will be used to encode the prompt before the similarity search query.

* Then, it loads the Chroma vector database previously created in memory, making it ready to be queried.

* Finally, the output of that search is passed to the chain created via `load_qa_chain()`, then run through the LLM, and 
the text response is displayed. Check out Langchain's 
[API reference](https://api.python.langchain.com/en/latest/index.html) to learn more about document chains.

### Adding output formatting 

The previous code snippet provided a raw text output, but in many cases, the user may need something more structured, 
depending on what will be done afterward. This is a good opportunity to introduce two other key Langchain 
concepts: *prompt templates* and *output parsers*.

* *Prompt templates* provide an abstraction layer on top of the text you send to your LLM. Basically, it allows you 
to define a dynamic blueprint from which the prompt text will be generated at execution time. 

* *Output parsers* help structure the LLM's output to constrain it to a specific format. It is particularly useful 
when the model's output is sent to another application  that expects a specific data structure.

The following example combines these elements with a question-answering chain to retrieve information in the form of a 
string with comma-separated values:

```{literalinclude} assets/notebook.py
:language: python 
:lines: 41-61
```

## Linking multiple enriched LLM queries

You now have all the building blocks to build a more complex item to add to your Flow. You already know how to build a 
chain that retrieves the list of the main regions of interest from the report: in this section, you will implement a 
recipe to combine it with another one that generates summary reports on a given list of topics for each region.

This will translate into running 2 chains sequentially, and while Langchain also has utilities to perform this kind 
of operation, for the sake of simplicity, you will use plain string interpolation. 

Since the final result of this operation is meant to be written in a Dataiku dataset, your first step is to define how 
this output should be formatted so that it can be easily passed to the dataset writer. 

In your project library, under gpt_utils create a new file called `wb_reporter.py` and add the following code: 

:::{dropdown} wb_reporter.py 
:open:

```{literalinclude} assets/wb_reporter.py 
:language: python 
```
:::

* `TOPICS` contains the names and descriptions of each topic to generate a report on.

* The `RegionOutlook` and `RegionOutlookList` are Pydantic models that will be used to parse the output into a JSON 
data structure containing the list of summary reports for each region by topic. To learn more about Langchain's 
`PydanticOutputParser`, check out its 
[documentation](https://python.langchain.com/docs/modules/model_io/output_parsers/#output-parser-types).

* `build_qa_chain()` and `run_qa_chain()` wrap the prompt templating and chain definition/run steps into functions to make the recipe's 
code more modular. `build_qa_chain()` uses a more elaborate version of the prompt template called `ChatPromptTemplate`, 
which structure follows the system and user message mechanism introduced in the OpenAI API client, see more details in its
[documentation](https://python.langchain.com/docs/modules/model_io/prompts/pipeline).

You can now embed those components into a recipe in your Flow! Create a new Python recipe using `vector_db` as input 
and a new dataset called `wb_regional_reports` as output with the code below. The highlighted parts indicate where you 
should put `vector_db`'s id.

:::{dropdown} compute_wb_regional_reports.py
:open:

```{literalinclude} assets/compute_wb_regional_reports.py
:language: python 
:emphasize-lines: 27
```

:::

In this recipe's code you start by running a first chain (`reg_chain`) that outputs the list of regions. Then, the `
rpt_chain` leverages that list to generate a summary analysis on each topic of interest and the final result is 
written in a dataset, each record representing a region and each topic aligned on a column. 

## Wrapping up 

Congratulations, you have implemented a full example of RAG-based LLM usage to extract information from a document! 
From there, you can dig deeper and for example:
* try uploading your own document(s) and adjust the prompt templates accordingly
* use Langchain's own tools like `SequentialChain` to run linked chains 
* play with the number of similarity search outputs to widen the information given to the model 

If you want a high-level introduction to LLMs in the context of Dataiku, check out 
[this guide](https://content.dataiku.com/llms-dataiku/dataiku-llm-starter-kit).

Here are the complete versions of the code presented in this tutorial: 

:::{dropdown} [compute_vector_db.py](./assets/compute_vector_db.py)

```{literalinclude} assets/compute_vector_db.py 
:language: python 
```
:::

:::{dropdown} [auth.py](./assets/auth.py)

```{literalinclude} assets/auth.py
:language: python 
```
:::

:::{dropdown} [models.py](./assets/models.py)

```{literalinclude} assets/models.py
:language: python 
```
:::

:::{dropdown} [wb_reporter.py](./assets/wb_reporter.py)

```{literalinclude} assets/wb_reporter.py 
:language: python 
```
:::

:::{dropdown} [compute_wb_regional_reports.py](./assets/compute_wb_regional_reports.py)

```{literalinclude} assets/compute_wb_regional_reports.py
:language: python 
```
:::
