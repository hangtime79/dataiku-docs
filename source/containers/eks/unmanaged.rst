Using unmanaged EKS clusters
############################

.. contents::
	:local:

Setup
======

Create your EKS cluster
------------------------

To create your Amazon Elastic Kubernetes Service (EKS) cluster, follow the `AWS user guide <https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html>`_. We recommend that you allocate at least 15 GB of memory for each cluster node. More memory may be required if you plan on running very large in-memory recipes.

You'll be able to configure the memory allocation for each container and per-namespace using multiple containerized execution configurations.


Prepare your local ``aws``, ``docker``, and ``kubectl`` commands
-----------------------------------------------------------------

Follow the `AWS documentation <https://docs.aws.amazon.com/index.html?nc2=h_ql_doc_do_v>`_ to ensure the following on your local machine (where Dataiku DSS is installed):

* The ``aws ecr`` command can list and create docker image repositories and authenticate ``docker`` for image push.
* The ``kubectl`` command can interact with the cluster.
* The ``docker`` command can successfully push images to the ECR repository.

.. include:: /containers/_managed-clusters-binary-versions-eks.txt

Create base images
------------------

Build the base image by following :ref:`these instructions <k8s_base_image>`.

Create a new execution configuration
------------------------------------

Go to Administration > Settings > Containerized execution, and add a new execution configuration of type "Kubernetes".

* The image registry URL is the one given by ``aws ecr describe-repositories``, without the image name.
  It typically looks like ``XXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com/PREFIX``, where ``XXXXXXXXXXXX``
  is your AWS account ID, ``us-east-1`` is the AWS region for the repository and ``PREFIX`` is an optional
  prefix to triage your repositories.
* Set "Image pre-push hook" to **Enable push to ECR**.

You're now ready to run recipes and models on EKS.


Using GPUs
===========

AWS provides GPU-enabled instances with NVIDIA GPUs. Using GPUs for containerized execution requires the following steps.

.. |base-image-type| replace:: container-exec

.. include:: /containers/_base-image-cuda-support.txt

Thereafter, create a new container configuration dedicated to running GPU workloads. If you specified a tag
for the base image, report it in the "Base image tag" field.

Enable GPU support on the cluster
---------------------------------

To execute containers that leverage GPUs, your worker nodes and the control plane must also support GPUs. The following
steps describe a simplified way to enable a worker node leverage its GPUs:

* `Install the NVIDIA Driver <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html>`_ that
  goes with the model of GPU on the instance.
* `Install the Cuda driver <https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html>`_. We
  recommend using the runfile installation method. Note that you do not have to install the cuda toolkit, as the driver
  alone is sufficient.
* Install the `NVIDIA docker runtime <https://github.com/NVidia/nvidia-docker>`_ and set this runtime
  as the default docker runtime.

.. note::
    These steps can vary, depending on the underlying hardware and software version requirements for your projects.

Finally, enable the cluster GPU support with the `NVIDIA device plugin <https://github.com/NVidia/k8s-device-plugin>`_. Be
careful to select the version that matches your Kubernetes version (``v1.10`` as of July 2018).

Add a custom reservation
-------------------------

For your container execution to be located on nodes with GPU accelerators, and for EKS to configure the CUDA driver on your containers, the corresponding EKS pods must be created with a custom "limit" (in Kubernetes parlance). This indicates that you need a specific type of resource (standard resource types are CPU and memory).

You must configure this limit in the containerized execution configuration. To do this:

* In the "Custom limits" section, add a new entry with key: ``nvidia.com/gpu`` and value: ``1`` (to request 1 GPU).
* Add the new entry and save the settings.

Deploy
-------

You can now deploy your GPU-required recipes and models.
