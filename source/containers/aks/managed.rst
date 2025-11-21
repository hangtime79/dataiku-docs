Using managed AKS clusters
############################

.. contents::
    :local:


Initial setup
=============

Create your ACR registry
------------------------

If you already have an Azure Container Registry (ACR) up and ready, you can skip this section and go to :ref:`aks_install_plugin`.

Otherwise, follow the Azure documentation on `how to create your ACR registry <https://docs.microsoft.com/en-us/azure/container-registry/>`_.

.. warning::
   We recommend that you pay extra attention to the Azure `container registry pricing plan <https://azure.microsoft.com/en-us/pricing/details/container-registry/>`_, as it is directly related to the registry storage capacity.

.. _aks_install_plugin:

Install the AKS plugin
----------------------

To use Microsoft Azure Kubernetes Service (AKS), begin by installing the "AKS clusters" plugin from the Plugins store in Dataiku DSS. For more details, see the :doc:`instructions for installing plugins </plugins/installing>`.

Prepare your local ``az``, ``docker``, and ``kubectl`` commands
---------------------------------------------------------------

Follow the Azure documentation to ensure the following on your local machine (where DSS is installed):

* The ``az`` command is properly logged in. This implies running the ``az login --service-principal --username client_d --password client_secret --tenant tenant_id`` command. More details in `Azure documentation <https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli>`__.

* The ``docker`` command can successfully push images to the ACR repository. This implies running the ``az acr login --name your-registry-name`` command.

* The ``kubectl`` command is installed.

.. include:: /containers/_managed-clusters-binary-versions-aks.txt

Create base images
------------------

Build the base image by following :ref:`these instructions <k8s_base_image>`.

Create a new containerized execution configuration
--------------------------------------------------

Go to Administration > Settings > Containerized execution, and add a new execution configuration of type "Kubernetes".

* In particular, to set up the image registry, the URL must be of the form ``your-registry-name.azurecr.io``.
* Finish by clicking **Push base images**.

Cluster configuration
=====================

* The **connection** is where you define how to connect to Azure. This can be done either inline in each cluster (not recommended) or via a preset in the "AKS connection" plugin settings (recommended).

* By default, the service principal associated to the cluster will be the same as the one used on the DSS machine. You can change this by enabling the **Use distinct credentials** option and defining a specific connection, either inline or via a preset.

* **Cluster nodes** is where you define the number and type of nodes that you want in your cluster. You can define the properties of a node pool either inline (not recommended) or as a preset in the "Node pools" plugin settings (recommended). You have the possibility to define multiple node pools, each with its own properties.

Using GPUs
==========

Azure provides GPU-enabled instances with NVIDIA GPUs. Using GPUs for containerized execution requires the following steps.

.. |base-image-type| replace:: container-exec

.. include:: /containers/_base-image-cuda-support.txt

Thereafter, create a new container configuration dedicated to running GPU workloads. If you specified a tag for the base image, report it in the "Base image tag" field.

Enable GPU support on the cluster
---------------------------------

When you create your cluster using the AKS plugin, be sure to select a VM with a GPU. See `Azure documentation for a full list <https://docs.microsoft.com/en-us/azure/virtual-machines/sizes-gpu>`_. You'll also need to enable the "With GPU" option in the node pool settings.

At cluster creation, the plugin will run the NVIDIA driver "DaemonSet" installation procedure, which needs several minutes to complete.

Add a custom reservation
------------------------

For your containerized execution task to run on nodes with GPUs, and for AKS to configure the CUDA driver on your containers, the corresponding pods must be created with a `custom limit` (in Kubernetes parlance). This indicates that you need a specific type of resource (standard resource types are CPU and memory).

You must configure this limit in the containerized execution configuration. To do this:

* In the "Custom limits" section, add a new entry with key ``nvidia.com/gpu`` and value ``1`` (to request 1 GPU).
* Add the new entry and save your settings.

Deploy
------

You can now deploy your GPU-based recipes and models.

Other
=====

When you create a cluster using the AKS plugin, Microsoft will receive information that this cluster was provisioned from a Dataiku DSS instance. Microsoft is able to correlate the Azure resources that are used to support the software. Microsoft collects this information to provide the best experiences with their products and to operate their business. The data is collected and governed by Microsoft's privacy policies, which can be found  `here <https://www.microsoft.com/trustcenter/>`_.

To disable this, set a ``DISABLE_AZURE_USAGE_ATTRIBUTION`` environment variable to ``1`` in ``DATADIR/bin/env-site.sh``.
