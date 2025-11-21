Extract failed rows
#####################################

.. contents::
	:local:

The "extract failed rows" recipe allows users to create a new dataset containing the records that failed the Data Quality rules defined on the input dataset.

The output dataset will include all columns from the original dataset and new columns that have been appended for each Data Quality rule.

.. seealso::

	For more information about Data Quality, see also the following article in the Knowledge Base:

    - `Concept | Data Quality rules <https://knowledge.dataiku.com/latest/automation/data-quality/concept-data-quality.html>`_
    - `Tutorial | Data Quality <https://knowledge.dataiku.com/latest/automation/data-quality/tutorial-data-quality.html>`_

Create a recipe
===============

Users have two options to extract their failed Data Quality rows.

The first option is to initiate the extract from the ‘Current status’ tab of the Data Quality view within a dataset under the vertical dots 'More actions'.

The second option is to click on the '+Recipe' button from the flow. Alternatively, if you have selected a dataset, go to the right panel’s Action tab, and select 'Other recipes' > 'Extract failed rows'.


Supported Data Quality rules
============================

The extract failed rows recipe is currently compatible with 6 rule types:

* Column values are not empty
* Column values are empty
* Column values are unique
* Column values in set
* Column values in range
* Column values are valid according to meaning (only with DSS engine)

Engines
=======

Depending on the input dataset types, DSS will adjust the engine it uses to execute the recipe, and choose
between Hive, Impala, SparkSQL, plain SQL, and internal DSS. The available engines can be seen and selected by
clicking on the cogwheel below the "Run" button.

Data Quality rules selection
============================

In the 'Selected rules' tab, you have the possibility to choose on which rules to apply the extraction.
If a rule is defined on multiple columns, there will be as many entries in the table to select on which rule/column to apply the extraction.

Rules are listed in the same order as in the Data quality tab of the input dataset.

At recipe creation, all compatible rules will be selected by default.
Moreover, the 'Always select all' option will be checked.
This option guarantees all new rules added on the input dataset after the last save of the recipe and compatible for extraction will automatically be selected.
Note that a rule can be compatible for extraction but not supported by the selected engine, e.g. the :ref:`meaning validity rule<meaning-validity-rule>` with any other engines than DSS.
