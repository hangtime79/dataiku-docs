Deployment on Google Kubernetes Engine
########################################

You can use the API Deployer Kubernetes integration to deploy your API Services on Google Kubernetes Engine.

Setup
======

Create your GKE cluster
------------------------

Follow Google documentation on how to create your cluster. We recommend that you allocate at least 7 GB of memory for each cluster node.

Prepare your local ``docker`` and ``kubectl`` commands
-------------------------------------------------------

Follow Google documentation to make sure that:

* Your local (on the DSS machine) ``kubectl`` command can interact with the cluster. As of July 2018, this implies running ``gcloud container clusters get-credentials <cluster_id>``
* Your local (on the DSS machine) ``docker`` command can successfully push images to your GAR repository. As of March 2025, this implies running ``gcloud auth configure-docker``

.. include:: /containers/_managed-clusters-binary-versions-gke.txt

Setup the infrastructure
-------------------------

Follow the usual setup steps as indicated in :doc:`setup`.

Make sure you have Google Artifact Registry (GAR) set up with a repository in your project. We recommend that it be specific to API Deployer. It will be used to prefix your image paths.

For example, if your GCP project is called ``my-gke-project`` and you have a GAR repository called ``my-repository``, all images must be prefixed by ``my-gke-project/my-repository/``.

* Go to the infrastructure settings > Kubernetes cluster
* In the Registry host field, enter the region's artifact registry hostname ``<region>-docker.pkg.dev``
* In the images prefix field, enter ``my-gke-project/my-repository``

Deploy
-------

You're now ready to deploy your API Services to GKE

Using GPUs
===========

Google Cloud Platform provides GPU-enabled instances with NVidia GPUs. Several steps are required in order to use them for API Deployer deployments

.. |base-image-type| replace:: apideployer

.. include:: /containers/_base-image-cuda-support.txt

If you used a specific tag, go to the infrastructure settings, and in the "Base image tag" field, enter ``dataiku-apideployer-base-cuda:X.Y.Z``

Create a cluster with GPUs
---------------------------

Follow GCP's documentation for how to create a cluster with GPU accelerators (Note: you can also create a GPU-enabled node group in an existing cluster)

Don't forget to run the "daemonset" installation procedure. This procedure needs several minutes to complete.

Add a custom reservation
-------------------------

In order for your API Deployer deployments to be located on nodes with GPU accelerators, and for GKE to configure the CUDA driver on your containers, the corresponding GKE pods must be created with a custom "limit" (in Kubernetes parlance) to indicate that you need a specific type of resource (standard resource types are CPU and memory)

You can configure this limit either at the infrastructure level (all deployments on this infrastructure will use GPUs) or at the deployment level.

At the infrastructure level
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

* Go to Infrastructure > Settings
* Go to "Sizing and Scaling"
* In the "Custom limits" section, add a new entry with key: ``nvidia.com/gpu`` and value: ``1`` (to request 1 GPU)
* Don't forget to add the new entry, save settings

At the deployment level
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

* Go to Deployment > Settings
* Go to "Sizing and Scaling"
* Enable override of infrastructure settings in the "Container limits" section
* In the "Custom limits" section, add a new entry with key: ``nvidia.com/gpu`` and value: ``1`` (to request 1 GPU)
* Don't forget to add the new entry, and save settings

Deploy
-------

You can now deploy your GPU-requiring deployments

This applies to:

* Python functions (your endpoint needs to use a code environment that includes a CUDA-using package like tensorflow-gpu)
* Python predictions (ditto)
