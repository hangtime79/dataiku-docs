Handling and display of dates
#############################

In Dataiku DSS, “datetimes with zone” mean “an absolute point in time”, that is, something expressible as a date plus time plus timezone.
For example, ``2001-01-20T14:00:00.000Z`` or ``2001-01-20T16:00:00.000+0200``, which refer to the same point in time
(14:00Z is 2pm UTC, and 16:00+0200 is 4pm UTC+2, so 2pm UTC too).

When the timezone indication is not present, the DSS type used is "datetime no zone", and corresponds to a date plus a time. When the time indication is also not present, the DSS type is "date only", and represents a calendar day, like ``2001-01-20``.

Displaying dates
================
DSS only displays datetime with zone values in UTC. This is especially true in charts.
If you use the format date processor with a proper ISO8601 format, it will temporarily show it as a different time zone,
but as soon as you write it out or read it in a chart, it will be in UTC again.

If you use a formatter to format as ``16:00+0200`` and selects the output to be a string,
then the string value will be preserved but it’s not a date anymore.

See :doc:`/preparation/dates` for more information.

Handling of dates in SQL
========================

DSS offers settings on the SQL datasets to control how date types and datetime no zone types are read. Datetimes with zone don't need additional settings since they correspond to values that are unambiguously defined.

A DATE column in a SQL database can be read by DSS:

- "As is" : as a date only column
- "As string" : the value is converted to a string representation and DSS handles it as a string. Note that the conversion is done by the database and the output format is often subject to database-specific settings
- "As datetime with zone" : the value is converted to a datetime with zone by DSS, by considering that the value stored in the SQL database is 00h 00m of the date, in the timezone selected as ``Assumed timezone`` on the dataset.

For databases offering such a type, columns in a SQL database whose values are datetimes without zone indication can be read by DSS:

- "As is" : as a datetime no zone column
- "As string" : the value is converted to a string representation and DSS handles it as a string
- "As datetime with zone" : the value is converted to a datetime with zone by DSS, by considering that the value stored in the SQL database is in the timezone selected as ``Assumed timezone`` on the dataset.

When selecting “Local” as “assumed time zone” in the settings of a SQL dataset, DSS will use the timezone of the server it is running on. For example when reading a value "2020-02-14" in the database with a DSS running in Amsterdam, DSS will consider that it is reading "2020-02-14 at midnight in Amsterdam", then displays it in UTC, so "2020-02-13T23:00:00Z". If you want it to show "2020-02-14T00:00:00Z", you must set the assumed time zone to UTC.

