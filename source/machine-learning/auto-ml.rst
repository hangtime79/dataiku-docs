Automated machine learning
############################

DSS contains a powerful automated machine learning engine that allows you to get highly optimized models with minimal intervention.

At your choice, in DSS, you can select between:

* Having the full control over all :doc:`training settings <supervised/settings>`, :doc:`algorithm settings <algorithms/index>` and :doc:`optimization process <advanced-optimization>`, including writing your own :doc:`custom models <custom-models>` and using advanced :doc:`deep learning models <deep-learning/index>`

* Using DSS powerful automatic machine learning engine in order to effortlessly get models

The Automated Machine Learning engine of DSS will analyze your dataset, and depending on your preferences, select the best :doc:`features handling <features-handling/index>`, :doc:`algorithms <algorithms/index>` and hyper parameters.

In addition to algorithms selection and optimization, the automated machine learning performs:

* Automatic :doc:`features handling <features-handling/index>`, including handling of categorical and text variables, handling of missing values, scaling, ...

* Semi-automatic massive features generation

* Optional features selection

.. contents::
	:local:

Creating an Automated Machine Learning model
=============================================

- Go to the Flow for your project
- Click on the dataset you want to use
- Select the *Lab*
- Select *AutoML Prediction*
- Choose your target variable (which column you want to predict)
- Select one of the AutoML prediction styles, such as *Quick Prototypes*


Prediction styles
------------------

The Automated Machine Learning engine allows you to choose between three main prediction styles.

Quick Prototypes
%%%%%%%%%%%%%%%%%%%%%

When selecting this prediction style, DSS will select a variety of models, prioritizing variety and speed over pure performance. The main goal of this is to quickly give you first results. It will help you decide whether you need to go further with more advanced models, or if you should first do some more feature engineering.

Interpretable Models
%%%%%%%%%%%%%%%%%%%%%

This prediction style is focused on giving "white-box" models for which it is easier to understand the predictions and the driving factors.

DSS will choose both decision trees and linear models.

Training is generally quick.

High Performance
%%%%%%%%%%%%%%%%%

When selecting this prediction style, DSS will select a variety of tree-based models with a very deep hyper-parameter optimization search. This will generally give the best possible prediction performance, at the expense of interpretability.

Training time will be strongly increased when choosing this prediction style

Customizing an automated machine learning model
-------------------------------------------------

Whereas you selected "Automated machine learning" or "Expert mode", you always keep full control over all of the :doc:`settings of your prediction model <supervised/settings>`, including :doc:`algorithms <algorithms/index>` and :doc:`feature handling <features-handling/index>`

Feature generation
===================

DSS can compute interactions between variables, such as linear and polynomial combinations. These generated features allow for linear methods, such as linear regression, to detect non-linear relationship between the variables and the target. These generated features may improve model performance in these cases.

See :doc:`supervised/settings` for more information.
