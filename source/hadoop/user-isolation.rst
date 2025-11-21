Hadoop user isolation
######################

The regular behavior of DSS is to run as a single UNIX account on its host machine (let's call it ``dssuser``). When a DSS end-user executes an Hadoop recipe or notebook, it runs on the cluster as the ``dssuser`` Hadoop user.

DSS supports an alternate mode of deployment, called *user isolation*. In this mode, DSS will *impersonate* the end-user and run all user-controlled code under a different identity than the ``dssuser`` user.

For more information, please see :doc:`User Isolation Framework on HAdoop </user-isolation/capabilities/hadoop-impersonation>`