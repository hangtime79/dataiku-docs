ML Assertions
##################

ML assertions provide a way to streamline and accelerate the model evaluation process, by automatically checking that predictions for specified subpopulations meet certain conditions.

With ML assertions, you can programmatically compare the predictions you expect with the model's output. You define expected predictions 
on segments of your test data, and DSS will check that the model's predictions are aligned with your judgment. 

By defining assertions, you are checking that the model has picked up the patterns that are most important for your prediction task.

ML assertions checks can be automated by using DSS :doc:`checks system<../../metrics-check-data-quality/checks>`. This will enable you to
be warned if new versions of your model do not behave as expected.

ML assertions are defined in Analysis > Design > Debugging.

ML assertions results are available:

* in the model page under the Metrics & Assertions tab.
* in deployed saved models under the `Metrics & Status` tab as metrics to display.
* in deployed saved models under the `Settings > Status checks` tab for defining checks that can be run in scenarios.
* in the output of an evaluation recipe in the metrics dataset.
* through the performance metrics API

-----

.. contents::
	:local:


Defining assertions
===================

To define assertions DSS provides a filter-recipe-like interface with multiple *where* criteria to define the subsample
and the condition that should be met by the model's predictions.

The *where* criteria will define a filter that DSS applies on the test set to extract the subsample on which assertion should be computed.
To define the assertion condition you will need to provide the following inputs:

* For classification you will be prompted to select one of the target classes and a minimum ratio of rows (Valid ratio) that should be predicted as this class for your assertion to pass.
* For regression you will be prompted to select a range of predicted values and a minimum ratio of rows (Valid ratio) that should fall within this range for your assertion to pass.

At the end of training, the assertions are tested against the test set. 
If the **effective** valid ratio is strictly less than the **expected** valid ratio the assertion is considered to fail, and a :doc:`diagnostic<../diagnostics>` will be raised.

Assertion's result
==================

For each assertion the computation will yield assertion metrics which are composed of:

* a name: the name of the assertion
* a result: whether the assertion passed
* a number of matching rows: number of rows that matched the assertion filter
* a number of rows dropped: number of rows that matched the assertion filter and were dropped by the model's preprocessing
* a valid ratio: percentage of rows that satisfy the assertion condition 

At the ml task level a **passing assertions ratio** is also computed. It is the ratio of passing assertions over the total number of assertions which were able to be calculated.

No matching row
=================

If no row matches the assertion filter (e.g. typo in one of the criteria), or all rows matching the filter are dropped by the model's preprocessing, part of the assertion result cannot be computed. 
The valid ratio and assertion result will not be defined. They will show as "-" in the UI and as ``null`` in the assertions metrics (in the evaluation recipe, metrics & checks...).

If all the assertions of the ML task yield null results, the passing assertions ratio is also undefined ("-" in the UI and ``null`` in assertions metrics).

When no row matches the filter or all rows are dropped, a specific :doc:`diagnostic<../diagnostics>` will be raised.

Assertions' metrics & Checks
============================

After deploying a model, in the `Metrics & Status` tab of the saved model you can add assertion metrics to the table by clicking on
the `X/Y metrics` button and by selecting some of the following metrics:

* `Dropped rows: ANY_AVAILABLE_ASSERTION_NAME`
* `Rows matching criteria: ANY_AVAILABLE_ASSERTION_NAME`
* `Valid ratio: ANY_AVAILABLE_ASSERTION_NAME`
* `Passing assertions ratio`

The same metrics are available in the `Settings > Status checks` tab for defining :doc:`checks<../../metrics-check-data-quality/checks>`.
These checks can be used in scenarios to automate model validation.

Evaluation recipe
=================

When running an evaluation recipe, DSS provides a checkbox to decide whether you want to compute assertions. 
If checked you will have two additional columns in the metrics dataset:

* `passingAssertionsRatio` is the ratio of assertions that pass
* `assertionsMetrics` is a map. Keys are assertion names and values are maps representing an assertion's result. These maps are composed of one key/value pair per attribute of assertion result. The list of attributes are defined in the assertion's result section above.

Limitations
===========

ML assertions are **not** available for:

* Clustering tasks
* Backends other than in-memory python backend
* Ensemble models
