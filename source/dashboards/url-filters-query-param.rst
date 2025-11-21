Filtering a dashboard using a query parameter in the URL
########################################################

If a dashboard contains filters, it can be pre-filtered by defining the filters default state in Edit mode.

However, in View mode changes are not kept. To share or bookmark a dashboard pre-filtered from the View mode, you can add a query string parameter to the dashboard URL and share or bookmark it.

.. note::
    If filters are present in the dashboard page's filters panel but absent from your URL, their default state will be applied.

Generating a URL from a filters panel
=====================================

The fastest and easiest way to create a ready-to-use dashboard URL with a filters query parameter is to open the dashboard, edit the filters to match the expected state, and click on the "Copy as URL in clipboard" button.

.. image:: img/filters-copy-as-url.png
  :width: 400
  :alt: The Copy as URL in clipboard button in a filters panel

Once the URL is ready, you will get a notification and it will be available in your clipboard so you can paste it wherever you want.

.. note::
    Opening a generated URL with a filters query parameter ensures that the insights in the dashboard are filtered as they were at generation time. The values available in the filter facets can be restricted to what's shown without the possibility to extend the selection. To be able to select more values, open a filter settings menu and switch to "All values in sample" mode.

Filters query parameter syntax
==============================

You will see below that the filters query parameter value uses a syntax that can be understood and written by humans.
However, it contains special characters that browsers will fail to parse. Once your filter query parameter value is ready, do not forget to encode it before appending it to the dashboard URL (many tools can be found online to encode a URL).

For example:

.. code-block::

    https://mydssinstance.com/projects/MYPROJECT/dashboards/42?pageFilters=foo:in("bar")

becomes:

.. code-block::

    https://mydssinstance.com/projects/MYPROJECT/dashboards/42?pageFilters=foo%3Ain%28%22bar%22%29

Value types
-----------

Column name
%%%%%%%%%%%

Column names are on the left part of a filter description, and they are always followed by a colon that separates the column name from the filter values. 
Special characters (any character that is not a letter or a digit) must be encoded. To encode a special character, use its hexadecimal ASCII code padded with 0 if necessary so that the code is 4 characters long, prefixed by ``_x`` and suffixed by ``_``.

For example ``Weight: maximum``` becomes ```Weight_x003A__x0020_`maximum```.  
The hexadecimal ASCII code of `:` is ``3A``. We pad it with two zeros to have a 4-digit code, it gives us ``003A``. Then, we add the prefix and suffix and obtain the final encoded version ``_x003A_``.  
The same reasoning is applied to the space characters: its hexadecimal ASCII code is ``20``, padded it gives ``0020``, and with the prefix and suffix ``_x0020_``.  

String
%%%%%%

A String is wrapped in double quotes. Double quotes and backslashes within the string content must be escaped by prefixing them with a backslash. For example ``"Hello", \ he says`` becomes ``"\"Hello\", \\ he says"``.

ISO Date
%%%%%%%%

An ISO Date is defined by the ISO 8601 norm and doesn't need any special formatting. For example, a valid ISO Date is ``2023-01-01T00:00:00.000Z``.

Number
%%%%%%

A Number is either an integer or a rational number and doesn't need any special formatting.

Constants
%%%%%%%%%

Constants are used to describe specific states. They are written using snake case with all uppercase letters.
The different special tokens are:
- ``OFF``, used to describe a deactivated filter. For example: ``ColumnName:OFF``;
- ``NO_VALUE``, used to describe the absence of value (ie an empty cell in a dataset);
- ``HOUR_OF_DAY``, ``DAY_OF_WEEK``, ``DAY_OF_MONTH``, ``MONTH_OF_YEAR``, ``WEEK_OF_YEAR``, ``QUARTER_OF_YEAR``, ``YEAR``, used to describe the date part on which a date part or relative date filter is applied.

Alphanumerical filter
---------------------

Alphanumerical filters can either specify a list of values to include, in case the ``in`` operator will be used, or a list of values to exclude, in case the ``nin`` operator will be used.

These operators can contain a list of values. These values are separated by commas and can be:

- Strings for alphanumerical filters based on alphanumerical columns;
- Numbers for alphanumerical filters based on numerical columns.


To filter on a column named City so as to include only Paris and New York:

.. code-block::

    ?pageFilters=City:in("Paris","New York")  

.. note::

    When using this syntax, the filter is in "Exclude other values" mode.

To filter on a column named Age so as to exclude 42 and 66:

.. code-block::

    ?pageFilters=City:nin(42,66)  

.. note::

    When using this syntax, the filter is in "Include other values" mode.

Custom filter
---------------------

Custom filters specify a list of values with normalization applied to the column and how to search, with the combination of ``in()``, ``.match()``, ``.normalization()`` operators.

The ``in()`` operator can contain a list of values. These values are separated by commas and can be:

- Strings for alphanumerical filters based on alphanumerical columns;
- Numbers for alphanumerical filters based on numerical columns.

The ``match()`` operator contains a list of constant values:

- **FULL_STRING**: Will perform a match on the full string
- **SUBSTRING**: Will perform a match on a part of the string
- **REGEX**: Will perform a match with regular expression

The normalizations are:

- **EXACT**: Case sensitive
- **IGNORE_CASE**: Case insensitive
- **NORMALIZED**: Transform to lowercase, remove punctuation and accents and perform Unicode NFD normalization (``Café`` -> ``cafe``)

To filter on a column named City to get all cities that contain an ``e`` ignoring the case:

.. code-block::

    ?pageFilters=City:in("e").match(SUBSTRING).normalization(IGNORE_CASE)
    ?pageFilters=City:in("[eE]").match(REGEX)

