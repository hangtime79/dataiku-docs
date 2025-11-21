User Isolation
##################

.. note::

	User Isolation Framework was previously called Multi-User-Security.

.. note::

    If using :doc:`Dataiku Cloud Stacks </installation/index>` installation, User Isolation is automatically managed for you, and you do not need to follow these instructions

.. note::

    If using :doc:`Dataiku Cloud </installation/index>`, User Isolation is automatically managed for you, and you do not need to follow these instructions


On an out-of-the-box installation of DSS, every action performed by DSS is performed as a single account on the host machine. This account which runs the DSS service is called the ``dssuser``. For example, when a DSS end-user executes a code recipe, it runs as the UNIX ``dssuser``

Similarly:

* Every action performed on a Hadoop cluster is performed by the ``dssuser`` service account. When a DSS end-user executes an Hadoop/Spark recipe or notebook on a Hadoop cluster, it runs on the cluster as the Hadoop ``dssuser``.
* Every action performed on Kubernetes is initialized through the ``dssuser`` service account
* Actions performed on external databases use the credentials configured in the database connection.

This default behavior has several limitations:

* There is a lack of traceability on the Hadoop clusters to identify which user performed which action.

* If the DSS end-user is hostile and has the permission to execute "unsafe" code, he can run arbitrary code as UNIX ``dssuser`` and modify the DSS configuration

DSS features a set of mechanisms to isolate code which can be controlled by the user, so as to guarantee both traceability and inability for a hostile user to attack the ``dssuser``. Together, these mechanisms form the *User Isolation Framework*.

The User Isolation Framework is not a single technology but a set of capabilities that permit isolation depending on the context. Most of the components of the User Isolation Framework imply that DSS *impersonates* the end-user and runs all user-controlled code under different identities than ``dssuser``.

This documentation includes a number of reference architectures showing common deployments of the various UIF components.

.. note::

	The User Isolation Framework may require specific editions of DSS. Please contact your Account Executive for any further information


.. toctree::
   capabilities-summary
   concepts
   prerequisites-limitations
   initial-setup
   troubleshooting
   reference-architectures/index
   capabilities/index
   advanced/index
