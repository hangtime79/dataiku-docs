Using managed GKE clusters
##########################

.. contents::
    :local:

Initial setup
=============

Install the GKE plugin
----------------------

To use Google Kubernetes Engine (GKE), begin by installing the "GKE clusters" plugin from the Plugins store in Dataiku DSS. For more details, see the :doc:`instructions for installing plugins </plugins/installing>`.

Prepare your local commands
-------------------------------------------------------------------

Follow the Google Cloud Platform (GCP) `documentation <https://cloud.google.com/kubernetes-engine/docs/quickstart>`_ to ensure the following on your local machine (where DSS is installed):

* The ``gcloud`` command is installed. See `install documentation <https://cloud.google.com/sdk/docs/install>`__. The ``gcloud`` command has the appropriate permissions and scopes to:

    - push to the Google Artifact Registry (GAR) service.
    - have full control on the GKE service.

* The ``gke-gcloud-auth-plugin`` command is installed. See `GCP documentation <https://cloud.google.com/blog/products/containers-kubernetes/kubectl-auth-changes-in-gke>`__.
* The ``kubectl`` command is installed. See `install documentation <https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl>`__.
* The ``docker`` command is installed, can build images and push them to GAR. The latter can be enabled by running the ``gcloud auth configure-docker`` command. See `install documentation <https://docs.docker.com/engine/install/>`__.

.. include:: /containers/_managed-clusters-binary-versions-gke.txt

Create base images
------------------

Build the base image by following :ref:`these instructions <k8s_base_image>`.

Create a new execution configuration
------------------------------------

Go to Administration > Settings > Containerized execution, and add a new execution configuration of type "Kubernetes."

* Configure the GAR repository URL to use, e.g. ``<region>-docker.pkg.dev/my-gcp-project/my-repository``

* Finish by clicking **Push base images**.

Cluster configuration
=====================

Connection
----------

The connection is where you define how to connect to GCP. This can be done either inline in each cluster (not recommended), or as a preset in the "GKE connection" plugin settings (recommended).

Network settings
----------------

The "network" field refers to the Virtual Private Cloud (VPC) where the cluster will be deployed. The "sub-network" field defines the IP space within that VPC where the pod IPs will be allocated.
If left blank, those fields will use default network settings, the details of which are explained in the `GCP documentation <https://cloud.google.com/kubernetes-engine/docs/quickstart>`__.

Cluster nodes
-------------

This is where you define the number and type of nodes that you want in your cluster. You can define the properties of a node pool either inline (not recommended) or as a preset in the "Node pools" plugin settings (recommended). You have the possibility to define multiple node pools, each with its own properties.


Using GPUs
==========

GCP provides GPU-enabled instances with NVIDIA GPUs. Using GPUs for containerized execution requires the following steps.

.. |base-image-type| replace:: container-exec

.. include:: /containers/_base-image-cuda-support.txt

Thereafter, create a new container configuration dedicated to running GPU workloads. If you specified a tag for the base image, report it in the "Base image tag" field.

Enable GPU support on the cluster
---------------------------------

When you create your cluster using the GKE plugin, be sure to enable the "With GPU" option in the node pool settings. Follow the `GCP documentation on GPUs <https://cloud.google.com/compute/docs/gpus/>`_ to select the GPU type.

At cluster creation, the plugin will run the NVIDIA driver "DaemonSet" installation procedure, which needs several minutes to complete.

Add a custom reservation
------------------------

For your containerized execution task to run on nodes with GPUs, and for GKE to configure the CUDA driver on your containers, the corresponding pods must be created with a `custom limit` (in Kubernetes parlance). This indicates that you need a specific type of resource (standard resource types are CPU and memory).

You must configure this limit in the containerized execution configuration. To do this:

* In the "Custom limits" section, add a new entry with key ``nvidia.com/gpu`` and value ``1`` (to request 1 GPU).
* Add the new entry and save your settings.

Deploy
------

You can now deploy your GPU-based recipes and models.
