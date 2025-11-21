Multimodal capabilities
***********************

Multimodal capabilities refer to a language model's (LLM) ability to simultaneously process
and understand various input types, such as text, images, audio, and video.
Initially, these models were focused solely on text, meaning that some could not process any other medium.
To utilize the multimodal capabilities of an LLM,
it is necessary to use a model trained explicitly on that type of data.
Additionally, some LLMs specialize in specific tasks and may be unable to handle others.
Therefore, verifying whether the LLM you choose can perform the required processing before you start coding your tasks is essential.

If you need to find some information about the capacity of an LLM,
you can use the :meth:`~dataikuapi.dss.project.DSSProject.list_llms` function,
as shown in :ref:`Code 1<tutorials_genai_multimodal_code>`:

.. code-block:: python
    :name: tutorials_genai_multimodal_code
    :caption: Code 1: finding information about the available LLMs

    import dataiku
    import pprint

    client = dataiku.api_client()
    project = client.get_default_project()
    llm_list = project.list_llms(purpose="IMAGE_GENERATION")

    for llm in llm_list:
        pprint.pp(llm)

The tutorial :doc:`./images-and-text/images-generation/index` focuses on image generation using a prompt.
Therefore, you only need a model capable of generating an image using a prompt.

The tutorial :doc:`/tutorials/genai/multimodal/images-and-text/images-captioning/index` uses an image as an input
and a prompt to modify the image. So, you will need an LLM that supports ImageInputs and is prompt-driven.



.. toctree::
    :hidden:
    :maxdepth: 1

    Images Generation<./images-and-text/images-generation/index>
    Images Captioning<./images-and-text/images-captioning/index>