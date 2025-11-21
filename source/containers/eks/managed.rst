.. |leq|   unicode:: U+02264 .. LESS-THAN OR EQUAL TO
.. |geq|   unicode:: U+02265 .. GREATER-THAN OR EQUAL TO

Using managed EKS clusters
###########################

.. contents::
	:local:

Initial Setup
==============

Install the EKS plugin
------------------------

To use Amazon Elastic Kubernetes Service (EKS), begin by installing the "EKS clusters" plugin from the Plugins store in Dataiku DSS. For more details, see the :doc:`instructions for installing plugins </plugins/installing>`.

Prepare your local commands
---------------------------------------------------------------

Follow the `AWS documentation <https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html>`__ to ensure the following on your local machine (where DSS is installed):

* The ``aws`` command has credentials that give it write access to Amazon Elastic Container Registry (ECR)  and full control on EKS.
* The ``aws-iam-authenticator`` command is installed. `See documentation <https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html>`__.
* The ``kubectl`` command is installed. `See documentation <https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html>`__.
* The ``docker`` command is installed and can build images. `See documentation <https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-docker.html>`__.

.. include:: /containers/_managed-clusters-binary-versions-eks.txt

Create base images
-------------------

Build the base image by following :ref:`these instructions <k8s_base_image>`.

Create a new containerized execution configuration
--------------------------------------------------

Go to Administration > Settings > Containerized execution, and add a new execution configuration of type "Kubernetes".

* The image registry URL is the one given by ``aws ecr describe-repositories``, without the image name.
  It typically looks like ``XXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/PREFIX``, where ``XXXXXXXXXXXX``
  is your AWS account ID, ``us-east-1`` is the AWS region for the repository, and ``PREFIX`` is an optional
  prefix to triage your repositories.
* Set "Image pre-push hook" to **Enable push to ECR**.

Cluster configuration
======================

Connection
----------

The connection is where you define how to connect to AWS. Instead of providing a value here, we recommend that you leave it empty, and use the AWS credentials found by the ``aws`` command in ``~/.aws/credentials``.

The connection can be defined either inline in each cluster (not recommended), or as a preset in the plugin's settings (recommended).

Network settings
-------------------

EKS requires two subnets in the same virtual private cloud (VPC). Your AWS administrator needs to provide you with two subnet identifiers.
We strongly recommend that these subnets reside in the same VPC as the DSS host. Otherwise, you have to manually set up some peering and routing between VPCs.

Additionally, you must indicate security group ids. These security groups will be associated with the EKS cluster nodes. The networking requirement is that the DSS machine has full inbound connectivity from the EKS cluster nodes. We recommend that you use the ``default`` security group.

Network settings can be defined either inline in each cluster (not recommended), or as a preset in the plugin's settings (recommended).

Cluster nodes
---------------

This setting allows you to define the number and type of nodes in the cluster.

Advanced settings
-----------------

Custom registry for autoscaler images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the plugin uses images from the public ``registry.k8s.io`` registry for the Kubernetes autoscaler images.
If your cluster does not have access to the internet, you can set up a private registry and mirror the images there.
You can then specify the URL of your private registry in the advanced settings of the cluster.
The image must be identifiable by the following pattern: ``${customRegistryURL}/autoscaler/cluster-autoscaler:${autoscalerVersion}`` where ``customRegistryURL`` is the URL of your private registry.
The ``autoscalerVersion`` will depend on your version of Kubernetes:

- For Kubernetes |leq| 1.24, use ``v1.24.3``
- For Kubernetes == 1.25, use ``v1.25.3``
- For Kubernetes == 1.26, use ``v1.26.4``
- For Kubernetes == 1.27, use ``v1.27.3``
- For Kubernetes |geq| 1.28, use ``v1.28.0``

Using GPUs
==========

AWS provides GPU-enabled instances with NVIDIA GPUs. Using GPUs for containerized execution requires the following steps.

.. |base-image-type| replace:: container-exec

.. include:: /containers/_base-image-cuda-support.txt

Thereafter, create a new container configuration dedicated to running GPU workloads. If you specified a tag for the base image, report it in the "Base image tag" field.

Enable GPU support on the cluster
---------------------------------

When you create your cluster using the EKS plugin, be sure to select a instance type with a GPU. See `EC2 documentation for a full list <https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/accelerated-computing-instances.html>`_. You'll also need to enable the "With GPU" option in the node pool settings.

At cluster creation, the plugin will run the NVIDIA driver "DaemonSet" installation procedure, which needs several minutes to complete.

Add a custom reservation
------------------------

For your containerized execution task to run on nodes with GPUs, and for EKS to configure the CUDA driver on your containers, the corresponding pods must be created with a `custom limit` (in Kubernetes parlance). This indicates that you need a specific type of resource (standard resource types are CPU and memory).

You must configure this limit in the containerized execution configuration. To do this:

* In the "Custom limits" section, add a new entry with key ``nvidia.com/gpu`` and value ``1`` (to request 1 GPU).
* Add the new entry and save your settings.

Deploy
------

You can now deploy your GPU-based recipes and models.
