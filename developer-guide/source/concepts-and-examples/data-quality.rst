Data Quality
################

..
  this code samples has been verified on DSS: 14.1.0
  Date of check: 09/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 04/10/2024

You can interact with Data Quality through the API.

Basic operations
================

Listing Data Quality rules of a dataset
---------------------------------------

.. code:: python

	project = client.get_project("SomeProjectId")
	dataset = project.get_dataset("SomeDatasetId")
	ruleset = dataset.get_data_quality_rules()
	rules = ruleset.list_rules()
	# Returns a list of DSSDataQualityRule

	for rule in rules:

		# Access to main information of the rule
		print("Rule id: %s" % rule.id)
		print("name: %s" % rule.name)

Computing a rule
----------------

.. code-block:: python

	project = client.get_project("SomeProjectId")
	dataset = project.get_dataset("SomeDatasetId")
	ruleset = dataset.get_data_quality_rules()
	rules = ruleset.list_rules()
	future = rules[0].compute()
	future.wait_for_result()

Creating a rule
---------------

.. code-block:: python

	project = client.get_project("SomeProjectId")
	dataset = project.get_dataset("SomeDatasetId")
	ruleset = dataset.get_data_quality_rules()
	rule_config = { "type": "RecordCountInRangeRule", "softMinimum": 10, "softMinimumEnabled": True, "displayName": "My newly created rule."}
	newRule = ruleset.create_rule(rule_config)

Deleting a rule
---------------

.. code-block:: python

	project = client.get_project("SomeProjectId")
	dataset = project.get_dataset("SomeDatasetId")
	ruleset = dataset.get_data_quality_rules()
	rules = ruleset.list_rules()
	rules[0].delete()


Reference documentation
=======================

Classes
-------

.. autosummary::
    dataikuapi.DSSClient
    dataikuapi.dss.data_quality.DSSDataQualityRule
    dataikuapi.dss.data_quality.DSSDataQualityRuleSet
    dataikuapi.dss.dataset.DSSDataset
    dataikuapi.dss.future.DSSFuture
    dataikuapi.dss.project.DSSProject

Functions
---------

.. autosummary::
    ~dataikuapi.dss.data_quality.DSSDataQualityRule.compute
    ~dataikuapi.dss.data_quality.DSSDataQualityRuleSet.create_rule
    ~dataikuapi.dss.data_quality.DSSDataQualityRule.delete
    ~dataikuapi.dss.dataset.DSSDataset.get_data_quality_rules
    ~dataikuapi.dss.project.DSSProject.get_dataset
    ~dataikuapi.DSSClient.get_project
    ~dataikuapi.dss.data_quality.DSSDataQualityRuleSet.list_rules
    ~dataikuapi.dss.future.DSSFuture.wait_for_result
