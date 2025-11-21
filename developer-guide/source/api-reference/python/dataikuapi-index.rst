:tocdepth: 2

Index of the ``dataikuapi`` package
####################################

This page contains the index of classes in the ``dataikuapi`` package and serve as entrypoint to its reference API documentation

Core classes
================

.. autosummary::
    dataikuapi.DSSClient
    dataikuapi.dss.project.DSSProject

Project folders
================

.. autosummary::
    dataikuapi.dss.projectfolder.DSSProjectFolder
    dataikuapi.dss.projectfolder.DSSProjectFolderSettings

Datasets
=========

.. autosummary::
    dataikuapi.dss.dataset.DSSDataset

Statistics worksheets
=====================

.. autosummary::
    dataikuapi.dss.statistics.DSSStatisticsWorksheet

Managed folders
=================

.. autosummary::
    dataikuapi.dss.managedfolder.DSSManagedFolder

Streaming endpoint
==================

.. autosummary::
	dataikuapi.dss.streaming_endpoint.DSSStreamingEndpoint

Recipes
========

.. autosummary::
    dataikuapi.dss.recipe.DSSRecipe
    dataikuapi.dss.recipe.GroupingRecipeCreator
    dataikuapi.dss.recipe.JoinRecipeCreator
    dataikuapi.dss.recipe.StackRecipeCreator
    dataikuapi.dss.recipe.WindowRecipeCreator
    dataikuapi.dss.recipe.SyncRecipeCreator
    dataikuapi.dss.recipe.SamplingRecipeCreator
    dataikuapi.dss.recipe.SQLQueryRecipeCreator
    dataikuapi.dss.recipe.CodeRecipeCreator
    dataikuapi.dss.recipe.SplitRecipeCreator
    dataikuapi.dss.recipe.EvaluationRecipeCreator

Machine Learning
=================

.. autosummary::
    dataikuapi.dss.ml.DSSMLTask
    dataikuapi.dss.ml.DSSMLTaskSettings

Experiment Tracking
====================

.. autosummary::
    dataikuapi.dss.mlflow.DSSMLflowExtension


Code Studios
============

.. autosummary::
	dataikuapi.dss.codestudio.DSSCodeStudioObject

Jobs
=====

.. autosummary::
    dataikuapi.dss.job.DSSJob

Scenarios
===============

.. autosummary::
    dataikuapi.dss.scenario.DSSScenario
    dataikuapi.dss.scenario.DSSScenarioRun
    dataikuapi.dss.scenario.DSSTriggerFire

API node services
==================

.. autosummary::
    dataikuapi.dss.apiservice.DSSAPIService
    dataikuapi.dss.ml.DSSMLTask


User-defined meanings
========================

.. autosummary::
    dataikuapi.dss.meaning.DSSMeaning

Administration
===============

.. autosummary::
    dataikuapi.dss.admin.DSSUser
    dataikuapi.dss.admin.DSSGroup
    dataikuapi.dss.admin.DSSConnection
    dataikuapi.dss.admin.DSSAuthorizationMatrix
    dataikuapi.dss.admin.DSSGeneralSettings
    dataikuapi.dss.admin.DSSUserImpersonationRule
    dataikuapi.dss.admin.DSSGroupImpersonationRule
    dataikuapi.dss.admin.DSSInstanceVariables
    dataikuapi.dss.admin.DSSGlobalUsageSummary
    dataikuapi.dss.admin.DSSPersonalApiKey
    dataikuapi.dss.admin.DSSPersonalApiKeyListItem
    dataikuapi.dss.admin.DSSGlobalApiKey
    dataikuapi.dss.future.DSSFuture
    dataikuapi.dss.admin.DSSCluster
    dataikuapi.dss.data_directories_footprint.DSSDataDirectoriesFootprint

Jupyter notebooks
====================

.. autosummary::
    dataikuapi.dss.jupyternotebook.DSSJupyterNotebook

SQL notebooks
===============

.. autosummary::
    dataikuapi.dss.sqlnotebook.DSSSQLNotebook
    dataikuapi.dss.sqlnotebook.DSSSQLNotebookListItem
    dataikuapi.dss.sqlnotebook.DSSNotebookContent
    dataikuapi.dss.sqlnotebook.DSSNotebookHistory
    dataikuapi.dss.sqlnotebook.DSSNotebookQueryRunListItem

SQL queries
====================

.. autosummary::
	dataikuapi.dss.sqlquery.DSSSQLQuery

Metrics and checks
====================

.. autosummary::
    dataikuapi.dss.metrics.ComputedMetrics

Model Evaluation Store
======================

.. autosummary::
        dataikuapi.dss.modelevaluationstore.DSSModelEvaluationStore
        dataikuapi.dss.modelevaluationstore.DSSModelEvaluationStoreSettings
        dataikuapi.dss.modelevaluationstore.DSSModelEvaluation
        dataikuapi.dss.modelevaluationstore.DSSModelEvaluationFullInfo
