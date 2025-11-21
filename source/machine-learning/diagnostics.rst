ML Diagnostics
##################

ML Diagnostics are designed to identify and help troubleshoot potential problems
and suggest possible improvements at different stages of training and building machine learning models.

Some checks are based on the characteristics of the datasets and serve as warnings
to avoid common pitfalls when interpreting the evaluation metrics.

Other checks run additional tests after training to identify overfitting or potential data leakage,
allowing you to fix these issues before deployment.

Use of Diagnostics can be disabled in Analysis > Design > Debugging.

.. contents::
	:local:


Dataset Sanity Checks
=====================

When evaluating a machine learning model it is important that the dataset used for evaluation is representative
of both the training data and future scoring data. This is often referred to as the
`i.i.d assumption <https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables>`_.

**Test set might be too small for reliable performance estimation**

    If the test dataset is too small, the performance measurement may not be reliable.
    If possible provide a larger test set. If the test set is split from the training set, either use a
    larger percentage for the testing (default being 20%) or use :ref:`five fold cross-validation <k-fold-cross-validation>`.

**Target variable distribution in test data does not match the training data distribution, metrics could be misleading**

    If the test dataset's target is drawn from a different distribution to that of the training dataset,
    the model may not be able to generalize and may perform poorly. For example if there is a difference in time between
    when the training and testing data were collected there may be changes in the data that it is important to address.

    Statistical tests are performed to assess if the target distribution for the test set is drawn from the same distribution
    as that of the training set. For classification tasks a Chi-squared test is used and for regression tasks a Kolmogorov-Smirnov is used.
    A p-value of less than 0.05 means that the difference was considered statistically significant.

    :doc:`Interactive statistics<../statistics/index>` can be used to examine and better understand the distributions of these two datasets targets.

**Training set might be too small for robust training**

    For training a ML model, the training dataset should be large and diverse enough to capture all the needed patterns in order
    to make reliable predictions. While this is task dependent, a good rule of thumb is to try to gather
    more than 1000 observations in the dataset.

**The dataset is imbalanced, metrics can be misleading**

    When training a classification model one factor that can negatively impact the model
    is the balance between different classes. If one class is strongly underrepresented in the training
    data this may make it difficult for the model to make accurate predictions for this class. While Dataiku uses class weighting
    to aid in training models in the presence of imbalanced data, it is always better to gather more data for the underrepresented classes
    if at all possible.

    During evaluation it is also important to be mindful of the impact this imbalance has on the metrics.
    For example in a binary classification task, if 94% of the target values are 1, then the accuracy would be 94%
    if the model always predicted 1. In this case it is best to use metrics that balance precision and recall, such as AUC or F1-score.
    The confusion matrix can also help to identify this type of failure.

**Only a subset of all time series charts are displayed**

    When training a time series forecasting model with too many time series (typically more than several thousands), then only a subset of them will be displayed in the model report forecast charts.
    Note that models are nevertheless trained on all time series and that evaluation metrics are available for all of them.

**Too many zero target values for the MAPE metric**

    The computation of the MAPE involves dividing by the target values. When training a time series forecasting model, if a time series contains
    too many zeros, then there is a high chance that all target values within an evaluation set are zero, resulting in an undefined MAPE metric. 


**The treatment variable is imbalanced**

    One of the treatment groups (including control) is severely underrepresented. This can cause issues such as: training or scoring failures (especially during hyperparameter search), biased predictions (CATEs), misleading causal metrics.

**The combination of treatment and outcome variables is imbalanced**

    One of the (treatment, outcome) variables combinations is severely underrepresented.
    Similarly to severe imbalance in the treatment variable, this can cause issues such as: training or scoring failures (especially during hyperparameter search), biased predictions (CATEs), misleading causal metrics.


Modeling Parameters
===================

Some modeling parameters need to be adapted to the characteristics of the data,
otherwise they could lead to slower training time, possible data leakage, overfitting or creation of a model learnt on an inaccurate data representation.

**Outlier detection: The mini-cluster size threshold may be too high with respect to the training dataset size.
Training might fail. Consider using a smaller value.**

    When performing outlier detection for a clustering ML task with a mini-cluster size threshold that is too high,
    all rows are likely to be dropped before training. If this happens, the training will fail.
    To avoid this, consider reducing the mini-cluster size threshold to less than ~10% of the training set size.

