# Howto: Configure an Azure instance as a HDInsight edge node

  * [1. Overview](#1-overview)
  * [2. Procedure](#2-procedure)

**HDInsight support is deprecated in DSS and will soon be removed. You should probably not be doing a new setup with HDInsight**

<a name="1-overview"></a>

## 1. Overview

Please first get familiar with the documentation on using HDInsight with DSS (<https://doc.dataiku.com/dss/latest/hadoop/distributions/hdinsight.html>)

This document provides a procedure that allows you to setup an Azure instance so that it can be used as an "edge node" to one or multiple HDInsight clusters.

Important note: This operation is not officially documented by Microsoft nor officially supported by Dataiku. To the best of our knowledge, this procedure is complete and there are no known issues with it at the time of writing. Furthermore, several customers currently use this kind of setup. It is however not part of the official DSS reference documentation.

This procedure has been tested with:

* HDI 3.6 / Spark 2.1 non-secured clusters
* HDI 3.6 / Spark 2.2 non-secured clusters
* HDI 3.6 / Spark 2.3 non-secured clusters
* HDI 4.0 / Spark 2.4 non-secured clusters

This procedure assumes good familiarity with Azure, Linux administration and Hadoop. It assumes that you already have an HDInsight cluster up and running, with SSH access to the head node.

<a name="2-procedure"></a>

# 2. Procedure

## 2.1: Initial setup

* create an Azure VM in the same vnet as the HDI cluster, using the same OS as HDI: Ubuntu 16.04

* copy the HDP repo files from a cluster node to the edge VM:

    ```
    /etc/apt/sources.list.d/HDP*.list
    ```

* install APT keys for Hortonworks and Microsoft

    ```
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 07513CAD 417A0893
    ```

- install Java and Hadoop client packages on the edge VM:

    ```
    apt-get update
    apt-get install \
        openjdk-8-jdk hadoop-client hive pig tez \
        spark2 spark2-python hadooplzo hadooplzo-native \
        libsnappy1 libssl-dev
    ```

- for HDI 3.x clusters only, install additional Hadoop client packages on the edge VM:

    ```
    apt-get install \
        hive2 tez-hive2-\* spark spark-python
    ```

* remove the initial set of Hadoop configuration directories

    ```
    rm -rf /etc/{hadoop,hive*,pig,spark*,tez*,zookeeper}/conf
    ```

* create a ssh keypair for the root account

* create a directory used by the HDInsight Spark config

    ```
    mkdir -p /var/log/sparkapp
    chmod 777 /var/log/sparkapp
    ```

* define the following environment variables (in `/etc/environment`, or `DSS_HOMEDIR/.profile`)

    ```
    AZURE_SPARK=1
    SPARK_MAJOR_VERSION=2
    PYSPARK_DRIVER_PYTHON=/usr/bin/python
    ```

## 2.2 Cluster association

* install the edge node ssh key on the head node (can be a non-privileged account on the head node side)

* copy the `/etc/hosts` definition for "headnodehost" from the head node to the edge node

* flush ssh key cache for headnodehost

    ```
    ssh-keygen -R headnodehost
    ```

* synchronize the following directories (as root on the edge node).

    ```
    rsync -a --delete USER@headnodehost:/etc/{hadoop,hive\*,pig,ranger\*,spark\*,tez\*,zookeeper} /etc/
    rsync -a --delete USER@headnodehost:/usr/lib/hdinsight\* /usr/lib/
    rsync -a --delete USER@headnodehost:/usr/hdp/ /usr/hdp/
    # A number of files and subdirectories in /usr/hdp and /etc/*/conf cannot be read from a non-privileged account,
    # these can be safely ignored.
    ```

* Recent versions of HDInsight configure JAVA_HOME to the Azul Zulu OpenJDK distribution, which is not available
  on the edge node. Change it to OpenJDK 8 instead:

    ```
    # Edit files:
    # /usr/hdp/current/hadoop-client/conf/hadoop-env.sh
    # /usr/hdp/current/spark-client/conf/spark-env.sh
    # /usr/hdp/current/spark2-client/conf/spark-env.sh
    # and set:
    export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
    ```

* (re-)run Hadop and Spark integration on DSS

* (re-)start DSS

## 2.3 Test

At that point, client connectivity to the cluster can be checked using the standard command line tools
(hdfs, yarn, hive, pyspark), and configured in DSS.
