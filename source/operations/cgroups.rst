Using cgroups for resource control
####################################

.. contents::
	:local:

.. note::

    If using :doc:`Dataiku Cloud Stacks </installation/index>` installation, cgroups are automatically managed for you, and you
    do not need to follow these instructions.

    These instructions do not apply to Dataiku Cloud


DSS can automatically classify a large number of its local subprocesses in Linux cgroups for resource control and limitation.

Using this feature, you can restrict usage of memory, CPU (+ other resources) by most processes. The cgroups integration in DSS is very flexible and allows you to devise multiple resource allocation strategies:

* Limiting resources for all processes from all users
* Limiting resources by process type (i.e. a resource limit for notebooks, another one for webapps, ...)
* Limiting resources by user
* Limiting resources by project key

.. warning::

	This requires some understanding of the Linux cgroups mechanism

.. warning::

  cgroups support is only available for Linux and is not available for macOS.

Prerequisites
===============

* You need to have a Linux machine with cgroups enabled (this is the default on all recent DSS-supported distributions)
* DSS supports version 1 and version 2 of the Linux cgroups subsystem. However these two versions have quite different configuration mechanisms, constraints and settings. You will need to know which version is currently active on your system.
* The DSS service account needs to have write access to one or several cgroups in which you want the DSS processes to be placed. This requires some privileged actions to be performed at system boot before DSS startup, and can be handled by the DSS-provided service startup script.
* On cgroups v2 systems, cgroup management by DSS is only possible when the :doc:`User Isolation Framework </user-isolation/index>` is enabled, due to the new "Delegation Containment" rules.

Recommended configuration (cgroups v1)
========================================

.. note::

  Use this recommended configuration on OS that use cgroups v1, such as:

    * RedHat Enterprise Linux 8
    * AlmaLinux 8
    * Rocky Linux 8
    * Oracle Linux 8 


Initial system configuration
------------------------------

First of all, you need (system administrator task) to make sure that DSS can write to ``/sys/fs/cgroup/memory/DSS``


Then, the cgroup hierarchies which are under control of DSS must be added to the ``additional_allowed_file_dirs``
configuration key under section ``[dirs]`` of the ``/etc/dataiku-security/INSTALL_ID/security-config.ini`` configuration file (you can find the ``INSTALL_ID`` in ``DATADIR/install.ini``).

.. code-block:: bash

  [dirs]
  dss_datadir = /data/dataiku/dss_datadir
  additional_allowed_file_dirs = /sys/fs/cgroup/cpu/DSS;/sys/fs/cgroup/memory/DSS

Configuration in DSS
---------------------

* Go to Admin > Settings > Resource control
* Check *Enable cgroups support*
* Select *Cgroups version* ``V1``
* Configure *Hierarchies mount root* to ``/sys/fs/cgroup``


Under *cgroups placements*, configure the following:

* For every entry (In-memory machine learning, Python and R recipes, ...) *except "Job execution kernels"*, add:

   * ``memory/DSS/${user}``


Under *cgroup limits*, add a limit:

* Path template: ``memory/DSS``
* Then click "Add limit":
  
  * Key: ``memory.limit_in_bytes``
  * Value: recommended memory limit

The recommended memory limit is as follows:

* For a VM with 32GB of memory, set `10g`
* For a VM with 64GB of memory, set `38g`
* For a VM with 96GB of memory, set `60g`
* For a VM with 128GB of memory, set 75% of the physical memory. For example, if you have 256 GB of RAM, set `192g`


Making the settings persistent at reboot
------------------------------------------

Edit the service configuration file (at ``/etc/dataiku/<INSTANCE_ID>/dataiku-boot.conf``) and set the following variable definitions:

* ``DSS_CGROUPS="cpu/DSS:memory/DSS"``


Additional details and examples
=================================

This section contains further details if you want to go further than the recommended configuration above

Applicability
--------------

cgroups restriction applies to:

* Python and R recipes
* PySpark, SparkR and sparklyr recipes (only applies to the driver part, executors are covered by the cluster manager and Spark-level configuration keys)
* Python and R recipes from plugins
* Python, R and Scala notebooks (not differentiated, same limits for all 3 types)
* In-memory visual machine learning and deep learning (for scikit-learn, computer vision and Keras backends. For MLlib backend, this is covered by the cluster manager and Spark-level configuration keys)
* Webapps (Shiny, Bokeh, Dash and Python backend of HTML webapps, not differentiated, same limits for all 4 types)
* Interactive statistics
* Statistics recipes (for univariate analysis, PCA and statistical test recipes)
* Custom Python steps and triggers in scenarios
* Jobs using the DSS engine (prepare recipe and others) via the Job Execution Kernels. However, for memory tuning of the JEK, prefer :doc:`memory` since cgroups will cause jobs to die.

