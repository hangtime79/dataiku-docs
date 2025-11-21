Extract with regular expression
#############################################

Extract chunks from a column using a regular expression. Note that regular expressions are not anchored: ``([0-9]*)`` will capture ``232`` in ``val-232``.

Options
=========

**Regular expression**

Once the input column is filled, use **Find with Smart Pattern** to help generate a regular expression. 

**Capture groups**

Use named or unnamed capture groups to extract distinct chunks into several output columns. Unnamed capture groups use the ``(pattern)`` syntax and place matches into numbered columns. Named capture groups use the ``((?<groupname>pattern)`` syntax and place matches into named columns using the group name. 

Example, unnamed group: 

* Cell value: ``id-37-X234``

* Pattern: ``id-([0-9]*)-([0-9A-Z]*)``

* Output column prefix: ``extracted_``

* Result: ``extracted_1=37 extracted_2=X234``

Example, named group: 

* Cell value: ``id-37-X234``

* Pattern: ``id-(?<numidentifier>[0-9]*)-(?<identifier2>[0-9A-Z]*)``

* Output column prefix: ``extracted_``

* Result: ``extracted_numidentifier=37 extracted_identifier2=X234``

**Found column**

Enable this option to create a column name *found* containing a boolean to indicate whether or not the pattern matched. 

**Extract all occurrences**

Enable this option to extract multiple matches of a group into one array. 

Related resources
====================

See `How-To: Extract Patterns With the Smart Pattern Builder <https://knowledge.dataiku.com/latest/courses/advanced-data-prep/prepare-recipe/smart-pattern-builder.html>`_ for a detailed example of working with the Smart Pattern Builder.

.. pristine
