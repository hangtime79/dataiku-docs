
Causal Prediction Algorithms
############################

Dataiku offers two different methodologies for estimating causal effects:

.. contents:: :depth: 1
    :local:

.. _meta learning: 

Meta-learning
-------------

Meta-learning leverages machine learning algorithms to learn the causal effect of the treatment (Conditional Average Treatment Effect or CATE). These ML models are called *base learners*. The specific way they are trained and combined is referred to as the *meta-learner*. Dataiku supports three meta-learners: 

* **S-learner**: a single model is trained with the treatment variable as an input feature. The predicted CATE is the difference between the prediction with the treatment variable set as ``treated`` and the prediction with the treatment variable set as ``control``.

* **T-learner**: two models are trained, one on the ``treated`` group, the other on the ``control`` group. The predicted CATE is the difference between the predictions from the two models.

* **X-learner**:

  * Two models are trained, one on the ``treated`` group, the other on the ``control`` group (same as T-learner).
  * They are used to individually predict the counterfactual outcome (i.e. control for treated group and treated for control group), which is combined with the observed outcome to estimate the individual treatment effect.
  * Then, two other models (again, one for ``treated`` group and one for ``control`` group) are trained on the individual effects previously predicted. The CATE prediction is the average prediction of these last two models weighted by a predicted propensity (individual predicted probability of getting the treatment).

You can combine any meta-learner with any available :doc:`Python-based ML algorithm </machine-learning/algorithms/in-memory-python>` as a base learner.


.. _causal forest:

Causal forest
-------------

Causal Forests are tree-based ensemble models similar to :ref:`Random Forests <random forest>`. The main differences are:

* the **value** of nodes and leaves are based on both the treatment and the outcome variables - they are an estimation of the Conditional Average Treatment Effect (CATE)
* the **splitting criterion** is also based on both the treatment and the outcome variables
* the **honest** framework (whenever enabled) allows using two separate subsets of the train set to compute the optimal split and the value of a node.


Parameters:

- **Number of trees**: Number of trees in the causal forest.  Increasing the number of trees in a causal forest does not result in overfitting. This parameter can be optimized.
- **Feature sampling strategy:** Adjusts the number of features to sample at each split.

  - Automatic will select 30% of the features.
  - Square root and Logarithm will select the square root or base 2 logarithm of the number of features respectively
  - Fixed number will select the given number of features
  - Fixed proportion will select the given proportion of features

- **Maximum depth of tree**: Maximum depth of each tree in the causal forest. Higher values generally increase the quality of the prediction but can lead to overfitting. Higher values also increase the training and prediction time. Use 0 for unlimited depth (i.e., keep splitting the tree until each node contains the minimum number of samples per leaf),
- **Minimum samples per leaf**: Minimum number of samples required in a single tree node to split this node. Lower values increase the quality of the prediction (by splitting the tree mode), but can lead to overfitting and increased training and prediction time.
- **Honest**: Whether or not the honest framework is used to build trees. If set to true, the learning algorithm will use two separate subsets of the train set to compute the optimal split and the value of a node.

- **Parallelism:** Number of cores used for parallel training. Using more cores leads to faster training but at the expense of more memory consumption, especially for large training datasets.