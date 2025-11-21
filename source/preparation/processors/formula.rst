Formula
#############################################

This processor computes new columns using formulas based on other
columns (like in a spreadsheet). The :doc:`formula language <../../formula/index>` provides:

-  Math functions
-  String manipulation functions
-  Date handling functions
-  Boolean and conditional expressions for rules creation

Usage examples
=================

-  Compute a numerical expression: ``(col1 + col2) / 2 * log(col3)``
-  Manipulate strings : ``toLowercase(substring(strip(mytext), 0, 7))``
-  Create a rule-based column: ``if (width > height, "wide", "tall")``

Getting help
===============

The formula editor provides live syntax checking, preview of results, a complete language reference, and examples.


.. pristine
