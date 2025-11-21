Flag invalid rows
#############################################

This processor flags rows with invalid values, ie values not matching a
selected meaning.

It creates a column which will contain '1' if the row matches (invalid),
nothing else

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
