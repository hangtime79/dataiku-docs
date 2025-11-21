Variables expansion in code recipes
####################################

Code recipes can use the two kinds of variables expansion in DSS:

* Expansion of user-defined variables. See :doc:`/variables/index`

* Expansion of "Flow" variables (ie, variables that are specific to this specific recipe)

Flow variables are mostly used for partitioning-related stuff. See :doc:`/partitions/variables` for more information.

Summary of expansion syntax
=============================


SQL
-------------

Both Flow and custom variables are replaced in your code using the ${VARIABLE_NAME} syntax. For example, if you have the following code:

.. code-block:: sql

	SELECT * from mytable WHERE condition='${DKU_DST_ctry}';

with a variable DKU_DST_ctry which has value France, the following query will actually be executed:

.. code-block:: sql

	SELECT * from mytable WHERE condition='France';

Hive
-----

Both Flow and custom  variables are replaced in your code using the ${hiveconf:VARIABLE_NAME} syntax. For example, if you have the following code:


.. code-block:: sql

	SELECT * from mytable WHERE condition='${hiveconf:DKU_DST_date}';

with a variable DKU_DST_date which has value 2013-12-21, the following query will actually be executed:

.. code-block:: sql

	SELECT * from mytable WHERE condition='2013-12-21';

Python
-------

Flow variables are available in a python dictionary called dku_flow_variables in the dataiku module. Example:

.. code-block:: py

	import dataiku
	print("I am working for year %s" % (dataiku.dku_flow_variables["DKU_DST_YEAR"]))


Custom variables are available in a python dictionary retrieved by the ``dataiku.get_custom_variables()``
function. Example:

.. code-block:: python

	import dataiku
	print("I am excluding %s" % (dataiku.get_custom_variables()["logs.preprocessing.excluded_ip"]))

R
--

Flow variables are retrieved using the ``dkuFlowVariable(variableName)`` function

.. code-block:: R

	library(dataiku)
	dkuFlowVariable("DKU_DST_ctry")

Custom variables are retrieved using the ``dkuCustomVariable(name)`` function.

.. code-block:: R

	library(dataiku)
	dkuCustomVariable("logs.preprocessing_excluded_ip")
