Elasticsearch and OpenSearch
############################

Data Science Studio can both read and write datasets on Elasticsearch versions
5.0 to 8.14.

Please note that support for Elasticsearch 1.x and 2.x is now deprecated and
will be removed in a future release.

Opensearch is also supported for versions
1.0 to 2.15: 
it uses the Elasticsearch connection type and provides the same features.

.. contents::
	:local:

Define an Elasticsearch connection
==================================

* Go to Administration > Connections
* Click the "New connection" button and pick Elasticsearch
* Enter a name for the new connection, and the required connection parameters,
  then test and save the new connection

.. note::

  The port parameter should be Elasticsearch's HTTP API port (9200 by default),
  not the Java API port.

.. note::

  The minimum privileges for DSS to be able to use Elasticsearch are the following (Elasticsearch v7+ example):

  * ``monitor`` at the ``cluster`` level to read version information
  * ``read``, ``view_index_metadata``, ``monitor`` on ``indices`` to check mapping and underlying aliases for datasets
  * ``create`` and ``manage`` on ``indices`` to write managed datasets


Managed Elasticsearch datasets
==============================

If you allow DSS to write :ref:`managed dataset <managed-datasets>` into the
Elasticsearch connection, you can use this connection to create output datasets
for recipes.

Creating such a dataset creates a new index on your Elasticsearch server with
the name of the dataset by default. For Elasticsearch 6 and below, a mapping type
is also created with the name of the dataset by default. For example, if your
Elasticsearch server is hosted on ``localhost:9200``, a managed dataset named
``Articles`` stores its data into ``localhost:9200/articles/articles``.
For Elasticsearch 7 and above, it will be stored into  ``localhost:9200/articles``.
This name will not change if you rename the dataset in case you are relying on
its presence, so if you rename the dataset and want those names to remain similar,
you should edit the index and type names after renaming the dataset,
then rebuild it and manually delete the previous index.

.. warning::

  For Elasticsearch 6 and below, you should not create other types in the index
  that are managed by DSS, they might be deleted or altered.

By default, fields get the default Elasticsearch mapping, e.g. string are
analyzed and indexed (mapped to ``text`` in Elasticsearch 5+). If you want
access to a non-analyzed version (mapped to ``keyword`` in Elasticsearch 5+) of
some or all of your columns, you can list those columns (comma-separated, or
``*`` for all string columns) in the dataset settings. You can also specify your
own complete `mapping
<https://www.elastic.co/guide/en/elasticsearch/reference/8.4/mapping.html>`_.

If your dataset is :doc:`partitioned </partitions/index>`, then one index per
partition is created (prefixed by the index name) and the index name is
actually an `Elasticsearch alias
<https://www.elastic.co/guide/en/elasticsearch/reference/8.4/aliases.html>`_
that points to all the partition's indices. You can still search or delete from
the alias normally.

If you want the index to have non-default settings, you can use an `index template
<https://www.elastic.co/guide/en/elasticsearch/reference/8.4/index-templates.html>`_ before
building the managed dataset for the first time.

External Elasticsearch datasets
===============================

You can also import existing data from Elasticsearch into DSS. Simply create
an Elasticsearch dataset and specify the index of the data (and the type name
for Elasticsearch 6 and below). If the connection is writable, DSS can also
overwrite that data, but the type mapping will not be modified by DSS and the
index/type will not be created if they don't already exist.

Your index may be an alias if it's only used for reading, or for writing if it
only points to one index (otherwise Elasticsearch refuses the write operation).

Partitioning
------------

You can partition your external dataset in DSS. The partitioning model can either be field-based or indices-based.

.. note::

  The **field-based** model is similar to the **column-based** model and the **indices-based** model is similar to the **files-based** model.
  See :doc:`/partitions/index` for more details.

Field-based
~~~~~~~~~~~

Simply specify the partitioning column and the type of partitioning (value or time-based).
You can only partition on one column for external datasets.

