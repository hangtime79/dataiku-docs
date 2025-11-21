# Howto: Connect to Databricks on AWS

  * [1. Overview](#1-overview)
  * [2. Prerequisites](#2-prerequisites)
  * [3. Initial AWS and Databricks setup](#3-initial-aws-setup)
  * [4. DSS setup](#4-dss-setup)
  * [5. Connect to S3](#5-connect)

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

* DSS must be installed on a EC2 machine, in a VPC/subnet that has full connectivity to your Databricks subscription. The hostname of the EC2 machine must be resolvable from the Databricks clusters. This can be done by peering your own VPC to the VPC of the Databricks workers
* Your Databricks subscription must already be up
* You need an administrator account on your Databricks subscription
* You need administrative access to your AWS account in order to edit IAM settings

<a name="3-initial-aws-setup"></a>

## 3. Initial AWS/Databricks setup

During operation, DSS needs to upload various files that the Databricks clusters will use. In order to ensure a secure distribution of files, you need to setup a S3 space where DSS will have read/write access, and Databricks clusters will have read access.

This path can either be a full bucket, or a subpath in a bucket. In the rest of this section, these will be denoted as "your-s3-bucket" and "your-path-within-the-bucket".

### 3.1. Create AWS access

* If needed, create the "your-s3-bucket" S3 bucket.
* Create an IAM role that will get read-only access to the bucket.
    * Create a policy that grants read-only access to the bucket
    * Create a new IAM role
    * Use AWS service as role type and select EC2 as attached service
    * Attach the policy
    * Write down both the "role ARN" and the "instance profile ARN" for this "read-only IAM role"

* Grant to the IAM role that was used to create the Databricks subscription the "iam:PassRole" permission on the instance profile ARN. You will need to add this to the policy:
    
    ```
    {
        "Effect": "Allow",
        "Action": "iam:PassRole",
        "Resource": "arn:aws:iam::XXXX:role/YYY" /* Beware, here it is the role ARN, not the instance profile ARN */
    }
    ```


* Create an AWS user with a keypair, and attach a policy that grants full control to this bucket. Write down the keypair for this "read-write keypair"

### 3.2. Mount the access point in DBFS

* Go to your Databricks Admin Console
* Add an IAM role. Enter the "read-only IAM role" instance profile ARN. Give access to this IAM role to the Databricks user who will end up creating clusters
* Create a new Databricks cluster, with the IAM role assigned.
* Create a Python Databricks notebook attached to the cluster you just created
* Run the following command (for example ```mount-point-in-databricks``` could be ```dku-dbfs-resources```) :

    ```
    dbutils.fs.mount("s3a://your-s3-bucket/your-path-within-the-bucket", "/mnt/mount-point-in-databricks")
    ```

### 3.3. Create a Databricks access token

For the user who will end up creating clusters, create a Databricks access token and write it down

<a name="4-dss-setup"></a>

## 4. DSS setup


* Install DSS normally
* On the DSS machine, download a Spark 2.3 with Hadoop distribution, and unzip it
* On the DSS machine, download dataiku-dss-hadoop-standalone-libs-databricks-X.Y.Z.tar.gz from the DSS download site
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

* Start DSS
* In DSS, create a S3 connection. As access and secret key, use the "read-write keypair" you created earlier. You don't need to enter any other setting
* In DSS, go to Administration > Settings > Spark
* Enable Databricks support
* Fill-in your Databricks URL (https://dbc-XXXXXXX.cloud.databricks.com) and your Databricks API token
* In "Conn. for resources upload", enter the name of the S3 connection you just created
* In "bucket for resources upload", enter "your-s3-bucket"
* In "Bucket DBFS mount point", use "your-path-within-the-bucket" (or / if empty)
* In "Mount point in DBFS", use "mount-point-in-databricks"

* In "Interactive SparkSQL", set "Execution mode" to "Databricks"
* In "Default configuration for recipes", set "Default engine (recipes)" to "Databricks"
* In the "Runtime configurations" section, for each Spark configuration you want to use (you can start only with "default"), edit the Databricks cluster definition "Raw JSON conf" to add (this last setup grants to the created clusters read-only access to the resources folder)

    ```
    "aws_attributes": {
        "instance_profile_arn": "read-only IAM role ARN" /* Starts with arn:aws:iam:: */
    }
    ```

* You may want to configure additional settings in the "Databricks clustere definition", like "custom_tags". The "Databricks cluster definition" follows the schema fo the "Create cluster" API call in Databricks: https://docs.databricks.com/api/latest/clusters.html#create

<a name="5-connect"></a>

## 5. Connect to S3 data

It is strongly recommended to access S3 data through a HDFS connection, in order to benefit from full Parquet capabilities. In order to provide multiple independent access with differing permissions, you need to use access/secret key pairs

* Create a new HDFS connection
* Use ```s3a://the-bucket-you-want-to-connect-to``` as the HDFS URL
* Add the following properties (having to enter your keys twice is expected):

    ```
    fs.s3a.access.key = YOUR_AWS_ACCESS_KEY
    fs.s3a.secret.key = YOUR_AWS_SECRET_KEY
    fs.s3n.awsAccessKeyId = YOUR_AWS_ACCESS_KEY
    fs.s3n.awsSecretAccessKey = YOUR_AWS_SECRET_KEY
    ```

* Set the "Connection details readable by" so that your user groups can use the connection
