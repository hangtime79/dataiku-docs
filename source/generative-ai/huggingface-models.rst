Running Hugging Face models
###########################

.. contents::
	:local:

The LLM Mesh supports locally-running Hugging Face transformers models, such as Mistral, Llama3, Phi, or smaller task-specific models.

Cautions
========

Running local large scale Hugging Face models is a complex and very costly setup, and both quality and performance tend to be below proprietary LLM APIs. We strongly recommend that you make your first experiments in the domain of LLMs using :doc:`hosted LLM APIs <llm-connections>`. The vast majority of LLM API providers have strong guarantees as to not reusing your data for training their models.

Pre-requisites
===============

In order to run local Hugging Face models, you will need:

* A running Elastic AI Kubernetes cluster with NVIDIA GPUs

    * Smaller models, such as Falcon-7B or Llama2-7B, work with an ``A10`` GPU with 24 GB of VRAM. Single-GPU nodes are recommended.

    * Larger models require multi-GPU nodes. For instance, Mixtral-8x7B or Llama2-70B work with 2 ``A100`` GPUs with 80 GB of VRAM each.

    * Large image generation models such as FLUX.1-schnell require GPUs with 40 GB of VRAM. Local image generation LLM Mesh models do not benefit from multi-GPU setups or quantization.

* GPUs `compute capability level <https://developer.nvidia.com/cuda-gpus>`_ must be >= 7.0 and NVIDIA driver version `compatible <https://docs.nvidia.com/deploy/cuda-compatibility>`_ with CUDA 12.8
* A fully setup Elastic AI computation capability, with Almalinux 9 base images (i.e. by adding ``--distrib almalinux9`` when building images)
* Python 3.11 setup


.. note::

	The base images and Python 3.11 requirements are automatically fulfilled when using Dataiku Cloud Stacks, you do not need additional setup for container images, as long as you have not customized base images.

	If you require assistance with the cluster setup, please reach out to your Dataiku Technical Account Manager or Customer Success Manager

.. note::

	For air-gapped instances, you will need to import the Hugging Face model manually to DSS's model cache and enable DSS's model cache in the Hugging Face connection. See below.

Create a containerized execution config
----------------------------------------

* Create a new containerized execution config.

* In "custom limits", add `nvidia.com/gpu` with value `1`.

    * If you are using multi-GPU nodes, you can set a higher value. In any case, it is strongly recommended to use a number of GPUs among `1`, `2`, `4`, or `8` in order to maximize compatibility with vLLM's tensor parallelism constraints.

* Enable "Increase shared memory size", without setting a specific value

Do not set memory or CPU requests or limits. Anyway, each node will only accommodate a single container, since the GPU is not shared.

Create a code env
------------------

* In "Administration > Code envs > Internal envs setup", in the "Local Hugging Face models code environment" section, select a Python interpreter in the list and click "Create code environment"
* Once your code env is created, go to the code env settings. In "Containerized execution", select "Build for": "All container configurations" (or select relevant, e.g. GPU-enabled, container configurations).
* Click "Save and update" (this will take at least 10-20 minutes)

Create a Hugging Face connection
--------------------------------

* In "Administration > Connections", create a new "Local Hugging Face" connection
* Enter connection name
* In "Containerized execution configuration", enter the name of the containerized execution config you just created
* In "Code environment", select "Use internal code env"
* Create the connection

If you want to use Llama or Mistral models, you must have a Hugging Face account in which access to these models have been approved. Enter an access token.

We recommend disabling "Use DSS-managed model cache" if your containers have good outgoing Internet connectivity, as it will be faster to download the models directly from Hugging Face.

Configuring a text generation model
===================================

DSS provides presets for popular LLMs such as Llama, Mistral, and Phi. Advanced users can also add custom models by specifying their Hugging Face ID.

Model compatibility
-------------------

DSS leverages `vLLM <https://docs.vllm.ai/>`_, a high-performance inference engine optimized for running large-scale language models on NVIDIA GPUs. 

Before adding a custom model, ensure that the model meets the following requirements:

* The model needs to use the standard HuggingFace configuration format.

    For example, the model `mistralai/Pixtral-12B-2409 <https://huggingface.co/mistralai/Pixtral-12B-2409>`_ uses a Mistral-specific configuration format and is not supported. However, there exist repackaged versions of the same model in a compatible format, such as `mistral-community/pixtral-12b <https://huggingface.co/mistral-community/pixtral-12b>`_.

