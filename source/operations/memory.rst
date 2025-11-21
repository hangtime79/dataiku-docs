Tuning and controlling memory usage
######################################

.. contents::
	:local:

.. note::

	It is strongly recommended that you get familiar with the different kind of processes in DSS to understand this section. See :doc:`processes` for more information

The backend
============

The backend is a Java process that has a fixed memory allocation set by the ``backend.xmx`` ini parameter.

It is recommended to allocate ample Java memory to the backend. Backend memory requirement scales with:

* The number of users
* The number of projects, datasets, recipes, ...
* Overall activity (automatically running scenarios, use of data preparation design)

For large production instances, we recommend allocating 12 to 20 GB of memory for the backend.

If the memory allocation is insufficient, the DSS backend may crash. This will result in the "Disconnected" overlay appearing for all users and running jobs/scenarios to be aborted. The backend restarts automatically after a few seconds.

Setting the backend Xmx
-------------------------

In this example, we are setting the backend Xmx to 12g

* Go to the DSS data directory

.. note::

	On macOS, the DATA_DIR is always: ``$HOME/Library/DataScienceStudio/dss_home``

* Stop DSS

	.. code-block:: bash

		./bin/dss stop

* Edit the install.ini file
* If it does not exist, add a ``[javaopts]`` section

* Add a line: ``backend.xmx = 12g``

* Regenerate the runtime config:

	.. code-block:: bash

		./bin/dssadmin regenerate-config

* Start DSS

	.. code-block:: bash

		./bin/dss start


For more details on how to tune Java processes settings, see :doc:`/installation/custom/advanced-java-customization`.


Investigate if a crash is related to memory
---------------------------------------------

If you experience the "Disconnected" overlay and want to know if it's related to lack of backend memory:

* Open the ``run/backend.log`` file (or possibly one of the rotated files ``backend.log.X``)

* Locate the latest "DSS startup: backend version" message

* Just before this, you'll see the logs of the crash. If you see ``OutOfMemoryError: Java heap space`` or ``OutOfMemoryError: GC Overhead limit exceeded``, then you need to increase ``backend.xmx``

The JEK
========

The default Xmx of the JEK is 2g. This is enough for a large majority of jobs. However, some jobs with large number of partitions or large number of files to process may require more. This is configured by the ``jek.xmx`` ini parameter.

Note that:

* The ``jek.xmx`` setting is global, and cannot be set per-job, per-user or per-project
* This memory allocation will be multiplied by the number of JEK (see :doc:`processes` for more details), so don't put a huge amount for ``jek.xmx`` as it will also be multiplied.

If you see JEK crashes due to memory errors, we recommend that you increase progressively. For example, first to 3g then to 4g.

Cgroups may also be used to set limits to JEK ressources. See :doc:`cgroups` for more details. However, for JEK memory, prefer using Xmx since cgroups will cause jobs to be killed.

Setting the JEK Xmx
-------------------------

In this example, we are setting the JEK Xmx to 3g

* Go to the DSS data directory

.. note::

	On macOS, the DATA_DIR is always: $HOME/Library/DataScienceStudio/dss_home

* Stop DSS

	.. code-block:: bash

		./bin/dss stop

* Edit the install.ini file
* If it does not exist, add a ``[javaopts]`` section

* Add a line: ``jek.xmx = 3g``

* Regenerate the runtime config:

	.. code-block:: bash

		./bin/dssadmin regenerate-config

* Start DSS

	.. code-block:: bash

		./bin/dss start


For more details on how to tune Java processes settings,  see :doc:`/installation/custom/advanced-java-customization`.


Investigate if a crash is related to memory
---------------------------------------------

If you experience job crashes without error messages and want to know if it's related to lack of JEK memory:

* Open the "Full job log" from the Actions menu of the job page

* Scroll to the end of the log.

* You'll see the logs of the crash. If you see ``OutOfMemoryError: Java heap space`` or ``OutOfMemoryError: GC Overhead limit exceeded``, then you need to increase ``jek.xmx``


The FEKs
========

The default Xmx of each FEK is 2g. This is enough for a large majority of tasks. There may be some rare cases where you'll need to allocate more memory (generally at the direction of Dataiku Support). This is configured by the ``fek.xmx`` ini parameter.

Note that:

* The ``fek.xmx`` setting is global, and cannot be set per-user or per-project
* This memory allocation will be multiplied by the number of FEK (see :doc:`processes` for more details), so don't put a huge amount for ``fek.xmx`` as it will also be multiplied.


Setting the FEK Xmx
-------------------------

In this example, we are setting the FEK Xmx to 3g

* Go to the DSS data directory

