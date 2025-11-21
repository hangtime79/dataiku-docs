SQL databases
###############

DSS can both read and write datasets in SQL databases. You can:

* Create datasets representing SQL tables (and read and write in them)
* Create datasets representing the results of a SQL query (and read them)
* Write code recipes that create datasets using the results of a SQL query on existing SQL datasets. See :doc:`/code_recipes/sql` for more information.

In addition, on most supported databases, DSS is able to:

* Execute Visual recipes directly in-database (ie: for a visual recipe from the database to the database, the data never moves out of the database)
* Execute Charts directly in-database

For more information on the range of what DSS can do with SQL databases, please see :doc:`/sql/index`.

.. note::

	You might want to start with our resources on `data connections <https://knowledge.dataiku.com/latest/data-sourcing/connections/index.html>`_ in the Knowledge Base. The rest of this section is reference information.

DSS provides full support for many databases and experimental support for others.  Click on a link for detailed support information for that database.

.. toctree::
  :maxdepth: 1

  introduction

  snowflake
  databricks  
  synapse
  fabricwarehouse
  bigquery
  redshift
  postgresql
  mysql
  sqlserver
  oracle
  teradata
  greenplum
  alloydb
  cloudsql
  athena
  trino
  treasure
  vertica
  saphana
  dremio
  netezza
  exasol
  db2
  ../kdbplus