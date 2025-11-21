# Connecting to Cloudera CDP Public Cloud Data Hub clusters

Starting with version 10.0.5, DSS can integrate with Cloudera CDP Public Cloud Data Hub clusters, when installed on a cluster "gateway" node.

This note describes the supported configurations, and associated setup steps.

## 1. Supported configurations

The deployments described below have been validated against the following configurations:

* Azure- or AWS-based CDP environments
* CDP runtime versions 7.2.14 and 7.2.15
* CDP Data Lake configured with coarse-grained (identity mappings using Knox IDBroker)
  or fine-grained (Ranger RAZ) authorization models
* DSS datasets stored on CDP-integrated S3 buckets (for AWS environments) or ADLS Gen2 storage containers (for Azure environments)
* DSS connected to Hive, Spark 2 and/or Impala CDP-based compute engines
* DSS configured with UIF (User Isolation Framework, recommended) or not

Note that the "Data Engineering: Apache Spark3" Data Hub clusters provide version 3.2 of Spark, which is not yet supported by DSS at the time of 
writing. As such, these clusters cannot be used with DSS. It is expected that future versions of DSS add support for Spark 3.2 as well.

The CDP "Cloudera Data Engineering" (CDE) managed Spark service is not supported.

## 2. CDP identities

DSS uses a number of CDP identities, to run Unix processes on its local node, to submit tasks to the CDP Hadoop services, and to access Cloud-based datasets.

### 2.1 DSS service account

You need to identify a CDP service account (aka "Machine user") which will be used to run DSS itself.
This account should have the "EnvironmentUser" role in the enclosing CDP environment.

Retrieve a keytab for this machine user and environment, to configure DSS Kerberos-based Hadoop integration below.

### 2.2 UIF user accounts

If DSS is to be configured in User Isolation mode, you need to identify the CDP accounts under which DSS users will run jobs and access CDP-managed datasets and compute engines.

These accounts can be CDP user accounts, or CDP machine accounts, and should at least have the "EnvironmentUser" role in the CDP environment.

You will need to define one or several CDP group(s) identifying these CDP user accounts, to configure the UIF impersonation authorization list (`allowed_user_groups` key in the `security-config.ini` file).

## 3. DSS installation

### 3.1 DSS node

DSS must be installed on a CDP-managed "gateway" node of a Data Hub cluster, typically a dedicated one.

The easiest way to provision such a node is to use the Cloudera-provided "Data Engineering" cluster template, and configure a non-zero count for 
the "gateway" node group in the cluster definition.

Alternatively, if using a custom cluster template, make sure to define a node group with the required gateway roles, supporting the cluster services with which DSS needs to integrate, typically:

* `hdfs-GATEWAY-BASE`
* `hms-GATEWAY-BASE`
* `hive_on_tez-GATEWAY-BASE`
* `tez-GATEWAY-BASE`
* `spark_on_yarn-GATEWAY-BASE`
* `yarn-GATEWAY-BASE`

The node on which DSS will be installed should be configured with at least one 
persistent data volume, of a large enough size to hold the DSS installation and data 
directories. For performance reasons, it is strongly recommended to use SSD-based volumes
for this purpose.

### 3.2 DSS installation

Once the required gateway node is provisioned, log onto it, switch to the DSS machine account, and install DSS following the standard procedure:

* installation kit extraction
* base DSS installation (`installer.sh`)
* Hadoop integration, using the Kerberos keytab retrieved above
* (optional) Spark integration
* (optional) UIF integration

Make sure that all directories holding DSS components are hosted on the gateway node persistent data disk (typically: `/hadoopfs/fsX`), including:

* the DSS installation directory
* the DSS data directory
* the keytab file
* the DSS UIF security directory (which can be set with an option to `dssadmin install-impersonation`)

[AWS only] Add the following to `DSS_DATADIR/install.ini`, regenerate the DSS config and restart DSS:
```
  [javaopts]
  # value from HADOOP_OPTS in /etc/hive/conf/hadoop-env.sh
  hproxy.additional.opts = -Dorg.wildfly.openssl.path=/usr/lib64
```

### 3.3 DSS configuration

#### 3.3.1 User account mappings

When UIF is configured, DSS user accounts should be provisioned and mapped to the CDP user accounts defined above, for both Unix and Hadoop impersonation.

Any approach can be used for this, including integrating DSS with the same user account database as CDP itself.

#### 3.3.2 Cloud storage connections

DSS connections to cloud storage should be defined using the "Hadoop HDFS" connection type, in order to leverage the CDP-specific authorization mechanisms:

[AWS-based environments] Define connections to S3-based datasets with:

  - Connection type = Hadoop HDFS 
  - Root path URI = `s3a://BUCKET/PREFIX`
  - [UIF only] ACL sync mode = None

[Azure-based environments] Define connections to Azure-storage-based datasets with:

  - Connection type = Hadoop HDFS
  - Root path URI = `abfs://CONTAINER@STORAGE_ACCOUNT.dfs.core.windows.net/PREFIX`
  - [UIF only] ACL sync mode = None

*WARNING:*

> Native "Amazon S3" and "Azure Blob Storage" DSS connections to cloud storage can be defined, but would not leverage the CDP-provided 
> authentication and authorization mechanisms. In particular they would need standalone cloud credentials and cloud-level authorization.
> 
> Such native connections would typically not be used in a CDP-integrated DSS instance, except for simple input/output connections to external cloud
> storage buckets.

#### 3.3.3 Hive configuration

DSS connection to Hive should be defined with the following custom JDBC URL:
```
  jdbc:hive2://MASTER_HOST.cloudera.site:2181/${database}
    ;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2;retries=5
    ;sslTrustStore=/var/lib/cloudera-scm-agent/agent-cert/cm-auto-global_truststore.jks
    ;trustStorePassword=TRUSTSTORE_PASSWORD
    ;hive.server2.proxy.user=${hadoopUser}
```
where:

- this URL is derived from the default one found in the beeline configuration file
  (`/etc/hive/conf/beeline-site.xml`) and should be checked against that one
- the values for `MASTER_HOST` and `TRUSTSTORE_PASSWORD` above can be found in the beeline 
  configuration file.
- the URL above has been broken down in lines for legibility but should be entered as a 
  single line
- the last clause (`hive.server2.proxy.user`) is specific for UIF impersonation and should be 
  left out if UIF is not used

#### 3.3.4 (Optional) Impala configuration

Download, extract and install the Cloudera JDBC 4.1 Impala driver (`ImpalaJDBC41.jar`).

Configure the DSS connection to Impala as follows:

* Use Cloudera driver
* Auth = Kerberos
* Principal = `impala/_HOST@<DEFAULT_REALM>`
* Use SSL
* Truststore path = `/var/lib/cloudera-scm-agent/agent-cert/cm-auto-in_cluster_truststore.jks`
* Truststore passwd = *[value from `/etc/hive/conf/beeline-site.xml`]*
* Impala hosts = *[see Impala page on Data Hub Cloudera Manager]*

#### (Optional) Spark configuration

Spark settings should contain the following additional key, which declares the cloud-based filesystem(s) which Spark jobs are expected to access:

* [AWS environments] `spark.yarn.access.hadoopFileSystems` = `s3a://BUCKET`
* [Azure environments] `spark.yarn.access.hadoopFileSystems` = `abfs://CONTAINER@STORAGE_ACCOUNT.dfs.core.windows.net`


## 4. Cluster-level authorizations

DSS needs a number of authorizations to be defined at the cluster level (DataLake cluster manager, DataLake Ranger service or DataHub cluster 
manager).

### 4.1 [UIF only] Impersonation authorizations

If UIF is configured, the CDP user account used by DSS (referenced below as `srv_DSS`) needs to be authorized to impersonate the group(s) of CDP user accounts used by DSS users to access cluster data and services (referenced below as `DSSUSERS_GROUP`).

#### 4.1.1 [Coarse-grained authorization mode only] IDBroker impersonation

- Connect to the DataLake cluster manager
- Navigate to: Clusters / Knox / Configuration
- Search for `idbroker_kerberos_dt_proxyuser_block`
- Add the following two clauses (including double quotes):
  ```    
  "hadoop.proxyuser.srv_DSS.groups": "DSSUSERS_GROUP"
  "hadoop.proxyuser.srv_DSS.hosts": "*"
  ```
- Restart the Knox IDBroker process

#### 4.1.2 General Hadoop impersonation

- Connect to the DataHub manager
- Navigate to: Cluster / HDFS / Configuration
- Search for `core_site_safety_valve`
- Add the following two clauses:
  ```
  hadoop.proxyuser.srv_DSS.groups = DSSUSERS_GROUP
  hadoop.proxyuser.srv_DSS.hosts = *
  ```

