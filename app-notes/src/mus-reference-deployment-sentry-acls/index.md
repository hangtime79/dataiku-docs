# MUS Reference deployment: Sentry ACLs synchronization

**This document is now superseded by the reference documentation**

  * [1. Basic assumptions and concepts](#1-intro)
  * [2. Setup](#2-setup)
  * [3. Possible deployments](#3-deployments)
  * [4. Test](#4-test)


When running on Cloudera, a possible deployment mode for user isolation is to leverage the ability of Sentry to synchronize ACLs defined at the database and table levels to HDFS ACLs. In that situation, the builtin HDFS ACLs synchronization mechanism of DSS is disabled.

This document is a broad description of a deployment model of DSS user isolation in a Cloudera environment, where HDFS authorization is handled by Sentry (through HDFS ACLs synchronization) rather than DSS-managed HDFS ACLs.

This model centralizes both HDFS and Hive tablespace authorization in Sentry rules, under control of the Hadoop administrator, instead of having Hive authorization managed by Sentry and HDFS authorization delegated to DSS.

The two main advantages of this deployment model are:

* Centralized authorization in Sentry rather than requiring managing Sentry rules in addition to the HDFS ACLs.
* For some customer deployments, working around limitations in number of HDFS ACLs (the default DSS-managed ACLs require a larger number of ACLs per path, which can overflow the limit to 32 ACLs per path in HDFS).

<a name="1-intro"></a>

## 1. Basic assumptions and concepts

In this model (as in the default DSS-managed-ACLs one btw) the security boundary is that of the Hive database.
There should be at least one Hive database per security tenant (ie set of different authorization rules).
Within a given Hive database, all tables (and thus all DSS datasets) have by default the same authorization
rules as the database itself.

In this model, each Hive database maps to a base directory of the HDFS filesystem. All datasets within this database are stored into a subdirectory of this base directory.

Authorization rules are defined in Sentry at the database level, and cover both Hive tablespace access and HDFS access (through Sentry HDFS ACLs synchronization).

DSS HDFS connections can be set up to map DSS projects to these security tenants in several ways, depending on the
application constraints, in particular:

* one DSS connection per tenant
* several tenants per connection, multiple projects per security tenant

<a name="2-setup"></a>

## 2. Setup

* Make sure the cluster is set up for Sentry HDFS ACLs synchronization (refer to Cloudera documentation - this is
normally the default for secure Cloudera clusters with Sentry)

* Create one or several root directories for DSS output directories. 

* Add these directories (or a parent of those) to the ```sentry.hdfs.integration.path.prefixes```
  Hadoop configuration key. Restart HDFS after changes to the latter.

    The net effect of this operation is that permissions within these directories will be dynamically overriden
    by HDFS to match Sentry authorization rules, whenever there is a matching Hive definition (database or table).

* For each Hive database which you want DSS to use:

    * create the database in HiveServer2 with a location at or inside one of the Sentry-managed directories:

        ```
        beeline> CREATE DATABASE <db_name> LOCATION 'hdfs://<namenode>/<path_to_dir>';
        ```

        Note : you will need to either create this dir first and give user "hive" write access to it or to give user "hive" write access to its parent so hive can create it
    
    * grant access to both database and underlying directory to both the DSS account and those DSS user groups which should be authorized to use it:

        ```
        beeline> GRANT ALL ON DATABASE <db_name> TO ROLE <dss_service_account_role>;
        beeline> GRANT ALL ON DATABASE <db_name> TO ROLE <some_dss_users_role>, ...;
        beeline> GRANT ALL ON URI 'hdfs://<namenode>/<path_to_dir>' TO ROLE <dss_service_account_role>;
        beeline> GRANT ALL ON URI 'hdfs://<namenode>/<path_to_dir>' TO ROLE <some_dss_users_role>, ...;
        ```

* Configure DSS managed HDFS connection(s) so that:
  
    * Hive database for datasets map to one of the databases defined above
    * HDFS paths for datasets map to the matching location for this database
    * Management of HDFS ACLs by DSS is turned off (ACL synchronization mode: None)

<a name="3-deployments"></a>

## 3. Possible deployments

There are several possible deployments of the above model, depending on the desired authorization and management 
model:

## 3.1: One DSS connection per database:
  
* directly configure the database name in "Hive database"
* add the DSS project key to the table names, as in : "Hive table name prefix" = ```${projectKey}_```
* root path URI : path to database directory
* Path prefix: ```${projectKey}/```
* optionally, you can restrict access to this DSS connection to its authorized DSS users, so the other ones do not see it at all

## 3.2: One database per DSS project, multiple databases per DSS connection

* Embed the DSS project key the Hive database name, as in: "Hive database" = ```dataiku_${projectKey}```
* Hive table name prefix can then be empty
* Root path URI must be a common parent to all database directories
* Embed the DSS project key in the HDFS path prefix, as in: "Path prefix" = ```${projectKey}/```
* You need to create each database using the above command sequence from an admin account (see 2.) when
   creating a DSS project

## 3.3: More complex setups

More complex setups are possible using per-project variables, typically representing the security tenant to
use for a given project, and expanding these variables in the database name or path prefix

<a name="4-test"></a>

# 4. Test

The setup above can be tested by:

* creating a DSS project and matching Hive database
* building a HDFS dataset in it
* checking the generated HDFS file permissions with ```hdfs dfs -getfacl <DATASET_PATH>```. These permissions should exactly match the Sentry rules defined for this database 
* test that HDFS-to-HDFS DSS recipes correctly work with all available backends (DSS, HiveServer2, Spark, Impala)
