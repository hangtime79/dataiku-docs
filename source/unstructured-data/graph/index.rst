Graph
########

Graph data structure natively represents relationships between data. The two main parts of a graph are:

- Vertices (or nodes) that represent objects and their properties

- Edges (or connections) that represent links between two vertices

Some of the key benefits are:

- **Enhanced Data Relationships & Insights**

  - Unlike traditional tabular data analysis, graph analytics enables users to explore intricate relationships between data points, providing a holistic view of connections and dependencies.

- **Identify unusual connections**

  - Graph analytics is particularly effective in identifying fraudulent activities by detecting unusual patterns, anomalies, and suspicious connections in financial transactions, cybersecurity, and compliance monitoring.

- **Faster query processing**

  - Graph analytics fundamentally changes the way relationships are queried and analyzed. By eliminating the need for expensive join operations and enabling high-speed relationship traversal, graph databases significantly outperform relational databases for complex, connected data.

Overview
--------

.. toctree::
    :maxdepth: 2

    visual-graph-plugin/index
    neo4j-plugin

The following table lists available plugins that you can use to work on graph data structures.

.. csv-table::
   :header: "Plugin", "Description", "Support tier"
   :widths: 60, 120, 40

    "`Visual Graph plugin <https://www.dataiku.com/product/plugins/visual-graph/>`_", "A set of Webapps, recipes and Agent Tool to collaboratively build & leverage graphs.", "`Tier 2 support </troubleshooting/support-tiers>`_"
    "`Graph analytics plugin <https://www.dataiku.com/dss/plugins/info/graph-analytics.html>`_", "Analyze and visualize graph data using in-memory tools.", "`Not supported </troubleshooting/support-tiers>`_"
    "`Neo4j plugin <https://www.dataiku.com/product/plugins/neo4j/>`_", "Read and write from/to the Neo4j graph database.", "`Not supported </troubleshooting/support-tiers>`_"