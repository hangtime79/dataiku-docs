Parse to standard date format
#############################################

Parse strings containing dates in any format into the standard ISO 8601 format (``yyyy-MM-ddTHH:mm:ss.SSSZ``) to work with them in DSS. Use Smart Dates to get semi-automatic date parsing with the assistance of DSS. 

Options
========

**Column**

Apply date parsing to the following: 

* A single column

* An explicit list of columns

* All columns matching a regex pattern

* All columns

**Output column**

Leave blank to parse data in-place or create a separate output column.

**Input date format(s)**

Open **Find with Smart Date** to get semi-automatic date parsing with the help of DSS. Otherwise, specify the format of your inputs column(s) using the `Java syntax for date specifiers <http://docs.oracle.com/javase/7/docs/api/java/text/SimpleDateFormat.html>`__. 

.. note:: 
    Common patterns include y (year), M (month in year), w (week in year), d (day in month), E (day name in week), a (am/pm marker), H (hour in day 0-24), h (hour in am/pm 1-12), m (minute in hour), s (second in minute), S (millisecond), Z (time zone).

**Locale**

Translate date information in locale format (like ‘mercredi’ or ‘janvier’ in French). 

**Timezone**

Provide details on the time zone, if needed. Options include using a TZ column, an IP column, or specifying a timezone from the dropdown. UTC is the default. 

Related resources
===================

For more information on managing dates with Dataiku DSS, please see the `reference documentation <https://doc.dataiku.com/dss/latest/preparation/dates.html>`__. If you prefer a hands-on approach, check out this `brief tutorial <https://knowledge.dataiku.com/latest/courses/basics/prepare-data/concept-date-handling.html>`__ on parsing dates with DSS.


.. pristine
