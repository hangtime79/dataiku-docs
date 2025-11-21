Clustering settings
####################

The "Settings" tab allows you to fully customize all aspects of your clustering.


.. contents::
	:local:

Sampling
===========

.. note::
	You can access the sampling settings in Models > Settings > Sampling

The available sampling methods depend on the :doc:`machine learning engine <../algorithms/index>`.

If your dataset does not fit in your RAM, you may want to extract a sample on which clustering will be performed. Data can be sampled from the beginning of a dataset (fastest) or randomly sampled from the entire dataset.

Features
===================

See :doc:`../features-handling/index`.


Dimensionality reduction
==========================

.. note::
	You can access the sampling settings in Models > Settings > Dimensionality Reduction

Dimensionality reduction reduces the number of variables by arranging them into 'principal components' grouping together all correlated variables. The principal components are computed to carry as much variance as possible from the original dataset.

The main interest of using PCA for clustering is to improve the running time of the algorithms, especially when you have a large number of dimensions.

You can choose to enable it, disable it, or try both options to compare.


Outliers detection
=====================

.. note::
	You can access the parameters for outlier detection in Models > Settings > Outlier detection

When performing clustering, it is generally recommended to detect outliers. Not doing so could generate very skewed clusters, or many small clusters and one cluster containing almost the whole dataset.

DSS detects outliers by performing a pre-clustering with a large number of clusters and considering the smallest "mini-clusters" as outliers, if:

- their cluster size is less than a specified threshold (ex : 10)
- their cumulative percentage is less than a specified threshold (ex: 1%)

Once outliers are detected, you can either:

- Drop: outliers are dropped.
- Cluster : create a "cluster" from all detected outliers.


Algorithms
============

.. note::
   You can change the settings for algorithms under Models > Settings > Algorithms

DSS supports several algorithms that can be used for clustering. You can select multiple algorithms to see which performs best for your dataset.

The algorithms depend on the :doc:`machine learning engine <../algorithms/index>`.
