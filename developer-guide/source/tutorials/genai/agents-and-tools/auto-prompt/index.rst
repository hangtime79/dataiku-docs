Building Auto Prompt Strategies with DSPy in Dataiku
====================================================

DSPy is the framework for **programming—rather than prompting—language models**.
It allows you to iterate fast on building modular AI systems.
It offers algorithms for optimizing their prompts and weights, whether you’re building simple classifiers, 
sophisticated RAG pipelines, or Agent loops.

This tutorial shows how we can seamlessly integrate DSPy Auto Prompting strategies into Dataiku.
DSPy has two main applications:

1. Describe AI behavior as code instead of strings.
2. Optimize your prompt to improve answer quality.

We will build a RAG module with DSPy to demonstrate the first application.

To demonstrate the second application, we will optimize our RAG module to maximize our answer quality.

Then, we can compare the performance of both RAG applications with the `LLM Evaluate
recipe <https://knowledge.dataiku.com/latest/ml-analytics/gen-ai/tutorial-llm-evaluation.html>`__.

This code could be run in a notebook. 
Let’s start!

Prerequisites
~~~~~~~~~~~~~

* Dataiku >= 13.3
* Python >=3.9
* A code environment:

  * with the "Retrieval Augmented Generation models (used by Knowledge banks)" package set installed
  * with the following packages:

  .. code:: python

      dspy-ai
      langchain
      langchain_community

You must also generate and add a Dataiku API key in your :doc:`user secrets<refdoc:security/user-secrets>` with the name ``dataiku_api_key``.

The starter flow must contain the following:

- A dataset with a set of questions & ground truth (for evaluation)
- A Knowledge Bank built with relevant information for the questions.
- Have a **baseline** prompt recipe run on the dataset using a :doc:`RAG LLM<refdoc:generative-ai/knowledge/introduction>` 
  built on the knowledge bank.

Setting up DSPy
~~~~~~~~~~~~~~~

We start by importing all relevant packages for this tutorial.

.. code:: python

    import dataiku
    import dspy
    import logging
    
    from langchain_core.documents.base import Document

To provide an LLM to DSPy, we will leverage Dataiku’s ability
to provide an :ref:`OpenAI-compatible endpoint <tutorials/nlp/openAIXmesh/client>`.

We build a ``get_key_from_user_secret`` function as a convenient way to get an API key saved in our user’s secrets.
We then build the parameters needed to configure the ``dspy`` client.

.. note:: 
    In this example, we saved an ``LLM_ID`` in the project variables to be defined once
    and reused many times across the project.

.. code:: python

    def get_key_from_user_secret(key_name : str):
        """
        Fetches API key secret in user credentials
        """
        auth_info = dataiku.api_client().get_auth_info(with_secrets=True)
        for secret in auth_info["secrets"]:
            if secret["key"] == key_name:
                logging.info(f"{key_name} has been set")
                return secret["value"]
        logging.error(f"The {key_name} is not provided in user credentials. Please set it in the user credentials")

.. code:: python

    # Prepare parameters
    project_key = dataiku.api_client().get_default_project().project_key
    base_url = f"https://design.ds-platform.ondku.net/public/api/projects/{project_key}/llms/openai/v1/"
    api_key = get_key_from_user_secret("dataiku_api_key")
    LLM_id = dataiku.get_custom_variables()["LLM_id"]
    
    # Load the LLM in DSPy as openai model
    lm = dspy.LM(f"openai/{LLM_id}", api_key=api_key, api_base=base_url)
    dspy.configure(lm=lm)

Building and Running a DSPy RAG Module on a set of queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's load the inputs to our recipe:

- We can load the input dataset containing questions and their ground truth answers.
- We also load relevant information for our use case as a Langchain Retriever into the knowledge bank to simplify the retrieval.

