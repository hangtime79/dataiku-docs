Understanding and tracking DSS processes
#########################################

A DSS instance is made of a number of different processes. Each process plays a specific role, and it's important to understand these in order to properly monitor and manage DSS

.. contents::
	:local:

.. _processes.supervisord:

supervisord
===========

When you run ``./bin/dss start``, it starts the supervisord, which is a Python process responsible for starting, restarting and monitoring the top-level DSS processes (nginx, backend, jupyter)

.. _processes.backend:

The backend
=============

The backend is the main process of DSS. It holds all of the configuration and the users, it handles the API and the UI of DSS and handles scheduling the scenarios.

The backend is forked by supervisord. The pid of the backend can be found using ``./bin/dss status``

Logs for the backend are in ``run/backend.log``

Ample Java memory should be allocated to the backend. See :doc:`memory` for more information.

The JEKs
==========

Each job in DSS runs in a separate process called a JEK. If you have 10 jobs running at a given time, there will be 10 running JEKs.

DSS will “pre-start” JEK processes so that jobs can start faster. This can be configured in Administration > Resources control > Job Execution Kernels. Each JEK consumes resources, even when they are not currently running jobs, so increase this value with caution.

JEKs are forked by the backend. They can be identified by the "DSSJobKernelMain" name in their command lines. When a JEK is running a job, its pid will appear in:

* The job UI
* The Administration > Monitoring > Background tasks UI
* The job "get status" API

Logs for the JEKs are segregated by job, and can be found in ``jobs/PROJECT/JOB_ID/output.log``

The Java memory of JEKs can be tuned (but doesn't often need to). See :doc:`memory` for more information.

The FEKs
========

From time to time, the DSS backend will "delegate" part of its work to worker processes called the FEKs. This is done mostly for work that may consume huge amounts of memory. If a memory overrun happens, the FEK gets killed but the backend is unaffected.

FEKs only run a single task at a time. When they are done with a task, the FEKs can be assigned another task. From time to time, DSS kills FEKs that have grown too much in size.

FEKs are forked by the backend. They can be identified by the "DSSFutureKernelName" name in their command lines

Logs for the FEKs appear directly within the backend log.

The Java memory of FEKs can be tuned (but doesn't often need to). See :doc:`memory` for more information.

Jupyter notebook server
========================

All Jupyter (Python, R, Scala) notebooks are managed by a top-level server, the Jupyter server.

The Jupyter server is forked by supervisord. Its pid can be found using ``./bin/dss status``

For historical reasons, logs for the Jupyter server are in ``run/ipython.log``

This process uses small amounts of memory.

Jupyter notebook kernels
=========================

Each time a user opens a notebook, a specific process is created (a Python process for a Python notebook, a R process for a R notebook, a Java process for a Scala notebook).

This per-notebook process holds the actual computation state of the notebook, and is called a "Jupyter kernel".

When a user navigates away from the notebook, the **kernel remains alive**. This is a fundamental property of Jupyter notebooks and kernels, which allows you to start a long running computation without having to keep the notebook open, and be able to retrieve the result of the computation at a later time.

An important consequence is that, left unchecked, you will generally, after a few days or weeks, have a huge number of alive Jupyter kernels consuming large amounts of memory.

* End-users can stop their kernels by going to the notebooks list in DSS, and clicking the "Unload" button
* End-users can also stop their kernels by going to their Activity indicator (from the Activity button in the title bar) and clicking "Abort"
* Administrators can list and stop kernels by going to Administration > Monitoring > Background tasks, and aborting individual notebooks
* Administrators can also automatically kill Jupyter kernels that have been left alive for too long using a dedicated macro.

Memory for notebook kernels can be controlled using :doc:`cgroups integration <cgroups>`. See :doc:`memory` for more information

Python / R recipes processes
=============================

When a job runs a Python or R recipe, a corresponding Python or R process is created.

Logs for these processes appear directly in the job logs.

Memory for these processes can be controlled using :doc:`cgroups integration <cgroups>`. See :doc:`memory` for more information

.. note::

	This does not apply if you used :doc:`containerized execution </containers/index>` for this recipe.
	See containerized execution documentation for more information about processes and controlling memory usage for containers

Spark recipes
==============

When a job runs a Spark recipe (including PySpark, SparkR, sparklyr, SparkSQL, Spark-Scala, and "Spark" engine for visual recipes) or R recipe, a Spark driver process (a Java process) is created. A corresponding Python or R process is also created for PySpark, SparkR and sparklyr recipes.

Logs for these processes appear directly in the job logs.

Memory for these processes can be controlled. See :doc:`memory` for more information

In-memory machine learning
=============================

For each model being trained using the "In-memory (scikit-learn, LightGBM, XGBoost)" or "Deep Learning" engines, a new Python process is created. This process is stopped at the end of the training session.

In-memory machine learning processes can be identified by the ``dataiku.doctor.server`` in their command-line. Logs for these processes can be found behind the "Logs" button in the machine learning session itself.

Memory for these processes can be controlled using :doc:`cgroups integration <cgroups>`. See :doc:`memory` for more information

.. note::

	This does not apply if you used :doc:`containerized execution </containers/index>` for this machine learning session.
	See containerized execution documentation for more information about processes and controlling memory usage for containers

Webapps
=======

For each running webapp backend (Flask, Shiny, Bokeh, Dash), a corresponding Python or R process is created.

Memory for these processes can be controlled using :doc:`cgroups integration <cgroups>`. See :doc:`memory` for more information


The governserver
=================

For Govern nodes, the backend process is replaced by the governserver process.
