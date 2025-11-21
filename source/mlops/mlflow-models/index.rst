MLflow Models
#############

`MLflow <https://www.mlflow.org>`_ is an open-source platform for managing the machine learning lifecycle.

MLflow offers a standard format for packaging trained machine learning models: `MLflow Models <https://www.mlflow.org/docs/2.17.2/models.html>`_.

You can import MLflow models in DSS, as DSS saved models. This allows you to benefit from all of the ML management capabilities of DSS on your existing MLflow models:

* Scoring datasets using a :ref:`scoring recipe <explanations_scoring_recipe_label>`
* Deploying the model in a bundle on an automation node. See :doc:`/deployment/index`
* Deploying the model for real-time scoring, using the :doc:`API node </apinode/index>`
* Managing multiple versions of the models
* Evaluating the performance of a classification or regression model on a labeled dataset, including all results screens
* Comparing multiple models or multiple versions of the model, using :doc:`Model Comparisons </mlops/model-comparisons/index>`
* Analyzing performance and evaluating models :doc:`on other datasets </mlops/model-evaluations/index>`
* :doc:`Analyzing drift </mlops/drift-analysis/index>` on the MLflow model
* :doc:`Governing the MLflow model using the Govern Node </governance/index>`

.. note::

	The MLflow model import feature is supported, and Dataiku tests it with a variety of different MLflow models.
	Dataiku makes best effort to ensure that the advanced capabilities of its MLflow import support are compatible with
	the widest possible variety of MLflow models. 

	However, MLflow imposes extremely few constraints on models, and different MLflow models are allowed to behave in arbitrary non-standard ways and to return completely different kind of data.

	It is thus not possible to guarantee unfettered ability to use all features (notably advanced features such as performance evaluation, model comparison or drift analysis) with all types of models.


.. toctree::
	:maxdepth: 1

	importing
	using
	training
	limitations
