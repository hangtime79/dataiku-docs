.. _formula-language:

Formula language
##################

.. contents::
	:local:
	:depth: 1

DSS includes a language to write formulas, much like a spreadsheet.

Formulas can be used:

* In data preparation, to create new columns, filter rows or flag rows

* More generally, to filter rows in many places of DSS:

  * In the Filtering recipe, to filter rows
  * In Machine Learning, to define the extracts to use for train and test set
  * In the Python and Javascript APIs, to obtain partial extracts from the datasets
  * In the Public API, to obtain partial extracts from the datasets
  * In the grouping, window, join and stack recipes, to perform pre and post filtering

Basic usage
============

Formulas define an expression that applies **row per row**.

Assuming that you have a dataset with columns N1 (numeric), N2 (numeric) and S (string) , here are a few example formulas:

* ``2 + 2``
* ``N1 + N2``
* ``min(N1, N2)`` # Returns the smallest of N1 and N2
* ``replace(S, 'old', 'new')`` # Returns the value of S with 'old' replaced by 'new'
* ``if (N1 > N2, 'big', 'small')`` # Returns big if N1 > N2, small otherwise

.. note::

	We also have a `How-To <https://knowledge.dataiku.com/latest/data-preparation/formulas/concept-formula-master.html>`_ that lists common use cases with examples.


Reading column values
======================

In almost all formulas, you'll need to read the values of the columns for the current row.

When the column has a "simple" name (i.e: starting by a letter, contains only letters, numbers and underscores), you just need to use the name of the column in the formula: ``N1 + 4``

For other cases, you can use:

* ``val("column with spaces")`` : returns the value of "column with spaces"
* ``strval("column with spaces")`` : returns the value of "column with spaces" as a string
* ``numval("column with spaces")`` : returns the value of "column with spaces" as a number

.. warning::

	``mycolumn`` evaluates to the value of the column named *mycolumn*

	Thus, ``strval(mycolumn)`` would not work because it would try to read as a string the value of
	the column whose name is the value of the *mycolumn* column.

	Instead, use ``strval("mycolumn")``.

You may also need to use ``strval`` to avoid DSS automatically typing a numerical variable. See `Variables typing and autotyping`_ for more details.

Accessing values from previous rows
------------------------------------

The ``val``, ``strval``, and ``numval`` functions optionally accept an offset argument. This allows you to access values from previous rows in the dataset. See `Value access functions`_ for more details.

.. note::

		The offset argument is only available in the Prepare recipe and only with the DSS engine.



Variables typing and autotyping
================================

Variables in the formula language can have one of the following types: string, integer, decimal, array, object, boolean, date

*Regardless of the schema of the dataset, or the meanings of the columns* (in the case of working on dynamically-generated columns), the following rules are applied:

* If column values are "standard" decimal, they are automatically parsed to decimal
* If column values are "standard" integer, they are automatically parsed to integer
* Else, they are kept as string

Columns containing dates, arrays, objects or booleans are not automatically converted to the matching Formula type.
However:

* all functions that require an array will automatically attempt to convert a string input to array (using the regular DSS JSON syntax)
* all functions that require a date will automatically attempt to convert a string input to date (using the ISO-8601 format)

In other words, if the column "begin_date" is a date (and thus contains properly-formatted ISO-8601):

* ``type(begin_date)`` returns "string"
* ``inc(begin_date, 2, "days")`` works as expected because the inc function performed automatic conversion to date

Avoiding auto-typing
---------------------

There are some cases where auto-typing is not a good thing. For example, a value like ``012345`` would be automatically converted to the number ``12345``.

* To avoid autotyping to numerical, use the ``strval("mycolumn")`` function (see above)
* To manually obtain an array or object, use the ``parseJson`` function
* To manually obtain a number, use the ``numval("mycolumn")`` function
* To manually obtain a date, use the ``asDatetimeTz``, ``asDatetimeNoTz`` or ``asDateOnly`` function
* To manually obtain a boolean, use the ``asBool`` function

Boolean values
================

The formula language uses "True" and "False", with quotes, as boolean values for true and false.

Operators
==========

The formula language supports the classical arithmetic operators:

* Regular math operators: ``+``, ``-``, ``*``, ``/``
* Comparison operators (evaluate to booleans): ``>``, ``>=``, ``<``, ``<=``, ``==``, ``!=``
* Arithmetic operators: ``//`` (integer division) and ``%`` (modulo)
* Boolean operators: ``&&``, ``||``

* The ``+`` operator also performs string concatenation.
* The comparison operators (and only them) can operate on dates. For dates arithmetic, see the ``diff`` and ``inc`` functions.

Array and object operations
=============================

Formula support accessing array elements and object keys using the traditional Python/Javascript syntax:

* ``array[0]``
* ``object["key"]``
* ``object.key`` (only valid if 'key' is a valid identifier, i.e. matches ``[A-Za-z0-9_]*``)

Note: this requires that you actually have an array or object. You might need to use the ``parseJson`` function (see above paragraph about typing)

Object notations
===================

For all functions, you can use them the "regular" way: ``replace(str, 'a', 'b')`` or in the "object" way: ``str.replace('a', 'b')``

In object notation, the first argument to the function is replaced by its 'context'.

For example, the two syntaxes are equivalent:

.. code-block:: javascript

	length(trim(replace(foo, 'a', 'b')))

	foo.replace('a', 'b').trim().length()


DSS variables
=============

You can retrieve the value of DSS variables via the syntax ``${variable_name}`` or ``variables["variable_name"]``. Both syntaxes have slightly different behaviors.

variables["variable_name"]
--------------------------

DSS evaluates ``variables["variable_name"]`` as JSON during the formula evaluation. If there is no variable defined with the supplied name, an empty cell is returned.

For example, given the following global variables

.. code-block:: json

	{
		"max_height": 500,
		"warning_msg": "too tall",
		"msgs": {"ok":"OK", "over":"too tall"}
	}

