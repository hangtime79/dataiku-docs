# Managing a DSS node in production

This applicative note gives a number of guidelines to manage DSS design and automation nodes in a production setting, i.e. a setting with multiple data analysts and scientists using the design node, and multiple scenarios running on the automation node

It is roughly organized by decreasing importance: the first recommendations are the most important ones.

  * [1. Capacity planning](#1-capacity)
  * [2. Backups](#2-backups)
  * [3. Tune memory consumption](#3-memory)
  * [4. Tune activities parallelism](#4-parallelism)
  * [5. Setup a sandbox instance](#5-sandbox)
  * [6. Setup an administrative project](#6-project)
  * [7. Setup management of disk space](#7-disk-space)
  * [8. Setup culling of Jupyter kernels](#8-jupyter)
  * [9. Setup monitoring](#9-monitoring)

<a name="1-capacity"></a>

# Capacity planning

Capacity planning is a complex topic that needs to be discussed as part of your DSS implementation planning.

One important recommendation is about disk usage: while DSS does not usually store datasets locally, you still need to allocate plenty of local disk space for all of the various things that DSS will store locally (machine learning models and splits, temporary data, exports, notebook results, ...).

We recommend dedicating at least 500 GB of disk for DSS. The biggest DSS instances can require up to a few terabytes.



<a name="2-backups"></a>

# Setup backups

The DSS data directory contains all user-generated code, flows, notebooks, ...

It is vital that the DSS data directory is:

* backed up
* archived

Archived means that there should be multiple "point in time" copies of the DSS data directory in the backups, so that an accidental deletion can be reverted even if a backup has run since, by restoring an older archive.

## Snapshot-based backups

The most efficient way to do backups is to use block-device-level or filesystem-level backups.

When running on one of the main cloud platforms (AWS, Azure, GCP), we recommend that you perform and keep multiple snapshots of the persistent disk hosting the DSS data directory

## File-based backups

If snapshot-based backups are not possible, run files-based backups. For consistency, these backups should be performed while DSS is not running.

Several directories can be safely ignored while doing backups. See https://doc.dataiku.com/dss/5.0/operations/backups.html for more information.




<a name="3-memory"></a>

# Tune memory consumption

## Java processes

Many of the processes running in DSS are Java processes, which have a fixed limit on the memory allocation that they can make.

The three main kinds of Java processes are:

* The "backend" is the main server, which handles all interaction with users, the configuration, and the visual data preparation. There is only one backend.
* The "JEK" is a process which runs the jobs (ie, what happens when you use "Build"). There are multiple JEKs (one per running job)
* The "FEK" handles long-running background tasks. It is also responsible for building the data samples. There are multiple FEKs (one per running background task)

When you install DSS out of the box, the following limits are set:

* 2 to 6 gigabytes for the backend (depending on machine size)
* 2 gigabytes for JEK
* 2 gigabytes for FEK

We recommend setting the following limits:

* Leave 2 gigabytes for JEK and FEK - these processes are multiplied rather than scaling.
* For backend:
    * Less than 10 users: 8 gigabytes
    * 10-50 users: 12 gigabytes
    * Over 50 users: 16 gigabytes

Note that this by no means put a limit on maximum global DSS memory usage, since:

* There can be multiple JEK and FEK processes running concurrently
* Python and R processes (for code recipes, notebooks, webapps and machine learning) are not subject to Java-level limitations.

## Restrict overall Python/R processes memory consumption

Python and R processes can allocate arbitrary amounts of memory, which could cause memory overruns and destabilize the whole DSS instance.

You can avoid this by using the cgroups integration. cgroups are a feature of the Linux kernel that allows to restrict maximum amounts of RAM consumed by groups of resources. DSS gives you a lot of flexibility in placing processes in groups and setting allocation limits per group.

See https://doc.dataiku.com/dss/latest/operations/cgroups.html for more information

## Tune internal databases cache size

Each project in DSS comes with an internal database called the timelines database which stores information like what actions are performed by users, comments, ...

Each timeline database has an internal memory-based cache. With a large number of active projects, these timelines can take a very high amount of memory. If you have or plan to have many projects (100 and more), follow these steps:

* Stop DSS
* Edit the ``config/dip.properties`` file
* Add a line ``dku.internalDatabases.timeline=CACHE_SIZE=1024``
* Start DSS




<a name="4-parallelism"></a>

# Tune maximum activities parallelism

The default configuration of DSS only allows for a limited number of parallel-running jobs. With large instances, this might lead to jobs being queued while other jobs are being processed, decreasing the perceived responsiveness from the users' point of view.

The parallelism limits thus can generally be increased.

We recommend setting the following limits:

* Max concurrent activities per job: 5 to 10
* Max concurrent total activities: 5 to 50 depending on number of users.

In particular, we don't recommend setting extremely high max concurrent total activities (like 500), as this could increase the risk of exhausting various machine resources.

More information can be found here: https://doc.dataiku.com/dss/latest/flow/limits.html





<a name="5-sandbox"></a>

# Setup a dedicated sandbox instance

As you scale your usage of DSS




<a name="6-project"></a>

# Setup an "Administrative" project to run various macros

In DSS, Macros are predefined actions that allow you to automate a variety of tasks, like maintenance and diagnostic tasks.

Macros always run within a DSS project. Therefore, you'll generally want to create an "Administration tasks" project, accessibly only to DSS administrators, that you will use as a container for all your cleanup / maintenance macros.

Macros can be scheduled as part of a scenario, which will also run as part of the administrative project



<a name="7-disk-space"></a>

# Setup management of disk space

Various subsystems of DSS consume disk space in the DSS data directory. Some of this disk space is automatically managed and reclaimed by DSS (like temporary files), but some needs some administrator decision and management.

## Job logs

Each time a job is run in DSS, DSS makes a snapshot of the project configuration/flow/code, runs the job, and keeps various logs and diagnostic information for this job.

This information is extremely useful for understanding job issues, and is not automatically garbage-collected by DSS, in case user wants to investigate what happened with a job at a later point.

For each job, a subfolder is created as ``jobs/PROJECT_KEY/JOB_ID``.

DSS provides a macro to remove old job logs that you can run autommatically in your administrative project.

See https://doc.dataiku.com/dss/latest/operations/disk-usage.html


## Scenario logs

Same thing, DSS provides a macro to remove old scenario logs. See https://doc.dataiku.com/dss/latest/operations/disk-usage.html



<a name="8-jupyter"></a>

# Setup culling of Jupyter kernels

Each time a user opens a notebook, a specific process is created (a Python process for a Python notebook, a R process for a R notebook, a Java process for a Scala notebook). 

This per-notebook process holds the actual computation state of the notebook, and is called a "Jupyter kernel".

When a user navigates away from the notebook, the **kernel remains alive**. This is a fundamental property of Jupyter notebooks and kernels, which allows you to start a long running computation without having to keep the notebook open, and be able to retrieve the result of the computation at a later time.

An important consequence is that, left unchecked, you will generally, after a few days or weeks, have a huge number of alive Jupyter kernels consuming large amounts of memory.


In addition to controlling and limiting the memory usage of notebooks using cgroups (see above), we recommend that you setup regular culling of Jupyter kernels.

DSS provides a macro for this.





<a name="9-monitoring"></a>

# Setup monitoring

Monitoring the behaviour and proper function of DSS is essential to production readiness.

onitoring DSS is essentially based on three topics:

* Raising alerts when some services are not working properly
* Storing and plotting immediate and historical data of host-level statistics (CPU, memory, IO, disk space, ...)
* Storing and plotting immediate and historical data of application-level statistics (users logged in, number of jobs, number of scenarios, ...)

DSS itself does not include a monitoring infrastructure (alerting or historical graphs) but provides many APIs and monitoring points that allow you to plug your own monitoring infrastructure onto it.

Any monitoring software that has the ability to run scripts or call HTTP APIs can be used to monitor DSS.

However, Dataiku provides a **non-supported** open source tool called **dkumonitor** that bundles together the common "Graphite / Grafana" stack for easy setup. Usage of dkumonitor is completely optional, it simply provides you with a quick way to deploy this monitoring stack.

See https://doc.dataiku.com/dss/latest/operations/monitoring.html for more information on how to setup monitoring
