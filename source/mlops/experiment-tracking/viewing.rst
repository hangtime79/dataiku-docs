Viewing experiments and runs
############################

The Experiment Tracking UI is available in the Machine Learning menu.

.. image:: img/menu.png

.. contents::
    :local:

Experiments
===========

The main screen displays active experiments by default. You can choose to show the experiments marked for deletion as well.

.. image:: img/experiments_list.png

You can then either:
 
* Click on an experiment to view all of its runs
* Select multiple experiments to compare runs between experiments

Runs
====

The runs list screen displays information on the runs, including which DSS user performed it, metrics, parameters, tags and
a link to the path of the DSS managed folder where the artifacts are stored.

In this screen, runs can be deleted (soft delete) or restored.

The metrics of the runs are represented using charts.

Bar charts
----------

Bar charts display the final performance value of runs. They can be keyed by a parameter or by the run id (default).

.. image:: img/runs_list_bar_chart.png

Line charts
-----------

Metrics can be logged multiple times in a given MLflow run. They are then available as series. You may optionally provide a step number when logging a metric, as the third parameter of the `mlflow.log_metric` function.

Line charts display those evolving metrics, supporting two modes: step and relative time.

.. image:: img/runs_list_steps.png

.. note::

    You may refresh the charts during the training of your models. Toggling autorefresh reloads data for selected experiments every 10 seconds.

.. note::

    Some MLflow autologgers do not correctly log steps.
    
Run
===

The run screen has two tabs to display:

* The details of the run, including its parameters, tags, metrics and models.
* The directory of the managed folder where artifacts of the run are stored.

In the details tab, metrics can be displayed as line graphs if more than one value was logged. Logged models can be visually deployed from this screen. See :doc:`deploying`.

Dataset
=======

It's possible to create a DSS dataset from the data of the experiment tracking runs of a project.

This lets you perform DSS analysis and compute visualization features on your runs data.

You can create such a dataset:

* from the flow, in +Dataset > Internal > Experiments
* from the Experiments screen, by selecting experiments then choose "Create dataset" in the mass actions.

The later method will prefill a set of experiments to retrieve.

The dataset is available in two formats:

* Long format, with one line per metric, param, tag
* JSON format, with metrics, params and tags as JSON columns

It also allows you to select runs according to an MLflow search runs expression, following the MLflow search syntax (a simplified versions of the SQL WHERE clause, see https://www.mlflow.org/docs/2.17.2/search-runs.html).

.. note::
    search-experiments (https://www.mlflow.org/docs/2.17.2/search-experiments.html) is not supported yet.



Delete/Restore/Clear
====================

Experiments and runs may be *deleted* and *restored*. Deletions are *soft deletions*: items are marked for deletion but will not be physically removed from storage until *cleared*.

To permanently delete items marked for deletion for a given project, use the ``Clear Deleted Experiments`` project macro. This macro is equivalent to the MLflow ``gc`` command.
You may also use the extensions of the python API (see :doc:`extensions`).

.. note::

    When clearing experiments and runs marked for deletion, related artefacts, including models, are deleted.

Cautions
========

* Only one experiment with a given name may be active.