.. code:: python

    df = dataiku.Dataset("test_dataset_filtered").get_dataframe()
    
    retriever = (
        dataiku.api_client()
        .get_default_project()
        .get_knowledge_bank("YK6IMhfU")
        .as_core_knowledge_bank()
        .as_langchain_retriever(search_kwargs={"k": 5})
    )

It is time to build the DSPy chain of the Thought RAG client.

Notice that with the DSPy Framework, we never provide any prompt templates or text. 
We explain functionally that we will provide and ``context`` and a ``question``,
and that should yield a ``response``.

We also define a ``semantic_search`` chain using the ``Retriever`` loaded
up previously & a Document serializer function ``format_docs``.

.. note::
    To compare apples with apples, we want the context serialization to be the same as the RAG baseline.

.. code:: python

    # Build DSPy predictor
    rag = dspy.ChainOfThought('context, question -> response')
    
    # Build Semantic Search Pipeline
    def format_docs(docs : list[Document]) -> list[str]:
        """
        Function to process a list of documents
        """
        return [f"{doc.page_content}\n{doc.metadata}" for doc in docs]
    semantic_search = retriever | format_docs

It is now time to check that everything is working as expected.

.. code:: python

    # Test dspy call
    question = "Can I use python for data preparation in Dataiku?"
    context = semantic_search.invoke(question)
    rag(context=context, question=question)

.. parsed-literal::

    Prediction(
        reasoning='Yes, you can use Python for data preparation in Dataiku. Dataiku allows you to write Python recipes that can read and write datasets from various storage backends. You can manipulate datasets using regular Python code or by utilizing Pandas dataframes, making it a flexible option for data preparation tasks.',
        response='Yes, you can use Python for data preparation in Dataiku. Dataiku supports Python recipes that allow you to read and write datasets, and you can manipulate the data using either standard Python code or Pandas dataframes.'
    )


We can now run the DSPy RAG Module on our corpus of questions and 
save the results in the Flow to run the Evaluation Recipe on the results later.

.. code:: python

    for i in df.index:
        question = df.at[i, "question"]
        context = semantic_search.invoke(question)
        answer = rag(context=context, question=question)
        df.at[i, "generated_answer"] = answer.get("response")
        df.at[i, "generated_reasoning"] = answer.get("reasoning")
        df.at[i, "context_with_metadata"] = str(context)

    dataiku.Dataset("answers_dspy").write_with_schema(df)


The answers generated by this RAG module should have comparable results
to the visual baseline created directly from the knowledge bank.

The advantage of this one is that we never had to write any prompts for the LLM explicitly.

We explained **functionally** what we wanted the LLM to do and let DSPy take care of the rest.

Optimize our DSPy RAG Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For this second application of DSPy, we will optimize our RAG module to generate higher-quality answers.

The Optimization can change both the generated prompt and the AI Module parameters, for example, 
the number of returned documents.

DSPy provides different optimizers which work by:

-  Synthesizing good few-shot examples for every module like ``dspy.BootstrapRS``
-  Proposing and intelligently exploring better natural-language instructions for every prompt like ``dspy.MIPROv2``
-  And build datasets for your modules and use them to finetune the LLM weights in your system, like ``dspy.BootstrapFinetune.3``

In this example, we will be using the ``dspy.MIPROv2`` Optimizer.

First we define our ``RAG`` DSPy module, which implements a ``forward`` function.

.. code:: python

    class RAG(dspy.Module):
        def __init__(self):
            self.respond = dspy.ChainOfThought('context, question -> response')
    
        def forward(self, question):
            context = semantic_search.invoke(question)
            return self.respond(question=question,context=context)

.. code:: python

    # Test the RAG module
    rag = RAG()
    rag(question = "Can I build and configure regression models in Dataiku?")
    #dspy.inspect_history(n=1) # Display the raw prompt generated for the last n calls

