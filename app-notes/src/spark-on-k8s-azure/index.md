# Howto: Run Spark on Kubernetes on Azure

  * [1. Overview](#1-overview)
  * [2. Prerequisites and limitations](#2-prerequisites)
  * [3. Initial setup with hadoop2](#3-initial-setup-hadoop2)
  * [4. Initial setup with hadoop3](#4-initial-setup-hadoop3) - _Experimental_ does NOT support SparkSQL
  * [5. Connect to Azure storage](#5-connect-azure-storage)

**This document is mostly deprecated as of DSS 6.0 - Please refer to the reference architectures in the reference documentation**

<a name="1-overview"></a>

## 1. Overview

It is possible to run Spark over Kubernetes in "client" mode. This howto documents the steps required to obtain this setup, and to be able to read and write files (including Parquet) on ADLS.

Note that this support is very experimental and Dataiku is not currently able to provide support on this setup.

<a name="2-prerequisites"></a>

## 2. Prerequisites and limitations

### 2.1. Prerequisites

* DSS must be installed on an Azure Virtual Machine, in a VNET that has connectivity to your Kubernetes vnet.
* The hostname of the DSS Azure Virtual machine must be resolvable from the K8S cluster
* The DSS Azure Virtual machine must be reachable on all ports from the K8S cluster

### 2.2. Limitations

* Only "client" deployment mode is supported. "cluster" deployment mode is not supported.
* Running DSS in user isolation mode with legacy storage is supported. However, each impersonated user (i.e. target UNIX user) must have a local Kubernetes credential (```~/.kube/config```) allowing him to use Kubernetes
* Running DSS in user isolation with ABFS (ADLS gen2) is NOT supported
* Running SparkSQL recipes with ABFS (ADLS gen2) is NOT supported
* Code environments can only be used on the Driver side. Code that executes on the executor can only use "base" packages. If you need more advanced packages on the executors side, you'll need to build custom Spark Docker images
* ADLS gen2 is supported starting DSS version 5.1.3 (see the next section for limitation and details)

### 2.3. ADLS gen2 (ABFS) Compatibility

**IMPORTANT** SparkSQL is not supported with ABFS (ADLS gen2) 

ADLS gen2 is still at an experimental phase and is integrated with hadoop3 starting hadoop 3.2
Spark versions to date (up to version 2.4.3) is *NOT* officially supporting hadoop 3, support is experimental and SparkSQL won't work 

If you plan to use ADLS gen2 you must jump to the [Initial setup with hadoop3](#4-initial-setup-hadoop3) section.

You should be able to run both ADLS versions with hadoop3 but this is not guaranteed.

Also MUS with ADLS gen2 will not be supported

<a name="3-initial-setup-hadoop2"></a>

## 3. Initial setup with hadoop 2

### 3.1. Initial Docker, Kubernetes and registry setup

Follow Microsoft documentation so that:

* The user running DSS on the DSS machine can use the local Docker daemon to build images
* The user running DSS on the DSS machine can push images to ACR (requires at least ``az login`` + ``az acr login``)
* The Kubernetes cluster can pull from ACR (requires a role assignment to the cluster)

### 3.2 DSS initial installation

* Install DSS version 5.1.1 or later
* On the DSS machine, download ```dataiku-dss-hadoop-standalone-libs-generic-X.Y.Z.tar.gz``` from the DSS download site
* Run

    ```
    ./bin/dssadmin install-hadoop-integration -standalone generic \
                -standaloneArchive /path/to/dataiku-dss-hadoop-standalone-libs-generic.X.Y.Z.tar.gz
    ```

### 3.3 Preparing the Spark distribution

* In the Spark 2.4, remove the Hadoop 2.7 JARs

    ```
    rm -f PATH_TO_SPARK/jars/hadoop-*2.7*
    ```
* In the Spark 2.4, remove the httpcore and httpclient jars (conflicts with AWS libs)

    ```
    rm -f PATH_TO_SPARK/jars/httpc*
    ```

* Copy the Hadoop 2.8 JARs plus additional support JARs from the DSS Hadoop libraries

    ```
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic/hadoop-*2.8* PATH_TO_SPARK/jars/
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic/htrace-core4-4.0.1-incubating.jar PATH_TO_SPARK/jars/
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic/azure* PATH_TO_SPARK/jars/
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic/*aws* PATH_TO_SPARK/jars/
    ```

* Copy the Snappy JAR from DSS (required to process compressed Parquet files)

    ```
    cp PATH_TO_DSS_INSTALL_DIR/lib/ivy/backend-run/snappy-java-1.0.5.jar PATH_TO_SPARK/jars/
    ```

* Copy the httpclient/httpcore JARs from DSS that we know work with the AWS libs

    ```
    cp PATH_TO_DSS_INSTALL_DIR/lib/ivy/backend-run/httpc* PATH_TO_SPARK/jars/
    ```

* Tweak the Spark Dockerfile (required to process compressed Parquet files)

    * Edit the ```PATH_TO_SPARK/kubernetes/dockerfiles/spark/Dockerfile``` file
    * Near the end, after the ```ENV SPARK_HOME``` line, add another line:

        ```
        ENV LD_LIBRARY_PATH /lib64
        ```

    * in the `apk add ...` line, add `nss` :

        ```
            apk add --no-cache bash tini libc6-compat linux-pam nss && \
        ```

* Build and push the Docker images for Spark (the tag name is an example, you can change it)

    ```
    ./bin/docker-image-tool.sh -r your-ACR-name.azurecr.io -t dss-511-spark-240 build
    ./bin/docker-image-tool.sh -r your-ACR-name.azurecr.io -t dss-511-spark-240 push
    ```

### 3.4 Setup of DSS (single-user-security)

* Follow Microsoft documentation to ensure that the user running DSS can access the Kubernetes cluster (```az aks get-credentials```)

* Find out the URL of the APIServer of your Kubernetes cluster:

  ```
  kubectl cluster-info
  ```

* Go to the DSS data directory and run

    ```
    ./bin/dssadmin install-spark-integration -sparkHome PATH_TO_SPARK
    ```

* Start DSS

* Go to Administration > Settings > Spark

* Edit the "default" configuration to add the following keys

    ```
    spark.master --> k8s://https://URL-OF-YOUR-APISERVER.azmk8s.io:443
    spark.kubernetes.container.image --> your-ACR-NAME.azurecr.io/spark-py:dss-511-spark-240
    ```

<a name="4-initial-setup-hadoop3"></a>

## 4. Initial setup with hadoop 3 - Experimental - does NOT work with SparkSQL

### 4.1. Initial Docker, Kubernetes and registry setup

Follow Microsoft documentation so that:

* The user running DSS on the DSS machine can use the local Docker daemon to build images
* The user running DSS on the DSS machine can push images to ACR (requires at least ``az login`` + ``az acr login``)
* The Kubernetes cluster can pull from ACR (requires a role assignment to the cluster)

### 4.2 DSS initial installation

* Install DSS version 5.1.3 or later
* On the DSS machine, download ```dataiku-dss-hadoop3-standalone-libs-generic-X.Y.Z.tar.gz``` from the DSS download site

Be careful  to **download the hadoop 3 version**

* Run

    ```
    ./bin/dssadmin install-hadoop-integration -standalone generic-hadoop3 \
                -standaloneArchive /path/to/dataiku-dss-hadoop3-standalone-libs-generic.X.Y.Z.tar.gz
    ```

### 4.3 Preparing the Spark distribution

* In the Spark 2.4, remove the Hadoop 2.7 JARs

    ```
    rm -f PATH_TO_SPARK/jars/hadoop-*2.7*
    ```

* In the Spark 2.4, remove the httpcore and httpclient jars (conflicts with AWS libs)

    ```
    rm -f PATH_TO_SPARK/jars/httpc*
    ```


* Copy the Hadoop 3.x JARs plus additional support JARs from the DSS Hadoop libraries

    ```
    cp /PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic-hadoop3/hadoop-*3.* PATH_TO_SPARK/jars/
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic-hadoop3/woodstox-* PATH_TO_SPARK/jars/
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic-hadoop3/stax2-* PATH_TO_SPARK/jars/
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic-hadoop3/commons-configuration2-* PATH_TO_SPARK/jars/
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic-hadoop3/htrace-core4-4.1.0-incubating.jar PATH_TO_SPARK/jars/
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic-hadoop3/re2j-1.1.jar PATH_TO_SPARK/jars/
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic-hadoop3/azure* PATH_TO_SPARK/jars/
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic-hadoop3/*aws* PATH_TO_SPARK/jars/
    cp PATH_TO_DSS_INSTALL_DIR/hadoop-standalone-libs/generic-hadoop3/wildfly-openssl-* PATH_TO_SPARK/jars/
    ```

* Copy the Snappy JAR from DSS (required to process compressed Parquet files):

    ```
    cp PATH_TO_DSS_INSTALL_DIR/lib/ivy/backend-run/snappy-java-1.0.5.jar PATH_TO_SPARK/jars/
    ```

* Copy the httpclient/httpcore JARs from DSS that we know work with the AWS libs

    ```
    cp PATH_TO_DSS_INSTALL_DIR/lib/ivy/backend-run/httpc* PATH_TO_SPARK/jars/
    ```

* Tweak the Spark Dockerfile (required to process compressed Parquet files)

* Edit the ```PATH_TO_SPARK/kubernetes/dockerfiles/spark/Dockerfile``` file
* Near the end, after the ```ENV SPARK_HOME``` line, add another line:

    ```
    ENV LD_LIBRARY_PATH /lib64
    ```

* in the `apk add ...` line, add `nss` :

    ```
    apk add --no-cache bash tini libc6-compat linux-pam nss && \
    ```

* Build and push the Docker images for Spark (the tag name is an example, you can change it)

    ```
    ./bin/docker-image-tool.sh -r your-ACR-name.azurecr.io -t dss-513-spark-240 build
    ./bin/docker-image-tool.sh -r your-ACR-name.azurecr.io -t dss-513-spark-240 push
    ```

### 4.4 Setup of DSS (single-user-security)

* Follow Microsoft documentation to ensure that the user running DSS can access the Kubernetes cluster (```az aks get-credentials```)

* Find out the URL of the APIServer of your Kubernetes cluster:

  ```
  kubectl cluster-info
  ```

* Go to the DSS data directory and run

  ```
  ./bin/dssadmin install-spark-integration -sparkHome PATH_TO_SPARK
  ```

* Start DSS

* Go to Administration > Settings > Spark

* Edit the "default" configuration to add the following keys

  ```
  spark.master --> k8s://https://URL-OF-YOUR-APISERVER.azmk8s.io:443
  spark.kubernetes.container.image --> your-ACR-NAME.azurecr.io/spark-py:dss-513-spark-240
  spark.executor.extraJavaOptions --> -Dorg.wildfly.openssl.path=/dev/null
  ```

__IMPORTANT__: ADLSv2 (ABFS) requires wildfly-openssl, however the current available package (1.0.4-Final) does not work with spark generated docker images due to inconsistencies with the libssl. This additional option forced wildfly to fallback on JSSE for SSL handling

* _(optional)_ if the operating system where DSS is installed is provided with a version of openssl incompatible with wildfly-openssl you may need to add the following key to your spark configuration as well
  ```
  spark.driver.extraJavaOptions --> -Dorg.wildfly.openssl.path=/dev/null
  ```

<a name="5-connect-azure-storage"></a>

# 5. Connect to Azure storage

## 5.1 Connect to ADLS gen1

ADLS gen1 data can be accessed through a HDFS connection.

Your HDFS connection will use OAuth client id / secret in order to connect to ADLS gen1. The recommended method is to use a client credential.

First, you will need to create a service principal and to add it to your ADL Account:

* Go to the portal
* Under services in left nav, look for Azure Active Directory and click it.
* Using “App Registrations” in the menu, create “Web Application”. Remember the name you create here - that is what you will add to your ADL account as authorized user.
* Go through the wizard
* Once app is created, go to “keys” under “settings” for the app
* Select a key duration and hit save. Save the generated keys.
* Go back to the App Registrations page, and click on the “Endpoints” button at the top a. Note down the “Token Endpoint” URL
* Note down the properties you will need to auth:
    * The “Application ID” of the Web App you created above
    * The key you just generated above
    * The token endpoint

Then add the service principal to your ADL Account:

* Go to the portal again, and open your ADL account
* Select Access control (IAM)
* Add your user name you created in Step 6 above (note that it does not show up in the list, but will be found if you searched for the name)
* Add “Owner” role

Then, in DSS:

* Create a new HDFS connection
* Use ```adl://youradlaccount.azuredatalakestore.net/path-within-adl-account``` as the HDFS URL
* Add the following properties (having to enter your keys twice is expected):

    ```
    fs.adl.oauth2.access.token.provider.type = ClientCredential
    fs.adl.oauth2.refresh.url = THE_TOKEN_ENDPOINT (usually starts by https://login.windows.net)
    fs.adl.oauth2.client.id = YOUR_CLIENT_ID
    fs.adl.oauth2.credential = YOUR_CLIENT_SECRET
    ```

For other methods, refer to the Azure Datalake store Hadoop driver documentation.

## 5.2. Connect to ADLS gen2 (ABFS)

### 5.2.1. Connect with Access key

* Retrieve the access key from your ADLSv2 storage Account
* Create a new HDFS connection in DSS
* Use ```abfss://<your_file_system_name>@<your_storage_account_name>.dfs.core.windows.net/``` as the HDFS URL
* Add the following property to the extra hadoop conf:

  ```fs.azure.account.key.<your_storage_account_name>.dfs.core.windows.net=<your_access_key>```
