ERR_DATASET_TRUNCATED_COMPRESSED_DATA: Error in compressed file: Unexpected end of file
#######################################################################################

The compressed file ends unexpectedly.
This error is typically caused by a problem in your data (i.e. data is invalid). If this data was created by DSS, you may need to rebuild it. This error can also be ignored, allowing you to process the available data.

Remediation
===========

* In the dataset, select "Settings" and "Format / Preview" tab
* In the "File read failure behaviour", choose "Emit a warning and continue with the next file (if any)"
* Rerun the recipe