.. note::

  The partitioning column must have `fielddata
  <https://www.elastic.co/guide/en/elasticsearch/reference/8.4/text.html#fielddata-mapping-param>`_
  enabled, which is the case by default for ``keyword`` fields in Elasticsearch 5+
  but not for ``text``.

Indices-based
~~~~~~~~~~~~~

.. warning:: Support for indices-based partitioning is experimental

Specify a partitioning format that will match all the indices you want to import.
This string will overwrite the index name value.
For each dimension, the pattern must contain a specifier that will be replaced by a wildcard when matching existing indices.
DSS will capture the value from each matching index name to set the value of the dimension corresponding to the specifier.
This field supports wildcards (``*``).

.. note:: See :doc:`/partitions/fs_datasets` for more details.

.. _Search view:

Search view
============================

On Elasticsearch datasets, an additionnal "Search" tab is available in the dataset view. From there you can:

* Write & perform search queries based on the `Elasticsearch query_string <https://www.elastic.co/guide/en/elasticsearch/reference/8.4/query-dsl-query-string-query.html>`_ syntax
* Use a set of visual filters, range conditions or wildcards, to build advanced queries
* Persist your query on the current dataset for later reuse
* Deploy your query to the Flow as a filter recipe (see :doc:`../other_recipes/sampling`)

.. note::

  The search applies to the whole dataset. Sample settings that may be defined on the other tabs do not impact the search results


In the following example, the query string will be replaced and sent to Elastisearch

.. code::

  GET /_search
  {
    "query": {
      "query_string": {
        "query": "${Your search query}",
      }
    }
  }

This fully functional search view can be exposed on a DSS dashboard. See :ref:`Dataset table tile display<Dataset table tile display>` for more details.

By default, DSS will retrieve the exact number of hits when executing the search. The query sent to Elasticsearch enables the `track_total_hits <https://www.elastic.co/guide/en/elasticsearch/reference/8.4/search-your-data.html#track-total-hits>`_ parameter. This behavior may be disabled by adding the custom property ``dku.connection.elasticsearch.interactiveSearch.exactTotalHits`` set to ``false`` in the connection settings. The count returned when searching will then be capped depending on the Elasticsearch configuration (10000 hits by default, see `index.max_result_window <https://www.elastic.co/guide/en/elasticsearch/reference/8.4/index-modules.html#dynamic-index-settings>`_ for more details).

Limitations:

- This feature is only available for Elasticsearch versions with a dialect compatible with 7.x
- Since results are not batched, DSS uses the `from field <https://www.elastic.co/guide/en/elasticsearch/reference/8.4/search-search.html#search-search-api-request-body>`_ property to paginate & display results.
- Thus, this may lead to some duplicate rows if some data have been appended to the Elasticsearch index while scrolling.
- Highlighting service is handled by Elasticsearch on text fields. So, date or ip type fields are not supported by the highlighter. Also, depending on the tokenization, some parts of a word may not be highlighted. DSS does not apply any further control.

Amazon OpenSearch Service
=========================

AWS provides two services for managing OpenSearch instances:

- `OpenSearch Managed Clusters <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html>`_, which deploys a regular OpenSearch cluster.
- `OpenSearch Serverless <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html>`_, that offers a serverless, on-demand service at the cost of some limitations listed below.

.. note::

  When setting up your connection, set the port to ``443`` and check ``Enable HTTPS``. When using an AWS authentication type, make sure to you select the correct ``service`` for your connection. 


Limitations of OpenSearch Serverless
------------------------------------

- You must select an AWS authentication type on your connection (OpenSearch Managed Clusters support all authentications types).
- DSS needs to wait for the new indexed rows to become available for search, which can delay the end of a job. Concurrent write operations are not supported.
- Listing indices used by an alias requires a ``*`` (to trigger a pattern match) at the end of the alias. This is mostly useful in Search notebooks or for non-managed datasets.
