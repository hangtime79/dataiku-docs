Cassandra
###################

.. warning::

	**Tier 2 support**: Connection to Cassandra is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

Requirements
===============

Data Science Studio can connect to clusters running Cassandra version 2.0.1 and later.
With additional restrictions, it can also connect to clusters running Cassandra version 1.2.

Cassandra clusters are accessed using CQL3 native transport (Cassandra binary protocol). Make sure that the native transport service is enabled on the Cassandra servers, and that the network port for this service is accessible from the Data Science Studio server. In particular the following configuration directives in the ``cassandra.yaml`` Cassandra configuration file may have to be adjusted:

+------------------------+--------------------------------------------------------------------------------------------+
|          Name          |                                        Description                                         |
+========================+============================================================================================+
| start_native_transport | Should be configured to true for native transport service to be enabled.                   |
+------------------------+--------------------------------------------------------------------------------------------+
| native_transport_port  | TCP port on which the Cassandra server listens for native transport queries. Default: 9042 |
+------------------------+--------------------------------------------------------------------------------------------+
| rpc_address            | IP address on which the Cassandra server listens for native transport queries,             |
|                        | or 0.0.0.0 to listen on all interfaces.                                                    |
|                        | Note that the default is localhost, which forbids remote access to this service.           |
+------------------------+--------------------------------------------------------------------------------------------+

Configuring Cassandra cluster connections
============================================
Accessing datasets stored on a Cassandra cluster first requires the definition of a connection to this cluster.


The following configuration parameters are available:

+-------------------+--------------------------------------------------------------------------------------------+
|        Name       |                                        Description                                         |
+===================+============================================================================================+
| Hosts             | Comma-separated list of Cassandra nodes to which to connect (names or addresses).          |
|                   | Note that it is not necessary to configure the entire list of Cassandra nodes here, as the |
|                   | driver will dynamically discover the full cluster topology                                 |
|                   | from the contact host once connected.It is mandatory to configure at least one             |
|                   | contact host.                                                                              |
|                   |                                                                                            |
|                   | It is usually better to configure more than one however,                                   |
|                   | so that the cluster can still be connected to when one of the configured hosts is down.    |
+-------------------+--------------------------------------------------------------------------------------------+
| Keyspace          | Cassandra keyspace in which to look for tables.                                            |
|                   |                                                                                            |
|                   | Mandatory The corresponding keyspace should exist on the cluster.                          |
+-------------------+--------------------------------------------------------------------------------------------+
| Port              | TCP port on which the Cassandra servers listen for native transport queries.               |
|                   | Optional, defaults to 9042                                                                 |
+-------------------+--------------------------------------------------------------------------------------------+
| User and          | Optional authentication credentials to use when connecting to the cluster.                 |
| password          | These parameters should be configured if the Cassandra cluster                             |
|                   | authenticates clients with the PasswordAuthenticator authenticator.                        |
+-------------------+--------------------------------------------------------------------------------------------+
| Protocol version  | Optional native protocol version to use when contacting the Cassandra cluster.             |
|                   |                                                                                            |
|                   | It is usually not necessary to configure this field, as the driver                         |
|                   | will by default auto-detect the protocol version as part of                                |
|                   | the connection (first attempting to connect with protocol version 2,                       |
|                   | then falling back to protocol version 1).                                                  |
|                   |                                                                                            |
|                   | It may be necessary to force it in certain configurations,                                 |
|                   | for example when connecting to a mixed cluster, or to avoid spurious warnings.             |
+-------------------+--------------------------------------------------------------------------------------------+
| Read timeout (ms) | Defines how long Data Science Studio waits for a given Cassandra                           |
|                   | node to answer a query before retrying it to another node.                                 |
|                   |                                                                                            |
|                   | Default value is 12000 ms (i.e. 12 seconds).                                               |
|                   | May need to be adjusted depending on the performance characteristics of the cluster.       |
+-------------------+--------------------------------------------------------------------------------------------+
| Use SSL           | Check this option to connect to the cluster using client-to-node encryption.               |
+-------------------+--------------------------------------------------------------------------------------------+

Configuring Cassandra datasets
================================

Data Science Studio managed datasets
---------------------------------------

Data Science Studio can store and retrieve datasets in a Cassandra cluster, with very few constraints, in tables that it directly manages.

These "managed" datasets are normally created with default parameters as part of the definition of a new data processing recipe, to store the output of this recipe. If necessary, their configuration can be further tuned using the dataset Settings configuration screen.

A non-partitioned dataset is stored as a single Cassandra table in the corresponding connection keyspace. This table has a schema modeled after the dataset schema, plus one additional column ``_dssId`` holding a unique timeuuid timestamp for each row and acting as the Cassandra partitioning key. The Data Science Studio dataset is thus represented using one Cassandra row per dataset record, and is naturally spread over the entire cluster.

