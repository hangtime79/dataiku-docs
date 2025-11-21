# HOWTO: configure a GCE instance as a DataProc edge node

  * [1. Overview](#1-overview)
  * [2. Procedure](#2-procedure)

<a name="1-overview"></a>

## 1. Overview

This document provides a procedure that allows you to setup a GCE instance so that it can be used as an "edge node" to one or multiple DataProc clusters.


This procedure has been tested with DataProc version 1.3.40-debian9.

### Pre-requisites

- You already have a DataProc cluster up and running, with root shell access to the master node.


<a name="1-overview"></a>

## 2. Procedure

### 2.1 GCE instance creation

Start a GCE instance that abides by the following rules:

* the Linux version must be the same as the one used in the target version of your DataProc cluster

* **Networking**: the instance must be in the same VPC as your cluster. Furthermore, TCP traffic on all ports should be allowed between the VM and the cluster nodes (you can achieve that by defining appropriate firewall rules.

* **OAuth access scopes**: the instance must have read/write access to the Google Cloud Storage API so that it can create (and interact) with the cluster's staging bucket.

### 2.2 Retrieve client libraries and config files from the DataProc master node

The next step is about installing the necessary client libraries and configuration on your edge node. 

In the case of DataProc, most of the client libraries can be installed directly as classical .deb packages using `apt`. However, some of them are compiled at cluster creation time, and thus must be directly fetched from the master node.

Fortunately, DataProc VMs provide environment variables that list all required components, including:

- deb repository lists
- GCS connector libraries
- Hadoop and Spark configuration files
- System-level environment variables

To retrieve all these elements, SSH to your master node and run the following commands:

```bash
# Retrieve and archive the client components
$ sudo tar -czvf /tmp/client-components.tgz /etc/environment /usr/lib/hadoop/lib/gcs-connector-*.jar /etc/apt/sources.list.d/*.list /etc/hadoop/conf/* /etc/hive/conf/* /etc/tez/*

# Make the archive readable by everyone
$ chmod a+r /tmp/client-components.tgz

# Export all GPG keys
$ sudo apt-key exportall > /tmp/trusted-keys
```

### 2.3 Setup the edge node

* SSH on your edge node and retrieve the `client-components.tgz` as well as the `trusted-keys` files from the master node (e.g. via SCP):

```bash
$ scp $CLUSTER_MASTER_NODE_IP:"/tmp/client-components.tgz /tmp/trusted-keys" /tmp
```

* Unpack the archive and specify `/` as the root directory for the operation:

```bash
$ tar -xzvf /tmp/client-components.tgz -C /
```

* Import the keys to the edge node's keyring:

```bash
$ sudo apt-key add /tmp/trusted-keys
```

* Update the list of apt repositories:

```bash
$ sudo apt update
```

**IMPORTANT**: After this operation you will need to log out and login again to refresh the environment variables.

* Install the packages listed in the newly created `$DATAPROC_COMMON_PACKAGES` environment variable, excluding anaconda and kerberos:

```bash
$ echo $DATAPROC_COMMON_PACKAGES | sed -e "s/anaconda//g" -e "s/kerberos//g" | xargs sudo apt --yes --force-yes install
```

Finally, create the following working directories and grant them proper permissions/ownership:

```bash
$ sudo mkdir -p /hadoop/ /hadoop/spark/work /hadoop/spark/tmp
$ sudo chmod 777 /hadoop/ /hadoop/spark/tmp /hadoop/spark/work
$ sudo chown -R spark /hadoop/spark
```

At that point, client connectivity to the cluster can be checked using the standard command line tools (`hdfs`, `yarn`, `hive`...).

### 2.4 Install and setup DSS

DSS install and integration with Hadoop and Spark can be setup using the standard procedure described in the reference documentation.

### Misc.

* If you want to use the Parquet format file, you will need to put additional libraries into the Hadoop classpath. To do so, if `$DKUINSTALLDIR` is the absolute path to your install dir, add the following line to `$DATADIR/bin/env-site.sh`:

    ```bash
    export DKU_HADOOP_CP="$DKU_HADOOP_CP:$DKUINSTALLDIR/lib/ivy/parquet-run/*"
    ```


