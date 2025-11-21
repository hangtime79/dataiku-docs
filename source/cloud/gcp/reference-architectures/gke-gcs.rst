Reference architecture: managed compute on GKE and storage on GCS
#################################################################

Overview
========

This architecture document explains how to deploy:

* A DSS instance running on a Google Compute Engine (GCE) virtual machine
* Dynamically-spawned Google Kubernetes Engine (GKE) clusters for computation (Python and R recipes/notebooks, in-memory visual ML, visual and code Spark recipes, Spark notebooks)
* Ability to store data in Google Cloud Storage

Security
========

The ``dssuser`` needs to be authenticated on the GCE machine hosting DSS with a GCP Service Account that has sufficient permissions to:

    - manage GKE clusters
    - push Docker images to Google Artifact Registry (GAR)


Main steps
==========

Prepare the instance
--------------------

* Setup an AlmaLinux 8 GCE machine and make sure that:

    - you select the right Service Account 
    - you set the access scope to "read + write" for the Storage API
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
* Set ``<region>-docker.pkg.dev/<gcp-project>/<repository-name>`` as the "Image registry URL"
* Push base images


Setup Spark and metastore in DSS
--------------------------------

* Create a new Spark configuration and enable "Managed Spark-on-K8S"
* Set ``<region>-docker.pkg.dev/<gcp-project>/<repository-name>`` as the "Image registry URL"
* Push base images
* Set metastore catalog to "Internal DSS catalog"


Setup GCS connections
---------------------

* Setup as many GCS connections as required, with appropriate credentials and permissions
* Make sure that "GS" is selected as the HDFS interface


Install GKE plugin
------------------

* Install the GKE plugin

* Create a new "GKE connections" preset and fill in :

    - the GCP project key
    - the GCP zone

* Create a new "Node pools" preset and fill in:

    - the machine type
    - the number of nodes


Create your first cluster
-------------------------

* Create a new cluster, select "create GKE cluster" and enter the desired name
* Select the previously created presets and create the cluster
* Cluster creation takes around 5 minutes

Use your cluster
----------------

* Create a new DSS project and configure it to use your newly-created cluster
* You can now perform all Spark operations over Kubernetes
* GCS datasets that are built will sync to the local DSS metastore








