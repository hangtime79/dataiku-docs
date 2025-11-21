# HOWTO: Run Spark on Kubernetes on GCP (regular security)


**This document is mostly deprecated as of DSS 6.0 - Please refer to the reference architectures in the reference documentation**

<a name="1-overview"></a>

## 1. Overview

Since DSS 5.1.3 and Spark 2.4.0, it is possible to [run Spark recipes in a Kubernetes cluster](https://doc.dataiku.com/dss/latest/spark/kubernetes.html). This HOWTO documents the steps required to obtain a Spark-on-Kubernetes working setup in Google Cloud Platform (GCP), with the ability to read and write Hadoop files on Google Cloud Storage (GCS).

> **NOTE**: this is an experimental setup, Dataiku won't be able to provide support on it.

<a name="2-prerequisites"></a>

## 2. Pre-requisites and limitations

### 2.1 Pre-requisites

Before building the setup, you will need the following items:

#### DSS host

You need a Google Compute Engine (GCE) virtual machine running on a [supported Linux distribution](https://doc.dataiku.com/dss/latest/installation/requirements.html#linux) with:

* a configured UNIX user account (e.g. `dssuser`) that will manage DSS
* a local Docker daemon installed and configured so that `dssuser` can build images
* appropriate access scopes and IAM roles granted to the service account that owns the VM for pushing images to Google Artifact Registry (GAR) ([ext.doc](https://cloud.google.com/artifact-registry/docs/docker/authentication)).

#### Kubernetes cluster

You need a Google Kubernetes Engine (GKE) cluster up and running. The service account that owns the cluster must have the appropriate access scopes and IAM roles to:

* read and write data from/to GCS
* pull Docker images from GAR (set [this](https://cloud.google.com/artifact-registry/docs/access-control#grant) *only when the registry and the cluster don't belong to the same GCP project*).

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

- Install DSS version >= 5.1.3.

- Download the `dataiku-dss-hadoop-standalone-libs-generic-X.Y.Z.tar.gz` archive corresponding to your DSS version from the [DSS download website](https://cdn.downloads.dataiku.com/public/studio/).

- From your data directory, run the following command:

    ```bash
    bin/dssadmin install-hadoop-integration -standalone generic \
      -standaloneArchive /path/to/dataiku-dss-hadoop-standalone-libs-generic-X.Y.Z.tar.gz
    ```

### 3.2 Preparing the Spark distribution

- Download Spark >= 2.4.0 and unzip the archive 

- Create the following environment variables with the appropriate values:

    ```
    export SPARK_DIR=/path/to/unzipped-spark-dir
    export DSS_INSTALLDIR=/path/to/dss-installdir
    export GAR_REPOSITORY="<region>-docker.pkg.dev/<project-name>/<repository-name>"
    export DOCKER_TAG_SPARK="a-tag-for-spark-docker-images"
    ```
- Run the following commands:

    ```
    # Remove the Hadoop 2.7 JARs
    rm -f $SPARK_DIR/jars/hadoop-*2.7*

    # Remove httpcore and httpclient JARs
    rm -f $SPARK_DIR/jars/httpc*

    # Copy the Hadoop 2.8 + additional support JARs from DSS Hadoop libraries:
    cp $DSS_INSTALL_DIR/hadoop-standalone-libs/generic/hadoop-*2.8* $SPARK_DIR/jars
    cp $DSS_INSTALL_DIR/hadoop-standalone-libs/generic/htrace-core4-4.0.1-incubating.jar $SPARK_DIR/jars

    # Copy the Cloud Storage connector
    cp $DSS_INSTALL_DIR/hadoop-standalone-libs/generic/gcs-connector-hadoop2-latest.jar $SPARK_DIR/jars

    # Copy the snappy JAR (required to process compressed Parquet files)
    cp $DSS_INSTALL_DIR/lib/ivy/backend-run/snappy-java-1.0.5.jar $SPARK_DIR/jars

    ```

- Edit Spark's Dockerfile located in `$SPARK_DIR/kubernetes/dockerfiles/spark`:

    * after `ENV SPARK_HOME`, add the following line:
    ```
    ENV LD_LIBRARY_PATH /lib64
    ```

    * make sure that the `apk add ...` line matches the following:
    ```
    apk add --no-cache bash tini libc6-compat linux-pam nss && \
    ```

- Build and push the Docker images for Spark:

    ```
    $SPARK_DIR/bin/docker-image-tool.sh -r $GAR_REPOSITORY -t $DOCKER_TAG_SPARK build

    $SPARK_DIR/bin/docker-image-tool.sh -r $GAR_REPOSITORY -t $DOCKER_TAG_SPARK push
    ```

### 3.3 Setting up Spark integration in DSS

- Follow the [GCP documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl) to ensure that `dssuser` can access the cluster.

- Retrieve the URL of your cluster's kube-apiserver by running:

    ```
    kubectl config view --minify | grep server | cut -f 2- -d ":" | tr -d " "
    ```

- In your data directory, run:

    ```
    ./bin/dssadmin install-spark-integration -sparkHome $SPARK_DIR
    ```

- Start DSS.

- In DSS, go to Administration > Settings > Spark.

- Edit the `default` configuration to add the following keys:

    | Key    | Value         |
    |--------------|---------------|
    | `spark.master`         | `k8s://https://URL-OF-YOUR-APISERVER:443`    |
    | `spark.kubernetes.container.image` | `$GAR_REPOSITORY/spark:DOCKER_TAG_SPARK` |

    > **NOTE**: in the Spark config you have to write the actual values contained in the `$GAR_REPOSITORY` and `$DOCKER_TAG_SPARK` variables.

From here, you can already test your setup by running a recipe on Spark.

## 4. Connect to GCS

You can read/write data stored in Cloud Storage as Hadoop files by creating a proper HDFS connection in DSS.

- In GCP, make sure that the GCS bucket you use allows read/write operations to service accounts that resp. own the DSS host VM and the GKE cluster. 

- In DSS, create a new HDFS connection:
    * Use `gs://YOUR-BUCKET-NAME/` for the root path URI
    * Add the following extra Hadoop conf item:

        | Key | Value |
        |-----|-------|
        | `fs.AbstractFileSystem.gs.impl` | `com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS` |

## Troubleshooting


Verify that your setup is compliant with the following items:

  * the GCE VM hosting DSS has the "Read Write" access scope for the Storage API
  * the service account owning the GCE VM has sufficient rights to read/write into the GCS bucket linked to GAR. 

- `No Filesystem for Scheme: gs`: this means that the GCS connector JAR is missing from your classpath. 
    * on the DSS host, double-check that the GCS connector JAR is present in `$DSS_INSTALLDIR/hadoop-standalone-libs/generic`
    * if the issue happens when an executor pod tries to write to GCS, double-check that you've properly copied the GCS connector JAR to `$SPARK_DIR/jars` *before building and pushing the Docker images*.
