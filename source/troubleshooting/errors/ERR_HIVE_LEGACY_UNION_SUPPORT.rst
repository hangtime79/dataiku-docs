ERR_HIVE_LEGACY_UNION_SUPPORT: Your current Hive version doesn't support UNION clause but only supports UNION ALL, which does not remove duplicates
#############################################################################################################################################################

The Hive query cannot be executed because it incudes a UNION clause that is not supported by this version of Hive

Remediation
===========

If you're running a stack recipe with Distinct rows post-filter there are following possibilities:

* Use stack recipe without distinct postfilter + create a distinct recipe for a result of a stack recipe
* Apply distinct recipe on each of the stacked datasets and then stack them
* Create a Hive recipe with a query that uses UNION ALL and then wrap the whole query with `SELECT DISTINCT {your column names} from {select with UNION ALL}`
