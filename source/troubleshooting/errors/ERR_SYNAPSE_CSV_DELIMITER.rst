ERR_SYNAPSE_CSV_DELIMITER: Bad delimiter setup
##############################################

DSS tried to load CSV data from a Azure Blob Storage file to Synapse or SQLServer DataWarehouse, but the delimiter settings on the CSV dataset aren't working for the actual Azure loader (Polybase or COPY statement)

This error can happen:

 * when the data contains multiline fields
 * when the field separator (usually the tab or semi-colon character) is present in the data, but no quoting character is used for the loader. This leads Azure to see more fields on a given row than it expects
 * when the string delimiter (usually the double quote character) is present in the data and quoting is used for the loader. Polybase can't handle such situations

Remediation
===========

* multiline fields are not handled by the Azure loader at all: disabling the fast-path and using the DSS (stream) engine is the only solution
* if quoting for the Azure loader is explicitly disabled on the DSS instance (i.e. the ``dku.azure_to_synapse.use.quoting=false`` line has been added to the ``config/dip.properties`` file), then you can force using quoting for the recipe by adding a property ``azure_to_synapse.use.quoting -> true`` on the input dataset in the Settings > Advanced tab, under Custom properties
* if the quoting character is present in the data, you can try switching the input dataset format to CSV with Unix style, and specify a non-common character as quoting character