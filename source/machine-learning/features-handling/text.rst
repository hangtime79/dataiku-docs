Text variables
###############

The **Text handling** and **Missing values** methods, and their related controls, specify how a text variable is handled.

Text handling
=================
* **Count vectorization**
* **TF/IDF vectorization**
* **Hashing trick** (producing sparse matrices)
* **Hashing trick + Truncated SVD** (producing smaller dense matrices for algorithms that do not support sparse matrices)
* :ref:`Text embedding` (Python training backend only)
    * :ref:`From the code environment resources <ml-text-feature-codeenv-resources-models>`
    * :ref:`From the LLM Mesh <ml-text-feature-llm-mesh-models>`

For the specific case of deep learning, see :doc:`text features in deep-learning models </machine-learning/deep-learning/text>`

.. _Text embedding:

Text embedding
------------------

Text embedding creates semantically meaningful dense matrix representations of text.
In DSS, this text handling method makes use of API-based models through the :doc:`LLM Mesh</generative-ai/llm-connections>` or local transformer models using the `transformers <https://huggingface.co/transformers/>`_ and `sentence-transformers <https://www.sbert.net/>`_ libraries.
Each text sample is passed through the selected model. The outputs are then pooled to an embedding with a model-specific fixed size. For local transformer models, the computations can be configured to use a GPU.
You can either choose models downloaded to the code environment resources or models from the :doc:`LLM Mesh </generative-ai/index>`.

.. _ml-text-feature-codeenv-resources-models:

Using models from the code environment resources
------------------------------------------------

When using text embedding in Visual ML, the selected environment in the runtime environment requires the ``sentence-transformers`` python package to be installed.
You can install all necessary packages by adding the "Visual Machine Learning with Sentence Embedding" package set, in the code-environment “Packages to install” tab.

Text embedding also requires models to be downloaded. This can be done via the :ref:`managed code environment resources directory <code-env-resources-directory>`.

See below for an example code environment resources initialization script.

.. code-block:: python

    ######################## Base imports #################################
    import logging
    import os
    import shutil

    from dataiku.code_env_resources import clear_all_env_vars
    from dataiku.code_env_resources import grant_permissions
    from dataiku.code_env_resources import set_env_path
    from dataiku.code_env_resources import set_env_var
    from dataiku.code_env_resources import update_models_meta

    # Set-up logging
    logging.basicConfig()
    logger = logging.getLogger("code_env_resources")
    logger.setLevel(logging.INFO)

    # Clear all environment variables defined by a previously run script
    clear_all_env_vars()

    ######################## Sentence Transformers #################################
    # Set sentence_transformers cache directory
    set_env_path("SENTENCE_TRANSFORMERS_HOME", "sentence_transformers")

    import sentence_transformers

    # Download pretrained models
    MODELS_REPO_AND_REVISION = [
        ("DataikuNLP/average_word_embeddings_glove.6B.300d", "52d892b217016f53b6c717839bf62c746a658933"),
        ("DataikuNLP/TinyBERT_General_4L_312D", "33ec5b27fcd40369ff402c779baffe219f5360fe"),
        ("DataikuNLP/paraphrase-multilingual-MiniLM-L12-v2", "4f806dbc260d6ce3d6aed0cbf875f668cc1b5480"),
        # Add other models you wish to download and make available as shown below (removing the # to uncomment):
        # ("bert-base-uncased", "b96743c503420c0858ad23fca994e670844c6c05"),
    ]

    sentence_transformers_cache_dir = os.getenv("SENTENCE_TRANSFORMERS_HOME")
    for (model_repo, revision) in MODELS_REPO_AND_REVISION:
        logger.info("Loading pretrained SentenceTransformer model: {}".format(model_repo))
        model_path = os.path.join(sentence_transformers_cache_dir, model_repo.replace("/", "_"))

        # Uncomment below to overwrite (force re-download of) all existing models
        # if os.path.exists(model_path):
        #     logger.warning("Removing model: {}".format(model_path))
        #     shutil.rmtree(model_path)

        # This also skips same models with a different revision
        if not os.path.exists(model_path):
            model_path_tmp = sentence_transformers.util.snapshot_download(
                repo_id=model_repo,
                revision=revision,
                cache_dir=sentence_transformers_cache_dir,
                library_name="sentence-transformers",
                library_version=sentence_transformers.__version__,
                ignore_files=["flax_model.msgpack", "rust_model.ot", "tf_model.h5",],
            )
            os.rename(model_path_tmp, model_path)
        else:
            logger.info("Model already downloaded, skipping")
    # Add text embedding models to the code-envs models meta-data
    # (ensure that they are properly displayed in the feature handling)
    update_models_meta()
    # Grant everyone read access to pretrained models in sentence_transformers/ folder
    # (by default, sentence transformers makes them only readable by the owner)
    grant_permissions(sentence_transformers_cache_dir)

.. _ml-text-feature-llm-mesh-models:

Using models from the LLM Mesh
------------------------------

You can also select text embeddings extraction models enabled from the :ref:`LLM connections <embedding_llms>`.

When selecting models from the LLM Mesh, the configuration of the connection exposing the model is applied (caching, auditing, …).

.. warning::
    Models from the LLM Mesh are not supported on the API node.

Missing values
==============

For text features except Text embedding, DSS supports treating missing values as empty strings. Missing values for Text embedding handling are imputed with empty embeddings (zeros).
