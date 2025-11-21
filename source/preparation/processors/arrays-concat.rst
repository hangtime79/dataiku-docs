Concatenate JSON arrays
#############################################

This processor concatenates N input columns containing arrays (as JSON)
into a single JSON array.

Example
=======

-  Input:

::

       a       b
       [1,2]   ["x","y"]

-  Output:

::

       [1, 2, "x", "y"]



.. pristine
