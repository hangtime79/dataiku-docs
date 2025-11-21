Managed Kubernetes clusters
##############################

.. contents::
	:local:

DSS can automatically start, stop and manage Kubernetes clusters running on the major cloud providers.

DSS provides managed Kubernetes capabilities on:

* Amazon Web Services through :doc:`EKS <eks/index>`
* Azure through :doc:`AKS <aks/index>`
* Google Cloud Platform through :doc:`GKE <gke/index>`

Creating a cluster
==================

To create managed clusters, you must first install the DSS plugin corresponding to your cloud provider (:doc:`EKS <eks/index>`, :doc:`AKS <aks/index>`, or :doc:`GKE <gke/index>`). Then follow these steps:

* Go to Administration > Clusters

* You can choose to create a new cluster or attach to an existing cluster

    * To create a new cluster, click **Create EKS/AKS/GKE Cluster**

    * To attach to an existing cluster, click **Add Cluster** and for "Type", select the appropriate "Attach" cluster type

* Fill in the required parameters

* Click **Start/Attach**

.. _managed-clusters.use-cluster:

Using the cluster
==================

You need to select the cluster to use. There is a global default for the cluster to use in Administration > Settings > Containerized execution.

In addition, each project can override this setting.

.. warning::

	If you forget to select any global default cluster, then by default, activities that try to run on Kubernetes will fail, since they don't have any cluster to run on.

Note that you do not need to use per-cluster container runtime configurations, or per-cluster Spark configurations. DSS automatically uses the requested cluster and the limits defined in the container runtime configuration.

Advanced usage for multiple managed clusters
==============================================

.. warning::

	We recommend that you discuss with your Dataiku Customer Success Manager before using this kind of setup, which have quite a few constraints

	It is most often preferable to use autoscaling clusters rather than dynamically creating clusters

Use a specific or dynamic cluster for scenarios
----------------------------------------------------

A common use case for clusters is to run one or multiple scenarios. You can use either:

* a specific named cluster — one that is already defined in the DSS settings, but that is not the default cluster for the project
* or a dynamic cluster — one that is created for the scenario and shut down after the end of the scenario (for fully elastic approaches).

Use a specific static cluster
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

In this case, you can use the variables expansion mechanism of DSS.

To denote the contextual cluster to use at the project level, use the syntax ``${variable_name}``, instead of the cluster identifier. At runtime, DSS will use the cluster denoted by the ``variable_name`` variable. Your scenario will then use a scenario-scoped variable to define the cluster to use for the scenario.

For example, if you want to use the cluster ``regular1`` for the design of the project and all activities not related to the scenario, and use the ``fast2`` cluster for a scenario, then set up your project as follows:

* Cluster: ``${clusterForScenario}``
* Default cluster: ``regular1``

With this setup, when the ``clusterForScenario`` variable is not defined (which will be the case outside of the scenario), DSS will fall back to ``regular1``.

In your scenario, add an initial step "Define scenario variables", and use the following JSON definition:

.. code-block:: json

	{
		"clusterForScenario" : "fast2"
	}

The steps of the scenario will execute on the ``fast2`` cluster.

Use a dynamic cluster 
%%%%%%%%%%%%%%%%%%%%%%%%

In the case of the dynamic cluster, the idea is to create a dynamic cluster, then place the identifier of the dynamically-created cluster into a variable, and then use the variables expansion mechanism described above.

For example, if you want to use the cluster ``regular1`` for the design of the project and all activities not related to the scenario, and use a dynamically-created cluster for a scenario, then set up your project as follows:

* Cluster: ``${clusterForScenario}``
* Default cluster: ``regular1``

With this setup, when the ``clusterForScenario`` variable is not defined (which will be the case outside of the scenario), DSS will fall back to ``regular1``

In your scenario, add an initial step "Setup cluster":

* Select the cluster type that you want to create (depending on the plugin you are using)
* Fill in the configuration form (depending on the plugin you are using)
* Set ``clusterForScenario`` as the "Target variable"

When the step (Setup cluster) runs, DSS creates the cluster and sets the "id" of the newly created cluster in the *clusterForScenario* variable. Given the project configuration, the steps of the scenario will automatically execute on the dynamically-created cluster.

At the end of the scenario (regardless of whether the scenario succeeded or failed), DSS automatically stops the dynamic cluster. Note that you can override this behavior in the scenario settings.

.. warning::

	If DSS unexpectedly stops while the scenario is running, the cluster resources will keep running on your cloud provider. We recommend that you set up monitoring for cloud resources created by DSS.


Automate start and stop of clusters
------------------------------------

DSS has scenario steps available for starting and stopping clusters. This feature is useful, for instance, to automatically start a cluster in the morning (so that it can be used during the day time), and then automatically shut down the cluster at night, to save on cloud consumption.

Permissions
------------

Each cluster has an owner and groups that are granted access levels. These access levels are:

* **Use cluster**: to select the cluster and use it in a project
* **Operate cluster**: to modify cluster settings
* **Manage cluster users**: to manage the permissions of the cluster

In addition, each group can be granted global permissions to:

* Create clusters and manage them
* Manage all clusters — including clusters for which they have not explicitly been granted access
