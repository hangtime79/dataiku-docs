Split invalid cells into another column
#############################################

This processor takes all values of a column that are invalid for a
specific meaning and moves them to another column.

Example
--------

With the following data:

+------+
| icol |
+------+
| 42   |
+------+
| Baad |
+------+

With parameters:

-  Column: icol
-  Column for invalid data: bad\_icol
-  Meaning to check: Number The result will be:

+------+-----------+
| icol | bad_icol  |
+------+-----------+
| 42   |           |
+------+-----------+
|      | Baad      |
+------+-----------+



.. pristine
