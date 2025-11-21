.. _code-recipes-python:

Python recipes
###############

Dataiku DSS lets you write recipes using the Python language. Python recipes can read and write datasets, whatever their storage backend is.

For example, you can write a Python recipe that reads a SQL dataset and a HDFS dataset and that writes an S3 dataset.
Python recipes use a specific API to read and write datasets.

Python recipes can manipulate datasets either :

* Using regular Python code to iterate on the rows of the input datasets and to write the rows of the output datasets
* Using Pandas dataframes.

Your first Python recipe
=========================

* From the Flow, select one of the datasets that you want to use as input of the recipe.
* In the right column, in the "Actions" tab, click on "Python"
* In the recipe creation window, create a new dataset that will contain the output of your Python code.
* Validate to create the recipe
* You can now write your Python code.

(Note that if needed, you might need to fill the partition dependencies. For more information, see :doc:`/partitions/index`)

First of all, you need to load the Dataiku API (the Dataiku API is preloaded when you create a new Python recipe)

.. code-block:: py

	import dataiku

You then need to obtain Dataset objects corresponding to your inputs and outputs.

For example, if your recipe has datasets A and B as inputs and dataset C as output, you can use :

.. code-block:: py

	datasetA = dataiku.Dataset("A")
	datasetB = dataiku.Dataset("B")
	datasetC = dataiku.Dataset("C")

Alternatively, you can get the inputs of the recipe as they are in the Input/Output tab with 

.. code-block:: py

	from dataiku import recipe
	# object_type can be omitted if there are only datasets
	all_input_datasets = recipe.get_inputs(object_type='DATASET')
	single_input_dataset = recipe.get_input(object_type='DATASET')
	second_input_dataset = recipe.get_input(index=1, object_type='DATASET')


Introduction to reading and writing datasets
=============================================

Pandas is a popular python package for in-memory data manipulation. http://pandas.pydata.org/

Using the dataset via Pandas will load your dataset in memory, it is therefore critical that your dataset is "small enough" to fit in the memory of the DSS server or container in which the recipe runs.

The core object of Pandas is the DataFrame object, which represents a dataset.

Getting a Pandas DataFrame from a Dataset object is straightforward:

.. code-block:: py

	# Object representing our input dataset
	cars = dataiku.Dataset("mycarsdataset")

	# We read the whole dataset in a pandas dataframe
	cars_df = cars.get_dataframe()

The cars_df is a regular Pandas data frame, which you can manipulate using all Pandas methods.

Writing the Pandas DataFrame in an output dataset
---------------------------------------------------

Once you have used Pandas to manipulate the input data frame, you generally want to write it to the output dataset.

The Dataset object provides the method :meth:`dataiku.Dataset.write_with_schema`

.. code-block:: py

	output_ds = dataiku.Dataset("myoutputdataset")
	output_ds.write_with_schema(my_dataframe)


Going further
===============

The above is only the very first example of reading and writing Dataiku datasets through the API.

The API for datasets has much more capabilities:

* Fine-grained control over the schema
* Chunked reading and writing, to read dataframes by blocks for large datasets
* Streaming API for reading and writing datasets row-by-row
* Fast-path access to certain storage types

More details about the whole dataset API can be found in the Developer Guide, at :doc:`devguide:concepts-and-examples/datasets/index`

In addition, the Python API cover much more, such as interacting with managed folders, models, ... For more details, please see the :doc:`devguide:index`



Using the streaming API
========================

If the dataset does not fit in memory, it is also possible to stream the rows. This is often more complicated, so we recommend using Pandas for most use cases

Reading
--------

Dataset object's:

* iter_rows method are iterating over the rows of the dataset, represented as dictionary-like objects.
* iter_tuples method are iterating over the rows of the dataset, represented as tuples. Values are ordered according to the schema of the dataset.

.. code-block:: py

	import dataiku
	from collections import Counter

	cars = dataiku.Dataset("cars")

	origin_count = Counter()

	# iterate on the dataset. The row object is a dict-like object
	# the dataset is "streamed" and it is not required to fit in RAM.
	for row in cars.iter_rows():
		origin_count[row["origin"]] += 1

Writing
--------

Writing the output dataset is done via a writer object returned by Dataset.get_writer

.. code-block:: py

	with output.get_writer() as writer:
		for (origin,count) in origin_count.items():
  			writer.write_row_array((origin,count))

.. note::

	Don't forget to close your writer. If you don't, your data will not get fully written. In some cases (like SQL output datasets), no data will get written at all.

	We strongly recommend that you use the ``with`` keyword in Python to ensure that the writer is closed.

Writing the output schema
---------------------------

Generally speaking, it is preferable to declare the schema of the output dataset prior to running the Python code. However, it is often impractical to do so, especially when you write data frames with many columns (or columns that change often). In that case, it can be useful for the Python script to actually modify the schema of the dataset.

The Dataset API provides a method to set the schema of the output dataset. When doing that, the schema of the dataset is modified each time the Python recipe is run. This must obviously be used with caution.

.. code-block:: py

	output.write_schema([
	{
	  "name": "origin",
	  "type": "string",
	},
	{
	  "name": "count",
	  "type": "int",
	}
	])


Going further
--------------

To see all details of the Python APIs for interacting with datasets, and other APIs that you can use in recipes, please see :doc:`devguide:concepts-and-examples/datasets/index`