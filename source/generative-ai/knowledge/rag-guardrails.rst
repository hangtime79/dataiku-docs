RAG guardrails
###############

Beware: should not be confused with the standard :doc:`Guardrails </generative-ai/guardrails/index>` that apply to all 
LLM use cases.

RAG guardrails are specific capabilities that only apply on Retrieval-Augmented LLM. Their sole focus is ensuring
that the selected context and answer make sense given the question and knowledge bank.


.. note::

    RAG Guardrails are available to customers with the *Advanced LLM Mesh* add-on

Select an auxiliary LLM and an embedding model to evaluate the answer of an augmented LLM. Define minimum thresholds for:

* the *relevancy* of the response: how much it addresses the user query
* the *faithfullness* of the response: how consistent it is with the retrieved excerpt

Set the outcome when the output is below threshold: either reject the request or replace the answer by an explanatory response.