A partitioned Data Science Studio dataset can be stored in Cassandra if it has exactly one partitioning dimension. It is then represented as a single Cassandra table, with a schema modeled after the dataset schema plus two additional columns:

* a ``_dssSpread`` column holding a random integer value in a configurable range (partition spread factor), acting as the Cassandra partition key along with the Data Science Studio partition column.
* a ``_dssId`` column holding a unique timeuuid timestamp for each row, acting as the Cassandra clustering key.

As a consequence, each Data Science Studio partition for this dataset is stored in a fixed, configurable number of Cassandra rows, so that partitions can be individually stored, enumerated and deleted in an efficient way by the Cassandra cluster.

External datasets
---------------------

Data Science Studio can read or write datasets in externally-managed tables, with some restrictions inherent to the query capabilities in CQL.

To configure such an "external" dataset, the underlying Cassandra table should have already been created. The dataset configuration dialog will then read the table schema, suggest a dataset schema suitable for it, and optionally prefetch and display a few rows from the table in order to help with the dataset configuration.

The dataset schema can be adjusted with the schema editor within the following type compatibility constraints:

+----------------------+------------------------------------------------+
|    Cassandra type    |                    DSS type                    |
+======================+================================================+
| ascii, text, varchar | string                                         |
+----------------------+------------------------------------------------+
| boolean              | boolean                                        |
+----------------------+------------------------------------------------+
| int                  | Integer                                        |
+----------------------+------------------------------------------------+
| bigint, counter      | Long int                                       |
+----------------------+------------------------------------------------+
| float                | Float                                          |
+----------------------+------------------------------------------------+
| double               | Double                                         |
+----------------------+------------------------------------------------+
| timestamp            | Date                                           |
+----------------------+------------------------------------------------+
| list, set            | String (JSON array)                            |
+----------------------+------------------------------------------------+
| map                  | String (JSON object)                           |
+----------------------+------------------------------------------------+
| decimal, varint      | String                                         |
+----------------------+------------------------------------------------+
| uuid, timeuuid, inet | String                                         |
+----------------------+------------------------------------------------+
| blob                 | Cassandra columns with these types are ignored |
| Custom type          |                                                |
+----------------------+------------------------------------------------+

External datasets can be optionally partitioned along one of their columns.

.. note::
	See below for Cassandra indexing constraints applicable to partitioned external datasets.

Dataset configuration parameters
===================================

The following table summarizes the configurable parameters for a Cassandra dataset:

+---------------------------+---------------+------------------------------------------------------------------+
|            Name           | Applicability |                           Description                            |
+===========================+===============+==================================================================+
| Connection                | Mandatory     | DSS connection to the cluster                                    |
+---------------------------+---------------+------------------------------------------------------------------+
| Table                     | Mandatory     | Name of the cassandra table holding the dataset,                 |
|                           |               | in the connection keyspace                                       |
+---------------------------+---------------+------------------------------------------------------------------+
| Partitioned               |               | Check for a partitioned dataset                                  |
+---------------------------+---------------+------------------------------------------------------------------+
| Partition colum           | Partitioned   | Name of the partitioning column in the dataset schema.           |
|                           | dataset       |                                                                  |
+---------------------------+---------------+------------------------------------------------------------------+
| Partition type            | Partitioned   | Whether the partitioning dimension represents a                  |
|                           | dataset       | time range or discrete values                                    |
+---------------------------+---------------+------------------------------------------------------------------+
| Range                     | Partitioned   | Time range of the partitioning                                   |
|                           | dataset       |                                                                  |
+---------------------------+---------------+------------------------------------------------------------------+
| Partition spread factor   | Managed       | Number of Cassandra rows on which to store each DSS partition.   |
|                           | partitioned   |                                                                  |
|                           |               | Defaults to 1. If this value is changed while                    |
|                           |               | the dataset is not empty, existing partitions should be rebuilt. |
+---------------------------+---------------+------------------------------------------------------------------+
| Delete before wirte       | Non managed,  | Uncheck this box if the Cassandra server cannot                  |
|                           | partitioned   | implement the deletion of a partition contents                   |
|                           |               | (see Restrictions below).                                        |
|                           |               |                                                                  |
|                           |               | Note that in this mode, rebuilding a partition                   |
|                           |               | will rewrite new contents without prior deletion,                |
|                           |               | which may lead to stale rows being leftover                      |
|                           |               | from the previous build.                                         |
+---------------------------+---------------+------------------------------------------------------------------+
| Forced list of partitions | Managed       | Specify the full list of partitions for this dataset.            |
|                           |               |                                                                  |
|                           | (optional)    | Use when it is not possible (because of Cassandra                |
|                           |               | query language limitations) or too expensive                     |
|                           |               | to obtain by querying the Cassandra table.                       |
|                           |               |                                                                  |
|                           |               | Can be specified using partition range spec syntax.              |
+---------------------------+---------------+------------------------------------------------------------------+
| Fetch size                | Optional      | Controls the number of results to retrieve from the server       |
|                           |               | per individual query when enumerating tables or partitions.      |
|                           |               |                                                                  |
|                           |               | Default (5000) should be suited to most deployment. It may       |
|                           |               | be necessary to reduce it if the Cassandra server cannot         |
|                           |               | reliably deliver this number of results within the configured    |
|                           |               | query timeout.                                                   |
+---------------------------+---------------+------------------------------------------------------------------+

