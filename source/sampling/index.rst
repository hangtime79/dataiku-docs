Sampling methods
#################

.. contents::
	:local:

Many parts of DSS support sampling data to extract subsets and/or reduce the size of data to process

Sampling can be configured in the following locations in DSS:

* Exploration
* Visual data preparation
* Charts
* Sampling recipe
* Machine learning
* API

Generic sampling methods
==========================

DSS provides a variety of sampling methods, listed below.

No sampling
------------

All data is taken, sampling does not happen.

First records
--------------

This method takes the first N rows of the dataset. It is very fast, as it only reads N rows, but may result in a very biased view of the dataset.

Random sampling (fixed number of records)
-------------------------------------------

This method randomly selects N records within the whole dataset. This method requires a full pass reading the data. The time taken by this method is thus linear with the size of the dataset.

Random sampling (approximate ratio)
------------------------------------

This method randomly selects approximately X% of the rows. The target count of records is approximate, and will be more precise with large input datasets.

This method requires a full pass reading the data.

Random sampling (approximate number of records)
-----------------------------------------------

This method randomly selects approximately N records. The target count of records is approximate, and will be more precise with large input datasets.

This method requires 2 full passes reading the data.

Column values subset
---------------------

This method randomly selects a subset of values and chooses all rows with these values, in order to obtain approximately N rows. This is useful for selecting a subset of customers, for example.

This sampling method requires 2 full passes reading the data. The time taken by this method is thus linear with the size of the dataset.

This method is useful if you want to have all records for some values of the column, for your analysis. For example, if your dataset is a log of user actions, it is more interesting to have "all actions for a sample of the users" rather than "a sample of all actions", as it allows you to really study the sequences of actions of these users.

"Column values subset" sampling will only provide interesting results if the selected column has a sufficiently large number of values. A user id would generally be a good choice for the sampling column.

Stratified (fixed number of records)
--------------------------------------

This method randomly selects N rows, ensuring that the distribution of values in a column is respected in the sampling. Ensures that all values of the column appear in the output.

This method may return a few more than N rows.

This sampling method requires 2 full passes reading the data. The time taken by this method is thus linear with the size of the dataset.

Stratified (approximate ratio)
-------------------------------

This method randomly selects X% of the rows, ensuring that the distribution of values in a column is respected in the sampling. Ensures that all values of the column appear in the output.

This method may return a bit more than X% rows.

This sampling method requires 2 full passes reading the data. The time taken by this method is thus linear with the size of the dataset.

Class rebalancing (approximate number of records)
--------------------------------------------------

This method randomly selects approximately N rows, trying to rebalance equally all modalities of a column. This method does not oversample, only undersample (so some rare modalities may remain under-represented).In all cases, rebalancing is approximative.

This sampling method requires 2 full passes reading the data. The time taken by this method is thus linear with the size of the dataset.

Class rebalancing (approximate ratio)
--------------------------------------

This method randomly selects approximately X% of the rows, trying to rebalance equally all modalities of a column.

This method does not oversample, only undersample (so some rare modalities may remain under-represented). In all cases, rebalancing is approximative.

This sampling method requires 2 full passes reading the data. The time taken by this method is thus linear with the size of the dataset.

Last records
--------------

This method takes the last N rows of the dataset.

This method requires a full pass reading the data. The time taken by this method is thus linear with the size of the dataset.

First records sorted by a column
--------------------------------

This method retrieves the first N rows (sorted by a column, ascending or descending) from the dataset.

This method requires to write all data on disk for sorting.

Sampling methods availability
=============================

Not all sampling methods are available in the different locations.

For **Exploration** and **Visual data preparation**, the available sampling methods are:

* First records
* Random sampling (fixed number of records)
* Random sampling (approximate ratio)
* Random sampling (approximate number of records)
* Column values subset
* Stratified (fixed number of records)
* Stratified (approximate ratio)
* Class rebalancing (approximate number of records)
* Class rebalancing (approximate ratio)
* Last records

See :doc:`Sampling in explore </explore/sampling>` for more information.

For **Charts**, the **Sampling recipe**, **Machine learning** and the **API**, the available sampling methods are:

* No sampling
* First records
* Random sampling (approximate ratio)
* Random sampling (approximate number of records)
* Column values subset
* Class rebalancing (approximate number of records)
* Class rebalancing (approximate ratio)
* First records sorted by a column