The formula ``if(height < variables["max_height"], "OK", variables["warning_msg"])`` is evaluated as ``if(height < 500.0, "OK", "too tall")``. Note that the max_height is evaluated as 500.0 as JSON consider all numbers to be decimal.

The formula ``if(height < variables["max_height"], "OK", variables["msgs"]["over"])`` is evaluated as ``if(height < 500.0, "OK", "too tall")``.

${variable_name}
----------------
During processing DSS replaces the ``${variable_name}`` placeholder with its verbatim content and then evaluate the formula. If there is no variable defined with the supplied name, an error is returned.

For example, given the following global variables:

.. code-block:: json

	{
		"max_height": 500,
		"warning_msg": "too tall",
		"msgs": {"ok":"OK", "over":"too tall"}
	}

The formula ``if(height < ${max_height}, "OK", "${warning_msg}")`` is converted into ``if(height < 500, "OK", "too tall")`` before being evaluated. Note that quotes have been added around ${warning_msg} to output an actual string.

The formula ``if(height < ${max_height}, "OK", ${warning_msg})`` is converted into ``if(height < 500, "OK", too tall)`` before being evaluated and will therefore issue a syntax error.

The formula ``if(height < ${max_height}, "OK", ${msgs}["over"])`` is converted into ``if(height < 500, "OK", {"ok":"OK", "over":"too tall"}["over"])`` before being evaluated and will therefore issue a syntax error.

The formula ``if(height < ${max_height}, "OK", ${msgs.over})`` will throw a syntax error as there is no variable named "msgs.over".

The formula ``if(height < ${max_height}, "OK", parseJson('${msgs}')["over"])`` is converted into ``if(height < 500, "OK", parseJson('{"ok":"OK", "over":"too tall"}')["over"])`` before being evaluated and will be evaluated as ``if(height < 500.0, "OK", "too tall")``.

Array functions
===============

**arrayContains(array a, item)** *boolean*

	Returns whether the array ``a`` contains ``item``

		``arrayContains([1, 2, 3], 5)`` returns ``false``

**arrayDedup(array a)** *array*

	Returns array a with duplicates removed

		``arrayDedup([0, 1, 0, 7])`` returns ``[0,1,7]``

**arrayIndexOf(array a, item)** *int*

	Returns the index (starting from 0) of ``item`` in the array ``a``, or -1 if the item is not found in the array.

		``arrayIndexOf([1 , 0],  2)`` returns ``-1``

**arrayLen(array a)** *int*

	Returns the length of the array ``a``

		``arrayLen([1,2,3])`` returns ``3``

**arrayReverse(array a)** *array*

	Reverses array a

		``arrayReverse([1,2,3])`` returns ``[3,2,1]``

**arraySort(array a)** *array*

	Sorts array ``a``

		``arraySort(["b", "1", "a"])`` returns ``["1","a","b"]``


**get(array a, from index, [to index])** *Output depends on arguments*

	Returns ``o[from, to]``. Omitting the optional number *to* will return what is at the first index specified.

		``get([1,2,3,4,5], 1, 4)`` returns ``[2,3,4]``

		``get([1,2,3,4,5], 1)`` returns ``2``

**join(array a, string sep)** *string*

	Returns the string obtained by joining the elements of array ``a`` with the separator ``sep``

	For example, the expression ``join(date_elements, '-')`` on a column ``date_elements`` produces:

		+---------------+-------------+
		+ date_elements + output      +
		+===============+=============+
		+ [2007, 7, 15] + 2007-7-15   +
		+---------------+-------------+
		+ [2016, 1, 8]  + 2016-1-8    +
		+---------------+-------------+

**objectKeys(object o)** *array*

	Returns the keys of an object as an array

**objectValues(object o)** *array*

	Returns the values of an object as an array

**slice(object o, from index, [to index])** *Output depends on arguments*

	If ``o`` is an array, returns an array containing the items between ``from`` and ``to`` (excluded). If ``o`` is a string, returns the part of the string between ``from`` and ``to`` (excluded). Omitting the optional number *to* will return the remainder of the string or array. Note: ``slice`` and ``substring`` are identical.

		``slice([1,2,3,4,5], 1, 4)`` returns ``[2,3,4]``

		``slice('hello', 1)`` returns ``'ello'``

**substring(object o, from index, [to index])** *Output depends on arguments*

	If ``o`` is a string, returns the part of the string between ``from`` and ``to`` (excluded). If ``o`` is an array, returns an array containing the items between ``from`` and ``to`` (excluded). Omitting the optional number *to* will return the remainder of the string or array. Note: ``substring`` and ``slice`` are identical.

	 	``substring('0123456', 2, 5)`` returns ``'234'``

	 	``substring([1,2,3,4,5,6], 3)`` returns ``[4,5,6]``

Boolean functions
=================

**asBool(o)** *boolean*

	Returns ``o`` converted to a boolean.

		``asBool(0)`` returns ``false``

		``asBool('yes')`` returns ``true``

**isFalse(boolean b)** *boolean*

	Returns whether ``b`` is false.

		``isFalse('false')`` returns ``false`` (the argument is a string, not a boolean, so this method returns ``false``)

		``isFalse(asBool(0))`` returns ``true``

**isTrue(boolean b)** *boolean*

	Returns whether ``b`` is true.

		``isTrue('true')`` returns ``false`` (the argument is a string, not a boolean, so this method returns ``false``)

		``isTrue(asBool(1))`` returns ``true``

**and(boolean a, boolean b)** *boolean*

	Evaluates logical AND (conjunction) on several statements. All conditions need to be fulfilled for the function to return true. Is equivalent to ``a && b``.

		``and(1==1, 3<4)`` returns ``true``

**not(boolean b)** *boolean*

	Evaluates logical NOT (negation) of a statement, returning the opposite of ``b``.

		``not(1!=1)`` returns ``false``

