Flag holidays
#############################################

This processor identifies whether a date is a school holiday, a bank
holiday or a weekend.

It takes as input a Date column and outputs 3 boolean columns :

-    ``*school``: whether this date is a school holiday or not. (FR)
-    ``*bank``: whether this date is a bank holiday or not. (FR,US,IN,DE,ES)
-    ``*weekend``: whether this date is a weekend or not.


It's worth noting that a Date in DSS corresponds to a point in time,
just like a timestamp. Conversely, a holiday is always defined by a
timezone-less tuple (year,month,day). Consequently, a timezone must be
provided in order to convert this timezone-less representation into a
Date.

Although the timezone can be specified explicitly, it may be more
convenient to use the country's default timezone.

+-----------+---------------------+
| Country   | Default timezone    |
+===========+=====================+
| DE        | Europe/Berlin       |
+-----------+---------------------+
| ES        | Europe/Madrid       |
+-----------+---------------------+
| FR        | Europe/Paris        |
+-----------+---------------------+
| IN        | Asia/Kolkata        |
+-----------+---------------------+
| US        | America/New\_York   |
+-----------+---------------------+


If you need to retrieve bank holidays and/or weekends in other countries, please use the "Holidays" plugin.

.. pristine
