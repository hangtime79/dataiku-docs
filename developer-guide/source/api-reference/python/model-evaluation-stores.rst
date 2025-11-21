:tocdepth: 2

Model Evaluation Stores
#######################

For usage information and examples, see :doc:`/concepts-and-examples/model-evaluation-stores`

There are two main parts related to the handling of model evaluation stores in Dataiku's Python APIs:

* :class:`dataiku.core.model_evaluation_store.ModelEvaluationStore` and :class:`dataiku.core.model_evaluation_store.ModelEvaluation` in the `dataiku` package. They were initially designed for usage within DSS.

* :class:`dataikuapi.dss.modelevaluationstore.DSSModelEvaluationStore` and :class:`dataikuapi.dss.modelevaluationstore.DSSModelEvaluation` in the `dataikuapi` package. They were initially designed for usage outside of DSS.

Both set of classes have fairly similar capabilities.


dataiku package API
-------------------

.. autoclass:: dataiku.ModelEvaluationStore
    :members:

.. autoclass:: dataiku.core.model_evaluation_store.ModelEvaluation
    :members:


dataikuapi package API
----------------------

.. automodule:: dataikuapi.dss.modelevaluationstore
	:members:
	:member-order: bysource
	:undoc-members:

