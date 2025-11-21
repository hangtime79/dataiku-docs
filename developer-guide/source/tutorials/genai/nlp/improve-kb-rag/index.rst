RAG: Improving your Knowledge Bank retrieval
********************************************

.. meta::
  :description: This tutorial aims to improve the retrieval quality of a Retrieval-Augmented Generation (RAG) system developed using Dataiku's LLM Mesh.

Once you have created a Knowledge Bank and used it as the base of your RAG, for example,
after following the :doc:`Programmatic RAG with Dataiku's LLM Mesh </tutorials/genai/nlp/llm-mesh-rag/index>` tutorial,
you can improve the quality of your retrieval with an additional pre-retrieval step.

Prerequisites
=============

- Dataiku >= 13.4
- An OpenAI connection
- Python >= 3.9
- A code environment with the following packages:

  .. code-block:: python

    langchain           #tested with 0.3.13
    langchain-chroma    #tested with 0.1.4
    langchain-community #tested with 0.3.13
    langchain-core      #tested with 0.3.63

Additionally, we will start with the RAG developed during the :doc:`Programmatic RAG with Dataiku's LLM Mesh </tutorials/genai/nlp/llm-mesh-rag/index>` tutorial.
As described in this previous tutorial, you will need the corresponding prerequisites.

Introduction
============

When a user prompt is processed by a RAG, the workflow usually involves first querying the vector store and using the result to enrich the context of the LLM query.
This tutorial will explain how to improve the final answer by enhancing the initial prompt before retrieval.
This additional step will clarify, rephrase, and expand the original prompt to match the context.
This step will result in a broader set of relevant documents retrieved, improving the global answer's precision.

Starter code for your RAG
==========================

The :ref:`code below<tutorials-genai-improve-rag-starter>` is a starter code for your RAG.
You define access to the Knowledge Bank with the embedded documents, and then use the corresponding vector store to run an enriched LLM query.

.. dropdown:: initial_rag.py

    .. literalinclude:: ./assets/initial_rag.py
        :language: python
        :caption: Code 1: Starter code for your RAG
        :name: tutorials-genai-improve-rag-starter

Rewriting the query
===================

If you want to improve the answer from your RAG system, you can first improve the original query.
The goal is to design the system prompt to guide the query's rewriting process, clarifying and expanding what was originally input.
The :ref:`following code<tutorials-genai-improve-rag-rewrite-query>` shows how to add this rewriting.

    .. literalinclude:: ./assets/rewriting.py
        :language: python
        :caption: Code 2: Add a query rewriting before the RAG query
        :name: tutorials-genai-improve-rag-rewrite-query

For example, an original query like ``inflation in Europe`` may be improved by asking ``What are the projected inflation trends in Europe for the next year, and what are the key factors influencing these trends?``
You have to tailor the system prompt to rewrite the query according to the context of your project.

Wrapping up
===========

Congratulations! You are now able to improve the results coming from your RAG.
Depending on the context of your usage, you may also use techniques like semantic enrichment or multi-query expansion.