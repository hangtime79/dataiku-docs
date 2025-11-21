Using unmanaged GKE clusters
#############################

.. contents::
    :local:

Setup
=====

Create your GKE cluster
-----------------------

To create a Google Kubernetes Engine (GKE) cluster, follow the Google Cloud Platform (GCP) documentation on `creating a GKE cluster <https://cloud.google.com/kubernetes-engine/docs/quickstart>`_.
We recommend that you allocate at least 16GB of memory for each cluster node. More memory may be required if you plan on running very large in-memory recipes.

You'll be able to configure the memory allocation for each container and per-namespace in Dataiku DSS using multiple containerized execution configurations.

Prepare your local ``gcloud``, ``docker``, and ``kubectl`` commands
-------------------------------------------------------------------

Follow the GCP `documentation <https://cloud.google.com/kubernetes-engine/docs/quickstart>`_ to ensure the following on your local machine (where DSS is installed):

* The ``gcloud`` command has the appropriate permission and scopes to push to the Google Artifact Registry (GAR) service.

* The ``kubectl`` command is installed and can interact with the cluster. This can be achieved by running the ``gcloud container clusters get-credentials your-gke-cluster-name`` command.

* The ``docker`` command is installed, can build images and push them to GAR. The latter can be enabled by running the ``gcloud auth configure-docker`` command.

.. include:: /containers/_managed-clusters-binary-versions-gke.txt

Create base images
------------------

Build the base image by following :ref:`these instructions <k8s_base_image>`.

Create the execution configuration
----------------------------------

Go to Administration > Settings > Containerized execution, and add a new execution configuration of type "Kubernetes".

* Configure the GAR repository URL to use, e.g. ``<region>-docker.pkg.dev/my-gcp-project/my-registry``
* Finish by clicking **Push base images**.

You're now ready to run recipes and ML models in GKE.

Using GPUs
==========

GCP provides GPU-enabled instances with NVIDIA GPUs. Using GPUs for containerized execution requires the following steps.

.. |base-image-type| replace:: container-exec

.. include:: /containers/_base-image-cuda-support.txt


Thereafter, create a new container configuration dedicated to running GPU workloads. If you specified a tag
for the base image, report it in the "Base image tag" field.

Enable GPU support on the cluster
---------------------------------

Follow the GCP documentation on `how to create a GKE cluster with GPU accelerators <https://cloud.google.com/kubernetes-engine/docs/how-to/gpus>`_. You can also create a GPU-enabled node pool in an existing cluster.

Be sure to run the "DaemonSet" installation procedure, which needs several minutes to complete.

Add a custom reservation
------------------------

For your containerized execution task to run on nodes with GPUs, and for GKE to configure the CUDA driver on your containers, the corresponding pods must be created with a `custom limit` (in Kubernetes parlance). This indicates that you need a specific type of resource (standard resource types are CPU and memory).

You must configure this limit in the containerized execution configuration. To do this:

* In the "Custom limits" section, add a new entry with key ``nvidia.com/gpu`` and value ``1`` (to request 1 GPU).
* Add the new entry and save your settings.

Deploy
------

You can now deploy your GPU-based recipes and models.
