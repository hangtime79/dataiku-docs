ERR_FORMAT_LINE_TOO_LARGE: Line is too long to be processed
###########################################################

Considering the current format configuration, a line cannot exceed a certain length.


Remediation
===========

This error often appears on the dataset formats ``One record per line`` or ``Separated Values (CSV, TSV, ...)``
when the dataset contains a line that is unexpectedly long.

You can increase the limit ``Maximum characters per line`` or ``Maximum characters per row`` in the dataset tab settings, which can be found under  "Settings > Format/Preview".
You can set them to 0 if you simply do not want any limit.
Beware that you may encounter out of memory errors.
