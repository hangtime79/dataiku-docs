Cost Control
################################

Cost Control in the LLM Mesh helps you manage your LLM costs by setting alerting & blocking thresholds.


.. note::
	You need a licence with Advanced LLM Mesh to customize quotas. If your license does not include it, you can only set up a single global quota (see *Fallback Quota*), which is applied to all LLM queries.

Concepts
=========

You can set **quotas** that allow you to track spending and decide whether to block queries once the quota is exhausted.

For each **quota**, you can specify:

* **scope**: LLM queries matched by the quota. Can be all queries, or matching a filter: LLM provider, DSS project, connections, users… Note that a single query can match multiple quotas.
* **quota amount**: maximum LLM costs, in US dollars, allocated for the quota.
* **blocking quota**: whether the LLM queries are blocked once the quota amount is reached.
* **reset period**: time period over which queries are aggregated, *e.g.* every calendar month or rolling 15 calendar days.
* **alerting**: optional cost thresholds that trigger an email alert. When set up, you are also notified when the quota becomes blocked.

.. note::
	A query can match *multiple quotas*, in that case *all matching quotas* see their current spend incremented.

The **Fallback Quota** applies to queries not matching any other quota.


Limitations
===========

Cost tracking is not supported for the following LLM providers: 

* *Amazon SageMaker LLM*
* *Databricks Mosaic AI*
* *Snowflake Cortex*

You cannot create a quota that targets these models specifically, but queries using these models can still match a quota (e.g. a quota with a DSS project scope). If a matched quota is blocking and exhausted, then these queries will be blocked.

*Local Hugging Face* models cannot be targeted nor blocked by quotas.

Setup
=====

A dedicated **Cost Control** section lets you configure the quotas and check their status. Find it in **Administration** > **Settings** > **LLM Mesh**.
