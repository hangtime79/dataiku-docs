:tocdepth: 3

Datasets
########

Please see :doc:`/concepts-and-examples/datasets/index` for an introduction to interacting with datasets in Dataiku Python API


The `dataiku.Dataset` class
============================================

.. autoclass:: dataiku.Dataset
	:members:
	:exclude-members: write_from_dataframe,set_preparation_steps

.. automethod:: dataiku.core.dataset.create_sampling_argument

.. autoclass:: dataiku.core.dataset_write.DatasetWriter
    :members:
	:exclude-members: active_writers,atexit_handler

.. autoclass:: dataiku.core.dataset.Schema
    :members:

.. autoclass:: dataiku.core.dataset.DatasetCursor
	:members:

The `dataikuapi.dss.dataset` package
=====================================================

Main DSSDataset class
----------------------

.. autoclass:: dataikuapi.dss.dataset.DSSDataset

Listing datasets
-----------------

.. autoclass:: dataikuapi.dss.dataset.DSSDatasetListItem

Settings of datasets
---------------------

.. autoclass:: dataikuapi.dss.dataset.DSSDatasetSettings

.. autoclass:: dataikuapi.dss.dataset.SQLDatasetSettings

.. autoclass:: dataikuapi.dss.dataset.FSLikeDatasetSettings

Dataset Information
--------------------

.. autoclass:: dataikuapi.dss.dataset.DSSDatasetInfo

Creation of managed datasets
-----------------------------

.. autoclass:: dataikuapi.dss.dataset.DSSManagedDatasetCreationHelper
