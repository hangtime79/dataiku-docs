Advanced Search
################

At its core, searching documents that are relevant in a Knowledge Bank (in order to perform RAG) is information retrieval.

While embedding text (also sometimes called "Semantic Search") is a modern way of doing this, other information retrieval and options exist.

These options can be configured:

* In the Augmented LLM settings
* When creating a Vector Search Query Tool in an agent

Diversity of documents
======================

If enabled, use the `MMR algorithm <https://www.cs.cmu.edu/~jgc/publication/The_Use_MMR_Diversity_Based_LTMIR_1998.pdf>`_ to improve the diversity of the documents retrieved. Not supported by Azure AI Search.

* **Diversity selection documents**: The total number of documents pre-selected before selecting the more diverse final documents.
* **Diversity vs Relevancy factor**: 0 to 1, trade off between diversity vs relevance of results. Lower favors more diverse documents.


Hybrid Search
=============

Combines both similarity search (default behaviour) and keyword search to retrieve more relevant documents. Only supported by Azure AI Search and Elasticsearch; and not compatible with the diversity option.

Additionally, both vector store offer advanced reranking capabilities, to enhance the mix of documents retrieved. Each has its own specific configuration. This advanced reranking requires a compatible subscription with these providers.

.. csv-table::
    :header: "Vector Store", "Advanced Reranking"
    :widths: 30, 70

    "**Azure AI search**", "Uses Azure AI proprietary `Semantic Ranker <https://learn.microsoft.com/en-us/azure/search/semantic-search-overview>`_."
    "**Elasticsearch**", "Uses advanced reranking leveraging `RRF (Reciprocal Ranking Fusion) <https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html>`_.
    This accepts two parameters: **Rank constant** and **Rank window size**"