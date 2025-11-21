Rate Limiting
#############

Rate limiting in the LLM Mesh helps manage the flow of LLM queries and ensure compliance with provider-side usage limits.

Concepts
========

Rate limits are enforced per LLM model and per provider. They apply to all queries executed through the LLM Mesh — across projects, LLM connections, and users.

Limits are expressed in *requests per minute* (*RPM*). If the rate is exceeded:

* Requests are automatically throttled (*i.e.*, delayed).
* If the request cannot be served within a reasonable delay, it fails with a rate limiting error.


DSS provides *baseline settings* with sensible production-ready defaults. These settings are fully configurable, allowing you to override them as needed to match your specific use case or provider requirements.

Rule Configuration
==================

Rate limiting rules are defined **per provider**, and can be defined in two ways:

* For *specific models* within that provider.
* As a *default fallback* that applies to all other models from the provider.

Each provider's default rule can target one of the following model categories:

* Completion models
* Embedding models
* Image generation models

Limitations
===========

Rate Limiting is not supported for the following LLM connections:

* *Amazon SageMaker LLM*
* *Databricks Mosaic AI*
* *Snowflake Cortex*
* *Local Hugging Face*

Setup
=====

A dedicated **Rate Limiting** section lets you configure the rate limits. Find it in **Administration** > **Settings** > **LLM Mesh**.
