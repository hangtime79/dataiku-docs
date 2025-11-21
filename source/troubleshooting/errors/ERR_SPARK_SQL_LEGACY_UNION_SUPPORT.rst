ERR_SPARK_SQL_LEGACY_UNION_SUPPORT: Your current Spark version doesn't support UNION clause but only supports UNION ALL, which does not remove duplicates
#########################################################################################################################################################################

The Spark SQL cannot be executed because it includes a UNION clause that is not supported by this version of Spark

Remediation
===========

If you're running a stack recipe with Distinct rows post-filter there are following possibilities:

* Use stack recipe without distinct postfilter + create a distinct recipe for a result of a stack recipe
* Apply distinct recipe on each of the stacked datasets and then stack them
* Create a Spark SQL recipe with a query that uses UNION ALL and then wrap the whole query with `SELECT DISTINCT {your column names} from {select with UNION ALL}`
