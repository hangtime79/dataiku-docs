Time Series Forecasting Settings
################################

The "Settings" tab allows you to fully customize all aspects of your time series forecasting task.

.. contents:: :depth: 1
    :local:

.. _forecasting-general-settings:

Settings: General settings
===========================

Set the base settings for time series forecasting (target variable, time variable, time series identifiers (if multiple time series in the dataset)) 

.. _forecasting-time-step-parameters:

Time step parameters
---------------------

Define what time step will be used for time series resampling. Indeed, forecasting models require the dataset to be sampled with equally spaced time steps.
A default setting is guessed by DSS, based on the input data.

Forecasting parameters
----------------------

Specify how many time steps will be forecast by the models (a.k.a forecasting horizon), as well as the number of skipped time steps for model evaluation (a.k.a gap).

You can also choose what quantiles will be forecasted by the models (also used for some evaluation metrics).

Partitioned Models
------------------

.. warning::

    DSS support for partitioned time series forecasting models is experimental

This allows you to train partitioned prediction models on partitioned datasets. In that case, DSS creates one sub model (or model partition) per partition of your dataset.

For more information, see :doc:`../partitioned`


Settings: Train / Test set
=============================

When training a model, it is important to test the performance of the model on a "test set". During the training phase, DSS "holds out" on the test set, and the model is only trained on the train set.

Once the model is trained, DSS evaluates its performance on the test set. This ensures that the evaluation is done on data that the model has "never seen before".

Splitting the dataset
------------------------

By default, DSS splits the input dataset (sorted by time) into a train and a test set. For time series forecasting, the size of the test set is the number of step in the forecasting horizon, minus the number of skipped steps (a.k.a gap).

Subsampling
%%%%%%%%%%%%

DSS defaults to using the first 100'000 rows of the dataset, but other options are available.

For more details, see the documentation on :doc:`../../explore/sampling`.

K-Fold cross-test
%%%%%%%%%%%%%%%%%%%%%%%

A variant of the single train/test split method is called "K-Fold cross-test": DSS uses the last forecasting horizon as a test set (while skipping the gap), and all time steps before as a train set.
It then shifts the test set backwards by one forecasting horizon, and takes all time steps before as a train set. This is repeated until we have **K** {train, gap, test} sets, or evaluation folds. 

This method strongly increases training time (roughly speaking, it multiplies it by **K**). However, it allows for two interesting features:

 * It provides a more accurate estimation of model performance, by averaging over K estimations (one per split) and by providing "error margins" on the performance metrics, computed as twice the standard deviation over the K estimations. When K-Fold cross-test is enabled, all performance metrics will have tolerance information.

 * Once the scores have been computed on each fold, DSS can retrain the model on 100% of the dataset's data. This is useful if you don't have much training data.

.. _forecasting-resampling:

Time series resampling
----------------------

As mentioned above, forecasting models require the dataset to be sampled with equally spaced time steps.

To do so, DSS needs to impute missing values for missing time steps in the dataset. You can set which method to use for numerical and non-numerical features interpolation (missing time steps in the middle of the time series) and extrapolation (missing time steps before the start, or after the end of the time series).

A few example of imputation methods are: linear, quadratic, cubic, mean, constant value, same as previous/next/nearest, most common (for non-numerical), or no imputation at all.

.. _forecasting-external-features:

Settings: External features
=============================

.. note::

    Some models do not support the usage of external features for time series forecasting.

.. warning::

    If external features are selected as known-in-advance, "future" values of those features are required when forecasting.

While time series forecasting model can only work with a time variable and a target variable, having external time-dependent features can improve some models' performance. You can select those that should be used by the model, along with handling settings for each.

The user can choose between two kinds of external features:

  - **Known-in-advance features**: features whose future values are known.
  - **Past-only features**: features whose future values are unknown after the current date.

.. note::

    Past-only features are only usable by time-series forecasting based on classical machine learning algorithms.

See :doc:`../features-handling/index`


.. _forecasting-feature-generation:

Settings: Feature Generation
==============================

.. note::

    Only time-series forecasting based on classical machine learning algorithms can use the generated features.

Feature generation transforms time-series data into structured features that classical machine learning algorithms can process, while preserving the temporal dependencies and chronological relationships in the data.


Shifts (lags)
--------------


Shifts refer to a transformation that moves the time-index of the data forward or backward in time.

