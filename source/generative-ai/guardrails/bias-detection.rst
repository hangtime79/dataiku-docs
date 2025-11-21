Bias Detection
##############

.. note::

    This capability is provided by the "Bias Detection Guardrail" plugin, which you need to install. Please see :doc:`/plugins/installing`.

    This plugin is :doc:`Not supported </troubleshooting/support-tiers>`.

    This capability is available to customers with the *Advanced LLM Mesh* add-on.

The Bias Detection guardrail check that questions to a LLM or responses do not exhibit bias or stereotyped statements, notably racial, religious, gender-based, sexuality-based or disability-based.

The Bias Detection guardrail first uses a small specialized model to provide a first level of filtering. This small specialized model however has a significant false positive rate. Optionally, the Bias Detection guardrail can then use an auxiliary LLM to confirm or infirm the initial assumption ("LLM as a judge" approach).


It can be configured to either:

* block the request (with an error)
* simply audit the biased conversation
* ask the guarded LLM to rewrite its answer