.. parsed-literal::

    Prediction(
        reasoning='Yes, you can build and configure regression models in Dataiku. The platform supports regression as one of the prediction types, allowing users to set a numeric target variable. In the Design tab, you can modify your target variable and choose regression for numeric targets. Additionally, Dataiku provides options for partitioning models, selecting performance metrics, and customizing hyperparameters, which are essential for effectively training regression models.',
        response='Yes, you can build and configure regression models in Dataiku. The platform allows you to set a numeric target variable and provides various options for model design, including partitioning, performance metrics, and hyperparameter customization.'
    )



We then format our input ground truth data to be compatible with the optimizer.

.. note::
    This is a proof of concept. You might need to increase the number of ground truth Q&A to get better results.

.. code:: python

    # Prepare data for optimization
    data = []
    for idx, row in df.iterrows():
        data.append({
            "question" :row["question"],
            "response" :row["ground_truths"],
            "gold_doc_ids" : [] # Not available in input dataset
        })
    data = [dspy.Example(**d).with_inputs('question') for d in data]
    
    trainset, devset = data[:20], data[20:50]
    len(trainset), len(devset)

We then define a metric for optimizing.

In this example, we use the ``SemanticF1``, but DSPy offers to choose from.

The ``dspy.Evaluate`` allows us to set an average performance for our  baseline RAG Module.

.. code:: python

    from dspy.evaluate import SemanticF1
    
    # Instantiate the metric & and evaluator
    metric = SemanticF1(decompositional=True)
    evaluate = dspy.Evaluate(devset=devset, metric=metric, num_threads=24,
                             display_progress=True, display_table=2)
    
    # This sets a baseline Module Score
    evaluate(RAG())
    # Baseline Average Score : SemanticF1 = 55.3

.. raw:: html

    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table class="dataframe" style="font-size:small;">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>question</th>
          <th>example_response</th>
          <th>gold_doc_ids</th>
          <th>reasoning</th>
          <th>pred_response</th>
          <th>SemanticF1</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>How can I write a if condition in a Prepare recipe?</td>
          <td>You should use th e "Create if, then, else statements" step. This p...</td>
          <td>[]</td>
          <td>To write an if condition in a Prepare recipe, you typically need t...</td>
          <td>To write an if condition in a Prepare recipe, you can add a step i...</td>
          <td>✔️ [0.286]</td>
        </tr>
        <tr>
          <th>1</th>
          <td>How can I transform a dataset into an editable dataset?</td>
          <td>The “Push to editable” recipe allows you to copy a regular dataset...</td>
          <td>[]</td>
          <td>To transform a dataset into an editable dataset in Dataiku, you ca...</td>
          <td>To transform a dataset into an editable dataset, follow these step...</td>
          <td>✔️ [0.400]</td>
        </tr>
      </tbody>
    </table>


.. raw:: html

    
    <div style='
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        color: #555;
        margin: 10px 0;'>
        ... 28 more rows not displayed ...
    </div>


It is time to feed some golden examples of questions and answers to our DSPy optimizer to optimize our module’s prompt generation.

.. warning::
    This step can take some time and is very LLM query heavy.
    Make sure to estimate the cost of running the optimization and
    configure the parameters to fit your budget and LLM rate limit.

.. code:: ipython3

    tp = dspy.MIPROv2(metric=metric, auto="medium", num_threads=25)  # use fewer threads if your rate limit is small
    
    optimized_rag = tp.compile(RAG(), trainset=trainset,
                               max_bootstrapped_demos=2, max_labeled_demos=2,
                               requires_permission_to_run=False)


Once the training has been completed, we want to save the optimized model as a ``json`` artifact to a Dataiku :doc:`Managed Folder<refdoc:connecting/managed_folders>`.

That way, next time we need the optimized prompt, we can load it back instead of optimizing the RAG module again!

Since the artifacts are saved as ``json`` objects, you can navigate the folders and see how the prompt configuration has changed.

.. code:: python

    # Save the optimized model to managed folder
    handle = dataiku.Folder("1fazm3ba")

    # Save baseline rag
    baseline_file_path = handle.get_path() + "/baseline_rag.json"
    rag.save(baseline_file_path)

    # Save optimized rag
    optimized_rag_file_path = handle.get_path() + "/optimized_rag.json"
    optimized_rag.save(optimized_rag_file_path)

