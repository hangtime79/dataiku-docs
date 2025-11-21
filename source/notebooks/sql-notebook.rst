SQL notebook
#############

The SQL notebook is an interactive environment for performing queries on all SQL databases supported by DSS.

It supports all kinds of SQL statements, from simplest SQL queries to advanced DDL, stored procedures, ...

A SQL notebook is attached to a single SQL connection of DSS.

Creating a SQL notebook
=========================

You can create a SQL notebook either from the "Notebooks" tab of your project. Select SQL and then select the SQL connection on which you want to create the notebook.


Cells and history
==================

A SQL notebook is made of several *cells*. Each cell is where you execute and modify a single query and view its results. The recommended way to work with a SQL notebook is to keep a single cell for each query that you might want to rerun at a later time.

Each cell has its own history so you can work on tuning and debugging your queries with confidence, you'll always be able to find previously executed states.


AI SQL Generation
=================

Dataiku includes an AI Assistant to help users write SQL queries. Please see :doc:`/ai-assistants/sql-assistant` 
