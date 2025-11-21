External Models
###############

External Models are a way to surface, evaluate and use in DSS Models that are already deployed on Amazon SageMaker, Azure Machine Learning, Google Vertex AI or Databricks.

Using External Models, you can create a DSS Saved Model from an endpoint deployed on the infrastructures of one of those supported cloud vendors.

This allows you to benefit from the ML management capabilities of DSS on your existing External Models:

* Scoring datasets using a :ref:`scoring recipe <explanations_scoring_recipe_label>`
* Managing multiple versions of the models
* Evaluating the performance of a classification or regression model on a labeled dataset, including all results screens
* Comparing multiple models or multiple versions of the model, using :doc:`Model Comparisons </mlops/model-comparisons/index>`
* Analyzing performance and evaluating models :doc:`on other datasets </mlops/model-evaluations/index>`
* :doc:`Analyzing drift </mlops/drift-analysis/index>` on the External Model

Creating an External Model
~~~~~~~~~~~~~~~~~~~~~~~~~~

Before creating an External Model, you must create the "External Models" code
environment. To do so, as an Administrator, go to "Administration > Code envs >
Internal envs setup", look for "External Models code environment", and click on "Create code
environment".

You can then create an External Model by going to a project, click on the
"Saved Models" link in the navigation bar, and, from the saved models page,
click on the "New External Saved Model" button.


You can also create an External Saved Model using the public Python API, with
:meth:`dataikuapi.dss.DSSProject.create_external_model` and
:meth:`dataikuapi.dss.DSSSavedModel.create_external_model_version`.

.. note::

  Most cloud vendors impose few constraints on models, and endpoints are
  allowed to behave in arbitrary ways and most noticeably to return any kind of data.

  It is thus not possible to guarantee compatibility or unfettered ability to
  use all features (notably advanced features such as performance evaluation,
  model comparison or drift analysis) for all models.

  See :doc:`/mlops/external-models/input-output-formats` for more details.


.. warning::

   External Models can not be included in an API package. External Models can not be exported.


.. toctree::
        :maxdepth: 2

        input-output-formats
