Unfold an array
#############################################

This processor takes a column containing JSON-formatted arrays and transforms it into several columns,
containing the number of occurrences of each term of the array.

You can prefix new columns by filling the "Prefix" option.

You can choose the maximum number of columns to create with the "Max nb. columns to create" option.

You can transform the original column into binary columns by unchecking the "Count of Values" option.

.. include:: snippets/_unfold-array-example-and-warning.rst

For more details on reshaping, please see :doc:`/preparation/reshaping`.