.. code:: python

    # Ex: Load the optimized model from a managed folder
    loaded_rag = RAG()
    loaded_rag.load(optimized_rag_file_path)

Running the same question through the baseline
and the optimized Module can already give us an idea of the difference in RAG performance.

.. code:: python

    question = 'How can I write a pandas dataframe to a dataset in Python?'
    baseline = rag(question=question)
    print(baseline.response)

.. parsed-literal::

    You can write a pandas DataFrame to a dataset in Python using the following code:

    ```python
    output_ds = dataiku.Dataset("myoutputdataset")
    output_ds.write_with_schema(my_dataframe)
    ```

    This code creates a Dataset object for your output dataset and writes the DataFrame `my_dataframe` to it while maintaining the dataset's schema.

.. code:: python

    pred = optimized_rag(question=question)
    print(pred.response)

.. parsed-literal::

    To write a Pandas DataFrame to a dataset in Python, you can use the following code:

    ```python
    import dataiku
    import pandas as pd

    # Assuming 'my_dataframe' is your Pandas DataFrame
    output_ds = dataiku.Dataset("myoutputdataset")
    output_ds.write_with_schema(my_dataframe)
    ```

    This code creates a Dataset object for the specified output dataset and writes the DataFrame to it while maintaining the schema

To understand why the answers are different, we can look at the differences in the prompts sent over 
to the LLM for both modules leveraging the ``dspy.inspect_history(n=2)`` tool.

.. code:: python
    
    dspy.inspect_history(n=2) # Display the last two calls above

Evaluating both RAG Modules with the LLM Evaluate Recipe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We could run the DSPy **evaluator** we created before, but the `LLM Evaluate Recipe <https://knowledge.dataiku.com/latest/ml-analytics/gen-ai/tutorial-llm-evaluation.html>`__ has a more comprehensive list of RAG metrics and integrates well with the rest of our Dataiku flow.

.. code:: python

    # Eval the optimized rag Module
    evaluate(optimized_rag)
    # Result : SemanticF1 = 52.04

.. raw:: html

    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table class="dataframe" style="font-size:small;">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>question</th>
          <th>example_response</th>
          <th>gold_doc_ids</th>
          <th>reasoning</th>
          <th>pred_response</th>
          <th>SemanticF1</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>How can I write a if condition in a Prepare recipe?</td>
          <td>You should use the "Create if, then, else statements" step. This p...</td>
          <td>[]</td>
          <td>In a Prepare recipe, you can write an if condition by using the sc...</td>
          <td>To write an if condition in a Prepare recipe, you need to add step...</td>
          <td>✔️ [0.400]</td>
        </tr>
        <tr>
          <th>1</th>
          <td>How can I transform a dataset into an editable dataset?</td>
          <td>The “Push to editable” recipe allows you to copy a regular dataset...</td>
          <td>[]</td>
          <td>To transform a dataset into an editable dataset in Dataiku, you ca...</td>
          <td>To transform a dataset into an editable dataset in Dataiku, follow...</td>
          <td>✔️ [0.600]</td>
        </tr>
      </tbody>
    </table>

For this tutorial, all we need to do is log the relevant information
to a dataset in the Flow to be used as input for the **LLM Evaluate Recipe**.

.. code:: python

    # Run optimized prompt
    #df.drop(["generated_answer", "generated_reasoning","context_with_metadata"], axis=1, inplace=True)
    for i in df.index:
        question = df.at[i, "question"]
        answer = optimized_rag(question=question)
        df.at[i, "generated_answer"] = answer.get("response")
        df.at[i, "generated_reasoning"] = answer.get("reasoning")
        df.at[i, "context_with_metadata"] = semantic_search.invoke(question)

    dataiku.Dataset("answers_dspy_optimized").write_with_schema(df)    