cgroups restrictions do not apply to:

* The DSS backend itself. For memory tuning of the backend, see :doc:`memory`
* The DSS public API, which runs as part of the backend


.. note::

  cgroups do not apply to recipes and machine learning that are using :doc:`containerized execution </containers/index>`
  See containerized execution documentation for more information about processes and controlling memory usage for containers

Configuration
--------------

All configuration for cgroups integration is done by the DSS administrator in *Administration > Settings > Resource control*.

You need to configure:

* The cgroup subsystem version currently active on your host (V1 or V2).
* [cgroup v2 only] The list of cgroup controllers used by your setup (comma-separated list, eg ``cpu,memory``). These controllers should have been enabled at boot time on the cgroup directories delegated to DSS.
* The global root (mount point) for the cgroups hierarchy on the host. On most Linux systems this is ``/sys/fs/cgroup``, unless customized by the administrator.
* For each kind of process, the list of cgroup(s) in which you want it placed, relative to this root. Each entry of the list can refer to some variables for dynamic placement.
* For each cgroup (which can also refer to some variables), the limits to apply. Refer to Linux cgroups documentation for available limits.

.. note::
  * Under cgroup v1, a given process can be placed in multiple cgroups, for different cgroup controllers (for instance, one cgroup for CPU control and one for memory control). Cgroup v2 uses a single unified tree for all controllers, so a given process can only be classified in a single cgroup.
  * Under cgroup v2, processes can only be placed in leaf nodes of the cgroup tree, not internal nodes. For instance, it is possible to classify some user processes in "dataiku/${user}/notebooks" and some others in "dataiku/${user}/recipes" (two distinct leaf nodes). However if your setup uses cgroup "dataiku/recipes/python" you cannot assign processes to parent cgroups "dataiku/recipes" nor "dataiku".

More complex configuration example (cgroup v1)
--------------------------------------------------------