* The model architecture must be supported by the installed vLLM version.

	* The model architecture can be determined by looking at the model's ``config.json`` file. Refer to `the list of supported architectures <https://docs.vllm.ai/en/v0.9.0.1/models/supported_models.html>`_ in vLLM's documentation.
	
	* The installed vLLM version depends on the DSS version. It can be found in Administration > Code envs > Internal envs setup > Local Hugging Face models code environment > Currently installed packages.

* The model must be an instruct or chat model.

    For example, the model `mistralai/Mistral-Small-24B-Base-2501 <https://huggingface.co/mistralai/Mistral-Small-24B-Base-2501>`_ is a base model and cannot be used in DSS, whereas `mistralai/Mistral-Small-24B-Instruct-2501 <https://huggingface.co/mistralai/Mistral-Small-24B-Instruct-2501>`_ is an instruction-fine-tuned version and is compatible.

* The model weights must be packaged using Safetensors format (``*.safetensors``) or PyTorch bin format (``*.bin``).

    For example, the weights of `microsoft/phi-4 <https://huggingface.co/microsoft/phi-4/tree/main>`_ are provided in ``*.safetensors`` format, which is supported.

* Supported quantized models formats are AWQ, GPTQ, FP8 and BitsAndBytes. GGUF is not supported.

    For example, `Meta-Llama-3.1-405B-Instruct-AWQ-INT4 <https://huggingface.co/hugging-quants/Meta-Llama-3.1-405B-Instruct-AWQ-INT4>`_ is supported.

.. note::

	For text generation, the LLM mesh automatically selects the LLM inference engine. It uses `vLLM <https://docs.vllm.ai/>`_ by default if the model and runtime environment are compatible.  If not compatible, it falls back to `transformers <https://huggingface.co/transformers/>`_ as a best effort. Serving models with transformers leads to degraded performance and loss of capabilities. This legacy mode is deprecated and may be removed in future versions of DSS.

	You can manually override this default behavior in the Hugging Face connection settings (Advanced tuning > Custom properties). To do so, add a new property ``engine.completion`` and set its value to ``TRANSFORMERS``, ``VLLM`` or ``AUTO`` (default, recommended unless you experience issues with the automatic engine selection).

.. Caution::
    Structured/JSON output and tool calling are experimental features.

Determining GPU memory requirements
-----------------------------------

Serving a large language model requires a significant amount of GPU memory, which is used for:

* Model weights

	Memory usage of weights is determined by the number of parameters and the precision. An un-quantized 24B model at BF16 (16 bits, or 2 bytes) precision requires 24 x 2 = 48GB of VRAM. A FP8 quantized version reduces this to 24 x 1 = 24GB.

* KV cache

	The minimum memory requirement for the KV cache is proportional to the context length, but the exact relationship depends on the model. For example, Llama-3.1-8B requires at least 16GB of KV cache with the default context length (128k tokens). Reducing the context length from 128k to 32k tokens decreases the memory requirement from 16GB to 4GB. Set the context length in the model's "Max tokens" setting.

	It is recommended to provide substantially more GPU memory than the minimum requirements. This allows for processing multiple requests concurrently (batching), which can massively increase throughput.

* Other overheads

	Some additional memory is required for activations and various runtime overheads, which depends on the model and is typically higher for multimodal models.

To reduce memory requirements:

	* Use a pre-quantized model in compatible format (AWQ/GPTQ/FP8). Make sure the "Model quantization mode" setting is set to "None" when using a pre-quantized model.

	* Adjust the "Max tokens" setting to reduce memory usage if memory-constrained.


Test
====

Text generation
---------------

In a project, create a new Prompt Studio (from the green menu). Create a new single prompt. In the LLM dropdown, choose for example Phi-4, and click Run.

The model is downloaded, and a container starts, which requires pulling the image to the GPU machine. The first run can take 10-15 minutes (subsequent runs will be faster).

Image generation
----------------

The image generation capabilities are only available through the Dataiku DSS API. See the :doc:`Developer Guide <devguide:tutorials/genai/multimodal/images-and-text/images-generation/index>` for tutorials using this feature.

Image-to-image mode is not available using local HuggingFace models.


.. _hugging-face-model-cache:

The model cache
=================


DSS has its own (optional) managed cache to store models from HuggingFace.

