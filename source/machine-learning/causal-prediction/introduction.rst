Introduction
############

`Causal prediction <https://knowledge.dataiku.com/latest/ml-analytics/causal-prediction/concept-causal-prediction.html>`_ should be used when you want to estimate the effect of a **treatment** variable onto an **outcome** variable.
For instance, you may want to predict:

- the effect of a drug on a patient, given their individual characteristics
- the effect of a discount on a customer, given their customer data.

Unlike the AutoML prediction task, the Causal Prediction modeling task focuses on predicting the **treatment effect** i.e. the difference between the outcomes with and without treatment, all else equal.

Note that at the individual level this difference is based on one observed outcome, and one unobserved outcome, referred to as the **counterfactual outcome**, for instance:

- the health outcome of a patient, would they have received the other possible drug/placebo treatment
- the sales outcome of a customer, would they have received the other discount/no-discount treatment.

This predicted difference is often referred to as the **Conditional Average Treatment Effect (CATE)**.

This CATE prediction can help identify rows of the dataset where the highest effects from the treatment are expected, and in turn optimize the treatment allocation.

.. contents:: :depth: 1
    :local:


Prerequisites and limitations
==============================

Training & running a causal prediction model requires a compatible :doc:`code environment </code-envs/index>`. Supported Python versions are 3.8 to 3.13.

Select the "Visual Causal Machine Learning" package preset in a code env's Packages to install > Add sets of packages, and update your code-env.

.. warning::

	Causal prediction is incompatible with the following:

	* MLflow models
	* Models ensembling
	* Model export
	* Model Evaluation Stores
	* Model Document Generator


Both **binary treatments**, i.e. with a control group and a single treatment group, and **multi-valued treatments** are supported. Binary treatments are either: 

* treatments with exactly two values (control and treated) 
* treatments with more than two values, when the multi-valued treatment option is disabled: the treatment values will be binarized as either equal to the selected control value (control group), or different from it (treated group). 

When the treatment variable contains more than two values and by enabling the multi-valued treatment option, as many models as there are treatment values (excluding the control value) are trained on the relevant subset of the train data.

For classification tasks, only binary outcome variables are supported.


Train a causal prediction model
===============================

From your dataset, in the *Lab* sidebar, select *Causal Prediction*. Specify the columns to use as outcome variable and treatment variable.

.. note::

	To get a concrete use case, see the `Tutorial | Causal prediction <https://knowledge.dataiku.com/latest/ml-analytics/causal-prediction/tutorial-causal-prediction.html>`_.


Treatment variable
------------------

Your dataset must contain a treatment variable.

If the treatment variable contains exactly two values (control and treated), the treatment is automatically considered binary.

If the treatment variable contains several values in addition of the control value, it is considered multi-valued by default. As many causal models as there are treatment values (excluding the control value) are trained on the relevant subset of the train data.
However, the treatment variable can also be binarized based on the **control value** setting, by opting out of the multi-valued option. The treatment is then considered binary, as either:

* equal to the control value (non treated), or
* different from it (treated). 


Outcome variable
----------------

Outcome can be either:

* numerical (causal regressions), or
* categorical (causal classifications): in this case, only binary outcome variables are supported.

For binary outcome variables, you need to select the **preferred class**. The predicted probabilities used to compute the predicted effects are the probabilities of the outcome variable being equal to the preferred class.
