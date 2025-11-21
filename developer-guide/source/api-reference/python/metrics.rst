:tocdepth: 2

Metrics and checks
###################

.. note::

	There are two main parts related to handling of metrics and checks in Dataiku's Python APIs:

	* :class:`dataiku.core.metrics.ComputedMetrics` in the `dataiku` package. It was initially designed for usage within DSS

	* :class:`dataikuapi.dss.metrics.ComputedMetrics` in the `dataikuapi` package. It was initially designed for usage outside of DSS.

	Both classes have fairly similar capabilities

For usage information and examples, see :doc:`/concepts-and-examples/metrics`

dataiku package API
====================


.. autoclass:: dataiku.core.metrics.ComputedMetrics
	:members:

.. autoclass:: dataiku.core.metrics.MetricDataPoint
	:members:

.. autoclass:: dataiku.core.metrics.ComputedChecks
	:members:

.. autoclass:: dataiku.core.metrics.CheckDataPoint
	:members:

dataikuapi package API
========================

.. autoclass:: dataikuapi.dss.metrics.ComputedMetrics
	:members:
	:exclude-members: get_raw