Dataset and table schemas
============================

The dataset configuration dialog automatically checks that the Cassandra table exists and has a schema compatible with
the Data Science Studio schema.

Additionally, it initializes the dataset schema from the table if the dataset schema is empty. It is always possible to override the suggested schema using the Schema editor in the "Schema" tab, within the type compatibility constraints described above.

Columns are matched by name and not by order between Data Science Studio datasets and Cassandra tables.

.. warning::

	This matching is always CASE-SENSITIVE.

Matching columns between a dataset and its Cassandra table must be of compatible types.

Cassandra collection types are seen as JSON strings within Data Science Studio.

Restrictions and caveats
==========================

Writing to external datasets
-----------------------------

When writing to external datasets, partitioned or not, be sure to have unique sets of values for the columns which form the Cassandra primary index for the table, in order to ensure that the successively written records do not overwrite each others.

If this is not the case, consider adding a unique id column to your dataset with a Data Science Studio data preparation recipe, and include this column in the Cassandra table primary key.

Enumerating a previously-written external dataset may return records in a different order, as Cassandra enumeration order is always driven by the values in the primary key columns.

.. note::

	This issue does not apply to managed datasets, as Data Science Studio always adds a hidden _dssId column containing a strictly increasing value for each row.

External partitioned datasets
------------------------------

When working with partitioned datasets, Data Science Studio needs to be able to enumerate individual partitions (on input), and overwrite them (on output). Additionally, it optionally needs to enumerate the list of partitions, and to count the number of records in each partition.

Combined with current Cassandra indexing capabilities, the following data modeling scenarios are possible, with a number of pros and cons:

* The DSS partition column is the unique Cassandra partition key for the table. In this mode:

	* Each dataset partition is stored as a single Cassandra row
	* All dataset operations are available and nominally efficient

* The DSS partition column is the first Cassandra clustering key for the table. In this mode:

	* Dataset partitions are spread over potentially many Cassandra rows, depending on the data distribution of the chosen Cassandra partitioning key
	* Deleting partition contents is not possible (on output)
	* Enumerating the list of partitions is not possible (an explicit partition list must be configured)
	* Enumerating a given partition (on input) requires a filtering query, since the Cassandra cluster cannot know which row(s) contain the given partition. This may or may not lead to performance problems, depending on the data distribution.

* The DSS partition column corresponds to a Cassandra column with a secondary index. In this mode:

	* Dataset partitions are spread over potentially many Cassandra rows, depending on the data distribution of the chosen Cassandra partitioning key
	* Deleting partition contents is not possible (on output)
	* Enumerating the list of partitions is not possible (an explicit partition list must be configured)
	* Enumerating a given partition (on input) is technically possible but at the time of writing (Cassandra 2.0.8) a huge performance bug in secondary-index-driven table enumeration makes it not practical but for small datasets. It is expected that this bug will be fixed in a further version of the Cassandra server.

.. warning::

	Secondary-index-based partition enumeration may incur very serious performance overheads, and may adversely load your cluster. Be sure to test before using in production.

.. note::

	This issue does not apply to partitioned managed datasets, as Data Science Studio generates the Cassandra table as follows:

	+-------------------------+---------------------+
	|   partitionColumnName   | partitionColumnType |
	+=========================+=====================+
	| ``_dssSpread``          | ``int``             |
	+-------------------------+---------------------+
	| ``_dssId``              | ``timeuuid``        |
	+-------------------------+---------------------+
	| <other dataset columns> |                     |
	+-------------------------+---------------------+

	Primary key: ``((partitionColumnName, _dssSpread), _dssId)``

 	This ensures that each partition is stored on a controlled number of Cassandra row, one per distinct value of _dssSpread.

Cassandra v1.2 compatibility
------------------------------

Data Science Studio may connect to Cassandra v1.2 clusters with the additional restrictions:

* It is never possible to enumerate partitions in a dataset, managed or external (no support for SELECT DISTINCT queries)
* Table and partition enumerations are performed through a series of queries to the server (no server support for result set pagination), which incurs a performance overhead.
* Writing to datasets requires one server round-trip per record (no support for batches of prepared queries), which incurs a performance overhead.
* Each connection to the cluster generates warning messages in the Data Science Studio log, as part of the protocol negotiation. These messages are harmless and can be ignored. They can be suppressed by forcing version 1 protocol in the connection definition dialog.
