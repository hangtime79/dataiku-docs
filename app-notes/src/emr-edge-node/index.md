# Howto: Configure an EC2 instance as an EMR edge node

  * [1. Overview](#1-overview)
  * [2. Procedure](#2-procedure)

<a name="1-overview"></a>

## 1. Overview

Please first get familiar with the documentation on using EMR with DSS: https://doc.dataiku.com/dss/latest/hadoop/distributions/emr.html

This document provides a procedure that allows you to setup an EC2 instance so that it can be used as an "edge node" to one or multiple EMR clusters.

This allows you to implement the "Connection to existing EMR clusters / DSS outside of the cluster" scenario. 

Note: This procedure also technically permits the "Let DSS dynamically manage one or several EMR clusters" scenario, however, for this latter scenario, we recommend that you preferably use the AMI that Dataiku provides to this effect, referenced in the "Dynamic EMR clusters" documentation page.

Important note: This operation is not officially documented by EMR nor officially supported by Dataiku. To the best of our knowledge, this procedure is complete and there are no known issues with it at the time of writing. Furthermore, several customers currently use this kind of setup. It is however not part of the official DSS reference documentation.

* This procedure has been tested with EMR 5.18 to 5.24, 5.29 and 5.30 (other 5.x versions may work but have not been verified)

* This procedure does not apply to EMR 6.x. At the time of writing, DSS does not support EMR 6.x.

* This procedure assumes good familiarity with AWS, AmazonLinux, cloud-init, yum and Hadoop.

* This procedure requires that you already have an EMR cluster up and running, with SSH access to the master node

<a name="2-procedure"></a>

# 2. Procedure

## Initial instance creation

* Start with an Amazon Linux instance with the same base version as the one used in the target version of EMR.
  This means Amazon Linux 2018.03 for EMR 5.18 to 5.29, and Amazon Linux 2 for EMR 5.30.

* Freeze the Amazon Linux version against updates by commenting out ```releasever=latest``` in ```/etc/yum.conf```

NB: it might be necessary to start the instance with a cloud-init stanza to disable the application of security
patches on first boot

```
    #cloud-config
    repo_upgrade: none
```

* Adjust the initial set of packages:

    - ```yum remove java-1.7.0-openjdk-\*    # Amazon Linux 2018.03 only```
	- ```yum install java-1.8.0-openjdk-devel R```
    - ```yum install python3    # Amazon Linux 2 only```

## Copy the repository

Copy the emr-apps repository definition from the EMR master, and its signing key:

* ```/etc/yum.repos.d/emr-apps.repo```
* ```/var/aws/emr/repoPublicKey.txt```

## Install packages

Install the following Hadoop and EMRFS packages (using yum):

```
    hadoop-client
    hadoop-lzo
    spark-core
    spark-python
    spark-R
    spark-datanucleus
    hive
    hive-hcatalog
    pig
    tez
    openssl-devel
    aws-hm-client
    emrfs
    emr-*
```

## Install Hive auxiliary libraries

Copy the following libraries from the EMR master, and symlink them into /usr/lib/hive/auxlib/ :

```
    /usr/share/aws/hmclient/lib/aws-glue-datacatalog-hive2-client.jar
    /usr/share/aws/emr/ddb/lib/emr-ddb-hive.jar
    /usr/share/aws/emr/goodies/lib/emr-hive-goodies.jar
    /usr/share/aws/emr/kinesis/lib/emr-kinesis-hive.jar
```

## Copy configuration

Copy the Hadoop and EMRFS configuration files from the EMR master (using scp / rsync):

``` 
    /etc/hadoop/conf
    /etc/hive/conf
    /etc/pig/conf
    /etc/spark/conf
    /etc/tez/conf
    /etc/zookeeper/conf
    /usr/share/aws/emr/emrfs/conf
    /usr/share/aws/emr/security     # If present - TLS certificates
```

## Create working directories

Create (mkdir -p) and allow write to (chmod 1777) the various scratch directories used by the EMR configuration
(this list may change a bit with EMR versions)

```
    /mnt/s3                    # fs.s3.buffer.dir
    /mnt1/s3                   # fs.s3.buffer.dir
    /mnt/var/lib/hadoop/tmp    # hadoop.tmp.dir
    /mnt/tmp                   # java.io.tmpdir
    /var/log/hive/user         # hive.log.dir
    /var/log/pig               # pig.logfile
```

## Miscellaneous configuration patches

Recent versions of EMRFS issue a number of warnings including a Java stack upon initialization, as they cannot read EMR configuration data from the local host.
These warnings can be ignored, and the Java stack may be suppressed by editing file ``/var/aws/emr/userData.json`` to contain an empty JSON object (``{}``).

Recent versions of EMR issue warnings on Spark startup due to a missing variable definition in the Spark Streaming logger. This can be shut off by commenting out
line ``log4j.logger.org.apache.spark.streaming`` in ``/etc/spark/conf/log4j.properties``.

## Test

At that point, client connectivity to the cluster can be checked using the standard command line tools
(hdfs, yarn, hive, pyspark).

## Setup DSS

DSS integration with Hadoop and Spark can be setup using the standard procedure.