If you want to implement the following policy (it's really more of an example, such a policy would be pretty weird):

* The total memory for each user (counting notebooks and recipes) may not exceed 3 GB
* The memory for the notebooks of each user may not exceed 1 GB
* The CPU for all notebooks in aggregate may not exceed 100% (i.e. one core)

Under cgroups v1, the "cpu" and "memory" controllers are normally mounted in different hierarchies, typically ``/sys/fs/cgroup/cpu`` and ``/sys/fs/cgroup/memory``.

You will first need to make sure that you have write access to a cgroup within each of these hierarchies. Let's say that the DSS user has write access to ``/sys/fs/cgroup/cpu/DSS`` and ``/sys/fs/cgroup/memory/DSS``

Global cgroups configuration
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

* Check *Enable cgroups support*
* Select *Cgroups version* ``V1``
* Configure *Hierarchies mount root* to ``/sys/fs/cgroup``

Placements configuration
@@@@@@@@@@@@@@@@@@@@@@@@@

Under *cgroups placements*, configure the following:

Placement of notebooks
%%%%%%%%%%%%%%%%%%%%%%

Add the following target cgroups to *Jupyter kernels (Python, R, Scala)*:

* ``memory/DSS/${user}/notebooks``
* ``cpu/DSS/notebooks``

When user u1 starts a notebook, its process will be placed in ``/sys/fs/cgroup/memory/DSS/u1/notebooks`` and ``/sys/fs/cgroup/cpu/DSS/notebooks``


Placement of Python and R recipes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Add the following target cgroups to *Python + R recipes*:

* ``memory/DSS/${user}/recipes``
* ``cpu/DSS/recipes``

When user u1 starts a Python or R recipe, its processes will be placed in ``/sys/fs/cgroup/memory/DSS/u1/recipes`` and ``/sys/fs/cgroup/cpu/DSS/recipes``

Limits configuration
@@@@@@@@@@@@@@@@@@@@@

We have placed processes in cgroups, we now need to implement the desired resource limitations.

Under *cgroups limits*, configure the following:

Global per-user memory restriction
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

* *Path template*: ``memory/DSS/${user}``
* *Limits*:

	* ``memory.limit_in_bytes`` : ``3G``

When placing a process in a given cgroup, DSS evaluates all limit configuration rules and applies those which match the target cgroup or one of its parents.

Here, we put all user processes below ``/sys/fs/cgroup/memory/DSS/${user}``, so the global per-user limit is enforced.

Per-user notebooks memory restriction
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

* *Path template*: ``memory/DSS/${user}/notebooks``
* *Limits*:

	* ``memory.limit_in_bytes`` : ``1G``

When placing a process in a given cgroup, DSS evaluates all limit configuration rules and applies those which match the target cgroup or one of its parents.

Here, we put all notebook processes for this user in ``/sys/fs/cgroup/memory/DSS/${user}/notebooks``, so the notebook-specific limit is enforced in addition to the above per-user limit.

CPU restrictions for all notebooks
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

* *Path template*: ``cpu/DSS/notebooks``
* *Limits*:

	* ``cpu.cfs_period_us`` : ``1000000``
	* ``cpu.cfs_quota_us`` : ``1000000``

Since we placed all notebooks at the same level in the CPU hierarchy, we can limit it directly.


Configuration example 2 (cgroup v2)
-------------------------------------

To implement the following policy:

* The total memory by all notebooks across the system may not exceed 25 GB (to protect other critical resources)

In recent Linux distributions, the cgroup v2 hierarchy is normally mounted at ``/sys/fs/cgroup``.

You will first need to make sure that you have been delegated a subdirectory of this hierarchy (e.g. ``/sys/fs/cgroup/DSS``), and that the ``memory`` cgroup controller has been enabled in it. This would require that the boot-time service configuration file for DSS contains:

* ``DSS_CGROUPS="DSS"``
* ``DSS_CGROUP_CONTROLLERS="memory"``

Global cgroups configuration
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

* Check *Enable cgroups support*
* Select *Cgroups version* ``V2``
* Configure *Controllers to enable* to ``memory``
* Configure *Hierarchies mount root* to ``/sys/fs/cgroup``

Placements configuration
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Under *cgroups placements*, configure the following:

Placement of notebooks
%%%%%%%%%%%%%%%%%%%%%%

Add the following target cgroup to *Jupyter kernels (Python, R, Scala)*:

* ``DSS/notebooks/${user}``

When user u1 starts a notebook, its process will be placed in ``/sys/fs/cgroup/DSS/notebooks/u1``


Limits configuration
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

We have placed processes in cgroups, we now need to implement the desired resource limitations.

Under *cgroups limits*, configure the following:

Global notebooks memory restriction
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

* *Path template*: ``DSS/notebooks``
* *Limits*:

	* ``memory.max`` : ``25G``

When placing a process in a given cgroup, DSS evaluates all limit configuration rules and applies those which match the target cgroup or one of its parents.

Here, you may have noticed that we have actually placed the notebooks in ``/sys/fs/cgroup/DSS/notebooks/${user}`` but applied the limit on ``/sys/fs/cgroup/DSS/notebooks`` (effectively limiting the cumulative memory consumption of notebooks for all users). We could have simply placed all notebooks in the same cgroup as the one we're limiting.

However, creating one cgroup for all notebooks of each user allows for better accounting: cgroups can be used to implement limitations, but each cgroup also contains accounting files that allows us to know how much memory the notebooks of each user are consuming, all while respecting the global limit.


Creating DSS-specific cgroups at boot time
--------------------------------------------

DSS requires write access to those subdirectories of the global cgroup hierarchies for which you have configured placement or resource limitation rules.

As the cgroup hierarchy is only writable by root, you will need to create these subdirectories, and change their permissions accordingly, before DSS can use them. Moreover, these subdirectories do not persist across system reboots, so you would typically configure a boot-time action for this, to be run before DSS startup.

.. note::

  To avoid conflicts with other parts of the system which manage cgroups (eg systemd, docker) it is advised to configure dedicated subdirectories within the cgroup hierarchies for DSS use.

Using the DSS-provided service management script (recommended)
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

The DSS service management script described :ref:`here <boot.startup>` can optionally create cgroup directories for DSS before starting DSS itself.

To configure this, edit the service configuration file (at ``/etc/dataiku/<INSTANCE_ID>/dataiku-boot.conf``) and add the following variable definitions:

* ``DSS_CGROUP_ROOT`` [optional] : global hierarchies mount root for your system (default ``/sys/fs/cgroup``)
* ``DSS_CGROUPS`` : colon-separated list of cgroup directories to create, relative to the global hierarchies mount root
* ``DSS_CGROUP_CONTROLLERS`` [cgroups v2 only] : space-separated list of cgroup controllers to enable on these directories

The required cgroups will be initialized by the execution of ``sudo systemctl start dataiku``, before DSS startup.

Corresponding log messages and error reporting can be retrieved with ``journalctl -u dataiku``.

Examples:

.. code-block:: bash

  # /etc/dataiku/9xC2VPsFcFTdO6gBIVDhRcNN/dataiku-boot.conf
  # Service configuration file for Dataiku DSS instance 9xC2VPsFcFTdO6gBIVDhRcNN
  # Cgroups v1 version
  DSS_DATADIR="/data/dataiku/dss_datadir"
  DSS_USER="dataiku"

  # Creates DSS-private cgroups: /sys/fs/cgroup/cpu/DSS and /sys/fs/cgroup/memory/DSS
  # DSS_CGROUP_ROOT=/sys/fs/cgroup
  DSS_CGROUPS="cpu/DSS:memory/DSS"

.. code-block:: bash

  # /etc/dataiku/XIgV6TDueYeam0NNIWMlh49X/dataiku-boot.conf
  # Service configuration file for Dataiku DSS instance XIgV6TDueYeam0NNIWMlh49X
  # Cgroups v2 version
  DSS_DATADIR="/data/dataiku/dss_datadir"
  DSS_USER="dataiku"

  # Creates DSS-private cgroup on startup: /sys/fs/cgroup/dataiku
  # DSS_CGROUP_ROOT=/sys/fs/cgroup
  DSS_CGROUPS="dataiku"
  DSS_CGROUP_CONTROLLERS="cpu memory"

Manual setup
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

You can set up DSS cgroups by other mechanisms if needed. What is required is that the Unix user account used to run DSS has permission to manipulate the cgroups directories in which you need it to put its children processes (ie create subdirectories, set up limits, assign processes). In practice this would amount to the following operations, to be run as root before DSS starts.

On a cgroups v1 system, you need to create the cgroup directories used by DSS and assign them to the DSS account.
For instance, assuming that:

* the global cgroup root on your system is ``/sys/fs/cgroup``
* the DSS service account is ``dataiku``
* you have configured a rule placing some processes into or below ``memory/DSS``

you would need to issue the following commands as root:

.. code-block:: bash

  mkdir -p /sys/fs/cgroup/memory/DSS
  chown -Rh dataiku /sys/fs/cgroup/memory/DSS

On a cgroups v2 system, you also need to ensure that the required cgroup controllers are enabled for cgroup directories used by DSS, by writing into the ``cgroup.subtree_control`` file for all parent directories, starting from the cgroup root. Assuming that:

* the global cgroup root on your system is ``/sys/fs/cgroup``
* the DSS service account is ``dataiku``
* you have configured rules placing some processes into subdirectories of ``DSS``
* you have configured rules controlling both CPU and memory usage

you would need to issue the following commands as root:

.. code-block:: bash

  mkdir -p /sys/fs/cgroup/DSS
  echo "+cpu +memory" >/sys/fs/cgroup/cgroup.subtree_control
  echo "+cpu +memory" >/sys/fs/cgroup/DSS/cgroup.subtree_control
  chown dataiku /sys/fs/cgroup/DSS /sys/fs/cgroup/DSS/cgroup.procs


Additional setup for User Isolation Framework deployments
------------------------------------------------------------

When DSS is configured with :doc:`User Isolation Framework </user-isolation/index>` enabled,
the cgroup hierarchies which are under control of DSS should be added to the ``additional_allowed_file_dirs``
configuration key under section ``[dirs]`` of the ``/etc/dataiku-security/INSTALL_ID/security-config.ini`` configuration file (you can find the ``INSTALL_ID`` in ``DATADIR/install.ini``).

That would result in specifying the set of toplevel directories where DSS will write into: in v1 that is usually one directory per controller, while in v2 all controllers live in the same directory tree.

Example on a cgroups v1 system:

.. code-block:: bash

  [dirs]
  dss_datadir = /data/dataiku/dss_datadir
  additional_allowed_file_dirs = /sys/fs/cgroup/cpu/DSS;/sys/fs/cgroup/memory/DSS

Example on a cgroups v2 system:

.. code-block:: bash

  [dirs]
  dss_datadir = /data/dataiku/dss_datadir
  additional_allowed_file_dirs = /sys/fs/cgroup/DSS