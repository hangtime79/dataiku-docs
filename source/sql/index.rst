DSS and SQL
#############

DSS can both read and write datasets in SQL databases. Using DSS with SQL, you can:

* create datasets representing SQL tables (and read and write in them)
* create datasets representing the results of a SQL query (and read them)
* write code recipes that create datasets using the results of a SQL query on existing SQL datasets. See :doc:`/code_recipes/sql` for more information about SQL recipes  
* use the SQL Notebook for interactive querying

In addition, on most supported databases, DSS is able to:

* execute :doc:`/other_recipes/index` directly in-database (ie: for a visual recipe from the database to the database, the data never moves out of the database)
* execute :doc:`/visualization/index` directly in-database
* create pipelines

For an overview of which databases are supported by DSS, see :doc:`the connecting to SQL reference </connecting/sql/index>`.

.. toctree::
   :maxdepth: 1
  
   datasets
   write_and_execute
   partition
   pipelines/index  