**Feature handling configuration on columns X, Y and Z is causing N% of the test/train/input dataset rows to be dropped during preprocessing**

    Feature Handling can be configured so that rows with no value on a certain column are dropped.
    When enabled, this diagnostic is displayed if more than 50% of the dataset is dropped during preprocessing. If this occurs, 
    consider modifying the Feature Handling configuration. 

    The columns named in the diagnostic message are sorted by the number of rows dropped.
    Dataiku performs each preprocessing step sequentially, dropping rows with null values one column at a time.
    These steps in which rows are dropped by column are ordered arbitrarily.
    This means that the per-column total dropped row counts are not completely accurate, as any given row could contain multiple null values across a number of columns and will be dropped in whichever column dropping step occurs first.
    In practice, disabling 'drop rows where missing values are null' for any single column mentioned in the error message may not lead to a reduction in the total percentage of rows dropped across the entire dataset.
    
    The 'input' designation is used when K-fold cross-testing is enabled.

**Calculation of X failed**

    The custom metric with name X has failed to calculate. Check the logs of the performed action for detailed information about the failure.

Training Speed
==============

Training speed might not be optimal due to runtime environment bottlenecks, hyperparameter search strategy or other factors.

**N remote workers failed**

    In distributed hyperparameter search mode, some of the remote workers may fail, without interrupting the whole search.
    The search thus runs slower because of a reduced number of running workers. This might be due to a failure to start a kubernetes pod,
    or some other issue on the cluster.

**N remote workers taking a long time to start**

    When performing a distributed hyperparameter search, some remote workers are taking more than 2 minutes to start.
    This might be due to a bottleneck in the kubernetes cluster, *e.g.* the maximum number of running pods is reached.

**N remote workers took more than T to start**

    In distributed hyperparameter search mode, some remote workers started successfully but took more than 2 minutes to start (`T` is the minimum time for a remote worker to start).
    This might be due to a bottleneck in the kubernetes cluster, or a slow starting process in the container.

**Requested GPU but no device is available, using CPU**

    For certain machine learning tasks, training will be significantly slower if performed on a CPU. This diagnostic is raised when a GPU was selected before training, but Dataiku was unable to detect one when executing the process. 
    If this happens, please contact your system administrator to verify your environment is correctly configured.

Overfitting Detection
=====================

Training a machine learning model is a delicate balance between bias and variance.
If the model does not capture enough information from the data, it is under-fit.
It will have a high bias and will be unable to make accurate predictions. On the other hand if the model is overfit,
it has fit the data in the training set too closely, learning the noise specific to this training set and it will fail
to generalize to new unseen data, it has too high variance.

**The algorithm seems to have overfit the train set, all the leaves in the model are pure**

    For tree-based algorithms, another way to identify likely overfitting is to examine the leaves in the trees.
    For a classification task if the model has been able to partition the data fully, unless the task is relatively simple,
    then it has probably overfit and the model size needs to be restricted. This can be detected if all the leaves in the model are pure.

**Number of tree leaves is too large with respect to dataset size**

    For regression tasks, the number of the leaves in a tree can hint at overfitting.
    If the number of leaves in a tree is greater than 50 percent of the number of samples then
    it could be indicative that this tree has overfit this data sample. For tree ensembles such as Random Forest, if more than 10 percent of the trees in the model are overfit,
    it may be worth checking the parameters of the model.

The best way to avoid overfitting is always to add more data if possible as well as adding regularization. This can be addressed by constraining the model further,
by changing the hyperparameters of the algorithm. Use additional regularization or decrease the values of the hyperparameters
that control the size of the model.

Leakage Detection
=================

Data Leakage occurs when information that will not be available at test/scoring time accidentally appears in the training dataset,
this allows the model to achieve unrealistically high performance during training, though it will fail to reproduce this performance once deployed.
A good example of data leakage would be for a sales prediction task, if windowing features capturing all sales for the previous week are used,
but that window includes the day to be predicted, the model will have information about the sales on the day it is trying to predict.

**Too good to be true?**

    One indicator that data leakage might have occurred is an extremely high performance metric such as > 98% AUC.

**Feature has suspiciously high importance which could be indicative of data leakage or overfitting**

    If data leakage has occurred, the feature importances can offer insights into which features contain leaked data as
    the model will attribute very high importances to these features.
    Dataiku will warn you if it identifies that a single feature accounts for more than 80% of the feature importance.

Model Checks
============