For instance, a shift of -1 (or equivalently a lag of 1) transforms the series ``0, 1, 2, 3, ... , t`` into the series ``-1, 0, 1, 2, ... , t-1``.

+------------+---------+-----------------+
|| date      || feature|| shifted feature|
||           ||        || (shift -1)     |
+============+=========+=================+
| 2025-09-01 |   42    |                 |
+------------+---------+-----------------+
| 2025-09-02 |   15    |      42         |
+------------+---------+-----------------+
| 2025-09-03 |   78    |      15         |
+------------+---------+-----------------+
| 2025-09-04 |   56    |      78         |
+------------+---------+-----------------+
| 2025-09-05 |   33    |      56         |
+------------+---------+-----------------+
| 2025-09-06 |   67    |      33         |
+------------+---------+-----------------+
| 2025-09-07 |   21    |      67         |
+------------+---------+-----------------+


In the context of multiple horizon forecasting with classical machine learning algorithms, past-only data up to indice ``t``, and known-in-advance data up to indice ``t+i``, can be used to predict values at ``t+i`` with ``i`` ranging in ``1, 2, ... , horizon``. In order to build data with shifts, two kinds of reference are available:

  - **Shifts from forecast origin**: ``t`` is taken as a reference, regardless of the predicted horizon
  - **Shifts from forecasted point**: ``t+i`` is taken as a reference, varying for each ``i`` to be predicted in ``1, 2, ... , horizon``.


Each external feature (known-in-advance and past-only), as well as the target (always considered as past-only), can be used to define shifted features.

Shifts with respect to forecast origin will yield the same shifted data for all forecasted points to be predicted. They are typically used with past-only features.


+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
|| date      || target|| feature|| target            || shifted feature                 || target            || shifted feature                 |
||           ||       ||        || horizon t+1       || horizon t+1                     || horizon t+2       || horizon t+2                     |
||           ||       ||        ||                   || (shift -2 from forecast origin) ||                   || (shift -2 from forecast origin) |
+============+========+=========+====================+==================================+====================+==================================+
| 2025-09-01 |   1    |   42    |        2           |                                  |        3           |                                  |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-02 |   2    |   15    |        3           |                                  |        4           |                                  |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-03 |   3    |   78    |        4           |      42                          |        5           |      42                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-04 |   4    |   56    |        5           |      15                          |        6           |      15                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-05 |   5    |   33    |        6           |      78                          |        7           |      78                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-06 |   6    |   67    |        7           |      56                          |        8           |      56                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-07 |   7    |   21    |        8           |      33                          |        9           |      33                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+


Shifts with respect to forecasted point will yield data shifted according to the prediction horizon. 

As a consequence the joint values of the target, and features shifted from horizon will stay the same, regardless of the horizon.



+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
|| date      || target|| feature|| target            || shifted feature                 || target            || shifted feature                 |
||           ||       ||        || horizon t+1       || horizon t+1                     || horizon t+2       || horizon t+2                     |
||           ||       ||        ||                   || (shift -2 from forecasted point)||                   || (shift -2 from forecasted point)|
+============+========+=========+====================+==================================+====================+==================================+
| 2025-09-01 |   1    |   42    |        2           |                                  |        3           |      42                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-02 |   2    |   15    |        3           |      42                          |        4           |      15                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-03 |   3    |   78    |        4           |      15                          |        5           |      78                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-04 |   4    |   56    |        5           |      78                          |        6           |      56                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-05 |   5    |   33    |        6           |      56                          |        7           |      33                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-06 |   6    |   67    |        7           |      33                          |        8           |      67                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+
| 2025-09-07 |   7    |   21    |        8           |      67                          |        9           |      21                          |
+------------+--------+---------+--------------------+----------------------------------+--------------------+----------------------------------+


Automatic shifts selection
---------------------

Instead of explicitly defining each shift for every feature, DSS can automate the process. 

The automatic mode is designed to identify and select the most impactful shifts (or lags) for each feature based on its relevance to the target variable.

.. note::

    The automatic shifts mode is available only for shifts defined from forecasted point.

When the mode is enabled on a specific feature, DSS uses the following user-defined parameters for the search of best shifts:

  - a maximum number of shifts to be selected
  - lower and upper bounds for shifts
  
DSS then evaluates the shifts within the provided ranges and selects the most correlated to the target.

