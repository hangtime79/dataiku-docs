Drift analysis
################

When models are deployed and used in production, over time, the conditions in real life may drift compared to what was the reality at train time and thus have a possibly negative impact on how the model behaves. This is known as Model Drift.

There can be data drift, i.e. change in the statistic distribution of features, or concept drift, which is due to a modification of the relationship between features and the target.

To monitor model drift, it is necessary to gather new data from the production environments and possibly have ground truth associated with it. See :doc:`/mlops/model-evaluations/automating` for more details.

When you are viewing a :doc:`Model Evaluation in a Model Evaluation Store </mlops/model-evaluations/analyzing-evaluations>`, in addition to the normal result screens, you have access to a "Drift" section, allowing you to perform three kind of drift analysis:

Drift analysis is always about comparing data on the current Model Evaluation compared to a *reference*.

.. toctree::

	reference
	sampling
	input-data-drift
	prediction-drift
	performance-drift
