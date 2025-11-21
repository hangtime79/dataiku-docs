ERR_DATASET_CSV_UNTERMINATED_QUOTE: Error in CSV file: Unterminated quote
#########################################################################

While parsing a CSV file, DSS encountered the start of a quoted field, but not the end. This prevents DSS from successfully parsing the CSV file.

While this can sometimes indicate a broken CSV file, in the vast majority of cases, this issue is caused by a wrong *CSV Quoting style*. For more details about CSV quoting styles, please see :doc:`/connecting/formats/csv`.

Generally speaking, it means you have used "Excel" quoting style (the default) but your file is actually Unix or Escaping-only

Remediation
===========

* Go to the dataset settings
* Go to the "Format/Preview" tab
* In the "Style" section, select "Unix"
* Save the settings and try again
* If you still encounter an issue, try again with "Escaping only"
