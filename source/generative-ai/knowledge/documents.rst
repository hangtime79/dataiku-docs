Embedding and searching documents
##################################

In addition to the traditional embedding of text and storage in Vector Stores, Dataiku can also work directly with unstructured documents.

The "Embed documents" recipe takes a managed folder of documents as input and outputs a Knowledge Bank that can directly be used to query the content of these documents.

To get started with document embedding, see our `Tutorial: Build a multimodal knowledge bank for a RAG project <https://knowledge.dataiku.com/latest/ml-analytics/gen-ai/tutorial-multimodal-embedding.html#tutorial-build-a-multimodal-knowledge-bank-for-a-rag-project>`_.

Supported document types
==========================

The "Embed documents" recipe supports the following file types:

* PDF
* PPTX/PPT
* DOCX/DOC
* ODT/ODP
* TXT
* MD (Markdown)
* PNG
* JPG/JPEG
* HTML

Text Extraction vs. VLM extraction
===================================

The "Embed documents" recipe supports two ways of handling documents.

Text extraction
----------------

The simplest one is Text Extraction, it extracts text from documents and uses headers when available to divide the content into meaningful extraction units.

Supported file formats are PDF, DOCX, PPTX, HTML, TXT, MD (and PNG, JPEG, JPG with OCR enabled).

The extraction runs as follow:

* The text content is extracted from the document.
* If headers are available, they are used to divide the content into meaningful units.
* The extracted text is split into chunks if necessary to fit the embedding model.
* The chunks are embedded.

Text can also be extracted from images with the Optical Character Recognition (OCR) image handling mode. You can either choose EasyOCR or Tesseract as OCR engines. 
EasyOCR does not require any configuration but is slow when running on CPU. Tesseract requires some configuration, see :ref:`ocr-setup` below.
Enabling OCR is recommended on scanned documents.

.. note::

   This feature requires internet access for PDF document extraction. The models that need to be downloaded are layout models available from Hugging Face. The runtime environment will need to have access to the internet at least at the beginning so that those models can be downloaded and placed in the huggingface cache.

   If your instance does not have external internet access then you can download those models manually. Here are the steps to follow:

   * Go to the `model repository <https://huggingface.co/ds4sd/docling-models/tree/v2.2.0>`_ and clone the repository (on the v2.2.0 revision)
   * Create a "ds4sd\-\-docling-models" repository in the resources folder of the document extraction code environment (or the code env you chose for the recipe), under: `/code_env_resources_folder/document_extraction_models/ds4sd\-\-docling-models`
   * The folder "ds4sd\-\-docling-models", should contain the same tree structure as https://huggingface.co/ds4sd/docling-models/tree/v2.2.0/

   If the models are not in this ressources folder, then the huggingface cache will be checked and if the cache is empty, the models will be downloaded and placed in the huggingface cache. 


.. note::

   You can edit the run configuration of the text extraction engine in the **Administration** > **Settings** > **Other** > **LLM Mesh** > **Configuration** > **Embed documents recipes**. 

VLM extraction
--------------

For complex documents, Dataiku implements another strategy based on Vision LLMs (VLM), i.e. LLMs that can take images as input. If your LLM Mesh is connected to one of these (see :doc:`/generative-ai/multimodal` for a list), you can instead use the VLM strategy.

* Instead of extracting the text, the recipe transforms each page of the document into images.
* Ranges of images are sent to the VLM, asking for a summary.
* The summary of each range of images is embedded.

At query time, when asking a text question:

* Using the embedding of the question, the relevant ranges are retrieved
* The matching images are directly passed in the context of the VLM
* The VLM then directly uses the images to answer

The advanced image understanding capabilities of the VLM allow for much more relevant answers than just using extracted text.

The "Embed Documents" recipe supports VLM strategy for DOCX/DOC, PPTX/PPT, PDF, ODT/ODP, JPG/JPEG and PNG files.

When creating the "Embed Documents" recipe, in addition to the knowledge bank, a managed folder with the images extracted from your documents is created as output of the recipe.

Initial setup
==============

* Document Extraction is automatically preinstalled when using Dataiku Cloud Stacks or Dataiku Cloud. If you are using Dataiku Custom, before using the VLM extraction, you need a server administrator with elevated (sudoers) privileges to run:

.. code-block:: bash

	sudo -i "/home/dataiku/dataiku-dss-VERSION/scripts/install/install-deps.sh" -with-libreoffice


* Text extraction on DOCX/PDF/PPTX requires to install and enable a dedicated code environment (see :doc:`/code-envs/index`):
   In **Administration** > **Code envs** > **Internal envs setup**, in the `Document extraction code environment` section, select a Python version from the list and click `Create code environment`.

.. _ocr-setup:

OCR setup
=========

When using the OCR mode of the text extraction, you can choose between EasyOCR and Tesseract. The AUTO mode will first use Tesseract if installed, else will use EasyOCR.

Tesseract
---------

Tesseract is preinstalled on Dataiku Cloud and Dataiku Cloud Stacks. If you are using Dataiku Custom, Tesseract needs to be installed on the system. Dataiku uses the `tesserocr` python package as a wrapper around the `tesseract-ocr` API. It requires `libtesseract (>=3.04` and `libleptonica (>=1.71)`.

The English language and the OSD files must be installed. Additional languages can be downloaded and added to the `tessdata` repository. Here is the `list <https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html>`_  of supported languages. 

For example on Ubuntu/Debian:

.. code-block:: bash

   sudo apt-get install tesseract-ocr tesseract-ocr-eng libtesseract-dev libleptonica-dev pkg-config

On AlmaLinux:

.. code-block:: bash

   sudo dnf install tesseract
   curl -L -o /usr/share/tesseract/tessdata/osd.traineddata https://github.com/tesseract-ocr/tessdata/raw/4.1.0/osd.traineddata
   chmod 0644 /usr/share/tesseract/tessdata/osd.traineddata

At runtime, Tesseract relies on the `TESSDATA_PREFIX` environment variable to locate the `tessdata` folder. This folder should contain the language files and config. You can either:

* Set the `TESSDATA_PREFIX` environment variable (must end with a slash `/`). It should point to the `tessdata` folder of the instance.
* Leave it unset. During the `Document Extraction internal code env` resources initialization, DSS will look for possible locations of the folder, copy it to the resources folder of the code env, then set the `TESSDATA_PREFIX` accordingly.

.. note::

   If run in a container execution configuration, DSS handles the installation of Tesseract during the build of the image.


EasyOCR
--------------

EasyOCR does not require any additional configuration. But it's very slow if run on CPU. We recommend using an execution environment with GPU. 


.. note::
   By default EasyOCR will try to download missing language files. Any of the `supported languages <https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html>`_ can be added in the UI of the recipe.
   If your instance does not have access to the internet, then all requested language models need to be directly accessible. 
   DSS expects to find the language files in the resources folder of the code environment: `/code_env_resources_folder/document_extraction_models/EasyOCR/model`. 
   You can retrieve the language files (`*.pth`) from `here <https://www.jaided.ai/easyocr/modelhub/>`_ 


"Embed documents" Update methods
================================

There are four different methods that you can choose for updating your vector store and its associated folder (used for VLM extraction).

You can select the update method in the embed document recipe output settings.

.. csv-table::
    :header: "Method", "Description"
    :widths: 20, 80

    "**Smart sync**", "Synchronizes the vector store to match the input folder documents, smartly deciding which documents to add/update or remove."
    "**Upsert**", "Adds and updates the documents from the input folder into the vector store. Smartly avoids adding duplicate documents. Does not delete any existing document that is no-longer present in the input folder."
    "**Overwrite**", "Deletes the existing vector store, and recreates it from scratch, using the input folder documents."
    "**Append**", "Adds the documents from the input folder into the vector store, without deleting or updating any existing records. Can result in duplicated records in the vector store."

Documents are identified by their path in the input folder. Renaming or moving around documents will prevent smart modes from matching them with any pre-existing
documents and can result in outdated or duplicated versions of documents in the vector store.

The update method also manages the output folder of the recipe to ensure its content synchronisation with the vector store.  Non-managed deletions
in the output folder is not recommended and can cause the vector store to point to a missing source.

.. tip::
	If your folder changes frequently, and you need to frequently re-run your embed document recipe, choosing one of the smart update methods, **Smart sync** or **Upsert**, will be much more efficient than **Overwrite** or **Append**.

	The smart update methods minimize the number of documents to be re-extracted and the calls to the embedding model, thus lowering the cost of running the recipe repeatedly.

.. warning::
	When using one of the smart update methods, **Smart sync** or **Upsert**, all write operations on the vector store must be performed through DSS.
	This also means that you cannot provide a vector store that already contains data, when using one of the smart update methods.

Metadata dataset
================

You can add a metadata dataset in the "Embed documents" recipe to:

* match recipe rules on a subset of documents based on their custom properties,
* propagate those custom properties into the knowledge bank allowing to filter search results later,
* use :doc:`Document-level security </generative-ai/knowledge/document-level-security>`

In the metadata dataset each row corresponds to a document of your folder, with:

* a column specifying the document path in your folder's root,
* (optional) a security column listing the security tokens to access the document's extracted content (:doc:`Document-level security </generative-ai/knowledge/document-level-security>`),
* (optional) other metadata columns, for rules matching in this recipe or filtering later in the resulting KB.