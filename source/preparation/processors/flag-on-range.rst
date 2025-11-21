Flag rows on numerical range
#############################################

This processor flags rows for which the value is within a numerical
range.

The boundaries of the numerical range are inclusive. If the column does
not contain a valid numerical value for a row, this row is considered as
being out of the range.

This processor creates a column containing '1' for matching (in-range)
rows, nothing else.

Columns selection
=================

This processor can check its matching condition on multiple columns:

-  A single column
-  An explicit list of columns
-  All columns matching a given pattern
-  All columns

You can select whether the row will be considered as matching if:

-  All columns are matching
-  Or, at least one column is matching



.. pristine
