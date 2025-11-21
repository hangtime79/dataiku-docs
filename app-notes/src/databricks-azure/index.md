# Howto: Connect to Azure Databricks

  * [1. Overview](#1-overview)
  * [2. Prerequisites](#2-prerequisites)
  * [3. Initial Azure Databricks setup](#3-initial-setup)
  * [4. DSS setup](#4-dss-setup)
  * [5. Connect to Azure Blob Storage](#5-connect-wasb)
  * [6. Connect to ADLS gen1](#6-connect-adls1)
  * [7. Connect to ADLS gen2](#7-connect-adls2)

<a name="1-overview"></a>

## 1. Overview

The Dataiku-Databricks integration allows you to leverage Databricks as the engine for running Spark computations in DSS.

DSS will automatically leverage the dynamic computation capabilities of Databricks and will automatically spawn Databricks clusters
corresponding to the computations requested by the DSS users.

The following DSS features are available when DSS is using Databricks as the Spark engine:

* Spark engine in visual recipes (prepare, grouping, join, split, distinct, ...)
* SparkSQL recipe
* Spark-Scala recipe
* Spark pipelines
* Pyspark recipe
* Working with multiple Pyspark code environments
* ML models using MLLib
* Running Optimized-scorable models in Spark
* Metastore synchronization
* Charts on SparkSQL
* SparkSQL notebook

The following DSS features are not available when DSS is using Databricks as the Spark engine:

* SparkR / sparklyr recipes
* Python and R notebooks using Spark (notebooks not using Spark remain available)
* Scala notebooks
* Conda code environments (for Pyspark recipes)


<a name="2-prerequisites"></a>

## 2. Prerequisites

* DSS must be installed on an Azure Virtual Machine, in a VNET that has full connectivity to your Databricks resource group. The hostname of the DSS Azure Virtual machine must be resolvable from the Databricks clusters
* Your Databricks subscription must already be up
* You need an administrator account on your Databricks subscription
* You need administrative access to your Azure account

<a name="3-initial-setup"></a>

## 3. Initial Azure Databricks setup

During operation, DSS needs to upload various files that the Databricks clusters will use. In order to ensure a secure distribution of files, you need to setup a space on Windows Azure Blob Storage space where DSS will have read/write access, and Databricks clusters will have read access.

This path can either be a full container, or a subpath in a container. In the rest of this section, these will be denoted as "your-storage-container" (contained within the storage account "your-storage-account") and "your-path-within-the-container".

Only a regular Blob container on Azure Blob Storage can be used. ADLS gen1 and ADLS gen2 cannot be used for the resources upload but can be used for data

### 3.1. Create Azure shared storage space

* If needed, create a new storage account, "your-storage-account" while ensuring that both your Databricks VNET and your DSS VNET have access to the storage account
* If needed, create a new Blob container "your-storage-container" in the storage account
* Write down the Access Key for the storage account
* Create a Shared Access Signature that will get read access to the storage account
    * In "Allowed permissions", select "Read" and "List"
    * Select a long expiration time
    * Don't restrict allowed IP addresses
    * Write down the SAS token

### 3.2. Mount the shared storage path in DBFS

* Go to your Azure Databricks Admin Console
* Create a new Databricks cluster
* Create a Python Databricks notebook attached to the cluster you just created
* Run the following command (for example ```mount-point-in-databricks``` could be ```dku-dbfs-resources```):
    ```
    dbutils.fs.mount(
       source="wasbs://your-storage-container@your-storage-account.blob.core.windows.net/your-path-within-the-container",
       mount_point = "/mnt/mount-point-in-databricks",
       extra_configs =  {
            "fs.azure.sas.your-storage-container.your-storage-account.blob.core.windows.net": "The SAS Token"
       }
    )
    ```

### 3.3. Create a Databricks access token

For the user who will end up creating clusters, create a Databricks access token and write it down

### 3.4. Setup vnet peering

When you install your Azure Databricks workspace, Azure Databricks automatically creates a new vnet and places the workers in this vnet. In the rest of this section, this vnet will be called the "workers vnet", while the vnet containing the DSS machine will be the "DSS vnet".

In order for DSS integration to work, the Databricks workers must be able to communicate with the DSS backend host. This is achieved by peering the two vnets together.

* Go to the Azure portal
* Go to your Azure Databricks Workspace, and select the "Virtual Network Peerings" tab
* Add a peering, give it a name (like "peering-to-dss-vnet"), and in "Virtual network", select the DSS vnet
* Click on the "Copy" button to copy the Databricks Virtual Network Resource Id (i.e. the workers vnet identifier) to your clipboard
* Click add to establish the first half of the peering (workers Vnet -> DSS vnet direction)

We now need to establish the second half of the peering

* Go to the Azure portal and select the "Virtual netowrks" service
* Go to the DSS vnet, and select the "Peerings" tab
* Add a peering, give it a name (like "peering-to-workers-vnet"), select "I know my resource" and paste the Databricks Virtual Network Resource Id
* Click add to establish the connection

In the DSS vnet's "Peerings" tab, the "peering-to-workers-vnet" must now appear as "Connected". 


<a name="4-dss-setup"></a>

## 4. DSS setup

ADLS gen 2 is only supported from Hadoop 3.2, jump to the [install with hadoop 3](#4-2-dss-setup-hadoop-3) section if you need to enable it 


<a name="4-1-dss-setup-hadoop-2"></a>

### 4.1 Install with Hadoop 2 (does NOT support ADLS gen 2)

* Install DSS normally
* On the DSS machine, download a Spark 2.3 with Hadoop distribution, and unzip it
* On the DSS machine, download ```dataiku-dss-hadoop-standalone-libs-databricks-X.Y.Z.tar.gz``` from the DSS download site
* Run

    ```
    ./bin/dssadmin install-hadoop-integration -standalone databricks \
                -standaloneArchive /path/to/dataiku-dss-hadoop-standalone-libs-databricks.X.Y.Z.tar.gz
    ```

* Run

    ```
    ./bin/dssadmin install-spark-integration -sparkHome /path/to/spark-2.3.X-bin-hadoop2.7
    ```

* Download the Spark JDBC driver from Databricks and copy the ```SparkJDBC41.jar``` file to the ```lib/jdbc``` folder of DSS

* Edit the ```bin/env-site.sh```, and add a line:
	```
	export DKU_BACKEND_EXT_HOST=xxx.yyy.zzz.ttt
	```

	where xxx.yyy.zzz.ttt is the private IP address of the DSS machine itself

* Start DSS
* In DSS, create a Azure Blob Storage connection. Enter your storage account name, and the access key of your storage account. You don't need to enter any other setting
* In DSS, go to Administration > Settings > Spark
* Enable Databricks support
* Fill-in your Databricks URL (```https://YOUR-REGION.azuredatabricks.net```) and your Databricks API token
* In "Conn. for resources upload", enter the name of the Blob Storage connection you just created
* In "bucket for resources upload", enter "your-storage-container"
* In "Bucket DBFS mount point", use "your-path-within-the-container" (or / if empty)
* In "Mount point in DBFS", use "mount-point-in-databricks"
* In "Interactive SparkSQL", set "Execution mode" to "Databricks"
* In "Default configuration for recipes", set "Default engine (recipes)" to "Databricks"
* For each named Spark configuration, set the "instance type" to the type of Azure instance you want to use. You may want to configure additional settings in the "Databricks cluster definition", like "custom_tags". The "Databricks cluster definition" follows the schema fo the ["Create cluster" API call in Databricks](https://docs.azuredatabricks.net/api/latest/clusters.html#create)

<a name="4-2-dss-setup-hadoop-3"></a>

### 4.2 Install with Hadoop 3 (supports ADLS gen 2)

* Install DSS normally
* On the DSS machine, download a Spark 2.3 with Hadoop distribution, and unzip it
* On the DSS machine, download ```dataiku-dss-hadoop3-standalone-libs-databricks-X.Y.Z.tar.gz``` from the DSS download site
* Run

    ```
    ./bin/dssadmin install-hadoop-integration -standalone databricks-hadoop3 \
                -standaloneArchive /path/to/dataiku-dss-hadoop3-standalone-libs-databricks-hadoop3.X.Y.Z.tar.gz
    ```

* Run

    ```
    ./bin/dssadmin install-spark-integration -sparkHome /path/to/spark-2.3.X-bin-hadoop2.7
    ```

* Download the Spark JDBC driver from Databricks and copy the ```SparkJDBC41.jar``` file to the ```lib/jdbc``` folder of DSS

* Edit the ```bin/env-site.sh```, and add a line:
        ```
        export DKU_BACKEND_EXT_HOST=xxx.yyy.zzz.ttt
        ```

        where xxx.yyy.zzz.ttt is the private IP address of the DSS machine itself

* Start DSS
* In DSS, create a Azure Blob Storage connection. Enter your storage account name, and the access key of your storage account. You don't need to enter any other setting
* In DSS, go to Administration > Settings > Spark
* Enable Databricks support
* Fill-in your Databricks URL (```https://YOUR-REGION.azuredatabricks.net```) and your Databricks API token
* In "Conn. for resources upload", enter the name of the Blob Storage connection you just created
* In "bucket for resources upload", enter "your-storage-container"
* In "Bucket DBFS mount point", use "your-path-within-the-container" (or / if empty)
* In "Mount point in DBFS", use "mount-point-in-databricks"
* In "Interactive SparkSQL", set "Execution mode" to "Databricks"
* In "Default configuration for recipes", set "Default engine (recipes)" to "Databricks"
* For each named Spark configuration, set the "instance type" to the type of Azure instance you want to use. You may want to configure additional settings in the "Databricks cluster definition", like "custom_tags". The "Databricks cluster definition" follows the schema fo the ["Create cluster" API call in Databricks](https://docs.azuredatabricks.net/api/latest/clusters.html#create)


<a name="5-connect-wasb"></a>

## 5. Connect to Azure Blob Storage

It is strongly recommended to access Azure Blob Storage data through a HDFS connection. We recommend that you use Shared Access Signatures rather than access keys (although access keys are also possible of course).

In DSS:

* Create a new HDFS connection
* Use ```wasbs://your-storage-container@your-storage-account.blob.core.windows.net/path-within-container``` as the HDFS URL
* Add the following properties
    ```
    fs.azure.sas.your-storage-container.your-storage-account.blob.core.windows.net = YOUR_SAS_TOKEN
    ```


<a name="6-connect-adls1"></a>

## 6. Connect to ADLS gen1

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
    dfs.adls.oauth2.access.token.provider.type = ClientCredential
    dfs.adls.oauth2.refresh.url = THE_TOKEN_ENDPOINT (usually starts by https://login.windows.net)
    dfs.adls.oauth2.client.id = YOUR_CLIENT_ID
    dfs.adls.oauth2.credential = YOUR_CLIENT_SECRET
    ```

For other methods, refer to the Azure Datalake store Hadoop driver documentation. Similarly to the ClientCredential mode, you'll need to duplicate the ```fs.adl.*``` properties and put them also as ```dfs.adls.*```.

<a name="7-connect-adls2"></a>

## 7. Connect to ADLS gen2

ADLS gen2 is builtin as an HDFS filesytem starting Hadoop 3.2 (ABFS) 

* Create a new HDFS connection
* Use ```abfss://<your_file_system>@<your_storage_account_name>.dfs.core.windows.net/``` as the HDFS URL
* Add the following extra hadoop properties:

    ```
    fs.azure.account.key.<your_storage_account_name>.dfs.core.windows.net = YOUR_ACCESS_SECRET
    ```
