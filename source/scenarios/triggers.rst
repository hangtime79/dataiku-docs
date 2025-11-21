Launching a scenario
####################

Scenarios can be started manually, or using the DSS Public API.

**Triggers** are used to automatically start a scenario, based on several conditions.

Each trigger can be enabled or disabled. In addition, the scenario must be marked as "active" for triggers to be evaluated.

Types of triggers
=================

In order to cover most usage cases, several types of triggers exist.

.. note::

        If a scenarios contains multiple active triggers, the trigger conditions are evaluated independently. This means that the scenario will be triggered when **any** trigger condition is true.


Time-based triggers
-------------------

These triggers launch scenarios at regular intervals. The periodicity can be monthly, weekly, daily or hourly. Within each period, a given time point is chosen when the scenario is to run (minute of hour, hour of day, ...)


Trigger on dataset change
-----------------------------

These triggers start a scenario whenever a dataset is changed, data-wise or settings-wise. Detection of changes to the data depends on the type of dataset. For filesystem-like datasets (Uploaded, Filesystem, HDFS), a change means a discrepancy in the file names, lengths or last modification time.

For SQL-like datasets however, changes to the data are not detected and a SQL trigger should be used.

Optionally, for filesystem-like datasets, it is possible to specify a file name as a "marker" file whose changing is understood as "the data has changed". When a marker file is specified, changing the other files of the data doesn't activate the **dataset modification trigger**. This makes it possible to prevent the trigger from activating while the dataset files are being modified, and protects against situation where refreshing of a dataset can hang.


Trigger on SQL query change
---------------------------

When the data is stored in a SQL database, one can usually check changes with a query, for example selecting the maximum of some date. A **SQL trigger** runs a query and activates when the output of the query changes (w.r.t. the last execution of the query).

Trigger after scenario
----------------------

These triggers start a scenario after the end of another scenario, optionally with a condition on the followed scenario's outcome (only if successful, only if failed,...).

Python triggers
---------------

Where a fully flexible approach is required, a **Python** trigger can be set up. This type of trigger executes a Python script, and the script can decide to activate the trigger. This makes it possible to query external APIs and do all sorts of checks.


Concurrent triggers
===================

In order to avoid simultaneous runs of a given scenario, the following rules apply to triggers:

* when a trigger activates, the scenario is promoted for execution
* a promoted scenario is launched after a delay of 60 seconds. If no other trigger associated with the scenario activates during the delay, the scenario is launched; otherwise, if another trigger does activate, the scenario is not launched and the delay is reset
* triggers are not evaluated while their scenario runs
* each run of a scenario records the last trigger that activated as the one which launched the run


Trigger parameters
==================

Triggers can pass parameters to the steps and scripts executed in a scenario run. All triggers pass at least their name and type, but some triggers pass additional data:

* SQL triggers pass the output of the query
* Python triggers may pass any data

Manual triggers
================

When you manually run a scenario (either through the DSS UI, or through the public API), you are actually using a specific "manual" trigger. The manual trigger may send parameters, which will be received like other trigger parameters.

To pass parameters through the UI, use the "Run with custom parameters" button in the Actions menu.

See the public API doc for information on how to trigger a scenario through the API.

Evaluation
============

Each trigger has an evaluation interval. DSS will perform the verification (Files timestamps, SQL query, Python code) at each interval.

Note: time-based triggers do not have an evaluation interval.

Examples
========

Launch a scenario every day at 10:00PM
--------------------------------------

* add a *Time-based trigger*
* set its frequency to ``Daily``
* set the field *every day at* to ``22:00``


Launch a scenario whenever a HDFS dataset changes
-------------------------------------------------

* add a *Dataset change trigger*
* select a dataset
* set the check periodicity


Launch a scenario whenever a SQL dataset changes
------------------------------------------------

The dataset change triggers do not read the data, only the dataset's settings, and in the case of datasets based on files, the files' size and last modified date. These triggers will thus not see changes on a SQL dataset, for example on a SQL table not managed by DSS. For these cases, a SQL query change trigger is needed.

* add a *SQL query change trigger*
* write a query that will return a value which changes when the data changes. For example, a row count, or the maximum of some column in the dataset's table.
* set the check periodicity
