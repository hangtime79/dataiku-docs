Compute difference between dates
#############################################

Compute the difference between an ISO-8601 formatted date column (``yyyy-MM-ddTHH:mm:ss.SSSZ``) and another time reference: the current time, a fixed date, or another column. 

Options
========

**Time since column**

Column containing data in ISO-8601 format. Use a Prepare step to parse your data into this format if it isn't already. 

**Until**

Choose the second time reference to compute the difference — now, another date column, or a fixed date.

**Output time unit**

Determine the unit of time in which to express the datetime difference — year, month, week, day, hour, minute or second. 

**Output column**

Column into which the datetime difference will be written. 

**Reverse output**

Multiply the computed difference by -1, reversing it: ``3 days`` → ``-3 days``. 



.. pristine
