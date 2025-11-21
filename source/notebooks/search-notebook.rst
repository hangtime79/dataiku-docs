Search notebook
###############

The Search notebook is an interactive environment to perform search queries leveraging the native search capabilities of Elasticsearch.

A Search notebook is attached to a single Elasticsearch connection of DSS. It allows searching into one or multiple Elasticsearch indices or datasets.

The search query is based on the `Elasticsearch query_string <https://www.elastic.co/guide/en/elasticsearch/reference/8.4/query-dsl-query-string-query.html>`_ syntax.

Creating a Search notebook
==========================

You can create a Search notebook from the "Notebooks" tab of your project. Select "Search" among the new notebook options and then select an Elasticsearch connection.

.. note::

    Only connections compatible with ES dialect v7 and higher are supported.

You can then configure the search scope of the first query.

Queries and search scope
========================

A Search notebook is made of several queries that can be rerun at any time. Each query has its own search scope that must be configured when adding a new query. The search scope of an existing query can be edited at any time.

The search scope can be based on *indices*, an *index pattern* or *datasets*.

Indices-based search scope
~~~~~~~~~~~~~~~~~~~~~~~~~~

DSS fetches all existing indices or aliases for the configured Elasticsearch connection. Select items from this list to configure the search scope of the current query.

.. warning::

    Elasticsearch might raise an error if the string describing the scope of the search contains too many items. This limit is set by the `http.max_initial_line_length <https://www.elastic.co/guide/en/elasticsearch/reference/8.4/modules-network.html#http-settings>`_ parameter. To search in a large volume of items, prefer configuring the scope using an index pattern.

Index-pattern-based search scope
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enter a comma-separated list of indices or aliases to search. The pattern supports wildcards (``*``). To learn more about the syntax, please refer to `Multi-target syntax <https://www.elastic.co/guide/en/elasticsearch/reference/8.4/api-conventions.html#api-multi-index>`_.

The pattern is resolved by Elasticsearch each time the query is executed.

Datasets-based search scope
~~~~~~~~~~~~~~~~~~~~~~~~~~~

DSS fetches all existing datasets for the configured Elasticsearch connection. By default, DSS searches for datasets in the current project only but you can ask to load all projects you have access.

.. note::

    The Search notebook does not allow explicit selection of partitions.
    Selecting specific partitions can be done either by:

    * editing the search scope for indices-based partitioned dataset
    * adding a filter in the search query for field-based partitioned datasets

.. note::

    The custom DSL that might be configured to prefilter an existing dataset will be ignored. DSS displays a message for each affected dataset. Use the dataset :ref:`Search<Search view>` tab if you want the custom DSL to be applied.

DSS resolves the underlying indices or aliases for all selected datasets when the notebook is loaded. To include changes from the index name setting of one of the selected datasets, you need to reload the page.

Exporting a search query to a dataset
=====================================

From a search query in a Search notebook, you can create a dataset so that you can apply further DSS recipes downstream on the Flow.
DSS creates the resulting dataset with the following settings:

* The index name is set to match the search scope of the query
* The search query is applied using the custom DSL
