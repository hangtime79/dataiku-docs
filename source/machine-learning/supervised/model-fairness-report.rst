Model fairness report
#####################

Evaluating the fairness of machine learning models has been a topic of both academic and business interest in recent years. However, before prescribing any resolution to the problem of model bias, it is crucial to learn more about how biased a model is, by measuring some fairness metrics. Model fairness reports is intended to help you with this measurement task.

Depending on the context and domain, different metrics of fairness can be applied. No model will be perfect toward all the metrics, thus the choice of metric is crucial. The report shows in a most transparent way several metrics and the difference between them, and from there you can choose the one that best evaluates the fairness of the situation at hand.

Setup
======

Model fairness report is provided by a plugin, which you need to install. You will then need to build the code-env for the plugin.

For more details, please see `the plugin page <https://www.dataiku.com/product/plugins/model-fairness-report/>`_ .

**Tier 2 support**: This capability is covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

Using model fairness report
============================

After training a model, go to the model's page and click on "Views", then select the "Model Fairness Report" view.

Inputs
-------

.. image:: img/model-fairness-report-input.png

* Sensitive column: the column contains sensitive group based on which we want to compute fairness metric.
* Sensitive group: the reference group from which we will compute the metric discrepancies.
* Positive outcome: the target value that is advantageous.

Metrics and Charts
----------------------

.. image:: img/model-fairness-report-output.png


Four different metrics will be computed. Here for illustration purposes we suppose that we are in a loan assessment use case:

* Demographic Parity: people across groups have the same chance of getting the loan.
* Equalized Odds:  
	* Among people who will not default, they have the same chance of getting the loan.
	* Among people who will default, they have the same chance of being rejected.
* Equality of Opportunity: among all people who will not default, they have the same chance of getting the loan.
* Predictive Rate Parity: among all people who are given the loan, across groups there is the same portion of people who will not default (equal chance of success given acceptance).

