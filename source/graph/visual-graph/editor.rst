Visual Graph Editor
####################

Overview
---------

Visual Graph **Editor** is a Dataiku webapp designed to streamline the workflow for data scientists working with graph data.

It facilitates the rapid exploration of data relationships and the iterative development of graph schemas to address specific analytical requirements.

.. image:: img/visual-graph-editor.png

.. note::
    
    We recommend that you **get started** by following this `tutorial <https://knowledge.dataiku.com/latest/ml-analytics/visual-graphs/tutorial-visual-graph.html>`_.

**Key features**

-  | **Data sampling**
   | Adjust the sampling of the source datasets to manage data volume during schema design and testing.
-  | **Schema management**
   | Create and manage node and edge groups.
-  | **Visual exploration**
   | Visualize graphs and interactively expand nodes to see their neighbors and explore relationships. Select any node/edge to inspect its properties.
-  | **Interactive querying**
   | Write and execute Cypher queries with results rendered dynamically as a graph or in a tabular format.
-  | **Query generator**
   | Generate complex queries using an LLM-powered assistant.
-  | **Saved queries**
   | Save and manage frequently used Cypher queries for reuse.
-  | **Save configuration**
   | Save graph configurations at key milestones.
-  | **Publish Saved configuration**
   | Publish saved configurations to the project Flow to be used by other components of the plugin.

**Technical considerations**

-  | **Multi-directed property graph**
   | **Visual Graph** is designed to efficiently handle **multi-directed property graphs**, a versatile graph model where edges can have multiple directions between the same pair of nodes and carry detailed properties.
   | This flexibility allows for richer data representation, making it ideal for use cases such as social networks, knowledge graphs, and complex relational data.
   | Each node and edge in the graph can store key-value properties, enabling expressive queries and advanced analytics.
   | For a deeper understanding of **property graphs**, refer to the `Property Graph Model <https://en.wikipedia.org/wiki/Graph_database#Property_graph_model>`_, and for more on **directed multigraphs**, see `Multigraphs and Directed Graphs <https://en.wikipedia.org/wiki/Multigraph>`_.

-  | **Data type inference**
   | **Visual Graph** automatically assigns data types to node and edge properties based on the data types of the corresponding columns in the tabular dataset.
   | This ensures consistency between the source data and the resulting graph structure.

.. note::

    Ensuring the correct data types is crucial for expected behavior in analytical operations such as aggregations. Proper type inference guarantees that numerical operations like summation, averaging, and sorting function correctly.
    Check out the `Dataiku documentation <https://knowledge.dataiku.com/latest/data-sourcing/datasets/concept-dataset-characteristics.html#storage-type>`_ and the `Kùzu data type documentation <https://docs.kuzudb.com/cypher/data-types/>`_.

========================= ============================
Dataiku dataset Data Type Inferred Graph Property Type
========================= ============================
object                    STRING
string                    STRING
boolean                   BOOLEAN
date                      TIMESTAMP
tinyint                   INT8
smallint                  INT16
int                       INT32
bigint                    INT64
float                     FLOAT
double                    DOUBLE
========================= ============================

-  | **Scalability**
   | Kùzu is `pushing back the limit of scalability <https://docs.kuzudb.com/#performance-and-scalability>`_ for embedded graph databases.
   | It should help you scale to hundreds of millions of nodes with the appropriate RAM resources. Beyond this threshold or if you have extensive graph algorithms workloads, you may consider exporting data to Neo4j and leverage their infrastructure and technology.
-  | **Multi-user support**
   | All users with access to the webapp can see all the configured graphs and saved queries, including the ones created by other users. They can also freely update the configuration and saved queries. This will impact all the other users.
   | The only aspect that is not shared between users is the graph and table views. Users can explore and execute their queries and see the results independently from each other.
   | In case of concurrent update to the graph configuration, the users will be warned and we will prevent further update to the configuration to prevent loss of work.

Settings
--------

.. note::

    Not configuring optional settings will simply disable the associated feature.


**Node/Edge Sources**
    * **Source Datasets for Nodes & Edges**: select one or multiple datasets that contain the source data for nodes and edges. The same dataset can be used for both nodes and edges.

**Internal Datasets**
    * **Internal Storage Dataset**: select or create the dataset persisting the internal state of the webapp. While any type of underlying storage (FileSystem, S3, SQL,...) is supported, a SQL-based dataset is recommended.
    * **Saved Configuration Dataset (Optional)**: select or create the dataset that will contain your saved configurations. It is used as the source of saved configurations that can be published.
    * **Connection for Publishing Graphs  (Optional)**: select the connection where the published graph databases will be stored. This connection is used by the Editor to automatically create a Dataiku Folder containing the published graphs.

**AI Assistant**
    * **LLM Connection (Optional)**: select a LLM connection to enable the AI-powered Query generator. It helps users construct complex Cypher queries using natural language.
    * **LLM History Dataset (Optional)**: select the dataset storing the history of all questions asked by users in the Query generator. It can be used for auditing or analysis.

**Advanced Settings**
    * **Cypher Query Timeout (seconds)**: set a maximum execution time for queries run within the Editor. This acts as a guardrail to prevent resource-intensive queries from impacting performance.
    * **Log Level**: configure the verbosity of the logs. Select **INFO** for standard operational logging (recommended for production) or **DEBUG** for detailed diagnostic information while troubleshooting issues.

