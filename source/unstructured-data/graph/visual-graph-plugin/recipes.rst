Recipes
#######

Execute Cypher recipe
---------------------

The **Execute Cypher** recipe allows you to run a query against a graph database stored in a Dataiku Folder and save the tabular results to a dataset.
This is useful for feature engineering, generating analytical reports, or exporting subsets of your graph.

Input / Output
~~~~~~~~~~~~~~

**Input**
    * Graph database folder: Dataiku Folder that contains your materialized graph database.
    
**Output**
    * Output dataset: Output dataset to store the results of the executed query.

Settings
~~~~~~~~

**Path to database file**

Select the specific database you wish to query from the dropdown list.

**Cypher query**

Enter the Cypher query to be executed.

Compute PageRank recipe
-----------------------

The **Compute PageRank** recipe calculates the PageRank centrality for nodes in your graph. `This algorithm <https://kuzudb.github.io/docs/extensions/algo/pagerank/>`_ is a common technique for identifying the most influential nodes based on the graph's structure.

To use this recipe, select **Compute PageRank** from the list of recipes under **Visual Graph**.

Input / Output
~~~~~~~~~~~~~~

**Input**
    * Graph database folder: Dataiku Folder that contains your materialized graph database.
    
**Output**
    * Output dataset: Output dataset to store the results of PageRank algorithm.

Settings
~~~~~~~~

**Path to database file**

Select the specific database you wish to run the PageRank algorithm on.

**Select node groups to rank**

Choose one or more node groups to include in the PageRank calculation. Only nodes from these groups will be ranked.

**Select edge groups used to rank nodes**

Select the edge groups that define the edges to be considered during the ranking process.

**Algorithm parameters**

    * **Damping factor**: The probability at each step that a random walker will continue following an outgoing edge. A typical value is 0.85.
    * **Max iterations**: The maximum number of iterations the algorithm will run.
    * **Tolerance**: The minimum change in scores between iterations required for the algorithm to be considered converged.
    * **Normalize initial scores to sum to 1**: If enabled, the initial scores for all nodes will be normalized to sum to 1.

**Advanced parameters**

    * **Batch Size**: Controls the number of results loaded into memory at a time. Adjust this value to manage memory usage when processing large graphs.

.. _collect-nodes-recipe-label:

Collect nodes recipe
--------------------

For use cases that exceed the scaling capabilities of the embedded database, **Collect nodes & edges** recipes can prepare your graph data for export to external systems like Neo4j, leveraging the :doc:`Neo4j plugin </unstructured-data/graph/neo4j-plugin>`.

Before using this recipe, you must first design your graph and create a Saved configuration within the Visual Graph Editor webapp.

Input / Output
~~~~~~~~~~~~~~

**Input**
    * Saved configurations dataset: Dataset containing the saved graph configuration you wish to use.
    * Datasets used as sources of the node group: Select all the original source datasets that are referenced for the target node group within your saved configuration.

.. warning::
    You must explicitly provide all required source datasets as inputs to the recipe. Due to Dataiku's security model, the recipe will fail if any source dataset defined in the configuration is not declared as an input.
    
**Output**
    * Output dataset: Dataset to store the collected nodes. The output will contain columns for the node identifier and all properties as defined in the saved configuration.

Settings
~~~~~~~~

**Select a saved configuration**

From the dropdown list, choose the specific Saved configuration you want to process.

**Select a node group**

Select the node group whose members you want to collect into the output dataset.

Collect edges recipe
--------------------

The configuration is similar to the :ref:`Collect nodes <collect-nodes-recipe-label>` recipe.

More graph algorithms to come
-----------------------------

We plan to add more graph algorithm recipes in future releases.

To help us prioritize development, please contact your Dataiku Account Executive or Dataiku Support with your specific needs and use cases.

For immediate or custom requirements, you can implement algorithms directly by leveraging the Kuzu graph database. Refer to the `Kuzu documentation <https://kuzudb.github.io/docs/extensions/algo/>`_ for implementation guidance.