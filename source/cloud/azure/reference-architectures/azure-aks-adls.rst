Reference architecture: manage compute on AKS and storage on ADLS gen2
######################################################################

Overview
========

This architecture document explains how to deploy:

* A DSS instance running on an Azure virtual machine
* Dynamically-spawned Azure Kubernetes Service (AKS) clusters for computation (Python and R recipes/notebooks, in-memory visual ML, visual and code Spark recipes, Spark notebooks)
* Ability to store data in Azure DataLake Storage (ADLS) gen2

Security
========

We assume that all operations described here are done within a common Azure Resource Group (RG), in which the Service Principal (SP) you are using has sufficient permissions to:

* Manage AKS clusters
* Push Docker images to Azure Container Registry (ACR)
* Read/write from/to ADLS gen 2

Main steps
==========

Prepare the instance
--------------------

* Setup an AlmaLinux 8 Azure VM in your target RG 
* Install and configure Docker CE
* Install kubectl
* Setup a non-root user for the ``dssuser``

Install DSS
-----------

* Download DSS, together with the "generic-hadoop3" standalone Hadoop libraries and standalone Spark binaries.
* Install DSS, see :doc:`/installation/index`
* Build base container-exec and Spark images, see :doc:`/containers/setup-k8s`

Setup containerized execution configuration in DSS
--------------------------------------------------

* Create a new "Kubernetes" containerized execution configuration
* Set ``your-cr.azurecr.io`` as the "Image registry URL"
* Push base images

Setup Spark and metastore in DSS
--------------------------------

* Create a new Spark configuration and enable "Managed Spark-on-K8S"
* Set ``your-cr.azurecr.io`` as the "Image registry URL"
* Push base images
* Set metastore catalog to "Internal DSS catalog"

Setup ADLS gen2 connections
---------------------------

* Setup as many Azure blob storage connections as required, with appropriate credentials and permissions
* Make sure that "ABFS" is selected as the HDFS interface

Install AKS plugin
------------------

* Install the AKS plugin

* Create a new "AKS connection" preset and fill in:

    - the Azure subscription ID
    - the tenant ID
    - the client ID
    - the password (client secret)

* Create a new "Node pools" preset and fill in:

    - the machine type
    - the default number of nodes

Create your first cluster
-------------------------

* Create a new cluster, select "Create AKS cluster" and enter the desired name
* Select the previously created presets
* In the "Advanced options" section, type an IP range for the Service CIDR (e.g. 10.0.0.0/16) and an IP address for the DNS IP (e.g. 10.0.0.10).
* Click on "Start/attach". Cluster creation takes between 5 and 10 minutes.

Use your cluster
----------------

* Create a new DSS project and configure it to use your newly-created cluster
* You can now perform all Spark operations over Kubernetes 
* ADLS gen2 datasets that are built will sync to the local DSS metastore.
