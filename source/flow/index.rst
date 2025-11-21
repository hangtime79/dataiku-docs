The Flow
#############

In DSS, the datasets and the recipes together make up the **flow**. We have created a visual grammar for data science, so users can quickly understand a data pipeline through the **flow**.

Using the flow, DSS knows the lineage of every dataset in the flow. DSS, therefore, is able to dynamically rebuild datasets whenever one of their parent datasets or recipes has been modified.

DSS can limit the resource usage of jobs building datasets. Users can configure their recipes and administrators can configure DSS to prevent some users, projects, recipes or plugins from consuming too many resources.

.. toctree::
    :maxdepth: 2

    visual-grammar
    zones
    building-datasets
    insert-delete
    limits
    graphics-export
    folding
    flow-document-generator
    flow-explanations
