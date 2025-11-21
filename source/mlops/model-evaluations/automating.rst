Automating model evaluations and drift analysis
##################################################

Interactively evaluating models is useful, but tracking the performance of a production model requires some level of automation.

Metrics and Checks
====================

The Model Evaluation Stores fully support DSS Metrics and Checks. Performance metrics and data drift metrics are saved as DSS metrics on each ME computation. You can therefore use metrics to, for instance, issue a warning or an error if one of those metrics falls too low (or rise too high in the case of the input data drift). See :doc:`/metrics-check-data-quality/metrics` and :doc:`/metrics-check-data-quality/checks` for additional information.


Scenarios and feedback loop
============================

To monitor the performance of your model over time, you need to evaluate it on a regular basis. This can be done using :doc:`/scenarios/index`.

Performing a new evaluation (and writing it to the Evaluation store) is done using the usual "Build/Train" step, selecting the Evaluation Store as the output.

.. image:: img/build-step.png


Depending on the output of the build, and whether a warning or an error was raised by a check, you may, for instance, send a message to your team or retrain your model and redeploy your model.


Feedback loop
===============

In most cases, in order to perform continuous evaluation and :doc:`/mlops/drift-analysis/index`, you will need to retrieve logs from API nodes in order to know what records are being scored. 

You can use the :doc:`Audit Dispatching and Event Server </operations/audit-trail/centralization-and-dispatch>` for this. This will give you a dataset containing all records scored on your API nodes, which can then be used as input of an Evaluation Recipe.

These records will not contain the "ground truth". In some cases, you will be able to "reconcile the ground truth". For example, if you are evaluating a churn prediction model, you can, after a couple of weeks/months, know whether each customer "ultimately churned". Reconciling the ground truth with the prediction allows you to compute whether the model was right and to perform :doc:`Performance drift analysis </mlops/drift-analysis/performance-drift>`.

Retrieving data from your production system and reconciling the ground truth will be specific to your organization but can usually be done through the Flow as a regular data analysis project.


