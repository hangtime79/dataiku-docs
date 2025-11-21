# How to setup a Edge Node for Google Dataproc on GCP



  * [1. Overview](#1-requirements)
  * [2. Building Edge Node Image](#2-build-edge-node-imag)
  * [3. Configuring the edge node](#3-configuration)
  * [4. Installing DSS and Dataproc plugin](#4-Installation)
  * [5. Upgrading to a new Edge Node image ](#4-upgrade)
<a name="1-requirements"></a>

## 1. Requirements 

This guide assume you possess minimal system administration skill like connecting to a server via SSH and transfering file via SCP or log as root via sudo. You must be familiar with Google Cloud Hosted services and basic Cloud and virtualization concepts. 

The VM designated as "Edge node" will be the VM that will host the DSS instance you inted to connect to Dataproc with. This instance is assumed to be a persistent Google Compute Engine virtual machine. 

- It's highly recommended (and required if you follow this guide ) that the edge node is installed with the same operating system as a supported OS for Dataproc. We will perform this installation on a Debian 9 (Stretch)

- It's required that the edge node is within the same network and that the tcp communitaiton bet

- Unless you choose to replace some default settings of the cluster the service account that starts your WM MUST have permissions on the temporary bucket used as scratch repository of your cluster. (we will call it SCRATCH_BUCKET)


The following guide as been written and tested with Dataiku DSS sersion 5.1.2 and Google DataProc

Before starting  you need : 
* have [Gcloud client installed](https://cloud.google.com/sdk/install) on your system 
* to create or use a service account that can run instance 
* to have a GCS bucket at your disposal with read and write permissions
* to create a subnet with private google access activated
* to have cloud dataproc api enabled on your GCP project
* For customer environment it's mandatory to install DSS on a dedicated additional disk (its location in the guide will be pointed out as "/path/to/dedicated/disk/")

<a name="2-build-edge-node-image"></a>

## Build Edge Node Image

GCP professionnal services recently released an edge node buiding toolkit so the first step is to refer to the "Usage > image Creation" section of [their documentation](https://github.com/GoogleCloudPlatform/professional-services/tree/master/tools/dataproc-edge-node).

It is about setting up image_src with : 
- your project name 
- a service account that will run your instance (that you need to create in advance )
- a region and a subnet on which private Google access is turned on



<a name="3-configuration"></a>
## Configuring the edge node 


The fist step at this stage will be to run a new instance based on the image previously created  and  SSH as sudo user. 


You want to update the repositories and base system packages: 

`sudo apt-get update `

You might experience waring messages  messages related to updating some dataproc repositories but this doesn't seem to impact the integration. 
```
W: An error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error: http://storage.googleapis.com/dataproc-bigtop-repo/1_4_deb9_20190808_014700-RC01 dataproc InRelease: The following signatures were invalid: EXPKEYSIG 567D794D3610E553 Google Inc. <dataproc-feedback@google.com>
W: Failed to fetch http://storage.googleapis.com/dataproc-bigtop-repo/1_4_deb9_20190808_014700-RC01/dists/dataproc/InRelease  The following signatures were invalid: EXPKEYSIG 567D794D3610E553 Google Inc. <dataproc-feedback@google.com>
W: Some index files failed to download. They have been ignored, or old ones used instead.
```


The next step related to the remaining dependences of DSS , you can wait for the kit and use install deps script but the only known missing dependences for a regular installation oare  acl and nginx

`sudo apt-get install acl nginx `


Due to a few issues encountered i also had to diable the timeline service by setting yarn.timeline-service.enabled to false in  /etc/hadoop/conf/yarn-site.xml. 
You will also have to  edit  /etc/spark/conf/spark-defaults.conf  and set `spark.eventLog.enabled=false`


<a name="4-installation"></a>
## Installing DSS and the plugin

As a reminder for customer environment you need to:
- create a system account for DSS (in this instance we use 'dataiku') by specifying an explicit UID to ease migration up
- attach an additional volume 
- format it (ideally using xfs)
- mount it (the mount point would be designated as "/path/to/dedicated/disk/")
- give ownership of /path/to/dedicated/disk/ to the system account of DSS


In this note we will perforom a installation based on Dataiku 7.0. 

```
 wget https://cdn.downloads.dataiku.com/public/dss/7.0.0/dataiku-dss-7.0.0.tar.gz
 tar -xvzf dataiku-dss-7.0.0.tar.gz
 ./dataiku-dss-7.0.0/installer.sh -d /path/to/dedicated/disk/dss -p 11200
 /path/to/dedicated/disk//dss/bin/dssadmin install-spark-integration
 /path/to/dedicated/disk/dss/bin/dss start
```
From DSS UI you will need to : 
- enter your DSS license
- login as administrator 
- Install Dataproc plugin using the store or an archive according to your network policy



<a name="5-upgrade"></a>
## Upgrading to a new Edge Node image 

This describe the process of upgrading or migrating to a new edge node image. 

For customer environment you need to:
- create a system account for DSS with the same UID as the primary installation
- mount the existing datadir volume to the same location ("/path/to/dedicated/disk/")
- give ownership of /path/to/dedicated/disk/ to the system account of DSS


In this note we will perforom an upgrade to Dataiku 7.0. 

```
 wget https://cdn.downloads.dataiku.com/public/dss/7.0.0/dataiku-dss-7.0.0.tar.gz
 tar -xvzf dataiku-dss-7.0.0.tar.gz
 ./dataiku-dss-7.0.0/installer.sh -d /path/to/dedicated/disk/dss -u
 /path/to/dedicated/disk//dss/bin/dssadmin install-hadoop-integration
 /path/to/dedicated/disk//dss/bin/dssadmin install-spark-integration
 /path/to/dedicated/disk/dss/bin/dss start
```