This feature is particularly useful when the optimal shifts are not obvious to the user, in order to accelerate the feature generation process.

The following parameters are available for configuration:

- **Maximum number of shifts**: This sets an upper limit on how many automatically generated shifts can be selected per feature. For example, if set to 5, DSS will identify and select between 0 and 5 shifts for each feature using the auto mode, and discard the rest. This helps control the total number of generated features in the final model.

- **Exploration ranges**: These parameters define the range of shifts (minimum and maximum shifts) that DSS will explore to find the most relevant ones. Two distinct ranges can be configured:

  - *Past-only features range*: The search space used for the target variable and all features considered "past-only".
  - *Known-in-advance features range*: A separate search space specifically for features whose future values are known.


.. note::

    Enabling the automatic shifts mode on a large number of features or using large exploration ranges, can significantly increase preprocessing time.


Windows
--------

Windows are defined by a beginning and an end, taking as reference either:

 * the forecast origin ``t``, or
 * the forecasted point ``t+i`` for each step ``i`` between ``t+1`` and ``t+horizon``.

 For each feature, any subset (including none and all) of the following operators can be selected: ``min``, ``max``, ``mean``, ``std`` and ``median``.

.. note::

    Only numerical variables can be used in windows feature generation.


Settings: Algorithms
===========================

DSS supports several algorithms that can be used to train time series forecasting models. We recommend trying several different algorithms before deciding on one particular modeling method.

See :ref:`Time series forecasting algorithms<timeseries-forecasting-algorithms>` for details.

You can choose among three types of forecasting algorithms:

 * **Baseline** algorithms (*Trivial identity*, *Seasonal naive*) and the *NPTS* algorithm: no parameters are learned, each time series is forecasted based on its past values only.

 * **Statistical** algorithms (*Seasonal trend*, *AutoARIMA*, *Prophet*): one model is trained for each separate time series.

 * **Deep learning** algorithms (*Simple Feed Forward*, *DeepAR*, *Transformer*, *MQ-CNN*): a single model is trained on all time series simultaneously. The model produces one forecast per input time series.

 * **Machine Learning** algorithms (*Random Forest*, *XGBoost*, *Ridge regression*): one model is trained for each separate time series, for each step of the prediction horizon. In this multiple-horizon forecasting framework, data from indices ``1, 2, ... , t-2, t-1, t`` is used to predict values at ``t+1, t+2, ... , t+horizon``. The use of :ref:`time-based feature generation (lags and windows)<forecasting-feature-generation>` is recommended in order to build informative feature matrices to feed the learning algorithm.


Additional information 
======================

Minimum required length per time series
---------------------------------------

Training
%%%%%%%%

During training, all time series must be longer than a minimum required length that depends on the session settings and on the algorithm and its hyperparameters.

Models require the input time series to be of a minimum length to be able to train.

Because models are trained separately on each fold during both the hyperparameter search and the final evaluation, what matters is the time series length in the first fold.
The first fold is the fold with the shortest train set (see the Splitting and Hyperparameters explanation schemas in the blue info box of the Design page to visually understand the folds).

The minimum required length depends on multiple settings:

 * **Forecasting horizon**: a longer horizon increases the required length.

 * **Models hyperparameters**: some hyperparameters like the **context length** of Deep Learning models or the **season length** of Statistical models require the input time series to be longer.

There are multiple ways to make the training session work when encountering the minimum required length error:

 * Decrease the number of folds of the hyperparameter search (or even don't do search at all).

 * Decrease the number of folds of the evaluation.

 * Decrease the forecast horizon and/or the number of horizons in evaluation.

 * Decrease the maximum context length or season length set for Deep Learning and Statistical models.

 * Use extrapolation in the resampling: if some time series are shorter than others, then extrapolation will align all time series to the longest one.


Scoring and evaluation
%%%%%%%%%%%%%%%%%%%%%%

During scoring and evaluation, time series shorter than the minimum required length for scoring are completely ignored (these ignored time series can be found in the logs).

Models require the input time series to be of a minimum length to be able to score (note that this required length is usually shorter than the required length for training).

During evaluation, time series are evaluated on the range of time steps that are after the minimum required length for scoring.
This means that some time series may be evaluated on fewer time steps than others.
Aggregated metrics over all time series are then weighted on the evaluation length of each time series.
