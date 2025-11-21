# HOWTO: Deploy DSS on ALIBABA Cloud (regular security)




<a name="1-overview"></a>

## 1. Overview

This Documentations is ment to guide you for a basic yet fully operational y deployment of Dataiku DSS on Alibaba cloud (Or Aliyun)


<a name="2-prerequisites"></a>

## 2. Pre-requisites and limitations

### 2.1 Pre-requisites



#### DSS host

You need an Elastic Compute Service (ECS) virtual machine running on a [supported Linux distribution](https://doc.dataiku.com/dss/latest/installation/requirements.html#linux) with a configured UNIX user account (e.g. `dssuser`) that will manage DSS. 

Alibaba Linux has been tested but requires a manual dependances installation and may very rarely be tested with DSS. 

If you plan on accessing/storing data into Alibaba Object Storage Service () with DSS . 

#### Kubernetes cluster


If you forcesee a Spark-on-Kubernetes integration with ACK you need 
* a local Docker daemon installed and configured so that `dssuser` can build images
* appropriate access credentials that would allow your Dataiku instance to push images to Alibaba Container Registry ([ext.doc](https://www.alibabacloud.com/help/doc-detail/60997.htm?spm=a2c63.l28256.a3.17.49981e88Pt6rll)).


You need an  ACK  (Alibaba Container service for Kubernetes) cluster up and running. The service account that owns the cluster must have the appropriate access to the custer

* read and write data from/to OSS
* pull Docker images from ACR 

#### Networking

* The DSS host and the cluster must be located in the same VPC.

* The DSS host must be reachable on all ports from the cluster.

* The hostname of the DSS host must be resolvable from the cluster. If you encounter issues where your executor pods cannot reach the DSS host, add the following line to the `bin/env-site.sh` file in your data directory:

    ```
    export DKU_BACKEND_EXT_HOST=my.host.name
    ```

where `my.host.name` is the fully qualified domain name (FQDN) of your DSS host, that you can obtain with the `hostname -f` command.


### 2.2 Limitations

- Only works in Spark client-mode. Cluster-mode is not supported.

- For Pyspark recipes, code environments can only be used on the Driver side, all code running on the executors will only have access to "base" packages. If you want to use additional packages inside executors, you will need to build custom Spark Docker images.

<a name="3-initial setup"></a>

## 3. Initial setup

### 3.1 Installing DSS

- Install DSS version >= 8.0.4

- Download the `dataiku-dss-hadoop-standalone-libs-generic-X.Y.Z.tar.gz` archive corresponding to your DSS version from the [DSS download website](https://cdn.downloads.dataiku.com/public/studio/).

- From your data directory, run the following command:

    ```bash
    bin/dssadmin install-hadoop-integration -standalone generic \
      -standaloneArchive /path/to/dataiku-dss-hadoop-standalone-libs-generic-X.Y.Z.tar.gz
    ```

### 3.2 Access to Object Storage Service  
#### Libraries and dependances 
In order to access to OSS object you need the hadoop interface of OSS (hadoop-aliyun) and the credential provider provided with the java sdk of OSS (aliyun-sdk-oss). 
- download  hadoop-aliyun jar  and the aliyun-sdk-oss dependances 
```
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aliyun/3.2.1/hadoop-aliyun-3.2.1.jar
wget https://repo1.maven.org/maven2/com/aliyun/oss/aliyun-sdk-oss/3.11.2/aliyun-sdk-oss-3.11.2.jar
```

- copy the jars in the hadoop standalone jars directory of DSS 
```
cp hadoop-aliyun-3.2.1.jar ./dataiku-dss-8.0.4/hadoop-standalone-libs/
cp aliyun-sdk-oss-3.11.2.jar  dataiku-dss-8.0.4/hadoop-standalone-libs/
```
- restart DSS instance 
`DATA_DIR/bin/dss restart`

#### OSS support configuration 

To make the Hadoop implementation of OSS active in Dataiku, you need  to pass the class that handles the the file system, along with the abstract implementatioin for for thrid party execution engines like yarn of the server side. 

From Dataiku user interface, go to  (Administration => settings => Hadoop) and add the following properties to Hadoop Config Keys : 
```
fs.oss.impl --> org.apache.hadoop.fs.aliyun.oss.AliyunOSSFileSystem
fs.AbstractFileSystem.oss.impl --> org.apache.hadoop.fs.aliyun.oss.OSS
```
#### Connection configuration 

At this moment, Dataiku , supports OSS access as via Hadoop connection. For each connection you must provide 

* The root path URI to your OSS bucket with the following structure 
`oss://$YOUR_OSS_BUCKET_NAME/$PATH_WITHIN_THE_BUCKET` 
* The endpoint of your bucket. There's a specific domain name by region - available in the reference docuemntation [Aliyun endpoints by region](https://www.alibabacloud.com/help/doc-detail/31837.htm) 
```
fs.oss.endpoint = OSS_ENDPOINT_DOMAIN_NAME
```
* The credentials properties for authentications 
```
fs.oss.accessKeyId --> YOUR_ACCESS_KEY_ID
fs.oss.accessKeySecret --> YOUR_ACCESS_KEY_SECRET
```

If you wish to implement a per-user connection , you can define user secrets for fs.oss.accessKeyId  and fs.oss.accessKeySecret for the required connection. 




## 4. Kubernetes integration (with ACK)
The Kubernetes integration is quite streightforward, but becarefull to have the image registry righfully initiallized  by the subscription administratior before starting. 

From there you nee to follow [this procedure](https://www.alibabacloud.com/help/doc-detail/198212.htm?spm=a2c63.l28256.b99.11.49981e88O9X5N5) to initialise the registry. 

Once the registry is created you need to create your culster and  import the configuraiton into  on the serveur and reference it DSS (in administartion > settings > container execution ) 







## Troubleshooting