If enabled at the connection level, the cache is automatically populated when using the :doc:`LLM Mesh<../generative-ai/huggingface-models>` with pre-trained models from HuggingFace.
Models are downloaded from `HuggingFace hub <HF_>`__.

.. _HF: https://huggingface.co/models

View the model cache content in: Administration > Settings > Misc. You can also delete, export or import models.

Import and export models
------------------------

If your DSS instance does not have access to HuggingFace (huggingface.co), you can manually import a model archive, typically one exported from the model cache of another DSS design or automation node with network access.

Build your own model archive to import
--------------------------------------

.. note::
    It is simpler (and recommended) to import a model that was previously exported by DSS
    when that is possible, instead of creating an archive manually.


If you want to manually create an archive it should contain the following structure:

- a root folder
    - a folder named "model" containing the HuggingFace model repo content
    - a file named "model_metadata.json"

To retrieve the ``model`` folder content from HuggingFace hub:

.. code-block:: bash

    git lfs install
    git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2


Example of a model archive content:

.. code-block:: md

    sentence-transformers_2fall-MiniLM-L6-v2 ← folder at the root (its name is not important)
    ├── model ← a folder named "model" containing the HuggingFace model repo content
    │   ├── 1_Pooling
    │   │   └── config.json
    │   ├── README.md
    │   ├── config.json
    │   ├── config_sentence_transformers.json
    │   ├── data_config.json
    │   ├── modules.json
    │   ├── pytorch_model.bin
    │   ├── sentence_bert_config.json
    │   ├── special_tokens_map.json
    │   ├── tokenizer.json
    │   ├── tokenizer_config.json
    │   ├── train_script.py
    │   └── vocab.txt
    └── model_metadata.json ← a file named "model_metadata.json"

The `model_metadata.json` file should have the following schema:

.. code-block::

    {
        "commitHash": "7dbbc90392e2f80f3d3c277d6e90027e55de9125",
        "downloadDate": 1698300636139,
        "downloadedBy": "admin",
        "lastDssUsage": 1699570884724,
        "lastModified": "2022-11-07T08:44:33.000Z",
        "lastUsedBy": "admin",
        "libraryName": "sentence-transformers",
        "modelDefinition": {
            "key": "hf@sentence-transformers/all-MiniLM-L6-v2"
        },
        "pipelineName": "sentence-similarity",
        "sizeInBytes": 91652688,
        "taggedLanguages": [
            "en"
        ],
        "tags": [
            "sentence-transformers",
            "pytorch",
            "tf",
            "rust",
            "bert",
            "feature-extraction",
            "sentence-similarity",
            "en",
            "dataset:s2orc",
            "dataset:flax-sentence-embeddings/stackexchange_xml",
            ...
            "arxiv:2104.08727",
            "arxiv:1704.05179",
            "arxiv:1810.09305",
            "license:apache-2.0",
            "endpoints_compatible",
            "has_space",
            "region:us"
        ],
        "url": "https://huggingface.co/sentence-transformers%2Fall-MiniLM-L6-v2/tree/main",
        "version": 0
    }


Most of these fields can be retrieved from the HuggingFace model repository.

The important ones are:

- `modelDefinition`:
    - `key`: consists of ``hf@<modelId>`` or ``hf@<modelId>@<revision>`` if a specific revision was used
- `version`: as of now should be `0`
- `url`: the url used to fetch the model

Access cache programmatically
-----------------------------

You can access models in the DSS-managed model cache programmatically using the following code:

.. code-block:: Python

    from dataiku.core.model_provider import get_model_from_cache
    model_path_in_cache = get_model_from_cache(model_name)

The Python code shown above will work both in a local execution and in a containerized execution. It expects the model to be
in the cache, it will not trigger its download to the cache.

To download a model from HuggingFace to the DSS-managed model cache programmatically, you can use the following code:

.. code-block:: Python

    from dataiku.core.model_provider import download_model_to_cache
    download_model_to_cache(model_name)

If the model is not already in the cache, this code downloads the model from HuggingFace and store it in the DSS-managed model cache. If the user running this code is not an administrator, the specified model must be enabled in a Hugging Face connection.

If the model requires a Hugging Face access token, you can provide a connection with a configured access token to use as an optional second argument:

.. code-block:: Python

    from dataiku.core.model_provider import download_model_to_cache
    download_model_to_cache(model_name, connection_name=your_connection)
