Deployment on AWS EKS
#####################

You can use the API Deployer Kubernetes integration to deploy your API Services on AWS Elastic Kubernetes Service (EKS).

Setup
=====

Create your EKS cluster
-----------------------

To create your Amazon Elastic Kubernetes Service (EKS) cluster, follow the `AWS user guide <https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html>`_. We recommend that you allocate at least 7 GB of memory for each cluster node.


Prepare your local ``aws``, ``docker``, and ``kubectl`` commands
-----------------------------------------------------------------

Follow the `AWS documentation <https://docs.aws.amazon.com/index.html?nc2=h_ql_doc_do_v>`__ to ensure the following on your local machine (where Dataiku DSS is installed):

* The ``aws ecr`` command can list and create docker image repositories and authenticate ``docker`` for image push.
* The ``kubectl`` command can create deployments and services on the cluster.
* The ``docker`` command can successfully push images to the ECR repository.

.. include:: /containers/_managed-clusters-binary-versions-eks.txt

Setup the infrastructure
------------------------

Follow the usual setup steps as indicated in :doc:`setup`.

* On EKS, the image registry URL is the one given by ``aws ecr describe-repositories``, without the image name. It typically looks like ``XXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/PREFIX``, where ``XXXXXXXXXXXX`` is your AWS account ID, ``us-east-1`` is the AWS region for the repository and ``PREFIX`` is an optional prefix to triage your repositories.

* Once you have filled the registry URL, the "Image pre-push hook" field becomes visible: set it to "Enable push to ECR".

Deploy
------

You are now ready to deploy your API Services to EKS.

Using GPUs
==========

AWS provides GPU-enabled instances with NVIDIA GPUs. Several steps are required in order to use them for API Deployer deployments.

.. |base-image-type| replace:: apideployer

.. include:: /containers/_base-image-cuda-support.txt

If you used a specific tag, go to the infrastructure settings, and in the "Base image tag" field, enter ``dataiku-apideployer-base-cuda:X.Y.Z``

Create a cluster with GPUs
--------------------------

Follow `AWS documentation <https://docs.aws.amazon.com/eks/latest/userguide/gpu-ami.html>`__ for how to create a cluster with GPU.

Add a custom reservation
------------------------

In order for your API Deployer deployments to be located on nodes with GPU devices, and for EKS to configure the CUDA driver on your containers, the corresponding EKS pods must be created with a custom "limit" (in Kubernetes parlance) to indicate that you need a specific type of resource (standard resource types are CPU and memory).

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
