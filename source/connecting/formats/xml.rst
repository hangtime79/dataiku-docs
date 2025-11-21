XML
############

The eXtensible Markup Language is a very widespread format, used in its raw or compressed form for storing all sorts of data and commonly used to encode messages over a network. RSS feeds, for example, publish their content in XML format.

.. contents::
    :depth: 2
    :local:

Handling the structure
======================

Data structured in XML is inherently hierarchical, which means a mapping has to be specified in order to convert the data its tre-like structure to the table-like structure Data Science Studio uses. Part of the conversion can be done using the parameters available when creating a dataset, and the rest of the conversion can be handled by a recipe.

Selection of the data to load
-----------------------------

When creating a dataset from a XML source, the goal should be to trim the source data and only load the part of the data that will be used in analyses, in order to not burden the system with unnecessary data. The XML importer creates dataset rows for each root element, and selects root elements using a `XPath <https://en.wikipedia.org/wiki/XPath>`_. Data Science Studio offers a few suggestions for the root element XPath, inferred from reading the beginning of the data source (the first 1 Mo).

The data from the parents of the root elements can be captured, either in a JSON array of all the parents, or in one column per parent, or even explicitly, using a XPath to specify which parent or parent attribute to pick. When using one column per parent, if several parents have the same tag, then the one closest to the element is picked.


JSON representation
-------------------

Data from a XML source that cannot be reduced to simple values (i.e. strings, numbers, ...) upon import will be represented as JSON objects in the dataset, and further manipulation of these data can be implemented using processors in a recipe. The reader loads child elements of a XML element into JSON arrays, one array per tag.


There are 2 options to store values in XML format : either as attributes of the elements, or as text inside the elements. Data Science Studio assumes the former, but can additionally load values stored as text elements, provided these elements only contain text and no attribute.


Example
~~~~~~~~~

When treating text-only elements as attributes

Input::

    <message sender="Fred">
      <timestamp>Tue, 22 Jan 2013 12:14:33</timestamp>
      <content word-count="2">
        hello dss!
      </content>
    </message>

Output:

+--------+---------------------------+-----------------------------------------+
| sender | timestamp                 | content                                 |
+========+===========================+=========================================+
| Fred   | Tue, 22 Jan 2013 12:14:33 | [{word-count:2, xml_text:"hello dss!"}] |
+--------+---------------------------+-----------------------------------------+


Using XPath to select data
============================

`XPath <https://en.wikipedia.org/wiki/XPath>`_ is the de facto standard for navigating into a XML document, and can express a path from any element in the document to any other element.

Limitations
-----------

In a streaming context like in Data Science Studio, where only a portion of the document is allowed to reside in memory at any given time, only a subset of the XPath language is possible. Data Science Studio supports all downwards operations from the root elements, but not operations accessing siblings of the root elements (ex: ``preceding-sibling::*[1]`` ), nor downward operations from a parent of the root elements (ex: ``../message-header`` when the root elements are not ``message-header``).


Selecting values explicitly
-----------------------------------

For finer control on what is loaded into a dataset, Data Science Studio offers the option of specifying explicitly the value for a column by a `XPath <https://en.wikipedia.org/wiki/XPath>`_ expression starting at the root element. The XPath expression is allowed to access the parents of the element, typically to retrieve some of their attributes, but not the other children of these parents.


Example
~~~~~~~~~

Using the XPaths ``@OBS_VALUE``, ``../@CURRENCY``, ``../@CURRENCY_DENOM``

Input::

    <DataSet xsi:schemaLocation="http://www.ecb.europa.eu/vocabulary/stats/exr/1">
        <Series FREQ="D" CURRENCY="NOK" CURRENCY_DENOM="EUR"  TIME_FORMAT="P1D" >
            <Obs TIME_PERIOD="1999-01-04" OBS_VALUE="8.8550" />
            <Obs TIME_PERIOD="1999-01-05" OBS_VALUE="8.7745" />
            ...

Output:

+-----------+----------+----------------+
| OBS_VALUE | CURRENCY | CURRENCY_DENOM |
+===========+==========+================+
| 8.8550    | NOK      | EUR            |
+-----------+----------+----------------+
| 8.7745    | NOK      | EUR            |
+-----------+----------+----------------+





