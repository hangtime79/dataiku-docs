SAP HANA
#########

.. warning::

	**Tier 2 support**: Connection to SAP HANA is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

DSS supports the full range of features for SAP HANA:

* Reading and writing datasets
* Executing SQL recipes
* Performing visual recipes in-database
* Using live engine for charts

DSS has been tested on HANA SPS 11.

Caveats
========

* In charts (live mode), filtering by date in "free range" mode is not supported
* In charts (live mode), aggregating with a date in "quarter", "month", "week", "day" or "hour" is not supported.
* SQL Pipelines are not guaranteed to work