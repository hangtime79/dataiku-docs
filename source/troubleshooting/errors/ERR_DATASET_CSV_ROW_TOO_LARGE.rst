ERR_DATASET_CSV_ROW_TOO_LARGE: Error in CSV file: Dataset row is too long to be processed
#########################################################################################

Considering the dataset's CSV format configuration, a row cannot exceed a certain length.


Remediation
===========

This error appears when the dataset contains a row that is unexpectedly long.

Make sure the quoting style, as well as the quote and escape characters, are well chosen.
It's very likely that the error comes from there.
You'll find those settings in the dataset tab "Settings > Format/Preview".
For more details about CSV quoting styles, please see :doc:`/connecting/formats/csv`.

If the long row is not due to the format configuration but inherent to the dataset, you can increase the limit ``Maximum characters per row`` in the same tab.
You can set them to 0 if you simply do not want any limit.
Beware that you may encounter out of memory errors.
