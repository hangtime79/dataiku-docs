kdb+
#######

.. warning::

	**Tier 2 support**: Connection to kdb+ is :doc:`Experimental </troubleshooting/support-tiers>` and not fully supported

DSS has experimental support for reading tables from kdb+


Installing support
===================

In order to enable support for kdb+, you must install the "kdb+" plugin. Please follow instructions from :doc:`/plugins/installing`

Creating a kdb+ connection
==========================

* Create a new "Other databases (JDBC)" connection
* In driver class, use "kx.jdbc.jdbc"
* In URL, use "jdbc:q:HOST:PORT"
* In Dialect, use "kdb+"

You can now use kdb+ as a normal SQL database and create SQL datasets on it. Note that you can either write direct SQL or q code by prefixing your query by `q)`