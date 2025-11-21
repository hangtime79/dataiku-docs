Image variables
################

Image variables are supported for training a tabular model in Visual ML with the Python backend. In order to leverage images, make sure they are stored in a :doc:`Managed Folder </connecting/managed_folders>`. Your training dataset should contain a column that indicates the path of each image within that managed folder.

Image variables are also usable for deep learning models. See :doc:`deep learning image features<../deep-learning/images>` for more information.

Image handling
==============

Image embedding
------------------

Image embedding creates semantically meaningful vector representation of images.

In DSS, this image handling method makes use of image embedding models from the :doc:`LLM Mesh </generative-ai/index>`. Each image is passed to the selected model, the outputs are then pooled to an embedding vector with a fixed size (specific to the model).

The supported models are:

* timm models using the `timm <https://huggingface.co/timm/>`_ library. To select a timm model you need access to a :doc:`Local HuggingFace connection </generative-ai/huggingface-models>` with image embeddings models enabled. |br|
  The configuration of the connection exposing the model is applied (caching, auditing, …).
* Google Vertex AI multimodal embedding. You need access to a Vertex Generative AI connection with a multimodal model enabled.
* AWS Titan Embeddings G1 - Multimodal. You need access to a Bedrock connection with a multimodal model enabled.

.. warning::
    Image embedding feature handling using local (Hugging Face) image embedding models is not supported on the API node.

Missing values
==============

Options for handling missing values in an image feature:

- **Drop rows** discards rows with missing values from the model building. This means dropping them from the training, and not predicting these rows when scoring. *Avoid discarding rows, unless missing data is extremely rare*.
- **Fail if missing values found** fails training (and scoring) when the image paths is either missing or does not correspond to an image file in the managed folder.
- **Impute** replaces missing values with empty embeddings (zeros).  This should be used for *randomly missing* data due to random noise or incomplete data. You can also use this if the trained model should support scoring rows without any image.