.. note::

	On macOS, the DATA_DIR is always: ``$HOME/Library/DataScienceStudio/dss_home``

* Stop DSS

	.. code-block:: bash

		./bin/dss stop

* Edit the install.ini file
* If it does not exist, add a ``[javaopts]`` section

* Add a line: ``fek.xmx = 3g``

* Regenerate the runtime config:

	.. code-block:: bash

		./bin/dssadmin regenerate-config

* Start DSS

	.. code-block:: bash

		./bin/dss start


For more details on how to tune Java processes settings,  see :doc:`/installation/custom/advanced-java-customization`.

Jupyter notebook kernels
=========================

Memory allocation for Jupyter notebooks can be controlled using the :doc:`cgroups integration <cgroups>`

.. warning::

    Please note that Jupyter notebook sessions are not terminated automatically. This means that Jupyter notebooks will continue to consume memory until the Jupyter session is explicitly terminated. As a result, you may observe that jupyter processes are consuming memory for days or weeks.

To view currently active Jupyter notebook sessions from the DSS UI, an administrator can navigate to Administration > Monitoring > Running background tasks > notebooks. You can manually unload notebooks to free up memory usage by following the options listed under :ref:`unloading jupyter notebooks<unloading>`.

To manage memory consumption from Jupyter notebooks on a more regular basis, you may want to consider setting up a scenario to run the "Kill Jupyter Sessions" macro to terminate Jupyter notebook sessions that have been open or idle for a long period of time (e.g. 15 days). Note that a notebook session may be triggering long-running computation, so you will want to ensure that this automation doesn't interfere with active work and that users are notified of this automation accordingly.


Python and R recipes
=====================

Memory allocation for Python and R recipes can be controlled using the :doc:`cgroups integration <cgroups>`

.. note::

	This does not apply if you used :doc:`containerized execution </containers/index>` for this recipe.
	See containerized execution documentation for more information about processes and controlling memory usage for containers

SparkSQL and visual recipes with Spark engine
===============================================

These recipes are made of a large number of processes:

* The Spark driver, a Java process that runs locally
* The Spark executors, Java processes that run in your cluster (usually through YARN)

Memory for both can be controlled using the usual Spark properties (``spark.driver.memory`` and ``spark.executory.memory``) which can be set in :doc:`Spark named configurations </spark/configuration>`

PySpark, SparkR and sparklyr recipes
=====================================

The case of these recipes is a bit particular, because they are actually made of several processes:

* A Python or R process which runs your driver code
* The Spark driver, a Java process that runs locally
* The Spark executors, Java processes that run in your cluster (usually through YARN)

Memory for the Spark driver and executors can be controlled using the usual Spark properties (``spark.driver.memory`` and ``spark.executory.memory``) which can be set in :doc:`Spark named configurations </spark/configuration>`

Memory for the local Python or R process can be controlled  using the :doc:`cgroups integration <cgroups>`

In-memory machine learning
=============================

Memory allocation for in-memory machine learning processes can be controlled using the :doc:`cgroups integration <cgroups>`

.. note::

	This does not apply if you used :doc:`containerized execution </containers/index>` for this recipe.
	See containerized execution documentation for more information about processes and controlling memory usage for containers

Webapps
========

Memory allocation for webapps can be controlled using the :doc:`cgroups integration <cgroups>`

API node
========

Memory consumption on the API node is generally light, so it's unlikely that you'll need to modify the API node memory allocation. If you do need to, memory allocation is set by the ``apimain.xmx`` property in the API node ``install.ini`` file. Here are the steps you would take to modify the ``apimain.xmx`` setting:

* In the API node DATADIR, add an entry in the ``install.ini`` file for ``apimain.xmx``

.. code-block:: bash

    [javaopts]
    apimain.xmx = 4g

* Regenerate the runtime config:

.. code-block:: bash

    ./bin/dssadmin regenerate-config

* Start DSS

.. code-block:: bash

    ./bin/dss start

Govern node
=================

The Govern node memory allocation is configured by the ``governserver.xmx`` setting.

In this example, we are setting the Xmx to 4g.

* Go to the Dataiku Govern data directory

* Stop Dataiku Govern

	.. code-block:: bash

		./bin/dss stop

* Edit the install.ini file
* If it does not exist, add a ``[javaopts]`` section

* Add a line: ``governserver.xmx = 4g``

* Regenerate the runtime config with the govern-admin cli:

	.. code-block:: bash

		./bin/govern-admin regenerate-config

* Start Dataiku Govern

	.. code-block:: bash

		./bin/dss start


For more details on how to tune Java processes settings, see :doc:`/installation/custom/advanced-java-customization`.