**or(boolean a, boolean b)** *boolean*

	Evaluates logical OR (disjunction) on several statements. At least one condition needs to be fulfilled for the function to return true. Is equivalent to ``a || b``.

		``or(1==1, 3>4)`` returns ``true``

Date functions
==============

**asDatetimeTz(object o, [format1, ...])** *datetime tz*

	Returns ``o`` converted to ``datetime tz`` (date/time with time zone), based on the format(s) provided. If your column contains more than one date format, you can give an ordered list of possible formats. If you don't give a format, ISO-8601 is used by default (`see more examples of the syntax for ISO-8601 <https://www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html>`_). Here is some example syntax:

	* 'y' (Year)
	* 'M' (month in year)
	* 'w' (week in year)
	* 'W' (week in month)
	* 'd' (day in month)
	* 'D' (day in year)
	* 'E' (day name in week)
	* 'e' (day number in week. Monday =1)
	* 'H' (hour in day, 0-23)
	* 'm' (minute)
	* 's' (second)
	* 'S' (millisecond)


		``asDatetimeTz('2020-04-15', 'yyyy-MM-dd')`` returns ``2020-04-15T00:00:00.000Z``

    .. note::

        The format arguments are ignored when using the SQL engine.

**asDatetimeNoTz(object o, [format1, ...])** *datetime no tz*

	Returns ``o`` converted to ``datetime no tz`` (date/time without time zone), based on the format(s) provided. If your column contains more than one date format, you can give an ordered list of possible formats. If you don't give a format, ``yyyy-MM-dd HH:mm:ss`` is used by default (`see more examples of the syntax for ISO-8601 <https://www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html>`_). Here is some example syntax:

	* 'y' (Year)
	* 'M' (month in year)
	* 'w' (week in year)
	* 'W' (week in month)
	* 'd' (day in month)
	* 'D' (day in year)
	* 'E' (day name in week)
	* 'e' (day number in week. Monday =1)
	* 'H' (hour in day, 0-23)
	* 'm' (minute)
	* 's' (second)
	* 'S' (millisecond)


		``asDatetimeNoTz('2020-04-15', 'yyyy-MM-dd')`` returns ``2020-04-15 00:00:00.000``

    .. note::

        The format arguments are ignored when using the SQL engine.

**asDateOnly(object o, [format1, ...])** *date only*

	Returns ``o`` converted to ``date only`` (Gregorian calendar date), based on the format(s) provided. If your column contains more than one date format, you can give an ordered list of possible formats. If you don't give a format, ISO-8601 is used by default (`see more examples of the syntax for ISO-8601 <https://www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html>`_). Here is some example syntax:

	* 'y' (Year)
	* 'M' (month in year)
	* 'w' (week in year)
	* 'W' (week in month)
	* 'd' (day in month)
	* 'D' (day in year)
	* 'E' (day name in week)
	* 'e' (day number in week. Monday =1)
	
		``asDateOnly('2020-04-15', 'yyyy-MM-dd')`` returns ``2020-04-15``

    .. note::

        The format arguments are ignored when using the SQL engine.

