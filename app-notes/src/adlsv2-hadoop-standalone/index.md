# Howto: Connect to ADLS gen2 and ADLS gen1 with Hadoop Standalone (no spark)

  * [1. Overview](#1-overview)
  * [2. Prerequisites and limitations](#2-prerequisites)
  * [3. Add Hadoop3 standalone capabilities to DSS](#3-hadoop-standalone)
  * [4. ADLS gen2 Connection Setup](#4-ADLSv2-connection-setup)
  * [5. ADLS gen1 Connection Setup](#5-ADLSv1-connection-setup)
  * [6. Test ADLS connection](#6-test-connection)

 **This document is only if you want to connect to ADLS gen1 / gen2 without having Spark or a Hadoop cluster or Kubernetes. Else, refer to the reference architectures. This document is mostly deprecated as of DSS 6.0**


<a name="1-overview"></a>

## 1. Overview


DSS can come with a light hadoop standalone that DSS will load at runtime.

Access to ADLSv1 and ADLSv2 is then performed via the HDFS abstraction.
Hadoop3 is the must go technology to support ADLSv2, hence the following will describe how to intergrate DSS with hadoop3 standalone mode and configure both ADLSv2 and ADLSv1 accesses

The access described here is done using Client keys, other methods of authentication have not been validated

<a name="2-prerequisites"></a>

## 2. Prerequisites and limitations

* You will need DSS 5.1.6 or higher, the setting may work with earlier versions but has not been tested.
* This configuration MUST NOT be applied if you already have a DSS integrated with an existing Hadoop stack
* The setup has NOT been validated for a MUS enabled instance
* This setup is NOT intended to be used with Spark, ADLSv1 data will be streamed and processed locally in DSS

<a name="3-hadoop-standalone"></a>

## 3. Add Hadoop3 standalone capabilities to DSS


- Log in via SSH to the DSS VM and sudo as the unix dataiku user
- Download the DSS standalone hadoop package on to the DSS VM:
```
wget https://cdn.downloads.dataiku.com/public/studio/X.Y.Z/dataiku-dss-hadoop3-standalone-libs-generic-X.Y.Z.tar.gz
```
where X.Y.Z is your DSS version
- Stop DSS
- Run the hadoop standalone integration
```
./bin/dssadmin install-hadoop-integration -standalone generic-hadoop3 -standaloneArchive /path/to/dataiku-dss-hadoop3-standalone-libs-generic.X.Y.Z.tar.gz
```

- Start DSS

<a name="4-ADLSv2-connection-setup">

## 4. ADLSv2 Connection Setup

- log into DSS as a DSS admin
- Go to Administration -> Connection -> New connection -> Hadoop HDFS
- Give the connection a name (for instance "myadlsgen2storage")
- Enter your root path URI:
``abfss://<fileSystem_name>@<Account Name>.dfs.core.windows.net/``

Where ``<fileSystem_name>`` is the name of the filesystem created via Azure console in the storage account and ``<Account Name>`` the storage account name

- In the extra hadoop conf add the properties:
```
fs.azure.account.key.<Account Name>.dfs.core.windows.net -> <the_storage_account_secret_key>
```
- click Save

<a name="5-ADLSv1-connection-setup">

## 5. ADLSv1 Connection Setup

### 5.1 Create an Azure Service Principal


You can skip this part if you already have a Service Principal (app registration) that has Owner role on the ADLS storage. In this case simply reuse the required credentials

Note: you must have elevated privileges in the Azure Active Directory to perform this operation

- Go to your portal.azure.com
- Switch to the Active Directory where the ADLS storage is configured
- Click on Azure Active Directory in the left panel
- Go to "App registration"
- Create a new one, you will be automatically redirected to the app view
- in the app view go to "Certificates & Secrets"
- in the Client Secrets section click "New client secrets"
- choose the expiration time, give it a name and click "Add"
- **IMPORTANT**: copy the value of the client secret (it will not be displayed anymore if you leave the page) and write it down, this will be your ``fs.adl.oauth2.credential`` value
- Go to Overview in the app view and write down the Application (client) ID, this will be your ``fs.adl.oauth2.client.id`` value
- In the same Overview tab of the app view, click "Endpoints" and copy down the Oauth 2 token endpoint (v1), this will be your ``fs.adl.oauth2.refresh.url`` value

Note: it is important you choose v1 and not v2

Now that you have a Service Principal ready you should give him Owner permission on the ADLS storage resource

- Go to the ADLS storage resource you want to access
- Click on "Access Control (IAM)" then Add -> Add role assignments
- Select role "Owner" and select your previously created app from the list of AD user  then "Save"


### 5.2 Configure HDFS over ADLSv1 connection


- log into DSS as a DSS admin
- Go to Administration -> Connection -> New connection -> Hadoop HDFS
- Give the connection a name (for instance "myadlsgen1storage")
- Enter your root path URI:
``adl://<Account Name>.azuredatalakestore.net/``

Where ``<Account Name>`` is your ADLS storage account name

- In the extra hadoop conf add the properties:
```
fs.adl.oauth2.client.id -> <the_client_id_your_wrote_down_previously>
fs.adl.oauth2.credential -> <the_client_secret_your_wrote_down_previously>
fs.adl.oauth2.refresh.url -> <the_refresh_url_your_wrote_down_previously>
fs.adl.oauth2.access.token.provider.type -> ClientCredential
```
- click Save

<a name="6-test-connection"></a>

# 6. Test the connections

- Go to a project (whatever) and create a new HDFS dataset
- Select the HDFS connection pointing at your ADLSv1 or ADLSv2 storage
- clic Test and / or browse to the desired folder to create your dataset

