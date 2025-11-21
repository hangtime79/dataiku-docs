Using unmanaged AKS clusters
#############################

.. contents::
    :local:

Setup
=====

Create your ACR registry
------------------------

If you already have an Azure Container Registry (ACR) up and ready, you can skip this section and go to :ref:`aks_create_cluster`.

Otherwise, follow the Azure documentation on `how to create your ACR registry <https://docs.microsoft.com/en-us/azure/container-registry/>`_.

.. warning::
   We recommend that you pay extra attention to the Azure `container registry pricing plan <https://azure.microsoft.com/en-us/pricing/details/container-registry/>`_, as it is directly related to the registry storage capacity.

.. _aks_create_cluster:

Create your AKS cluster
-----------------------

To create your Azure Kubernetes Service (AKS) cluster, follow the Azure documentation on `how to create your AKS cluster <https://docs.microsoft.com/en-us/azure/aks/>`_. We recommend that you allocate at least 16GB of memory for each cluster node.

Once the cluster is created, you must modify its IAM credentials to `grant it access to ACR <https://docs.microsoft.com/en-us/azure/container-registry/container-registry-auth-aks#grant-aks-access-to-acr>`_ (Kubernetes secret mode is not supported). This is required for the worker nodes to pull images from the registry.


Prepare your local ``az``, ``docker``, and ``kubectl`` commands
------------------------------------------------------------------

Follow the Azure documentation to ensure the following on your local machine (where Dataiku DSS is installed):

* The ``az`` command is properly logged in. As of October 2019, this implies running the ``az login --service-principal --username client_d --password client_secret --tenant tenant_id`` command. You must use a service principal that has sufficient IAM permissions to write to ACR and full control on AKS.

* The ``docker`` command can successfully push images to the ACR repository. As of October 2019, this implies running the ``az acr login --name your-registry-name`` command.

* The ``kubectl`` command can interact with the cluster. As of October 2019, this implies running the ``az aks get-credentials --resource-group your-rg --name your-cluster-name`` command.

.. include:: /containers/_managed-clusters-binary-versions-aks.txt

Create base images
------------------

Build the base image by following :ref:`these instructions <k8s_base_image>`.

Create a new containerized execution configuration
--------------------------------------------------

Go to Administration > Settings > Containerized execution, and add a new execution configuration of type "Kubernetes".

* In particular, to set up the image registry, the URL must be of the form ``your-registry-name.azurecr.io``.
* Finish by clicking **Push base images**.

You're now ready to run recipes, notebooks and ML models in AKS.

Using GPUs
==========

Azure provides GPU-enabled instances with NVIDIA GPUs. Several steps are required in order to use them for containerized execution.

.. |base-image-type| replace:: container-exec

.. include:: /containers/_base-image-cuda-support.txt

Thereafter, create a new container configuration dedicated to running GPU workloads. If you specified a tag
for the base image, report it in the "Base image tag" field.

Create configuration and add a custom reservation
-------------------------------------------------

Create a new containerized execution configuration dedicated to running GPU workloads. If you specified a tag for the base image, report it in the “Base image tag” field.

In order for your container execution to be located on nodes with GPU accelerators, and for AKS to configure the CUDA driver on your containers, the corresponding AKS pods must be created with a custom “limit” (in Kubernetes parlance) to indicate that you need a specific type of resource (standard resource types are CPU and Memory). Also, NVIDIA drivers should be mounted in the containers.

To do so:

- in the “Custom limits” section, add a new entry with key: ``alpha.kubernetes.io/nvidia-gpu`` and value: ``1`` (to request 1 GPU). Don’t forget to effectively add the new entry.

- in "HostPath volume configuration", mount  ``/usr/local/nvidia`` as ``/usr/local/nvidia``. Don’t forget to effectively add the new entry, and save the settings.

Create a cluster with GPUs
--------------------------

Follow Azure documentation for how to create a cluster with GPU accelerators.

Deploy
------

You can now deploy your GPU-requiring recipes and models.
