Model error analysis
####################

After training a machine learning model, data scientists often investigate the model's failures to build intuition around
which subpopulations the model performed most poorly on. This analysis is essential in the iterative process
of model design and feature engineering, and is usually performed manually.

Model error analysis provides the user with automatic tools to help break down the model's errors into meaningful groups,
which are easier to analyze, and highlight the most frequent types of errors, as well as the characteristics correlated
with the failures.

Principle
=========

Model error analysis streamlines the analysis of the samples mostly contributing to the model's mistakes.
We call the model under investigation the primary model.

This approach relies on an Error Tree, a secondary model trained to predict whether the primary model prediction is
correct or wrong, i.e. a success or a failure. More precisely, the Error Tree is a binary DecisionTree classifier
predicting whether the primary model will yield a Correct Prediction or an Incorrect Prediction.

The Error Tree can be trained on any DSS dataset meant to evaluate the primary model's performance, i.e. containing
ground truth labels. By default, the Error Tree is trained on the primary model's original test set.

In classification tasks a model failure is an incorrectly predicted class, whereas in the case of regression tasks, a
failure is defined as a large deviation of the predicted value from the true one. In the latter case, when the absolute difference
between the predicted and the true value is higher than a threshold ε, the model outcome is considered as a Wrong Prediction.
The threshold ε is computed as the knee point of the Regression Error Characteristic
(`REC <http://homepages.rpi.edu/~bennek/papers/rec.pdf>`_) curve, ensuring the absolute error
of primary predictions to be within tolerable limits.

The nodes of the Error Tree decision tree break down the test dataset into smaller segments with similar features and
similar model performances. Analyzing the subpopulation in the error nodes, and comparison with the global population,
provides insights around critical features correlated with the model failures.

The Model Error Analysis plugin automatically highlights any information relevant to the model's errors, helping the
user to focus on what are the problematic features, and what are the typical values of these features for the
mispredicted samples. This information can later be exploited to support the strategy selected by the user :

* Improve model design: removing a problematic feature, removing samples likely to be mislabeled, ensemble with a model trained on a problematic subpopulation;
* Enhance data collection: gather more data regarding the most erroneous or under-represented populations;
* Select critical samples for manual inspection thanks to the Error Tree, and avoid primary predictions on them using :doc:`model assertions </machine-learning/supervised/ml-assertions>`.

Setup
======

Model error analysis is provided as a plugin, which you need to install and build the code-env for.

For more details, please see `the plugin page <https://www.dataiku.com/product/plugins/model-error-analysis/>`_ .

**Tier 2 support**: This capability is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

Using model error analysis
==========================

After training a model, go to the model's page and click on "Views", then select the "Model error analysis" view.

Error Tree
----------

.. image:: img/mea_error_tree.png

The Error Tree for the analyzed model is shown in the main window. This is a Decision Tree which breaks down all the
errors constituting the original model's mistakes into interpretable subgroups.

The top panel highlights the main metrics:

* Original model error rate: proportion of samples in the test set the original model predicted incorrectly.
* Fraction of total error: incorrect predictions present in a selected node over the total number of incorrect predictions in the whole population.
* Local error: incorrect predictions in a selected node over the number of samples in the node.

The fraction of total error is represented in the width of the tree branches, and draws a path towards the nodes
containing the majority of mistakes.

The local error is represented with the level of red in a node, and is the error rate within the node's subpopulation.

The interesting nodes are the ones containing the majority of errors (thickest branches), and possibly with the highest
local error rates (highest red levels, especially higher than the original model error rate).

Nodes and Charts
----------------

.. image:: img/mea_histograms.png

When clicking on a node, a panel appears on the left with local information regarding the population in that node.
In particular the decision rule section allows the user to know at a glance the segment of data represented by the node,
while the univariate histograms show the features most correlated with the errors.

For each feature, we can compare its distribution in the node to its distribution in the whole test set
(by enabling 'in all samples'). Looking at the discrepancy between the two distributions helps you to interrogate which
feature values characterize the majority of the model errors.

Template Notebook
-----------------

For coders who want to go further in their analysis, a python library is also provided with the plugin.
Inside a notebook or a python recipe, users can use Model error analysis to investigate a visual DSS model, as described
in the template notebook released with the plugin.

.. image:: img/mea_notebook_template.png
