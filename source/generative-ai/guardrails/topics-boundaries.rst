Topics Boundaries
##########################

.. note::

    This capability is provided by the "Topics Boundaries Guardrail" plugin, which you need to install. Please see :doc:`/plugins/installing`.

    This plugin is :doc:`Not supported </troubleshooting/support-tiers>`.

    This capability is available to customers with the *Advanced LLM Mesh* add-on.

The Topics Boundaries guardrail check that questions to a LLM or responses, either:

* Discuss only about one of the allowed topics
* Do not discuss about one of the forbidden topics

This is particularly useful to ensure that users cannot cause a Chatbot designed to discuss about a certain topic to veer off course.

Topics Boundaries guardrail leverages an auxiliary LLM for assessing whether a query or response respects the rule ("LLM as a judge" approach).

It can be configured to either:

* block the request (with an error)
* simply audit the off-track conversation
* politely decline to respond
