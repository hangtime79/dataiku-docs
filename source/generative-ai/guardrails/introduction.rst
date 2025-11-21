Introduction to guardrails
##########################

Guardrails pipeline
====================

Each time a LLM query or response must be verified, this is handled by a *guardrails pipeline*. 

A guardrails pipeline is made of a number of individual steps. Each step can perform checks on either the queries, the responses or both.

Some of the available steps are:

* :doc:`PII detection <pii-detection>`
* Forbidden terms detection
* :doc:`Prompt injection detection <prompt-injection-detection>`
* :doc:`Toxicity detection <toxicity-detection>`
* :doc:`Topics boundaries checking <topics-boundaries>`
* :doc:`Bias detection <bias-detection>`

In addition to the builtin guardrails, you can write your own, to add your own specific rules. For example, you can write a guardrail to ensure a certain tone of response, to check correctness against custom ontologies, etc...

See :doc:`custom-guardrails` for more details

Connection-level guardrails
============================

The first place where guardrails are used is at the connection level, where you define which LLMs DSS can connect to. Guardrails are per-connection, which allow you to apply
differentiated policies.

For example, you could have a policy where PII can only be processed using locally-running models, but for non-PII data, you can use external providers. You would then define guardrails
with PII detection enabled on the external connections, but not on the HuggingFace connection.


Agent-level guardrails
========================

When you use :doc:`DSS agent-building capabilities </agents/index>`, you are in effect creating a new kind of LLM, that can be leveraged in the various "usage points" of the LLM Mesh (Prompt Studio, Prompt Recipe, Chat UIs, API).

In addition to the processing done by the agent itself, you may wish to add guardrails on that agent, e.g. to make sure that an unplanned case cannot does not lead to unexpected outcomes.

Usage-time guardrails
======================

In addition to the "enforcement" guardrails defined on the connection, guardrails can also be defined "at time of usage".

This allows guardrails to be used not only on a generic "per LLM" manner (where you are mostly trying to "protect the LLM and protect against the LLM"), but also on a "per use case", whereby you can define guardrails for this use case.

For example, if you are using a Prompt Recipe to process a dataset containing customer complaints, in order to write email responses to these customers, it can make sense to add a "Topics Boundaries" guardrail on the Prompt Recipe itself to ensure that none of the generated emails is suggesting giving a discount or refund.