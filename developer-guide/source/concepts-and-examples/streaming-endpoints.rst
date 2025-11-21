Streaming Endpoints
###################

..
  this code samples has been verified on DSS: 14.2.0-alpha3
  Date of check: 16/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 03/10/2024

.. note::

	There are two main classes related to streaming endpoint handling in Dataiku's Python APIs:

	* :class:`dataiku.StreamingEndpoint` in the ``dataiku`` package. It was initially designed for usage within DSS in recipes and Jupyter notebooks.

	* :class:`dataikuapi.dss.streaming_endpoint.DSSStreamingEndpoint` in the ``dataikuapi`` package. It was initially designed for usage outside of DSS.

	Both classes have fairly similar capabilities, but we recommend using :class:`dataiku.StreamingEndpoint` within DSS.

	For more details on the two packages, please see :doc:`/getting-started/dataiku-python-apis/index`.


Reference documentation
=======================

Use the following classes to interact with streaming endpoints in Python recipes and notebooks.


.. autosummary:: 
    dataiku.StreamingEndpoint
    dataiku.core.streaming_endpoint.StreamingEndpointStream
    dataiku.core.continuous_write.ContinuousWriterBase
    dataiku.core.continuous_write.StreamingEndpointContinuousWriter

Use the following class preferably outside of DSS.

.. autosummary:: 
    dataikuapi.dss.streaming_endpoint.DSSStreamingEndpoint
    dataikuapi.dss.continuousactivity.DSSContinuousActivity