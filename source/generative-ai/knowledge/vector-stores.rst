Working with Vector stores
###########################

Vector store types
======================

Out of the box, Knowledge Banks are created with a Vector Store called **Chroma**. This does not require any setup, and provides good performance even for quite large corpus.

As an alternative, other no-setup Vector Stores are available: Qdrant and FAISS.

For more advanced use cases, you may wish to use a dedicated Vector Store. Dataiku supports several third-party vector stores that require you to set up a dedicated connection beforehand:

* Azure AI search
* Elasticsearch
* OpenSearch, including `AWS OpenSearch services <../connecting/elasticsearch.html#amazon-opensearch-service>`_ (both managed cluster & serverless)
* Pinecone
* Vertex Vector Search (based on a Google Cloud Storage Connection)

When creating the Embedding recipe, select the desired vector store type, then select your connection.
You can also change the vector store type later, by editing the settings of the Knowledge Bank.

For Azure AI Search, Vertex Vector Search, Elasticsearch and OpenSearch, we provide a default index name that you can update if needed. For Pinecone, make sure to provide an existing index name.

.. note::
	When setting up an Elasticsearch, an OpenSearch or a Google Cloud Storage connection, you must allow the connection to be used with Knowledge Banks. There is a setting in the connection panel to allow this.


Limitations
------------

* Rebuilding a Pinecone-based Knowledge Bank may require that you manually delete and recreate the Pinecone index.
* You need an Elasticsearch version >=7.14.0 to store a Knowledge Bank.
* Elasticsearch >=8.0.0 and <8.8.0 supports only embeddings of size smaller than 1024. Embedding models generating larger embedding vectors will not work.
* Only Private key authentication is supported for Google Cloud Storage connections used for Knowledge bank usage.
* Smart update methods (**Smart sync** and **Upsert**) are not supported on the following vector store types: Pinecone, AWS OpenSearch serverless.
* Note that, after running the embedding recipe, remote vector stores might take some time to update their indexing data in their respective user interfaces.
