# Connecting to MapR clusters in User Isolation mode

  * [1. Prerequisites and limitations](#1-prereq)
    + [1.1 Full control cluster privilege](#11-full-control)
    + [1.2 Compute engines](#12-engines)
    + [1.3 ACL support](#13-acl)
    + [1.4 Tickets renewal](#14-renewal)

  * [2. Deployment procedure](#deployment)
    + [2.1 Full control privilege](#21-full-control)
    + [2.1 Impersonating ticket](#22-ticket)
    + [2.3 DSS install](#23-install)
    + [2.4 MaprFS Security rules](#24-ace)
    + [2.4 Hive security](#25-hive)

Starting with version 4.3.3, DSS has partial support for connecting to secure MapR clusters in user isolation mode.

<a name="1-prereq"></a>

## 1. Prerequisites and limitations

In addition to the standard prerequisites which apply to running DSS in user isolation mode when connected
to Hadoop clusters, the following constraints must be met, and a number of features are not supported:


<a name="11-full-control"></a>

### 1.1 Full control cluster privilege

The DSS service account must have "full control" cluster privilege for Spark to work.

Due to a MapR limitation (delegation tokens not supported), DSS can only run impersonated Spark-based actions which access cluster resources when the DSS service account has been granted "full control" cluster privileges (ie cluster privileges equivalent to that of the standard "mapr" administrative account).

The security-related impact of this constraint should be carefully reviewed and considered acceptable for the target 
application environment. It implies in particular that the following category of users can directly or indirectly gain access to full cluster administrative privileges, and should be considered equivalent to MapR administrators from a security standpoint:

* all Unix users having access to the DSS Unix service account (including all local Unix administrators)
* all DSS users which are member of a DSS group with "DSS administrator" privilege
* all DSS users allowed to add non-impersonated local code to DSS, including members of DSS groups with one of the following global permissions:
    * "Write unsafe code"
    * "Manage all code envs"
    * "Manage own code envs"
    * "Develop plugins"
    * "Edit lib folders"

*WARNING: do not run DSS in user isolation mode in a MapR environment unless the above limitations are compatible with
your security constraints.*

<a name="12-engines"></a>

### 1.2 Unsupported compute engines

The following compute engines are not supported:

- Due to a MapR limitation (impersonation not supported), Impala is not supported in user isolation mode.
- The Map-Reduce backend is not supported for DSS preparation recipes.
- The "Hive CLI" backend is not supported for Hive-based recipes.

Lack of Impala support applies to:

* All visual recipes
* The Impala recipe
* Charts running on Impala
* Metrics running on Impala

<a name="13-acl"></a>

### 1.3 No HDFS access control lists

DSS does not support dynamic management of access control lists for files underlying datasets stored on MapR-FS
(as MapR-FS does not support standard HDFS access control lists).

It is nevertheless possible to define static user isolation rules on MapR-FS dataset connections, through 
MapR Access Control Expressions (ACEs) set up by the cluster administrator.

<a name="14-renewal"></a>

### 1.4 No renewal of impersonation tickets

Automatic renewal of impersonation tickets is not supported for Spark-based jobs.

In order for impersonated Spark jobs to be able to access cluster resources on behalf of the user, DSS uses its own
service ticket to issue a temporary MapR ticket for the user before starting the job, stores this ticket in a temporary 
file private to the user, and configures the job to authenticate to the cluster from this ticket file.

This temporary per-job MapR ticket has a fixed duration which is chosen at the time it is issued. As a consequence, 
impersonated DSS Spark jobs have a maximum lifetime which is that of this ticket, and would loose cluster access if still
running after this ticket has expired.

By default, DSS issues per-job tickets with a duration of 24 hours. This limit is globally configurable through a DSS 
configuration directive &mdash; choosing a shorter duration provides a better security against unauthorized uses or leaks of 
these temporary ticket files, while choosing a longer one allows running longer jobs.


<a name="deployment"></a>

## 2. Deployment procedure

The procedure to connect DSS to secure MapR clusters in user isolation mode is similar to the procedure to connect DSS to secure MapR in regular mode (<https://doc.dataiku.com/dss/latest/hadoop/distributions/mapr.html>),
with the following additions:

<a name="21-full-control"></a>

### 2.1 Grant "full cluster" privilege to the DSS service account

As described in the "prerequisite and limitations" section of this document, the MapR service account used by DSS should
be granted "full control" cluster privilege in order for impersonated Spark jobs to be possible.

This can be done through the MapR Control System graphical interface, or with the following command line run from a cluster
administrator account (typically, the "mapr" account) :

    maprcli acl edit -type cluster -user DSS_USER:fc

<a name="22-ticket"></a>

### 2.2 Create an impersonating service ticket for DSS instead of a regular service ticket

The service ticket used by DSS to authenticate to the cluster should have impersonation privileges.
To create this ticket, connect to a MapR administrator session, and issue the following command:

```
maprlogin generateticket -type servicewithimpersonation -user DSS_USER -out DSS_TICKET_FILE
```

As for the regular procedure, store this ticket in a location accessible, and private to, the DSS service account.

Note that it is still necessary to configure regular Hadoop impersonation authorization, through "proxyuser" Hadoop
configuration variables, declared in `core-site.xml`.

<a name="23-install"></a>

### 2.3 Install DSS and setup user isolation

You can then install DSS following the standard procedure for secure MapR clusters, and setup user isolation following the standard procedure.

Optionally, you can configure the duration of temporary per-job user tickets issued by DSS for Spark jobs, by adding the 
following directive to the DSS installation configuration file at ```DSS_DATADIR/install.ini```:

```
[mus]
mapr_ticket_duration = DURATION
```

The value for this variable should be a valid MapR duration argument, using format ```[Days:]Hours:Minutes```. The default value is `1:0:0`, ie one day.

<a name="24-ace"></a>

### 2.4 Configure MapR-FS security rules

You must set MapR access control expressions (ACEs) on all MapR-FS output directories used by DSS, which grant full 
recursive read-write-execute access to the DSS service account itself, and to all users allowed to write into this 
directory through DSS.

A typical example would be as follows. Considering:

- a DSS managed connection of type "HDFS" configured with a root path of `maprfs:///SOME_DIR_1`
- a DSS service account named `dataiku`
- a group of users named `dss_users_1` allowed to read and write into this connection

you would set the associated ACE on this root directory with:

```
hadoop mfs -setace \
  -readfile "u:dataiku | g:dss_users_1" \
  -writefile "u:dataiku | g:dss_users_1" \
  -executefile "u:dataiku | g:dss_users_1" \
  -addchild "u:dataiku | g:dss_users_1" \
  -deletechild "u:dataiku | g:dss_users_1" \
  -lookupdir "u:dataiku | g:dss_users_1" \
  -readdir "u:dataiku | g:dss_users_1" \
  -setinherit true \
  maprfs:///SOME_DIR_1
```

This example should of course be adapted to the particular security policy suitable for your deployment.
For finer access control, you can define several DSS connections, each with a custom ACE, or you can configure a given DSS  connection to have one subdirectory for each DSS project, and use different ACEs on subdirectories for different projects. 

Similarly, you should add read-only ACE entries for groups which should be granted read-only access to datasets.


<a name="25-hive"></a>

### 2.5 Hive tablespace security

HiveServer2 should be configured with impersonation enabled, and storage-based security on the Hive metastore (this is the  default for secure MapR clusters). In that mode, Hive tablespace security leverages the underlying MapR-FS security, so it automatically inherits the security rules defined by the filesystem ACEs above.

