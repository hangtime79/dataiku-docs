Initial setup
################

Install and enable the RAG code env
=============================================

In order to work with knowledge banks and perform RAG, you need a dedicated code environment (see :doc:`/code-envs/index`) with the appropriate packages.

* In **Administration** > **Code envs** > **Internal envs setup**, in the **Retrieval augmented generation code environment** section, select a Python version in the list and click **Create code environment**
* In **Administration** > **Settings** > **LLM Mesh**, in the **Retrieval augmented generation** section, select **Use internal code env**


.. _embedding_llms:

Embedding LLMs
===============

In order to use RAG, you must have at least one LLM connection that supports embedding LLMs. At the moment, embedding is supported on the following connection types:

* OpenAI
* Azure OpenAI
* AWS Bedrock
* Databricks Mosaic AI
* Snowflake Cortex
* Local Hugging Face
* Mistral AI
* Vertex Generative AI
* Amazon Sagemaker LLM
* Custom LLM Plugins