**datePart(date d, string part, [timezone])** *Output depends on arguments*

	Extracts a date component from ``date d`` (`date` being either `datetime tz`, `datetime no tz` or `date only`).  Returned date components are always in local timezone--unless the optional ``timezone`` is included--and in English (`see a complete list of supported timezones.  <http://joda-time.sourceforge.net/timezones.html>`_). The available components are:

	* ‘years’ (or ‘year’)
	* 'isoWeekYear' gives the ISO week-numbering year
	* ‘months’ (or ‘month’)
	* 'weekOfYear' gives the week of the year (as per server locale's convention)
	* 'isoWeekOfYear' gives the ISO week number of the year
	* ‘weeks’ (or ‘week’ or ‘w’)
	* 'isoWeekOfMonth' gives the ISO week number of the month
	* ‘days’ (or ‘day’ or ‘d’)
	* ‘weekday’ (the name of the day of the week, capitalized)
	* 'dayofweek' (day of the week as a number. Monday=1, Tuesday=2, ... Sunday=7)
	* ‘hours’ (or ‘hour’ or ‘h’)
	* ‘minutes’ (or ‘minute’ or ‘min’)
	* ‘seconds’ (or ‘second’ or ‘s’)
	* 'unixTime' (number of seconds since epoch)
	* 'millisecond' (or 'millisecond', or 'ms')
	* ‘time’ (number of milliseconds since epoch)


		``datePart('2020-04-15T00:00:00.000Z', 'weekday')`` returns ``"Wednesday"``

		``datePart('2020-01-01T00:00:00.000Z', 'year', '-08:00')`` returns ``2019``

**diff(date d1, date d2, [string unit])** *number*

	Returns the difference between two dates expressed in given time units. The default unit of time is ``days``. The available units are:

	* ‘years’ (or ‘year’)
	* ‘months’ (or ‘month’)
	* ‘weeks’ (or ‘week’ or ‘w’)
	* ‘days’ (or ‘day’ or ‘d’)
	* ‘hours’ (or ‘hour’ or ‘h’)
	* ‘minutes’ (or ‘minute’ or ‘min’)
	* ‘seconds’ (or ‘second’ or ‘s’)

		``diff('2019-03-15T00:00:00.000Z', '2020-04-15T00:00:00.000Z', 'month')`` returns ``-13``

		``diff('2019-03-15 11:17:59', '2019-03-15 11:12:13', 'min')`` returns ``5``

		``diff('2019-03-01', '2019-02-01', 'days')`` returns ``28``

**inc(date d, number value, string unit)** *datetime tz, datetime no tz or date only depending on arguments*

	Returns ``d`` incremented or decremented by the number value in the specified unit of time; a decimal number value will be truncated to an integer. The available units are:

	* ‘years’ (or ‘year’)
	* ‘months’ (or ‘month’)
	* ‘weeks’ (or ‘week’ or ‘w’)
	* ‘days’ (or ‘day’ or ‘d’)
	* ‘hours’ (or ‘hour’ or ‘h’)
	* ‘minutes’ (or ‘minute’ or ‘min’)
	* ‘seconds’ (or ‘second’ or ‘s’)

		``inc('2020-04-15T00:00:00.000Z', -3, 'week')`` returns ``2020-03-25T00:00:00.000Z``

		``inc('2020-04-15', 2, 'days')`` returns ``2020-04-17``

**now()** *datetime tz*

	Returns the current time

**trunc(date d, string unit)** *datetime tz, datetime no tz or date only depending on arguments*

	Returns ``d`` truncated to the unit specified.
	The available units are:

	* ‘years’ (or ‘year’)
	* ‘months’ (or ‘month’)
	* ‘weeks’ (or ‘week’ or ‘w’)
	* ‘days’ (or ‘day’ or ‘d’)
	* ‘hours’ (or ‘hour’ or ‘h’)
	* ‘minutes’ (or ‘minute’ or ‘min’)
	* ‘seconds’ (or ‘second’ or ‘s’)

		``trunc('2020-04-03T07:47:45.245Z', 'month')`` returns ``2020-04-01T00:00:00.000Z``

		``trunc('2020-04-03', 'month')`` returns ``2020-04-01``

Math functions
==============

**abs(number d)** *number*

	Returns the absolute value of a number

		``abs(-7)`` returns ``7.0``

**acos(number d)** *number*

	Returns the arc cosine of an angle, in the range 0 through PI

		``acos(-1)`` returns ``3.141592654``

**asin(number d)** *number*

	Returns the arc sine of an angle in the range of -PI/2 through PI/2

		``asin(1)`` returns ``1.570796327``

**atan(number d)** *number*

	Returns the arc tangent of an angle in the range of -PI/2 through PI/2

**atan2(number x, number y)** *number theta*

	Converts rectangular coordinates (x, y) to polar (r, theta)

**avg(number n1, number n2, ...)** *number*

	Returns the average of a series of numbers, including numeric strings (e.g., "4.5"), while ignoring empty elements.

		``avg(1, "2", 3, "")`` returns ``2.0``

**ceil(number n)** *number*

	Returns the ceiling of a number

		``ceil(4.67)`` returns ``5``

		``ceil(-4.67)`` returns ``-4``

**combin(number n, number k)** *number*

	Returns the number of combinations for n elements divided into groups of k, *n!/k!(n-k)!*

		``combin(6, 2)`` returns ``15``

**cos(number d)** *number*

	Returns the trigonometric cosine of an angle

		``cos(0)`` returns ``1.0``

**cosh(number d)** *number*

	Returns the hyperbolic cosine of a value

		``cosh(0)`` returns ``1.0``

**dec2hex(long)** *string*

	Returns an hexadecimal representation of the input number

		``dec2hex(10)`` returns ``a``
		``dec2hex(256)`` returns ``100``


**degrees(number d)** *number*

	Converts an angle from radians to degrees.

		``degrees(PI())`` returns ``180.0``

**even(number n)** *number*

	Rounds the number up to the nearest even integer

		``even(3)`` returns ``4.0``

		``even(2.3)`` returns ``4.0``

		``even(-2.3)`` returns ``-2.0``

		``even(-3)`` returns ``-2.0``

**exp(number n)** *number*

	Returns the exponential of a number

		``exp(2)`` returns ``7.38905609893065``

**fact(number i)** *number*

	Returns the factorial of a number i

		``fact(4)`` returns ``24``

**factn(number i, number d)** *number*

	Returns the factorial of a number i, omitting every dth item from the multiplication

		``factn(7, 3)`` returns ``28``

**floor(number d)** *number*

	Returns the floor of a number

		``floor(4.7)`` returns ``4``

**gcd(number d, number e)** *number*

	Returns the greatest common denominator of the two numbers

		``gcd(21, 28)`` returns ``7.0``

**hash(string)** *long*

	Returns a 64 bits numerical hash of the input (not crypto-secure)

		``hash("goo")`` returns ``2774880816139997119``

**hex2dec(string)** *long*

	Returns a decimal representation of an hexadecimal string

		``hex2dec("a")`` returns ``10``

**lcm(number d, number e)** *number*

	Returns the least common multiple of the two numbers

		``lcm(20, 42)`` returns ``420.0``

**ln(number n)** *number*

	Returns the natural log of a number

		``ln(exp(1))`` returns ``1.0``
		``ln(2.72)`` returns ``1.000631880307906``

**log(number n)** *number*

	Returns the base 10 log of a number

		``log(100)`` returns ``2.0``

**max(a, b, ...)** *Output depends on arguments*

	Returns the greater of two or more numbers, two or more strings, or the more recent of two or more dates

		``max(-1, 3)`` returns ``3``

		``max('luke', 'leia')`` returns ``'luke'``

		``max('2020-01-01T00:00:00.000Z', '2021-01-01T00:00:00.000Z')`` returns ``2021-01-01T00:00:00.000Z``

**min(a, b, ...)** *number*

	Returns the smaller of two or more numbers, two or more strings, or older of two or more dates

		``min(-1, 3)`` returns ``-1.0``

		``min('luke', 'leia')`` returns ``'leia'``

		``min('2020-01-01T00:00:00.000Z', '2021-01-01T00:00:00.000Z')`` returns ``2020-01-01T00:00:00.000Z``

**mod(number a, number b)** *number*

	Returns a modulus b

		``mod(5, 3)`` returns ``2``

		``mod(7.8, 3)`` returns ``1``

**multinomial(number d1, number d2 ...)** *number*

	Returns the multinomial of a series of numbers, ``(sum(d1, d2, d3,...))! / d1! * d2! * d3! ...``

		``multinomial(1, 1, 2, 1)`` returns ``60``

**odd(number d)** *number*

	Rounds the number up to the nearest odd integer

		``odd(5.3)`` returns ``7.0``

		``odd(-5.3)`` returns ``-5.0``

**PI()** *number*

	Returns the value of PI

**pow(number a, number b)** *number*

	Returns ``a`` to the power of ``b``

		``pow(2, -1)`` returns ``0.5``

**quotient(number numerator, number denominator)** *number*

	Returns the integer portion of a division

		``quotient(7, 2)`` returns ``3.0``

**radians(number d)** *number*

	Converts an angle in degrees to radians

		``radians(180)`` returns ``3.141592653589793``

**rand([long min], [long max])** *double or long*

	Without arguments, returns a random float between 0 and 1. With two positive long integers as ``min`` and ``max`` arguments, returns a random long integer between ``min`` (inclusive) and ``max`` (exclusive)

**round(number n)** *number*

	Returns the rounding of number to the nearest integer

		``round(3.5)`` returns ``4.0``

		``round(-3.5)`` returns ``-3.0``

**sin(number d)** *number*

	Returns the trigonometric sine of an angle

		``sin(radians(90))`` returns ``1.0``

**sinh(number d)** *number*

	Returns the hyperbolic sine of an angle

		``sinh(0)`` returns ``0.0``

**sqrt(number n)** *number*

	Returns the square root of number n.

		``sqrt(81)`` returns ``9.0``

**sum(array a)** *number*

	Sums the numbers of an array. Skips non-number elements from the array.

		``sum([1, 2, "string", 3])`` returns ``6.0``

**tan(number d)** *number*

	Returns the trigonometric tangent of an angle

		``tan(0)`` returns ``0.0``

**tanh(number d)** *number*

	Returns the hyperbolic tangent of a value

**toNumber(o)** *number*

	Returns o converted to a number

		``toNumber("5")`` returns ``5``

Object functions
================

**get(object o, string field, [string defaultValue])** *Output depends on arguments*

	Returns ``o[from]``. If ``o[from]`` is empty and ``default`` has been provided, returns ``default``.

		``get(parseJson('{"name":"joe", "age":42}'), "age")`` returns ``42``

		``get(parseJson('{"name":"joe"'), "age", 37)`` returns ``37``

**hasField(object o, string name)** *boolean*

	Returns whether ``o`` has the field ``name``

		``hasField(parseJson('{""name"": ""joe"", ""age"": 42 }'), ""age"")`` returns ``true``

**htmlAttr(Element e, String s)** *string*

	Selects a value from an attribute on an Html Element

**htmlText(Element e)** *string*

	Selects the text from within an element (including all child elements)

		``htmlAttr(select(parseHtml('<div><a href="www.dataiku.com"></div>'), '[href]')[0], "href")`` returns ``"www.dataiku.com"``

**innerHtml(Element e)** *string*

	The innerHtml of an HTML element

**jsonize(value)** *JSON literal value*

	Quotes a value as a JSON literal value

**objectDel(object o, key, [key...])** *object*

	Removes one or several keys from an object and returns it. The keys must not be null

		``objectDel(parseJson('{"firstName": "birdie", "company": "Dataiku" }'), 'firstName')`` returns ``{"company":"Dataiku"}``

**objectNew(k1, v1, k2, v2, ...)** *object*

	Creates a new object, optionally pre-filled with key/values.
	Must get an even number of arguments, as successive key-value pairs.
	Giving 0 arguments is possible and will return an empty object (you can use objectPut to add to it)

		``objectNew("firstName", "birdie", "company", "Dataiku")`` returns ``{"firstName": "birdie", "company": "Dataiku" }``

**objectPut(object o, key, value)** *object*

	Adds a key/value pair to an object and returns it. The key must not be null

**ownText(Element e)** *string*

	Gets the text owned by this HTML element only; does not get the combined text of all children.

**parseHtml(string s)** *HTML object*

	Parses a string as HTML

**parseJson(string s)** *object or array*

	Parses a JSON string as an object or array

**select(Element e, String s)** *HTML Elements*

	Selects an element from an HTML elementn using selector syntax

**type(object o)** *string*

	Returns the type of ``o``

		``type(3.126)`` returns ``number``

String functions
================

**char(number value)** *string*

    Returns the character that represents the specified unicode of ``value``.

       ``char(65)`` returns ``"A"``

**chomp(string s, string tail)** *string*

	Removes ``tail`` from the end of ``s`` if it’s there, otherwise leaves it alone.

		``chomp("foobar", "bar")`` returns ``"foo"``

**coalesce(value1, value2, ...)** *Output depends on arguments*

	Returns the first non-empty value.

		``coalesce("", "foo")`` returns ``"foo"``

**concat((object a1, [object a2, ...]))** *Output depends on arguments*

	Returns a string of concatenated values. If one of your columns contains leading 0 (zeros), wrap it in a ``strval('column_name')`` to preserve them.

		``concat("Birds", " ", "fly")`` returns ``"Birds fly"``

		``concat(1, 2, 3)`` returns ``"123"``


**contains(string s, string frag)** *boolean*

	Returns whether ``s`` contains ``frag``

		``contains("hello world ", "llo")`` returns ``true``

**endsWith(string s, string tail)** *boolean*

	Returns whether ``s`` ends with ``tail``

		``endsWith("hello world", "rld")`` returns ``true``

**escape(string s, string mode)** *string*

	Escapes a ``s`` using the escaping mode specified. Supported modes: *'html', 'xml', 'csv', 'url', javascript'*. Note that the escape uses the standard java URLEncoder for urls and StringEscapeUtils for others

**format(string format, object... args)** *string*

	Formats a string using printf-like formatting using the `Java Formatter syntax <https://docs.oracle.com/javase/7/docs/api/java/util/Formatter.html#summary>`_.

		``'%4d-%02d'.format(2004,2)`` returns ``'2004-02'``

**fromBase64(string s, [string charset])** *string*

	Returns the string whose Base64 representation is given. By default, the string is read using the UTF-8 charset.

		``fromBase64('SA==')`` returns ``"H"``

**get(string s, from index, [to index])** *Output depends on arguments*

	Returns ``s.substring(from, to)``. Omitting the optional number *to* will return what is at the first index specified.

		``get('Oh no, kittens!', 0, 5)`` returns ``'Oh no'``

		``get('Oh no, kittens!', 1)`` returns ``'h'``

**indexOf(string s, string sub)** *number*

	Returns the index of the first occurrence of ``sub`` in ``s``. Index begins at 0. Returns -1 if there is no such occurrence.

		``indexOf("hello world", "world")`` returns ``6``

**lastIndexOf(string s, string sub)** *number*

	Returns the index of the last occurrence of ``sub`` in ``s``. Index begins at 0. Returns -1 if there is no such occurrence.

		``lastIndexOf("hello world", "o")`` returns ``7``

**length(array or string o)** *number*

	Returns the length of o

		``length("hello world")`` returns ``11``

		``length([4,5,6])`` returns ``3``

**match(string a, string or regexp)** *array of strings*

	Returns an array of the matching groups found in ``s``. Groups are designated by () within the specified string or regular expression.

		``match('hello world', 'he(.*)wo(rl)d')`` returns ``["llo ","rl"]``

**md5(string s)** *string*

	Returns the MD5 hash of a string

		``md5('hi')`` returns ``"49f68a5c8493ec2c0bf489821c21fc3b"``

**ord(string s)** *number*

    Returns the number representing the unicode code of a specified character in ``s``. The ``s`` string must contain only one character.

       ``ord('A')`` returns ``65``

**partition(string s, string or regex frag, [boolean omitFragment])** *array*

	Returns an array of strings ``[a,frag,b]`` where ``a`` is the part before the first occurrence of ``frag`` in ``s`` and ``b`` is the part after the occurrence. If ``omitFragment`` is true, ``frag`` is not returned in the array.

		``partition(""hello"", ""he"")`` returns ``["""",""he"",""llo""]``

		``partition(""hello"", ""he"", asBool(1))`` returns ``["""",""llo""]``

		``partition(""hello"", /.l/)"`` returns ``[""h"",""el"",""lo""]``

**replace(string s, string or regex f, string replacement)** *string*

	Replaces all occurrences of substring / regex  ``f`` found in string ``s`` with the ``replacement`` string.

		``replace('hello world', 'hel', 'a')`` returns ``"alo world"``

		``replace(""Oh my!"", /\w/, 'x')`` returns ``"xx xx!"``


**replaceChars(string s, string f, string r)** *string*

	Returns the string obtained by replacing all character in ``s`` that match ``f`` with the character in ``r`` at that same position. The function can be used to delete characters by replacing them with nothing.

		``replaceChars('abcba', 'bc', 'BC')`` returns ``aBCBa``
		``replaceChars('abcba', 'bc', 'Z')`` returns ``aZZa``

**rpartition(string s, string or regex frag, [boolean omitFragment])** *array*

	Returns an array of strings ``[a,frag,b]`` where ``a`` is the part before the last occurrence of ``frag`` in ``s`` and ``b`` is the part after the occurrence. If ``omitFragment`` is true, ``frag`` is not returned in the array.

		``rpartition("hello world", "o")`` returns ``["hello w","o","rld"]``

**sha1(string s)** *string*

	Returns the SHA-1 hash of a string

		``sha1('goo')`` returns ``3f95edc0399d06d4b84e7811dd79272c69c8ed3a``

**sha256(string s)** *string*

	Returns the SHA-256 hash of a string

**sha512(string s)** *string*

	Returns the SHA-512 hash of a string

**split(string s, string or regex sep, [boolean preserveAllTokens])** *array*

	Returns the array of strings obtained by splitting ``s`` with separator ``sep``. If ``preserveAllTokens`` is true, then empty segments are preserved.

		``split(""hello"", ""he"")`` returns ``[""llo""]``

		``split(""hello"", ""he"", asBool(1))`` returns ``["""",""llo""]``

		``split(""hello"", /.l/)`` returns ``[""h"",""lo""]``

		``split("Hello world!", /\s+/)`` returns ``["Hello","world!"]``

**splitByCharType(string s)** *array*

	Returns an array of strings obtained by splitting s grouping consecutive chars by their unicode type

		``splitByCharType("Hello_world 101!?!")`` returns ``["H","ello","_","world"," ","101","!?!"]``

**splitByLengths(string s, number length1, [...])** *array*

	Returns an array of strings obtained by splitting ``s`` into substrings, each with its own specified length.

		``splitByLengths("Hello world", 1, 2, 3, 4)`` returns ``["H","el","lo ","worl"]``

**startsWith(string s, string sub)** *boolean*

	Returns whether ``s`` starts with ``sub``

		``startsWith("Hello world", "He")`` returns ``true``

**strip(string s)** *string*

	Returns copy of the string, with leading and trailing whitespace omitted. This function is the same as trim.

		``strip(" Hello World ")`` returns ``"Hello World"``

**toBase64(string s, [string charset])** *string*

	Returns the Base64 representation of a string. By default, the string is written using the UTF-8 charset.

		``toBase64("H")`` returns ``"SA=="``

**toLowercase(string s)** *string*

	Converts a string to lowercase

		``toLowercase("HELLO WORLD")`` returns ``"hello world"``

**toString(o, string format (optional))** *string*

	Returns o converted to a string

		``toString(5)`` returns ``"5"``

**toTitlecase(string s)** *string*

	Converts a string to titlecase

		``toTitlecase("hello world")`` returns ``"Hello World"``

**toUppercase(string s)** *string*

	Converts a string to uppercase

		``toUppercase("hello world")`` returns ``"HELLO WORLD"``

**trim(string s)** *string*

	Returns copy of the string, with leading and trailing whitespace omitted.

		``trim(" Hello World ")`` returns ``"Hello World"``

**unescape(string s, string mode)** *string*

	Unescapes all escaped parts of the string depending on the given escaping mode. Available modes: 'html', 'xml', 'csv', 'url', 'javascript'

**unicode(string s)** *string*

	Returns the input string as an array of the unicode codepoints (numbers)

		``unicode("Hi!")`` returns ``[72,105,33]``

**unicodeType(string s)** *string*

	Returns an array of strings describing each character of the input string in their full unicode notation

		``unicodeType("y 0H?")`` returns ``["lowercase letter","space separator","decimal digit number","uppercase letter","other punctuation"]``

**uuid()** *string*

	Returns a type 4 (pseudo randomly generated) UUID.
	The UUID is generated using a cryptographically strong pseudo random number generator.

		``uuid()`` returns ``7af14645-bcd9-4af2-bca8-390fc67e9a0b``



.. _formula-index-geometry:

Geometry functions
======================

.. _formula-index-geobuffer:

**geoBuffer(geometry geom, double distance, [int quadrantSegment])** *string*

    Returns a geometry that represents all points whose distance from this geometry is less than or equal to ``distance``.
    The ``distance`` parameter can be either a value or a column name from the dataset. The distance unit depends on the
    CRS of the given geometries (e.g., degrees for SRID=4326). A negative distance can be used with polygons,
    which will shrink the polygon rather than expand it. Specify an optional ``quadrantSegment`` value to set the
    number of segments to approximate a quarter circle (the default is 8)

.. _formula-index-geocontains:

**geoContains(geometry geomA, geometry geomB)** *bool*


    Compute the boolean {geomA `contains` geomB} for two input geometries A and B.


    The implementation of this function depends on the engine it is run on but its definition is standard: "Geometry A contains Geometry B if and only if no points of B lie in the exterior of A, and at least one point of the interior of B lies in the interior of A." (https://postgis.net/docs/ST_Contains.html)


    A polygon A does not contain a point B if B is exactly on its boundary.


    ``geoContains("POLYGON((0 0,3 0,0 3,0 0))", "POINT(1 1)")`` returns ``true``


    ``geoContains("POLYGON((0 0,3 0,0 3,0 0))", geometry)`` returns the evaluation of the boolean predicate for each input geometry row of dataset column `geometry`

.. image:: img/geoContains-formula-screenshot.png


.. _formula-index-geoenvelope:

**geoEnvelope(geometry geom)** *string*

    Returns the envelope of a geometry, i.e., the minimum bounding box containing this geometry.

.. _formula-index-geomakevalid:

**geoMakeValid(geometry geom)** *string*

    Returns a valid representation of an invalid geometry. Valid geometries remain unchanged.

    .. note::

        This function can return slightly different results whether the recipe engine is PostgreSQL or a local stream.
        If the method is unable to make a geometry valid, it returns an empty cell.

.. _formula-index-geosimplify:

**geoSimplify(geometry geom, double toleranceDistance)** *string*

    Returns a simpler geometry based on the Douglas-Peucker algorithm, with respect to a non-negative
    ``toleranceDistance`` parameter. The simplification of the geometry will result in a geometry with fewer vertices.
    A vertex is removed only if the distance between this vertex and the edge
    resulting from removing this vertex is within the specified ``toleranceDistance``.
    The ``toleranceDistance`` parameter can be either a value or a column name from the dataset.
    The toleranceDistance unit depends on the CRS of the given geometries (e.g., degrees for SRID=4326).


.. _formula-index-geowithin:

**geoWithin(geometry geomA, geometry geomB)** *bool*
    Returns a result opposite to **geoContains** (see above).  **geomA** is within **geomB** if **geomB** contains **geomA**.


.. _formula-index-geodistance:

**geoDistance(geopoint geoPointA, geopoint geoPointB, string unit)** *number*
	Compute the distance between two geographical points. The available units are: ``KILOMETERS``, ``MILES``.


Value access functions
======================

**numval(object o, [number offset])** *number*

	Returns the numerical value of a column. If the value is not numerical, an empty value is returned. Specify an optional `Offset argument`_ to return the value of a previous row.

	.. note::

		Use numval when your column name contains spaces or periods to ensure DSS parses it properly as in ``numval("my.column")`` or ``numval("my column")``.
		Remember to always write the column name in "quotes" when using numval.


**strval(object o, [string defaultValue], [number offset])** *string*

	Returns the string value of a column. If the value is not a string, an empty value is returned. Specify an optional defaultValue to replace empty cells with defaultValue. Specify an optional `Offset argument`_ to return the value of a previous row.

	.. note::

		Use strval when your column name contains spaces or periods to ensure DSS parses it properly as in ``strval("my.column")`` or ``strval("my column")``.
		Remember to always write the column name in "quotes" when using strval.

**val(object o, [string defaultValue], [number offset])** *Output depends on argument*

	Returns the value of a column. Specify an optional defaultValue to replace empty cells with defaultValue. The type of the resulting column is auto-detected (use strval or numval to force it). Specify an optional `Offset argument`_ to return the value of a previous row.

	.. note::

		Use val when your column name contains spaces or periods to ensure DSS parses it properly as in ``val("my.column")`` or ``val("my column")``. 
		Remember to always write the column name in "quotes" when using val.

Offset argument
----------------

.. note::

		The offset argument is only available in the Prepare recipe and only with the DSS engine.


* Set offset to ``1`` to retrieve a value from the previous row
* Set offset to ``2`` to retrieve a value from two rows before the current row
* ...
* Set offset to ``0`` to retrieve a value from the current row
* An error is returned if offset is set to a negative value

Control structures
===================

Control structures allow you to perform advanced operations.

Beware: control structures cannot use object notation !

**filter(array a, variable v, expression e)** *array*

	Evaluates expression a to an array. Then for each array element, binds its value to variable name v, evaluates expression e, and pushes the result onto the result array if the result is truish.

		``filter(['aa', 'bb', 'cc', 'ab', 'bc'], item, item.startsWith('a'))`` returns ``["aa","ab"]``

	.. note::

		``filter(myarray, v, v < 2)`` is equivalent to this Python syntax: ``[v for v in myarray if v < 2]``
		and returns the array with only the elements below 2

**forEach(array a, variable v, expression e)** *array*

	Evaluates expression a to an array. Then for each array element, binds its value to variable name v, evaluates expression e, and pushes the result onto the result array.

		``forEach(['aa', 'bb', 'cc', 'ab', 'bc'], item, item.startsWith('a'))`` returns ``[true,false,false,true,false]``

	.. note::

		``forEach(myarray, v, v + 2)`` is equivalent to this Python syntax: ``[v+2 for v in myarray]``

**forEachIndex(array a, variable i, variable v, expression e)** *array*

	Evaluates expression a to an array. Then for each array element, binds its value to variable name v and its index to variable name i, evaluates expression e, and pushes the result onto the result array.

		``forEachIndex(['aa', 'bb', 'cc', 'ab', 'bc'], index, item, index < 2 || item.startsWith('a'))`` returns ``[true,true,false,true,false]``

	.. note::

		``forEachIndex(myarray, i, v, v + i)`` is equivalent to this Javascript syntax: ``myarray.map(function(v, i) { return v+i ;})``

**forRange(from, to, step, variable v, expression e)** *array*

	Iterates, starting at ``from``, incrementing by ``step`` each time while less than ``to`` (or while more than ``to`` if ``step < 0``). At each iteration, binds the variable ``v`` to the iteration value, evaluates expression ``e``, and pushes the result onto the result array.

		``forRange(0, 21, 3, v, v)`` returns ``[0,3,6,9,12,15,18]``
		``forRange(0, 21, 3, v, v*5)`` returns ``[0,15,30,45,60,75,90]``

	.. note::

		``forRange(0, 100, 3, v, v * 2)`` is equivalent to this Python syntax: ``[v * 2 for v in xrange(0, 100, 3)]`` and returns [0, 6, 12, 18 .... 198]

**if(boolean, expression_true, expression_false)** *Output depends on expression*

	Evaluates to ``expression_true`` if the condition is ``true``, to ``expression_false`` otherwise

		``if(3>2, "I heart #s", "my brain hurts")`` returns ``"I heart #s"``

**objectFilter(expression a, variable k, variable v, expression test)** *object*

	Evaluates expression a to an object. Then for each element (k, v) of this object, binds its key to variable name k, its value to variable name v, evaluates expression test which should return a boolean. If the boolean is true, pushes (k, v) onto the result object.

		``objectFilter('{"fName":"Joe", "lName":"Smith", "age":42 }', k, v, k.contains("Name"))`` returns ``{"fName":"Joe","lName":"Smith"}``

**switch(expression_to_match, match_1, return_1, match_2, return_2, ..., [return_default])** *Output depends on expression*

	Compares ``expression_to_match`` to ``match_1``, then to ``match_2``, etc. When match is found, returns the corresponding ``return_i``. If no match is found, returns ``return_default``, or nothing if there is no ``return_default``.

		``switch("Paris", "Paris", 1, "New York", 2, 0)`` returns ``1``

		``switch("Berlin", "Paris", "1", "New York", "2", "Other")`` returns ``"Other"``

                ``switch(col1, col2+col3, "sum",  "Other")`` returns ``"sum" if value of column col1 equals value of col2+col3, "Other" otherwise``

                ``switch("true", col1 >= 10, "good", col1 >= 5 "okay", "bad")`` returns ``"good", "okay", or "bad" depending on col1 value``

**with(expression o, variable v, expression e)** *Output depends on expression*

	Evaluates expression o and binds its value to variable name v. Then evaluates expression e and returns that result. The ``with`` control allows you to "split" a very big expression into more manageable chunks. It also makes reusing the result of a complex computation easier to read and faster to process.

		``with("european union".split(" "), a, a.length())`` returns ``2``

		``with("european union".split(" "), a, forEach(a, v, v.length()))`` returns ``[8,5]``

Tests
======

Beware: tests cannot use object notation

**isBlank(expression o)** *boolean*

	Returns whether ``o`` is null or an empty string. IsBlank() returns true when value is null or empty ("").
	It does not consider a string made of blank spaces as blank; it considers an expression with an error as blank.

		``isBlank("")`` returns ``true``

		``isBlank(" ")`` returns ``false``

		``isBlank(abs("a"))`` returns ``true``

**isError(expression o)** *boolean*

	Returns whether ``o`` is an error

		``isError(abs("a"))`` returns ``true``

**isNonBlank(expression o)** *boolean*

	Returns whether ``o`` is non-null or a not-empty string. IsNonBlank() returns false when value is null or empty ("").
	It considers a string made of blank spaces as NonBlank; it considers an expression with an error as blank.

		``isNonBlank("")`` returns ``false``

		``isNonBlank(" ")`` returns ``true``

		``isNonBlank(abs("a"))`` returns ``false``

**isNotNull(expression o)** *boolean*

	Returns whether ``o`` is not null. IsNotNull() returns false when value is null or empty ("").
	It does not consider a string made of blank spaces as not null, and considers an expression with an error as not null.

		``isNotNull("")`` returns ``false``

		``isNotNull(" ")`` returns ``false``

		``isNotNull(abs(a"))`` returns ``true``

**isNull(expression o)** *boolean*

	Returns whether ``o`` is null or an empty string. IsNull() returns true when value is null or empty ("").
	It considers a string made of blank spaces as null, and does not consider an expression with an error as null.

		``isNull("")`` returns ``true``

		``isNull(" ")`` returns ``true``

		``isNull(abs("a"))`` returns ``false``

**isNumeric(expression o)** *boolean*

	Returns whether ``o`` can represent a number