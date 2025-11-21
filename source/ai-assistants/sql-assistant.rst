SQL Assistant
################

The SQL Assistant helps users with SQL writing in both SQL recipes and SQL notebooks.

The SQL Assistant has awareness of the tables in your database and database type in order to generate accurate SQL code across all databases.

Powered by a Large Language Model (LLM), this tool analyzes dataset schemas to craft queries tailored to your needs. Each query is accompanied by a detailed reasoning section explaining how queries are constructed.


Setup
========================

Go to **Administration > Settings > AI Services > AI Generate SQL** to enable AI Assistant

Usage in recipes
=================

To use this feature, you must have access to the input datasets SQL connection, and WRITE permissions to the DSS project where the SQL recipe resides. You can then use AI to generate SQL queries, review the generated query, and import it to your code editor, where you can modify or execute it as needed.

SQL Assistant is only supported on "regular" SQL recipes, not on Impala, Hive or Spark SparkSQL


Usage in notebooks
====================

To use this feature, you must have WRITE permissions on the project where the SQL notebook resides. In the left generate tab of the left panel, you can then use AI to generate SQL queries, review the generated query, and import it to you notebook, where you can modify or execute it as needed.


SQL Assistant is only supported on "regular" SQL notebooks, not on Impala, Hive or Spark SparkSQL



