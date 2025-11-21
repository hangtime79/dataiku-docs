Count occurrences
#############################################

This processor counts the number of occurrences of a pattern in the
specified column

Matching modes
==============

-  'Complete value' : counts complete cell values (output can only be 0
   or 1)
-  'Substring' : counts all occurrences of a string within the cell
-  'Regular expression': counts matches of a regular expression

Normalization modes
===================

-  Case-sensitive matches ('Exact' mode)
-  Case-insensitive matches ('Lowercase' mode)
-  Accents-insensitive matches ('Normalize' mode)

Note: accent-insensitive matching is only available for 'complete value'
matching.


.. pristine
