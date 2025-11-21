Document-Level Security
#######################

Document-Level Security enables granular access control over documents within a knowledge bank. It ensures that when a user performs a search or query, the results only include documents that user is authorized to view.

This feature matches permissions attached to individual documents with permissions granted to individual users.

Security Tokens
===============

The mechanism for document-level security relies on **security tokens**.

* **Definition**: Security tokens are arrays of strings used to tag both documents and users.
* **On Documents**: A document's security tokens represent the permissions required to access it. A common implementation is to use the names of user groups that are allowed to view the document (e.g., ``["legal-department", "executives"]``).
* **On Users**: A user's security tokens represent the permissions they possess. This is typically the list of groups they belong to.

Access is granted if a user's list of security tokens and a document's list of security tokens have at least one token in common (i.e. the intersection of the two lists is non-empty). You can see an example in the implementation section below.

Implementation
==============

The Embed Document recipe, Embed Dataset recipe, Knowledge Bank Search tool, and LLM Mesh caller (for example, your own application or Dataiku :doc:`Chat UIs </generative-ai/chat-ui/index>`) can work together to provide document-level security. 

For a step-by-step guide, see `this tutorial <https://knowledge.dataiku.com/latest/gen-ai/rag/tutorial-manage-rag-access.html>`_ on the knowledge base. 

Enabling document-level security typically involves three stages:

1. **Tag Documents/Dataset with Security Tokens**: Before your documents/dataset are embedded, you must add a metadata table for your documents or a dedicated column to your dataset. This must contain the **security tokens** for each document, which define its access permissions. These tokens are typically formatted as a JSON array of strings (e.g., ``["administrators", "legal_dept"]``).
2. **Configure Indexing**: Next, you must configure the embedding process to recognize the security tokens. This is done within the settings of either the :doc:`Embed Dataset </generative-ai/knowledge/first-rag>` or the :doc:`Embed Documents </generative-ai/knowledge/documents>` recipes. In the recipe, you specify which column contains the security tokens, ensuring they are indexed alongside the document content in the knowledge bank.
3. **Filter During Retrieval**: Finally, when a user makes a query, their security tokens must be passed along with it. This is handled by the calling application, such as the :doc:`Knowledge Bank Search tool </agents/tools/knowledge-bank-search>`, inside a :doc:`RAG Model </generative-ai/knowledge/first-rag>` or a custom RAG application using the LLM Mesh. Dataiku filters results by comparing the user's tokens against the indexed tokens of each document. A document is only returned if there is at least one match. If no security tokens are provided with the query, the search will return no results, preventing unauthorized data access.

:doc:`Agent Hub </agents/agent-hub>` and :doc:`Agent Connect </generative-ai/chat-ui/agent-connect>` pass user information via the completion context in the following format, here the ``administrators`` group matches the document's security token we set earlier:

.. code-block:: json

   {
     "context": {
       "callerSecurityTokens": [
         "administrators",               // list of user groups
         "dss_group:administrators",     // group names prefixed with "dss_group:"
         "dss_user_login:admin",         // user login
         "dss_user_emailaddress:admin@localhost" // user email address
       ]
     }
   }

.. important::  

   You must make sure to pass tokens of the *final* end-user, not the technical user simply calling the agent or tool.