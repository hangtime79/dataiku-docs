Evaluating GenAI use cases
############################

.. contents::
    :local:

With the adoption of large language models (LLMs), which are able to use natural language as input or output, the topic of evaluating their performance is both important and not trivial.
Standard model evaluation techniques are not well-suited; evaluation of LLMs requires a specific treatment.

This is why Dataiku offers the "Evaluate LLM" recipe. This recipe generates various outputs, the most pivotal of which is a model evaluation stored in a :doc:`model evaluation store </mlops/model-evaluations/analyzing-evaluations>`. From this model evaluation store, you can then complete your LLMOps actions with alerting or automated actions.

.. note::

    The "Evaluate LLM" recipe is available to customers with the *Advanced LLM Mesh* add-on.

For more details on LLM evaluation, please see :doc:`/mlops/model-evaluations/llm-evaluation`
