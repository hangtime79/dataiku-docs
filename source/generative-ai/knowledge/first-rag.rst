Embedding & searching datasets
##############################

Your first RAG using a dataset:
===============================

* In your project, select the dataset that will be used as your corpus. It needs to have at least one column of text
* Create a new Embed Dataset recipe
* Give a name to your knowledge bank
* Select the embedding model to use
* In the settings of the Embed Dataset recipe, select the column of text

    * (Optional) select one or several **metadata columns**. These columns will be displayed in the **Sources** section of the answer
    * (Optional) configure :doc:`Document-Level Security </generative-ai/knowledge/document-level-security>` by selecting the column containing your security tokens

* Run the Embed Dataset recipe
* Open the Knowledge Bank
* Define a Retrieval-Augmented LLM
    
    * Select the underlying LLM that will be queried
    * (Optional) tune the advanced settings for the search in the vector store
    * (Optional) configure :doc:`Document-Level Security </generative-ai/knowledge/document-level-security>` to control access to documents based on end-user permissions
    
* Click the **Test in Prompt Studio** button for your new Retrieval-Augmented LLM

    * This will automatically open Prompt Studio and create a new prompt for you, with your Retrieval-Augmented LLM pre-selected

* Ask your question
* You will now receive an answer that feeds on info gathered from your corpus dataset, with **Sources** indicating how this answer was generated


"Embed dataset" Update methods
===============================


There are four different methods that you can choose for updating your vector store.

You can select the update method in the embed dataset recipe settings.

.. csv-table::
    :header: "Method", "Description"
    :widths: 20, 80

    "**Smart sync**", "Synchronizes the vector store to match the input dataset, smartly deciding which rows to add/remove/update."
    "**Upsert**", "Adds and updates the rows from the input dataset into the vector store. Smartly avoids adding duplicate rows. Does not delete any existing records that are not present in the input dataset."
    "**Overwrite**", "Deletes the existing vector store, and recreates it from scratch, using the input dataset."
    "**Append**", "Adds the rows from the input dataset into the vector store, without deleting existing records. Can result in duplicate records in the vector store."

The two smart update methods, **Smart sync** and **Upsert**, require a **Document unique ID** parameter.
This is the ID of the document before any chunking has been applied.
This ID is used to avoid adding duplicate records and to smartly compute the minimum number of add/remove/update operations needed.

.. tip::
	If your dataset changes frequently, and you need to frequently re-run your embed dataset recipe, choosing one of the smart update methods, **Smart sync** or **Upsert**, will be much more efficient than **Overwrite** or **Append**.

	The smart update methods make fewer calls to the embedding model, and thus lowering the cost of running the embedding recipe repeatedly.

.. warning::
	When using one of the smart update methods, **Smart sync** or **Upsert**, all write operations on the vector store must be performed through DSS.
	This also means that you cannot provide a vector store that already contains data, when using one of the smart update methods.

Document-Level Security
=======================

:doc:`Document-level security </generative-ai/knowledge/document-level-security>` is a data governance feature that enables granular access control over documents within a collection or knowledge bank. It ensures that when a user performs a search or query, the results only include documents that the user is explicitly authorized to view.

To enable document-level security in your Embed Dataset recipe:

* Navigate to Advanced Settings,
* Under Document-Level Security, select the column containing your security tokens

To enable document-level security in your RAG model:

* In the RAG model, select 'Enforce document-level security',
* Provide the end-user security tokens at query time
