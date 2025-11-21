Multimodal capabilities
########################

The LLM Mesh provides multimodal capabilities to handle:

* Image inputs. Images can be mixed with text in LLM queries, in order to answer queries like "please describe what is in this image"
* Image outputs. The LLM Mesh can generate images.

Image input
============

Supported models
-----------------

Multimodal input with images is supported with the following providers:

* OpenAI (GPT-4o)
* Azure OpenAI (GPT-4o)
* Vertex Gemini Pro
* Bedrock Claude 3
* Bedrock Claude 3.5
* Local HuggingFace models

API
---

Image input is available in the LLM Mesh API.

For more details, please see :doc:`devguide:concepts-and-examples/llm-mesh`

Answers
--------

Image input is available in :doc:`the Chat UIs <chat-ui/index>`

Image output
=============

Supported models
----------------

Image generation is supported with the following providers:

* OpenAI (DALL-E 3)
* Azure OpenAI (DALL-E 3)
* Google Vertex (Imagen 3 and Imagen 3 Fast)
* Stability AI
* Bedrock Titan Image Generator 
* Bedrock Stability AI models
* Local HuggingFace models

Image-to-image support
----------------------

Bedrock Amazon Titan Image Generator G1 supports image-to-image with the following image edition modes:

* Image-to-image with prompt
* Image-to-image without prompt
* Image-to-image inpainting

    * Black mask mode

Bedrock Stability AI SDXL 1.0 also supports image-to-image with the following image edition modes:

* Image-to-image with prompt
* Image-to-image inpainting

    * Black mask mode
    * Transparent original image mode

Stability AI Stable Diffusion 3 Large supports image-to-image mode with prompt.

The Stability AI connection also supports `CONTROLNET_SKETCH` and `CONTROLNET_STRUCTURE` image edition modes.

API
---

Image output is available through the LLM Mesh API.
Note that some parameters are not supported by all providers / models.

For more details, please see :doc:`devguide:concepts-and-examples/llm-mesh`