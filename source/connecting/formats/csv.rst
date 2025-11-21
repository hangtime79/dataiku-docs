Delimiter-separated values (CSV / TSV)
#######################################

"CSV" in DSS format covers a wide range of traditional formats, including comma-separated values (CSV) and tab-separated values (TSV).

Despite its apparent simplicity, there are subtleties in the DSV format.  Data Science Studio reads the DSV according to the specifications you give, so if the file doesn't conform to the spec, you may end up with misaligned, misplaced fields, or fields consisting of almost all the file (and out of memory issues).


.. contents::
    :depth: 2
    :local:

Quoting and escaping styles
==============================

The main problem with DSV is the handling of special characters within the fields.

Several methods exist, and Data Science Studio supports all of the following.

Excel-style
-------------

Also known as RFC4180, the most common variant of DSV.

* The quoting char is a double quote (``"``)
* If the separator char appears in a field, the field is enclosed in the quoting char
* If a \\n or \\r char appears in a field, the field is also enclosed in the quoting char
* If the quoting char appears in the field the quoting char itself is doubled

Example
~~~~~~~~

With separator: ``,``

Input ::

    a normal,line
    "the,delimiter","in,a field"
    "but ""also""","double ""quotes"", in a field"

Output::

    a normal            line
    the, delimiter      in, a field
    but "also"          double "quotes", in a field

.. _csv-unix:

Unix-style
-------------

* If the separator char appears in a field, the field is enclosed in a quoting char  (generally a double quote)
* If a \\n or \\r char appears in a field, the field is also enclosed in the quoting char
* If the quoting char appears in the field, it is prefixed with the escape char (generally \\)
* If the escape char appears in a field, it is prefixed with itself

Example
~~~~~~~~~

With separator: ``,``, quoteChar: ``"``, escapeChar: ``\``

Input::

    a normal,line
    "the,delimiter","in,a field"
    "but \"also\"","double \"quote\", in a field"
    and \\ in a field, "is \"possible\" too

Output::

    a normal            line
    the, delimiter      in, a field
    but "also"          double "quotes", in a field
    and \ in a field    is "possible" too

Escaping only
----------------

* If the separator char appears in a field, it is prefixed with the escape char (generally \)
* If \\n or \\r appears in a field, it is prefixed with the escape char
* If the escape char appears in a field, it is prefixed with itself

In this format, the double quote is not a special character

Example
~~~~~~~~~

With separator: ``,``, escapeChar: ``\``


Input::

    a normal,line
    the \,delimiter, in \,a field
    but "also", double "quotes"\,in a field
    and \\ in a field, is "possible" too

Output::

    a normal            line
    the, delimiter      in, a field
    but "also"          double "quotes", in a field
    and \ in a field    is "possible" too

No escaping, no quoting
-------------------------

* The separator may not appear in a field
* \\n or \\r may not appear in a field

In this format, the double quote is not a special character.

Input::

    a normal, line
    is the, only "possible" thing

Output::

    a normal            line
    is the              only "possible" thing


Usage in datasets
=====================

Data Science Studio tries to autodetect the quoting style when you create a new external dataset.

This will not always be able to detect the correct quoting style, as quoting/escaping chars might not appear in the first lines.

Make sure to select the correct quoting style for your dataset. Using wrong quoting styles can lead to huge number of columns being generated or values of arbitrarily large size. This may cause some memory issues.

.. note::

    When using "no quoting, no escaping" style, it is highly recommended to have a very exotic separator like \u0001

    Note also that this style is not able to represent all data.

Usage in recipes
==================

+-------------+---------------------------------------------------------------------------------------+
| Recipe type |                                      Restrictions                                     |
+=============+=======================================================================================+
| Hive        | Escaping only and "no escaping no quoting"  are the only supported styles             |
| Spark       |                                                                                       |
|             | When creating a new managed dataset from the Hive recipe editor,                      |
|             | it automatically gets "Escaping only " style                                          |
|             |                                                                                       |
|             | Additionally, due to Hadoop limitations, files with newlines in fields cannot be used |
|             |                                                                                       |
+-------------+---------------------------------------------------------------------------------------+
| Other       | If "no escaping, no quoting" is used as output and either                             |
|             | the delimiter, \\n or \\r appears in a field,                                         |
|             | the offending character is automatically replaced by a space                          |
+-------------+---------------------------------------------------------------------------------------+
