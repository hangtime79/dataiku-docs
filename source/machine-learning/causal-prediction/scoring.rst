Scoring recipe
##############

.. contents:: :depth: 1
    :local:

Causal scoring
==============

The purpose of this recipe is to build a scored dataset by computing the predicted treatment effect based on the input data and the saved causal model. For multi-valued treatment variables, the recipe outputs as many treatment effects as there are treatment values (excluding the control value).

By design, neither the outcome, nor the treatment variable are required as input.

For binary treatment variables, the treatment recommendation option allows you to select rows with the largest predicted effects, based on:

* an explicit CATE value: all rows with a predicted effect above the threshold will be recommended for treatment.
* an exact ratio of the population to be scored: the dataset is scored to predict all the treatment effects, then sorted by predicted effects (requires holding the full dataset in memory) and the rows with the largest values will be recommended for treatment.
* an approximate ratio of the population to be scored: same as the previous option except that small fluctuations of the input ratio are tolerated in order to compute the top values without holding all the data in memory (recommended for larger datasets).


Propensity scoring
==================

If a propensity model was trained by enabling the :ref:`Treatment Analysis <treatment analysis>` setting in the Lab Analysis, the recipe additionally computes the predicted propensity, i.e. probability of receiving the treatment on each row. For multi-valued treatment variables, it outputs as many propensities as there are treatment values (including the control value).