#### 4.1.3 Impala impersonation (if used)

- Connect to the DataHub cluster manager
- Navigate to: Cluster / impala / Configuration
- Search for `impala_authorized_proxy`
- Add user- or group-based impersonation authorization clauses

#### 4.1.4 [Fine-grained authorization mode only] Ranger RAZ impersonation

- Connect to the DataHub cluster manager
- Navigate to: Clusters / Ranger Raz / Configuration
- Search for `ranger-raz-site.xml_role_safety_valve`
- Add the following two clauses:
  ```
  ranger.raz.proxyuser.srv_DSS.groups = DSSUSERS_GROUP
  ranger.raz.proxyuser.srv_DSS.hosts = *
  ```

When the above is complete, restart stale services on the DataHub Cluster Manager.

### 4.2 Data access authorizations

The following authorizations allow the DSS service account and impersonated user accounts to access cloud-based datasets through the CDP 
authorization layers:

#### 4.2.1 "Hadoop SQL" Ranger policies:

For each Hive/Impala database used by DSS users:

- configure a database-level rule granting the required accesses
- configure a URI-level rule granting the required accesses to the underlying cloud storage (`s3a://...` or `abfs://....`)

#### 4.2.2 [Fine-grained authorization mode only] "S3" or "ADLS" Ranger policies:

For each cloud-storage-based connection used by DSS users:

- configure a S3/ADLS rule granting the required accesses to cloud-based directories used by DSS datasets:
  - for the `srv_DSS`, `hive` and `impala` accounts
  - for the required DSS user account groups

- [AWS only] Spark jobs typically use staging directories located under the user's home directory in
  the target dataset bucket (`s3a://BUCKET/user/{USER}`), in order to leverage the specialized S3-specific output committers.
  
  If Spark is used, make sure that each user can access his home directory on each S3 bucket used by Spark jobs.
  - This is normally ensured by the "Default: User Home" Ranger rule for the default bucket of the DataLake.
  - If access to additional buckets is required, you can add them to this default rule, or create additional rules using the same model
  - Alternatively, you can adjust the Spark committer staging directories location through the appropriate Spark property

#### 4.2.3 [Coarse-grained authorization mode only] Native cloud-based authorizations:

In coarse-grained mode, the DSS service account and DSS user accounts are individually mapped to native cloud roles (for AWS) or managed identities (for Azure) through Knox IDBroker mapping rules defined at the CDP environment level.

You must make sure these native cloud identities have the required authorizations at the cloud level, to allow access to the files backing the DSS datasets.

[AWS only] Spark jobs typically use staging directories located under the user's home directory in the target dataset bucket (`s3a://BUCKET/user/{USER}`), in order to leverage the specialized S3-specific output committers.
- You must ensure these directories are accessible as well
- Alternatively, you can adjust the Spark committer staging directories location through the appropriate Spark property.

## 5. Handling DSS node reprovisioning

CDP cluster nodes, including the gateway node used by DSS, may be reprovisioned by CDP for maintenance or fault recovery operations.

The default reprovisioning sequence typically consists in:

- terminating the running instance and its system disk
- preserving any additional data disk
- recreating the instance from a new system disk
- reattaching any additional data disk
- restarting services on the reprovisioned node

In order for DSS to survive this operation, you should make sure that all DSS-related local storage on the node is hosted on a data disk,
ie in a file system mounted at `/hadoopfs/fsX` where X is the index of the local disk chosen for DSS. This includes:

- the DSS installation directory (`dataiku-dss-VERSION`)
- the DSS data directory
- [UIF only] the DSS security directory (the location of which can be chosen with an option to the `dssadmin install-impersonation` step)

Nevertheless, a number of system-related DSS files still need to reside on the root filesystem of the node, including:

- any additional system dependencies (OS-level packages) which would be needed for custom processing needs
- the system-level service definition which allows DSS to automatically start at boot time (installed by the DSS `install-boot.sh` script)
- when using UIF, the sudoer snippet file which authorizes DSS to run privileged operations (installed by the `dssadmin install-impersonation` step, and located in `/etc/sudoers.d`)

These files will be lost, and need to be reinstalled or regenerated after a reprovisioning of the DSS gateway node.

This can be done manually by logging onto the instance after reprovisioning and before restarting DSS, or automated by defining a custom CDP recipe to be run on the node as part of its provisioning.
