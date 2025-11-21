ERR_RECIPE_ENGINE_NOT_DWH: Error in recipe engine: SQLServer is not Data Warehouse edition
#######################################################################################################

DSS attempted to use an Azure Data Warehouse engine on a standard SQLServer database.

Remediation
===========

* If the Azure database is indeed a Data Warehouse edition, go to its connection settings in the administration section, and check the "Azure Data Warehouse" box.
* If the Azure database is not a Datawarehouse edition, choose the DSS Recipe engine instead of Azure to SQLServer