When evaluating machine learning models, it is helpful to have a baseline model to compare with
in order to establish that the model is performing better than an extremely simple rule.
A good baseline is a dummy model which simply predicts the most common value.
Especially in the presence of imbalanced data, this can give a more accurate picture of how much value this model is really able to bring.

**The model does not perform better than a random classifier**

    Dataiku calculates the performance a dummy classifier would achieve on this dataset and performs a statistical test
    to ensure that the trained model performs better. If the trained model does not outperform the dummy classifier
    it could be indicative of problems in the data preparation or a lack of data for underrepresented classes.


**R2 score is suspiciously low - the model is marginally better than a naive model which always predicts the mean** / **This model performed worse than a naive model which always predicts the mean**

    For a regression model, if the R2 metric is too low it means that the model is unable to perform better than a naive model which always predicts the mean.
    It could be beneficial to add more features or data to the model.

Training Reproducibility
========================

**Hyperparameter search might not be reproducible when training time series forecasting models with multiple threads**

    For time series forecasting models, hyperparameter search might not be reproducible if the select number of threads is not 1.

Scoring Dataset Sanity Checks
=============================

**Ignoring time series not seen during training**

    When running a scoring recipe for a statistical time series forecasting model, time series that were not
    seen during training are ignored.

**Ignoring time series with not enough past values**

    Time series forecasting models require input time series to have a minimum length.
    When running a scoring recipe, time series that are too short are ignored. 

**Ignoring time series with not enough future values of external features**

    Time series forecasting models trained with external features require one horizon of future values of these external features to make forecasts.
    When running a scoring recipe, time series that don't have enough future values of external features are ignored.

Evaluation Dataset Sanity Checks
================================

**Ignoring time series not seen during training**

    When running an evaluation recipe for a statistical time series forecasting model, time series that were not
    seen during training are ignored.

**Ignoring time series with not enough past values**

    Time series forecasting models require input time series to have a minimum length.
    When running an evaluation recipe, time series that are too short are ignored. 

Time Series Resampling Checks
=============================

**Ignoring time series with less than 2 valid time steps**

    Only time series with at least 2 valid time steps (i.e. with valid target value) can be resampled. Time series with less than 2 time steps are ignored in the scoring and evaluation recipes.


Causal Prediction Treatment Checks
==================================

**The treatment variable is not randomly distributed**

    Standard metrics could be misleading. To mitigate this, try enabling inverse propensity weighting. 
    This is not necessarily an issue for the reliability of predictions (CATEs).

**Treatment values probability distributions have non-overlapping supports (positivity failure)**

    Predictions (CATEs) could be biased due to missing data to model counterfactuals (see the main documentation on :doc:`causal predictions<causal-prediction/introduction>` for definitions). To mitigate this issue, the study should be restricted to a subpopulation where the :ref:`positivity assumption <positivity>` holds. The treatment allocation process should also be investigated and modified to guarantee that all individuals are exposed to all treatments (including the control).


Causal Prediction Propensity Model Checks
=========================================

**The propensity model is not well calibrated**

    If not well calibrated, propensity predictions can be biased, and inverse propensity weighted metrics (if enabled) can be misleading. To mitigate this, try enabling calibration for the propensity model or increasing the ratio of the calibration data.


ML assertions
=============

:doc:`ML assertions<supervised/ml-assertions>` provide a way to streamline and accelerate the model evaluation process, by automatically checking that predictions for specified subpopulations meet certain conditions.

Dataiku raises diagnostics to warn you when assertions could not be computed or fail.

**X assertion(s) failed**

    Dataiku computes each assertion and warns you if any fail.

**X assertion(s) got 0 matching rows**

    After applying the filter on the test set, a diagnostic is raised if the subsample is empty i.e. none of the rows met the criteria.

**X assertion(s) got matching rows but all rows were dropped by the model's preprocessing**

    After applying the model's preprocessing to the subsample a diagnostic is raised if the preprocessed subsample is empty, i.e. all rows that matched the criteria were dropped during the preprocessing. Rows may have been dropped because of the feature handling chosen, or because targets were not defined for those rows.

In the 3 diagnostic examples above, X is an integer less than or equal to the total number of assertion defined for the ml task.

Abnormal Predictions Detection
==============================

An imbalanced dataset or inadequate training parameters can lead to models that almost always predict the same class.

**The model predicts almost always the same class**

    A diagnostic is raised if a model predicted the same class for almost all the samples. It could be indicative
    of an imbalanced dataset.
