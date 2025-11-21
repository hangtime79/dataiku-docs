Knowledge Bank Search tool
###########################

This tool searches for relevant documents in a Knowledge Bank.

Importantly, this tool is a search/retrieval tool. It does not perform "Retrieval-Augmented Generation": it does not "generate an answer" but simply returns matching documents. Generating the answer is the responsibility of the calling agent.

Core configuration
==================

You configure the Knowledge Bank to use for the tool. For more information on how to build Knowledge Banks, see :doc:`documentation about Knowledge bank </generative-ai/knowledge/index>`.

Retrieval settings
====================

The tool supports a variety of search options, some depending on the underlying vector store of the Knowledge Bank. The Knowledge Bank Search tool has the same retrieval options as the builtin RAG. See :doc:`/generative-ai/knowledge/advanced-search` for details about the retrieval settings.

Sources
========

In order for the :doc:`Chat UIs </generative-ai/chat-ui/index>` or your own application to properly display documents, the tool returns rich source items, that can include a title, text, URL (for building a link to the document, for example in your Sharepoint site) and thumbnail URL (for displaying an image next to the result).

All of these are configured by optionally selecting which meta stored in the Knowledge Bank holds the information. Stored meta are configured in the embedding recipes.

Global filter
=============

The "Perform filtering" option allows the tool creator to define a filter that applies on the documents of the Knowledge Bank, in order for the tool to be restricted to a subset of the Knowledge Bank

.. _document-level-security:

Document-Level Security
=======================
:doc:`Document-Level Security </generative-ai/knowledge/document-level-security>` enables granular access control over documents within a knowledge bank. It ensures that when a user performs a search or query, the results only include documents that user is authorized to view.

To enable document-level security:

* A security token column must selected in the :doc:`Embedding recipe </generative-ai/knowledge/first-rag>` settings,
* In the Knowledge Bank Search Tool, select 'Enforce document-level security',
* Provide the end-user security tokens at query time

Passing security tokens to the tool is done via the "context" parameter, in a key called "callerSecurityTokens". Dataiku Chat UIs do this automatically along with :doc:`Agent Hub </agents/agent-hub>` and :doc:`Agent Connect </generative-ai/chat-ui/agent-connect>`. Importantly, you must make sure to pass tokens of the "final" end-user, not the technical user simply calling the agent or tool.