.. note::

    When using this syntax, the filter is in "Exclude other values" mode.

Numerical range filter
----------------------

Numerical range filters can only be applied to numerical columns and use the `range` operator.  
This operator takes two optional Number parameters: a minimum value and a maximum value, separated by a comma (``,``).

To filter on a column named Age so as to restrict the values from 24 to 42:

.. code-block::

    ?pageFilters=Age:range(24,42)  

To filter on a column named Age so as to restrict the values to at least 24:

.. code-block::

    ?pageFilters=Age:range(24)  

To filter on a column named Age so as to restrict the values to at most 42:

.. code-block::

    ?pageFilters=Age:range(,42)  

To filter on a column named Age so as to include all values:

.. code-block::

    ?pageFilters=Age:range()  

Date range filter
-----------------

Date range filters can only be applied to date columns and use the `daterange` operator.  
This operator takes two optional ISO Date parameters: a minimum value and a maximum value, separated by a comma (``,``).


To filter on a column named Birthday so as to restrict the values from a date to another:

.. code-block::

    ?pageFilters=Birthday:daterange(2022-01-01T00:00:00.000Z,2023-01-01T00:00:00.000Z)  

To filter on a column named Birthday so as to restrict the values from a date:

.. code-block::

    ?pageFilters=Birthday:daterange(2022-01-01T00:00:00.000Z)  

To filter on a column named Birthday so as to restrict the values until a date:

.. code-block::

    ?pageFilters=Birthday:daterange(,2023-01-01T00:00:00.000Z)  

To filter on a column named Birthday so as to include all values:

.. code-block::

    ?pageFilters=Birthday:daterange()  

Date part filter
----------------

Date part filters can be applied to date columns only and use two operators:

- the ``datepart`` operator taking a date part constant as parameter;  
- either the ``in`` or ``nin`` operator depending on whether the values should be included or excluded and taking as parameters a list of comma delimited values that are Strings for days and months and Numbers for other date parts.

The two operators are separated by a dot (``.``).

Example of a date part filter on a column Birthday to include dates from the years 2022 and 2023:

.. code-block::

    ?pageFilters=Birthday:datepart(YEAR).in(2022,2023)

Example of a date part filter on a column Birthday to exclude dates corresponding to Mondays and Wednesdays:

.. code-block::

    ?pageFilters=Birthday:datepart(DAY_OF_WEEK).nin("Monday","Wednesday")

Relative date filter
--------------------

Relative date filters can only be applied to date columns and use at least two operators:

- the ``datepart`` operator taking a date part constant as a parameter;  
- Operators such as ``this``, ``ts``, ``next``, or ``last`` that can be combined together. Among these, ``this`` and ``ts`` do not require any parameters, while ``next`` and ``last`` necessitate one Number parameter.

Example of a relative date filter on a column Birthday to include values in the current day of week:

.. code-block::

    ?pageFilters=Birthday:datepart(DAY_OF_WEEK).this()

Example of a relative date filter on a column Birthday to include values in the year to date (until now):

.. code-block::

    ?pageFilters=Birthday:datepart(YEAR).td()

Example of a relative date filter on a column Birthday to include values in the next 3 months:

.. code-block::

    ?pageFilters=Birthday:datepart(MONTH_OF_YEAR).next(3)

Example of a relative date filter on a column Birthday to include values in the last 3 months:

.. code-block::

    ?pageFilters=Birthday:datepart(MONTH_OF_YEAR).last(3)

Example of a relative date filter on a column Birthday to include values from the last week to the end of the current one:

.. code-block::

    ?pageFilters=Birthday:datepart(WEEK_OF_YEAR).last(1).this()

Example of a relative date filter on a column Birthday to include values from the last week until now:

.. code-block::

    ?pageFilters=Birthday:datepart(WEEK_OF_YEAR).last(1).this().td()

Example of a relative date filter on a column Birthday to include values from today until tomorrow:

.. code-block::

    ?pageFilters=Birthday:datepart(DAY_OF_WEEK).this().next(1)

Example of a relative date filter on a column Birthday to include values from the last 2 months, the current month, and the next 3 months:

.. code-block::

    ?pageFilters=Birthday:datepart(MONTH_OF_YEAR).last(2).this().next(3)

Multidimensional exclude filters  
---------------------------------  

Multidimensional exclude filters offer a method for combining multiple conditions to exclude data that satisfy all specified criteria.  

Filters eligible for this type of combination include:  

- Alphanumerical filters in include mode (using the ``in`` operator) with exactly one value;  
- Date part filters in include mode (using the ``in`` operator) with exactly one value;  
- Numerical and date range filters with both a min and a max.  

To form a multidimensional exclusion condition, combine these filters using the "not" operator:  

Example of a multidimensional filter excluding all data points for which City is equal to New Work, Birthdate is a date for which the month is January, and Age is between 0 and 18:  

.. code-block::

    ?pageFilters=not(City:in("New work");Birthdate:datepart(MONTH_OF_YEAR).in("January");Age:range(0,18))  


Multiple filters at once
------------------------

If you need multiple filter facets in your URL, separate them with semicolons (``;``).

Example of multiple filter facets:

.. code-block::

    ?pageFilters=City:in("Paris","New York");Age:range(24);Birthday:datepart(YEAR).nin("2022","2023")

Once encoded and appended to the URL:

.. code-block::
    
    https://mydssinstance.com/projects/MYPROJECT/dashboards/42?pageFilters=City%3Ain%28%22Paris%22%2C%22New%20York%22%29%3BAge%3Arange%2824%29%3BBirthday%3Adatepart%28YEAR%29.nin%28%222022%22%2C%222023%22%29
