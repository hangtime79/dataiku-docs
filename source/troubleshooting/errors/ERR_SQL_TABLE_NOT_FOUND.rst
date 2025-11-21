ERR_SQL_TABLE_NOT_FOUND: SQL Table not found
##############################################

DSS tried to access a table in a SQL database, but the SQL database does not contain the table.

This error can happen:

 * When trying to view a SQL dataset

Remediation
===========

* If this error occurs on a "source" dataset (i.e. a dataset that is at the beginning of the flow), you need to check the settings of the dataset. The table name might be incorrect
* If this error occurs on a "managed" dataset (i.e. a dataset that is built as part of the Flow), you might need to rebuild this dataset, as it may have been previously cleared.
* Check that, in addition to the table name, the schema name is also correct
* Pay attention to case: most SQL databases are case-sensitive, "MYTABLE" is not the same as "mytable"
* This error can also be caused by permission issues. On some databases, if you don't have permission to read or write a table, you will get a "table not found" error