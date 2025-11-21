Deployment on Azure AKS
#########################

You can use the API Deployer Kubernetes integration to deploy your API Services on Azure Kubernetes Service (AKS).

Setup
======

Create your ACR registry
------------------------

Follow the Azure documentation on `how to create your ACR registry <https://docs.microsoft.com/en-us/azure/container-registry/>`_. We recommend that you pay extra attention to the pricing plan since it is directly related to the registry storage capacity.

Create your AKS cluster
------------------------

Follow Azure's documentation on `how to create your AKS cluster <https://docs.microsoft.com/en-us/azure/aks/>`_. We recommend that you allocate at least 8GB of memory for each cluster node.

Once the cluster is created, you must modify its IAM credentials to `grant it access to ACR <https://docs.microsoft.com/en-us/azure/container-registry/container-registry-auth-aks#grant-aks-access-to-acr>`_ (Kubernetes secret mode is not supported). This is required for the worker nodes to pull images from the registry.


Prepare your local ``az``, ``docker`` and ``kubectl`` commands
--------------------------------------------------------------

Follow the Azure documentation to make sure that:

* Your local (on the DSS machine) ``az`` command is properly logged in. As of October 2019, this implies running the ``az login --service-principal --username client_d --password client_secret --tenant tenant_id`` command. You must use a service principal that has sufficient IAM permissions to write to ACR and full control on AKS.

* Your local (on the DSS machine) ``docker`` command can successfully push images to the ACR repository. As of October 2019, this implies running the ``az acr login --name your-registry-name``.

* Your local (on the DSS machine) ``kubectl`` command can interact with the cluster. As of October 2019, this implies running the ``az aks get-credentials --resource-group your-rg --name your-cluster-name`` command.

.. include:: /containers/_managed-clusters-binary-versions-aks.txt

Setup the infrastructure
-------------------------

Follow the usual setup steps as indicated in :doc:`setup`. In particular, to set up the image registry, in the API Deployer go to Infrastructures > your-infrastructure > Settings, and in the "Kubernetes cluster" section, set the "Registry host" field to ``your-registry-name.azurecr.io``.

Deploy
-------

You're now ready to deploy your API Services to Azure AKS.

Using GPUs
==========

Azure provides GPU-enabled instances with NVIDIA GPUs. Several steps are required in order to use them for API Deployer deployments.

.. |base-image-type| replace:: apideployer

.. include:: /containers/_base-image-cuda-support.txt

If you used a specific tag, go to the infrastructure settings, and in the "Base image tag" field, enter ``dataiku-apideployer-base-cuda:X.Y.Z``

Create a cluster with GPUs
--------------------------

Follow `Azure documentation <https://docs.microsoft.com/en-us/azure/aks/gpu-cluster>`__ for how to create a cluster with GPU.

Add a custom reservation
------------------------

In order for your API Deployer deployments to be located on nodes with GPU devices, and for AKS to configure the CUDA driver on your containers, the corresponding AKS pods must be created with a custom "limit" (in Kubernetes parlance) to indicate that you need a specific type of resource (standard resource types are CPU and memory).

You can configure this limit either at the infrastructure level (all deployments on this infrastructure will use GPUs) or at the deployment level.

At the infrastructure level
%%%%%%%%%%%%%%%%%%%%%%%%%%%

* Go to Infrastructure > Settings
* Go to "Sizing and Scaling"
* In the "Custom limits" section, add a new entry with key ``nvidia.com/gpu`` and value: ``1`` (to request 1 GPU)
* Don't forget to add the new entry, and save settings

At the deployment level
%%%%%%%%%%%%%%%%%%%%%%%

* Go to Deployment > Settings
* Go to "Sizing and Scaling"
* Enable override of infrastructure settings in the "Container limits" section
* In the "Custom limits" section, add a new entry with key ``nvidia.com/gpu`` and value: ``1`` (to request 1 GPU)
* Don't forget to add the new entry, and save settings

Deploy
------

You can now deploy your GPU-requiring deployments.

This applies to:

* Python functions (your endpoint needs to use a code environment that includes a CUDA-using package like tensorflow-gpu)
* Python predictions
