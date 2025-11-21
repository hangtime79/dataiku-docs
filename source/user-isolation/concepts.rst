Concepts
#########

.. contents::
	:local:

The fundamental layer
=======================

The User Isolation Framework is made of a number of isolation capabilities that depend on the context. For example, if you have a "traditional" Hadoop cluster (like Cloudera or Hortonworks), you'll want to leverage the Hadoop (HDFS, YARN, Hive, Impala) impersonation capability.

However, whatever the context, it is mandatory to deploy at least the "local code isolation" capability of the UIF. Without this fundamental layer in place, any user who has the permission to run code locally could take over the ``dssuser`` and bypass the various other isolation capabilities.

The local code isolation capability of the UIF requires the ability for the ``dssuser`` user to "become" other users. This is done by leveraging *sudo*.

Means of isolation
===================

In many cases, UIF requires the ability for the ``dssuser`` user to "become" other users. This is called *impersonation*, and is done by leveraging multiple mechanisms:

* For local code isolation (Python, R, Shell) which executes on the DSS host, DSS uses the *sudo* mechanism

* For Hadoop and Spark code, executing on YARN cluster, and access to HDFS data, DSS uses a feature of Hadoop called *proxy user* which allows an authenticated ``dssuser`` to submit work to the cluster on behalf of another user.

* For some SQL databases, UIF leverages native impersonation capabilities of the database

In some other cases, isolation does not require impersonation. For example, when executing code using Docker, a fundamental property of Docker is that each container is independent and cannot access other containers. This ensures that the code running in one container is *isolated* from code running in another container without a specific need for *impersonation*.


Identity mapping
==================

One of the main challenges of the User Isolation Framework is the ability to collaborate. In a too simple UIF setup, when a dataset D is built by user A, another user B wouldn't be able to override it since the files belong to A.

When UIF is enabled, DSS goes to great lengths to ensure that collaboration abilities are preserved. It makes "full" impersonation possible, meaning that each end-user connecting to DSS is impersonated to its corresponding underlying Hadoop / UNIX user.

DSS also supports more complex mappings of "DSS end-user" to "UNIX/Hadoop user". For example, you could declare:

* When working on project A, all users (who have access to project A in DSS) will see their jobs executed as user "projectA" on UNIX/Hadoop
* When working on project B, all users (who have access to project B in DSS) will see their jobs executed as user "projectB" on UNIX/Hadoop
* In all other cases, users are impersonated on a 1-to-1 basis.

There are several use cases for this kind of advanced mapping:

* If not all your end-users have UNIX accounts (since this is required for them to run jobs)
* In some cases, to strengthen security. For example, in a case where users U1 and U2 must collaborate on a project, U1 being very privileged and U2 having low privileges. Since both users collaborate on a project, U2 can write code that U1 will later execute. If U1 is not careful and does not check the code written by U2, this code will run with its higher privileges. In the case where U2 is hostile, this leaves more burden on U1 to verify the code written by U2. By mapping both users to a per-project user and restricting the "project" user to project-specific resources, you can eliminate this risk.
