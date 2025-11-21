# Connecting DSS to secure EMR clusters

  * [1. Overview](#1-overview)
  * [2. DSS installed on EMR cluster node](#2-cluster-node)
  * [3. DSS installed on an unmanaged cluster edge node](#3-edge-node)
  * [4. DSS connected to multiple secure EMR clusters](#4-multiple-clusters)

This application note discusses possible deployments of DSS connected to kerberized EMR clusters, and in particular possible
deployment scenarios of DSS in user isolation mode when connected to EMR clusters.

**Note:** Amazon EMR clusters can be deployed with a number of optional security features.
This note only discusses the following ones, which are relevant to DSS user isolation:

- mandatory: Kerberos authentication (<https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-kerberos.html>)
- optional: IAM Roles for EMRFS (<https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-emrfs-iam-roles.html>)

This application note has been validated with DSS 5.0 and EMR 5.19. Care should be exercised if applying these procedures to other 
versions.


<a name="1-overview"></a>

## 1. Overview

When installed in user isolation mode (<https://doc.dataiku.com/dss/latest/user-isolation/>), DSS can only 
connect to secure (ie kerberized) Hadoop clusters.

EMR clusters can be configured with Kerberos authentication using an option of the "security configuration" cluster creation 
parameter. Once this is done, DSS can connect to a kerberized EMR cluster using the standard procedure
(<https://doc.dataiku.com/dss/latest/hadoop/secure-clusters.html>) provided the standard prerequisites are met, in particular:

- the DSS host must be configured as a client of the same Kerberos realm as the cluster (or a Kerberos realm with a trust 
  relationship)
- DSS must be configured with a valid Kerberos account (principal), and a keytab file for this account
- the DSS Hadoop account must have a valid HDFS home directory on the default cluster filesystem
- the Unix account mapped to the DSS Hadoop account must exist on all cluster nodes

In addition, it is possible to configure user isolation on the DSS instance when the required additional prerequisites are met,
in particular:

- all DSS user accounts must have a matching Unix account on the DSS host, or be mapped to a valid Unix account through 
  impersonation mapping rules (<https://doc.dataiku.com/dss/latest/user-isolation/concepts.html#identity-mapping>)
- all DSS user accounts must have a matching Hadoop account, or be mapped to a valid Hadoop account through impersonation 
  mapping rules
- all Hadoop accounts for DSS users must have a valid HDFS home directory on the default cluster filesystem
- the Unix accounts mapped to the Hadoop accounts for DSS users must exist on all cluster nodes
- the DSS Hadoop account should be allowed to impersonate all Hadoop accounts for DSS users, through directives in `core-site.xml`.
  On EMR, these additional directives should be provided through a custom "Classification" option at the time of cluster creation.

However, the above does not address the fundamental use case of EMR clusters, where persistent datasets are stored on EMRFS
instead of HDFS, as EMRFS does not implement standard Hadoop filesystem security nor Hadoop impersonation. It does not address
multi-user Hive tablespace security either, as EMR does not come with Sentry nor Ranger (though Ranger can be added through a quite 
involved custom installation procedure).

Multi-user authorization for EMRFS can be configured with the "IAM Roles for EMRFS" security option to EMR. Using this option:

- a mapping from Hadoop user or group to IAM role can be configured at the time of cluster creation
- this mapping will be evaluated by the EMRFS client library at the time of access. In case of a match, the library code will then
  assume the corresponding IAM role when accessing EMRFS, which allows the IAM administrator to grant different effective rights to
  different Hadoop accounts with respect to accessing EMRFS-based datasets.
- this IAM role mapping is evaluated by all Hadoop processes running on EMR cluster nodes, including the HiveServer2 and Hive 
  metastore servers. Hive being configured with end-user impersonation and storage-based authorization on EMR clusters, this also 
  provides Hive tablespace authorization for Hive tables hosted on EMRFS buckets, through the access privileges granted to the 
  different IAM roles mapped to different Hadoop users.

**Important note:**

- The "IAM Roles for EMRFS" feature, being directly implemented by the EMRFS client library, does not offer strong security against
  a hostile user who can run arbitrary code on a cluster node, as this code could get access to the instances's underlying IAM 
  account, and use it to directly impersonate any other end-user IAM mapped role.
- In the context of DSS, this would include any Spark or Pyspark job running on the cluster, as well as any local Python/R recipe or
  notebook when DSS is directly installed on a cluster node.
- This limitation is further documented in an AWS blog post
  (<https://aws.amazon.com/blogs/big-data/best-practices-for-securing-amazon-emr/>).

This application note describes three possible patterns for deploying DSS in user isolation mode with EMR clusters:

- DSS installed on a cluster node, with optional EMRFS IAM mapping rules
- DSS installed on a manually attached (unmanaged) edge node, with optional EMRFS IAM mapping rules
- DSS connected to multiple kerberized EMR clusters, each runnning with optional EMRFS IAM mapping rules. Though this setup
  is quite more complex to deploy than the first two ones, it allows for strong security against privilege escalation through
  hostile code, at the inter-cluster level.


<a name="2-cluster-node"></a>

## 2. DSS installed on EMR cluster node

This deployment scenario is the simplest. In order to run DSS in user isolation mode, you need the following configuration
steps:

### 2.1 Planning

- Identify Unix and Hadoop accounts for the DSS service account, and all impersonated DSS users
- Identify required Unix and Hadoop groups for DSS impersonated users (for impersonation authorization, and any IAM-role-based 
  EMRFS authorization)
- Identify and create any required IAM roles for EMRFS authorization
- Identify and create the IAM instance role for cluster nodes, with authorization to assume the above roles if any

### 2.2 Cluster deployment

- Configure the cluster to use Kerberos authentication (either with a standalone Kerberos KDC or a cross-realm trust)
- Add custom Hadoop configuration keys to `core-site.xml`, authorizing the DSS Hadoop account to impersonate the Hadoop groups of 
  DSS users (this cannot be changed after cluster creation).
- Optionally, configure EMRFS IAM role mapping rules (this cannot be changed after cluster creation)

### 2.3 Cluster post-install steps

The following can be done manually, or as part of cluster creation (using EMR bootstrap actions or initialization steps):

- Create Unix accounts for DSS and all impersonated DSS user accounts (on all cluster nodes)
- Create Unix home directories for DSS and all impersonated DSS user accounts (on the DSS node)
- Create any required Unix group (on the DSS node)
- Create the DSS Kerberos account, extract a keytab for it on the DSS node
- Create HDFS home directories for the DSS Hadoop account and all DSS users impersonated Hadoop accounts

### 2.4 DSS installation

DSS can then be installed on the chosen EMR cluster node (typically: the master node) using the standard installation procedure:

- DSS base installation
- secure Hadoop integration
- Spark integration
- optional R integration
- user isolation configuration

### 2.5 Configuration of EMRFS connections

You can then configure one or several EMRFS connections in DSS as follows:

- use the *HDFS* connection type
- configure the *Root Path URI* to an EMRFS prefix, ie `s3://BUCKET_NAME/[OPTIONAL_PATH_PREFIX]`
- do not configure explicit connection-level AWS credentials (AWS authentication is inherited from the underlying IAM instance 
  role, potentially modified by EMRFS IAM role mapping rules if any)
- configure the Hive database and naming rules for new datasets as usual
- make sure the IAM role used by DSS (as defined by the EMRFS IAM role mapping rules) has read-write access to the configured EMRFS 
  prefix
- make sure the IAM roles used by all DSS users allowed to use this connection (after mapping to a Hadoop user through the DSS 
  identity mapping rules, then mapping to an IAM role through the EMRFS IAM role mapping rules) have read-write access to the 
  configured EMRFS prefix

**Warning:** as stated above, this mode does not offer strong security against a hostile user with respect to accessing EMRFS 
resources, as it is technically possible to override the EMRFS role mapping rules using custom Python or Spark code.


<a name="3-edge-node"></a>

## 3. DSS installed on an unmanaged cluster edge node

Another DSS application note (<https://doc.dataiku.com/app-notes/5.0/emr-edge-node/>) documents a non-officially-supported but
known-to-be-working procedure to attach an existing EC2 instance to an external, non-kerberized EMR cluster, so that DSS can be
installed on this instance and attached to this cluster.

The same procedure can be applied to attach an external EC2 instance as a client to a kerberized EMR cluster, provided that
the client instance is also configured as a Kerberos client to the same Kerberos realm as the cluster, ie:

- the Amazon Linux Kerberos client package must be installed on the client instance (`krb5-workstation`)
- the Kerberos client configuration file must be copied over from the master EMR node (`/etc/krb5.conf`)

Once that is done, the same procedure as described in the first scenario above can be used to install DSS on the client instance, 
and enable user isolation on it.

Any EMRFS IAM role mapping rules configured on the EMR cluster will also apply to processes running on the DSS host, as these are 
taken from Hadoop configuration key `fs.s3.authorization.roleMapping` in file `/usr/share/aws/emr/emrfs/conf/emrfs-site.xml`, which 
should have been copied over to the DSS node as part of the client attachment procedure.

The DSS EC2 instance must be assigned an IAM role with all required privileges, and in particular must be authorized to assume the 
different IAM roles defined by the EMRFS IAM role mapping rules. This is typically done with an IAM policy containing statements 
similar to:

    {
        "Effect": "Allow",
        "Action": "iam:AssumeRole",
        "Resource": [
            "arn:aws:iam::<ACCOUNT_ID>:role/<IMPERSONATED_ROLE_NAME>",
            "arn:aws:iam::<ACCOUNT_ID>:role/<IMPERSONATED_ROLE_NAME>",
            ...
        ]
    }

**Warning:** as above, this mode does not offer strong security against a hostile user with respect to accessing EMRFS resources, 
as it is technically possible to override the EMRFS role mapping rules using custom Python or Spark code.


<a name="4-multiple-clusters"></a>

## 4. DSS connected to multiple secure EMR clusters

Both deployment templates described above cannot enforce strong security against hostile users allowed to inject and execute 
untrusted code on a host where EMRFS IAM mapping rules are defined (using e.g. Python or Spark), as the current implementation of 
this mechanism requires the underlying privileged IAM role (allowed to impersonate less-privileged end-user IAM roles) be 
accessible to user code, which could then use it in unintended ways.

It is nevertheless possible to ensure strong security at a coarse (cluster-level) granularity by attaching a user isolation-
enabled DSS instance to multiple EMR clusters, making sure each cluster has only access to a subset of the EMRFS data lake, and 
configuring DSS to restrict access to each cluster to a chosen subset of users.

This setup is obviously more complex than the two previously described ones. Its important points are the following:

- processes running on the DSS host must be able to authenticate to kerberized services on all EMR clusters. In practice, this 
  means that all EMR clusters must be configured with a cross-realm trust to a common Kerberos realm, and that DSS itself must be 
  attached to this common Kerberos realm
- EMRFS IAM role mapping cannot be used on the DSS host itself (as this would be insecure). Instead, EMRFS access control should be 
  done by defining multiple EMRFS connections in DSS, with AWS credentials defined in connection-level Hadoop configuration keys, 
  and DSS-level authorization rules restricting access to these connections to authorized users only.
- for convenience, it is still possible to configure EMRFS IAM role mapping rules at the level of each EMR cluster, keeping in mind 
  that these do not offer strong security against hostile users running on the same cluster. In this model, strong security is at 
  the cluster level only.

A detailed setup procedure for this deployment model would be outside the scope of this application note, but can be obtained by 
putting together setup steps from the previously described procedure, and standard steps for DSS multicluster connectivity.
An outline of this procedure is given below:

### 4.1. DSS base setup

- start a standalone EC2 instance suitable for client attachment to an EMR cluster. For example, this could be an instance of the
  suitable Dataiku-provided `dataiku-emrclient-5.XX` EMR client AMI
- configure or locate a master Kerberos domain controler. This could be an externally-available Microsoft Active Directory domain 
  controler, or a local KDC running on the DSS EC2 instance
- configure the DSS EC2 instance as a Kerberos client to this master domain controler. Create all required accounts and principals 
  into it, including the cross-realm principals for each trusting EMR cluster
- install DSS on this EC2 instance, configure Hadoop and Spark integration, configure user isolation

### 4.2 Cluster setup:

For each required EMR cluster:

- create the cluster with a cross-realm trust to the master Kerberos realm
- make sure the IAM role assigned to the cluster hosts only allows access to EMRFS resources belonging to the associated security 
  tenant
- if you configured EMRFS IAM mapping rules for this cluster, make sure all accessible mapped roles only allow access to EMRFS 
  resources belonging to the associated security tenant
- build a cluster definition in DSS for this EMR cluster, and restrict access to this cluster definition to DSS groups authorized 
  to the associated security tenant
- build one or several EMRFS connection definitions in DSS for the datasets to be accessed by this cluster, with embedded AWS 
  credentials, and restrict access to these connections to DSS groups authorized to the associated security tenant.

With such a setup:

- DSS-level user isolation ensures that (non-admin) DSS users only have access to EMRFS connections in their security tenant, 
  and can only submit jobs to clusters in their security tenant
- jobs running on a cluster only have access to EMRFS resources in the associated security tenant based on the EC2 instance role 
  for cluster members defined at cluster creation
