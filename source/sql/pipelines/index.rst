SQL pipelines in DSS
#####################

A SQL pipeline is a process that combines several consecutive recipes (each using the same SQL engine) in a DSS workflow. These combined recipes, which can be both visual and "SQL query" recipes, can then be run as a single job activity. Using a SQL pipeline strongly boosts performance by avoiding unnecessary writes and reads of intermediate datasets. 

SQL pipelines also allow you to optimize the data storage capacity without having to manually re-factor the Dataiku flow (for example, by reducing the number of datasets). 

.. warning::

	**Experimental feature**: The SQL pipeline feature is considered experimental and not officially supported.
	In case of issues, you always have the option to disable SQL pipelines on a per-project basis.


Topics
=======

.. contents::
	:local:

.. toctree::
   :maxdepth: 1
  
   sql_pipelines
   views
   partitions





.. Topics
.. =======



.. :doc:`./sql_pipelines`
.. ---------------------------------------
.. Use SQL pipelines in your workflow to avoid unnecessary reads and writes of intermediate datasets.

.. :doc:`./views`
.. ---------------------------------------
.. Learn how views are named and cleaned up in DSS.

.. :doc:`./partitions`
.. ---------------------------------------
.. Create unions of virtualized (and non-virtualized) partitions. 


  
