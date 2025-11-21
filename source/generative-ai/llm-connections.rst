LLM connections
################

.. contents::
	:local:

In order to start using the LLM Mesh, an administrator first needs to define connections to LLM models.

There are two kinds of connections to LLM models:

* Hosted LLM APIs
* Locally-running LLM models, using HuggingFace models running on GPUs.


Hosted LLM APIs
===============

The LLM Mesh provides support for a vast number of LLM API providers in order to maximize your options for choosing your preferred LLM provider.


Anthropic
----------

The Anthropic connection provides connection to Anthropic text models. You will need a Anthropic API key.

The Claude, Claude-instant, Claude 2 and Claude 3 models are supported.


AWS Bedrock
------------

The Bedrock connection provides access to models through Amazon Bedrock. You will need:

* An AWS account with Bedrock access enabled
* An existing S3 connection with credentials properly setup.

The Bedrock connection provides access to the following Bedrock models:

* The Anthropic Claude models family (Instant v1, v2, v3, v3.5 Sonnet)
* The AI21 Labs Jurassic 2 models family
* The Cohere Command models family (Command, Command Light, Command R, command R+), and Cohere Embed models
* The AWS Titan G1 models family, AWS Titan v2 Embeddings
* The Mistral models family (7B, 8x7B, Large)
* The Meta Llama2 and Llama3 Chat models
* The Stability AI image generation models

    * SDXL 1.0
    * Stable Image Core
    * Stable Diffusion 3 Large
    * Stable Image Ultra

Text completion, chat completion, image generation and text/image embedding models are supported.

Inference profile
^^^^^^^^^^^^^^^^^
A cross-region inference profile allows you to distribute traffic across different AWS regions, therefore increasing throughput and resilience.
When provided, an inference profile applies to all enabled models, including custom models.
However, the inference profile is not applied to any custom models with an application inference profile ARN as the id.

Note that some models/regions require an inference profile to work on AWS' side, and that Bedrock's support for them varies by model/region. See `this list <https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html>`_ of supported inference profiles by region and model.
See the `AWS documentation <https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html>`_ for more information.

AWS SageMaker LLM
------------------

The SageMaker LLM connection allows connecting to some completion and summarization models deployed as SageMaker endpoints. You will need an existing SageMaker connection.

The following models have builtin handling modes:

* The Anthropic Claude models family (v1, v2)
* The AI21 Labs Jurassic 2 models family
* The Cohere Command and Cohere Command Light models
* The LLama2 family (v1, v2, v3)
* Hugging Face models

Limited support for some other models and endpoints is provided through configuration of a custom query template.


Azure OpenAI
-------------

The Azure OpenAI connection provides connection to Azure OpenAI text and image models. You will need:

* An Azure account with Azure OpenAI enabled
* A deployed Azure OpenAI service
* One or several Azure OpenAI model deployments
* An Azure OpenAI API key

You will need to declare each Azure OpenAI model deployment, as well as the underlying model that is being deployed (for the purpose of cost computation).

Text completion, chat completion, image generation and text embedding models are supported.

As of October 2023, Azure OpenAI Terms and Conditions indicate that Azure will not retain your data for enhancing its models.

For Azure OpenAI connections made through an `APIM gateway <https://azure.microsoft.com/en-us/products/api-management>`_, there are two available options:

1. Custom headers can be provided in the Azure OpenAI connection, e.g. to set an APIM subscription key
2. For more complex APIM setups, the Azure OpenAI APIM Custom LLM plugin is available on demand through the Dataiku plugin store, e.g. for setting custom OAuth scopes, and dynamic correlation IDs


Azure LLM
---------

The Azure LLM connection provides connectivity for models deployed with Azure Machine Learning (also known as Azure ML or Azure AI | Machine Learning Studio) or Azure AI Studio.

You will need:

* An Azure account with Azure ML or Azure AI Studio enabled
* If using Azure AI Studio, a deployment on a serverless endpoint
* If using Azure ML, a serverless endpoint
* In both cases, the Key provided by Azure

You will need to declare each Azure ML Endpoint or Azure AI Studio Deployment, with the Target URI as provided by Azure.

The serverless endpoints should conform to the `Open AI v1 API Reference <https://platform.openai.com/docs/api-reference>`_. `Chat <https://platform.openai.com/docs/api-reference/chat>`_ and `Embbeddings <https://platform.openai.com/docs/api-reference/embeddings>`_ endpoints are supported.


Cohere
-------

The Cohere connection provides connection to Cohere text models. You will need a Cohere API key.

The command and command-light models are supported.


Databricks Mosaic AI (previously MosaicML)
------------------------------------------

The Databricks Mosaic AI connection provides connection to Databricks Foundation Model APIs. You will need an existing Databricks Model Deployment connection.

The supported models are:

* BGE Large En (text embedding)
* DBRX Instruct
* Llama3.1 (70B, 405B)
* Mixtral 8x7B

.. note::

    MosaicML Inference has been retired by MosaicML, and therefore the MosaicML connection has been removed in DSS 12.6.

    Databricks Mosaic AI connections should be used as a replacement.


Google Vertex Generative AI
---------------------------

The Google Vertex LLM connection provides connection to Vertex PaLM text models. You will need:

* a service account key, or OAuth credentials
* at least the Vertex AI Service Agent role

The Chat Bison and Gemini Pro models are supported.

Image generation Imagen 3 and Imagen 3 Fast models are also supported.


Mistral AI
----------

The Mistral AI connection provides connection to Mistral AI text models. You will need a Mistral AI API key.

The supported models are:

* Mistral 7B
* Mistral 8x7B
* Mistral Small
* Mistral Large
* Mistral Embed


OpenAI
-------

The OpenAI connection provides connection to OpenAI text models (GPT 4o, O1, O3, GPT 3.5 Turbo, GPT 4) and the image generation model DALL·E 3. You will need an OpenAI API key (not to be confused with a ChatGPT account). You can select which OpenAI models are allowed.

The OpenAI connection supports text completion, image generation and embedding.


Snowflake Cortex
----------------

The Snowflake Cortex connection provides connection to some Snowflake Cortex text models. You will need an existing Snowflake connection.

The following chat models are supported:

* Gemma 7B
* Llama2 70B
* Mistral 7B
* Mixtral 8x7B
* Mistral Large
* Snowflake Arctic


Stability AI
------------

The Stability AI connection provides connection to image generation models. You will need a Stability AI API key.

The following image generation models are supported:

* Stable Image Core
* Stable Diffusion 3.0 Large
* Stable Diffusion 3.0 Large Turbo
* Stable Image Ultra


Locally-running HuggingFace models
====================================

See :doc:`huggingface-models`
