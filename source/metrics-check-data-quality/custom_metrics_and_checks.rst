Custom probes and checks
##########################

.. contents::
    :depth: 2
    :local:


The predefined probes and checks handle simple cases, and more complex computations can be done using custom probes and custom checks. These are python functions, and run with access to the DSS :doc:`devguide:api-reference/python/index`.

Custom probe
==============

A custom python probe is a function taking the dataset or folder as parameter and returning values.

Return values
-------------

The function can return a single value, in which case the metric gets the generic name "value":

.. code-block:: py

    def process(dataset):
        return dataset.get_dataframe().shape[1]


A custom probe can also compute several values in one pass, and return them as a dictionary of name to value:

.. code-block:: py

    def process(dataset):
        df = dataset.get_dataframe()
        return {'num_rows' : df.shape[0], 'num_cols' : df.shape[1]}


DSS automatically infers the type of the metric's value, among DOUBLE, BOOLEAN, BIGINT, STRING and ARRAY, but in some cases one wants to explicitly specify the type. For example, to get a ISO-formatted UTC timestamp recognized as a date, one has to pass the metric value under the form of a pair of (value, type)

.. code-block:: py

	from datetime import datetime as dt
	from dataiku.metric import MetricDataTypes

	def process(dataset):
	    now = dt.strftime(dt.now(), '%Y-%m-%dT%H:%M:%SZ')
	    return {'now_as_string' : now, 'now_as_date' : (now, MetricDataTypes.DATE)}


Partitioned datasets
--------------------

For partitioned datasets, the function of the custom probe receives a second parameter: the partition on which the computation is requested. When the computation is requested on the full dataset and not on just one partition, the value passed is "ALL".


Custom check / Custom Data Quality rule
=======================================

A custom check or Data Quality rule is a function taking the folder, saved model, model evaluation store or dataset as parameter and returning a check or rule outcome.

.. note::

	It is advised to name all custom checks in order to distinguish the values they produce in the checks display, because custom checks can't auto-generate a meaningful name.


If appropriate, a message can be returned as a second return value.

.. code-block:: py

	def process(last_values, dataset):
	    if dataset.name == 'PROJ.a_dataset':
	        return 'OK'
	    else:
	        return 'ERROR', 'not the expected dataset'

The last values of each metric for the dataset, folder or saved model are passed as the first parameter. This parameter is a `dict` of metric identifier to metric data point.

.. code-block:: py

	def process(last_values):
	    if int(last_values['basic:COUNT_FILES'].get_value()) > 10:
	        return 'OK'
	    else:
	        return 'ERROR', 'not enough files'

Here's another example of a custom check that compares the max value of the dataset column ``order_date`` to the last build date for the dataset. Note that in the *Metrics* tab, the "Column statistics" metric for the dataset column ``order_date`` is set to ``MAX`` in this example. This makes the metric value ``last_values['col_stats:MAX:order_date']`` available in our custom check.  

.. code-block:: py
    
    from datetime import datetime, timedelta
    
    def process(last_values):
        build_start_date = last_values['reporting:BUILD_START_DATE'].get_value()
        max_data_timestamp = last_values['col_stats:MAX:order_date'].get_value()
        
        # turn our values into datetime objects to allow us to use datetime functions 
        build_date_datetime = datetime.strptime(build_start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        max_timestamp_datetime = datetime.strptime(max_data_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        # flag if the difference is greater than 1 day 
        if build_date_datetime > max_timestamp_datetime + timedelta(days=1):
            return 'ERROR'
        else:
            return 'OK', build_date_formatted.isoformat()
