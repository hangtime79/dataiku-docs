Creating and using a Knowledge Bank
***********************************

.. meta::
  :description: This tutorial shows how to create a Knowledge Bank and add documents to it.

This tutorial teaches you how to create a :doc:`Knowledge Bank <refdoc:generative-ai/knowledge/introduction>`.
You will then learn how to store the embeddings of your content into the newly created Knowledge Bank.
Finally, this tutorial will show you how to use this Knowledge Bank in your RAG.

Prerequisites
=============

* Dataiku >= 14.1
* permission to use a Python code environment with the **RAG and Agents** package set installed, plus the ``pypdf`` package
* Python >= 3.9
* LLM connection to a model able to embed text content

Creating a Knowledge Bank
=========================

Dataiku provides a way to store and manipulate your embedded documents through the :class:`~dataikuapi.dss.knowledgebank.DSSKnowledgeBank` class.
The first step is to create a Knowledge Bank from your :class:`~dataikuapi.dss.project.DSSProject`.

.. literalinclude:: ./assets/complete.py
        :language: python
        :caption: Code 1: Creating your Knowledge Bank
        :name: tutorials-genai-creating-knowledge-bank
        :lines: 1,5-13

The storage of the vectorized content will be based here on ChromaDB, but you have several other options as per the :meth:`~dataikuapi.dss.project.DSSProject.create_knowledge_bank` documentation.
The parameter ``EMBED_LLM_ID`` defines the model that will be used in the next step during vectorization of the content.
This :ref:`code sample <ce/llm-mesh/native-llm-list-with-purpose>` will help you find an LLM with the proper purpose.

Adding content to the Knowledge Bank
====================================

Now that we have a Knowledge Bank, we must add the content for our use case.
It is a common practice to split the text into smaller chunks before indexing the embedded result.
:doc:`This tutorial </tutorials/genai/nlp/llm-mesh-rag/index>` provides more information on the complete process.

.. literalinclude:: ./assets/complete.py
        :language: python
        :caption: Code 2: Adding content to your Knowledge Bank
        :name: tutorials-genai-adding-content-knowledge-bank
        :lines: 2-3,5-6,16-35

The combination of :meth:`~dataiku.KnowledgeBank.get_writer` and :meth:`~dataiku.KnowledgeBank.as_langchain_vectorstore` will provide access to the vector store.
You can then use the `add_documents <https://python.langchain.com/api_reference/core/vectorstores/langchain_core.vectorstores.base.VectorStore.html#langchain_core.vectorstores.base.VectorStore.add_documents>`__ method to embed and add the content of your chunks of content.


.. caution::
    This tutorial uses the World Bank's Global Economic Prospects (GEP) report.
    If the referenced publication is no longer available, look for the latest report's
    PDF version on `this page <https://www.worldbank.org/en/publication/global-economic-prospects>`__.


Using the Knowledge Bank
=========================

Once you have a Knowledge Bank with the content you want, you can use it in your RAG.
:doc:`The tutorial </tutorials/genai/nlp/llm-mesh-rag/index>` shows you a complete approach, and the :ref:`Code 3<tutorials-genai-using-knowledge-bank>` below is a good reminder of how to do a RAG query.

.. literalinclude:: ./assets/complete.py
        :language: python
        :caption: Code 3: Using the Knowledge Bank
        :name: tutorials-genai-using-knowledge-bank
        :lines: 4,5-6,38-50

Wrapping up
===========

Congratulations! You are now able to create, enrich, and use a Knowledge Bank.
This provides a way to improve and enrich the answers of your LLMs or your Agents.

Here is the complete code of all the steps.

.. dropdown:: `Knowledge Bank tutorial complete code`

    .. literalinclude:: ./assets/complete.py
        :language: python
        :name: tutorials-genai-complete-knowledge-bank

Reference documentation
=======================

Classes
-------

.. autosummary::
    dataikuapi.DSSClient
    dataikuapi.dss.knowledgebank.DSSKnowledgeBank
    dataikuapi.dss.project.DSSProject
    dataiku.KnowledgeBank

Functions
---------

.. autosummary::
    ~dataikuapi.dss.knowledgebank.DSSKnowledgeBank.as_core_knowledge_bank
    ~dataikuapi.dss.llm.DSSLLM.as_langchain_chat_model
    ~dataiku.core.vector_stores.data.writer.VectorStoreWriter.as_langchain_vectorstore
    ~dataiku.KnowledgeBank.as_langchain_vectorstore
    ~dataikuapi.dss.project.DSSProject.create_knowledge_bank
    ~dataikuapi.DSSClient.get_default_project
    ~dataiku.KnowledgeBank.get_writer

