Custom Guardrails
###################

.. note::

    Custom Guardrails are available to customers with the *Advanced LLM Mesh* add-on


Custom Guardrails can be written in Python, in a plugin.

You must be familiar with plugin development (see :doc:`/plugins/reference/index`
and :doc:`devguide:tutorials/plugins/index`).

You can find a tutorial in the Developer Guide: :doc:`devguide:tutorials/plugins/guardrail/generality/index`.

A sample Custom Guardrail can be found at https://github.com/dataiku/dss-plugin-sample-guardrail-rewrite-answer/

Here are some of the capabilities that Custom Guardrails can implement, in addition to the obvious "reject failing requests"

* Modify requests (before the LLM) and responses (after the LLM)
* Ask the LLM to retry / rewrite its answer (providing additional instructions)
* Short-circuit the LLM and directly respond (for example, to politely decline to engage in the topic)
* Add information to the audit log

Of course, Custom Guardrails can themselves leverage LLMs (and many will usually do). Custom Guardrails are fully integrated in Dataiku's Unified LLM Tracing and this "sub-call" to a LLM will appear in the "upper trace".