Visual Graph Editor Interface
------------------------------

Landing Page
~~~~~~~~~~~~

It lists all the created graphs. You can also create new graphs from there.

Graph Page
~~~~~~~~~~

Schema section
*********************

The **Schema** section on the left panel allows you to define the structure of your graph by creating node and edge groups.

Node group definition
======================

- **Select dataset**: Select the dataset containing the nodes information.
- **Filter data** (Optional): If the source dataset contains records for multiple node types, use **Filter data** to specify the conditions for including a record in this specific group.
- **Select column with unique identifiers**: Select the column that serves as the unique identifier (i.e., primary key) for each node.
- **Select column with names**: Select the column whose values will be used as the display name for the nodes. You can re-use the identifier column if a dedicated name column is not available.
- **Node properties** (Optional): Select any additional columns from the source dataset to be included as properties for each node.

- **+ Add additional definition** (Optional): If the data for a node group is distributed across multiple datasets, click **+ Add additional definition**. This allows you to map another data source to the same node group by repeating the configuration process.

- **Customize** (Optional): Customize the visual representation of nodes within the graph visualization, by setting a color, icon or size.

Edge group definition
======================

- **Select source node group**: Select the source (origin) node group for the edge.
- **Select target node group**: Select the target (destination) node group for the edge.

.. note::

	A node group can be both the source and target, which is useful for defining edges between nodes of the same type.

- **Select dataset**: Select the dataset containing the edges information.
- **Filter data** (Optional): If the source dataset contains records for multiple edge types, use **Filter data** button to specify the conditions for including a record in this specific group.
- **Select column with source identifiers**: Select the column containing the unique identifiers (i.e., primary key) of the source nodes.
- **Select column with target identifiers**: Select the column containing the unique identifiers (i.e., primary key) of the target nodes.
- **Select additional properties** (Optional): Select any additional columns from the source dataset to be included as properties for each edge.

- **+ Add additional definition** (Optional): If the data for an edge group is distributed across multiple datasets, click **+ Add additional definition**. This allows you to map another data source to the same edge group by repeating the configuration process.

- **Customize** (Optional): Customize the visual representation of edges within the graph visualization, by setting a color or size.

Sampling section
*********************

To manage performance and ensure rapid iteration during schema development, the Editor builds the graph using a sample of your source data by default.

**Sampling Method**
    * **Head**: Builds the graph using the first N rows of each source dataset. This is the default setting.
    * **Random**: Builds the graph using N randomly selected rows from each source dataset.

**Sample Size**
    * Adjust the number of rows (N) to be included from each dataset. Increasing this value provides a more comprehensive view of your data at the cost of longer processing times.

**Disable Sampling**
    * Disable sampling entirely to build the graph using the full contents of your source datasets.

.. warning::
   Disabling sampling is not recommended during the iterative design phase. Processing the entire content of source datasets can be time-consuming and may significantly slow down schema exploration and validation, especially with large data volumes.

Saved configurations section
******************************************

This section allows you to manage different versions of your graph configuration. You can **create** and **publish** current configurations whenever you reach a significant milestone in your design process.

.. image:: img/visual-graph-flow-publish.png

Graph exploration
*******************

-  | **Interactive graph exploration**
   | Select any node or edge to inspect its details, including its identifier, name, properties and neighbors.
   | The **Neighbors** tab provides an overview of all directly connected nodes, displaying the total neighbor count and a breakdown by node group.
   | You can also selectively expand all neighbors or only those belonging to a specific group to explore the graph's structure interactively.
-  | **View controls and statistics**
   | The left panel provides controls for managing the graph visualization.
   | **Group visibility**: For each node and edge group, you can toggle its visibility on or off to show or hide all elements of that group in the current view.
   | **Graph statistics**: Key metrics are also displayed. 
   | **View count**: Shows the total number of nodes and edges per group currently displayed as a result of the last executed query.
   | **Total count**: Shows the total number of nodes and edges in the underlying graph database, based on your sampling configuration.
-  | **Cypher query execution**
   | The bottom panel contains a Cypher query editor with smart autocompletion that adapts to your defined schema.
   | Executing a query returns results in either a visual graph or a table format.
   | Aggregation queries results are available in the table format.
   | Any query you find useful can be saved to the **Saved queries** tab for reuse or sharing with team members.
-  | **Query generator**
   | The **Query generator** tab allows you to ask a question in natural language.
   | It will generate a corresponding Cypher query designed to answer your question. You can then save the generated query or ask another question.
-  | **Saved queries**
   | Save and manage frequently used Cypher queries for reuse.

Next topics
------------
**For Business Users**: Configure an :doc:`Explorer <./explorer>` webapp using this graph for interactive exploration and discovery.

**For Data Scientists**: Perform advanced analytics and feature engineering at scale using the :doc:`Execute Cypher <./recipes>` and :doc:`Compute PageRank <./recipes>` recipes.

**For AI applications**: Utilize the graph as a dynamic knowledge source for Retrieval-Augmented Generation (RAG) with the :doc:`Graph Search <./agent-tool>`  Agent Tool.
