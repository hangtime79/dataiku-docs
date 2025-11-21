# Howto: High-Availability and Disaster Recovery on Azure

  * [1. Overview](#1-overview)
    + [1.1. Introduction](#11-introduction)
    + [1.2. Not covered](#12-notcovered)
  * [2. Intra-AZ HA with Azure Managed Disks](#2-intra-az-ha)
    + [2.1. Manual failover](#21-intra-az-ha-manual)
    + [2.2. Automated failover](#22-intra-az-ha-auto)
  * [3. Disaster recovery with Azure Managed Disks snapshots](#4-dr-ebs)
    + [3.1. Snapshot strategy](#41-dr-ebs-snapshot)
    + [3.2. Complete restore](#42-dr-ebs-complete)
    + [3.3. Partial restore](#43-dr-ebs-partial)
  * [4. Conclusion and recommended setup](#5-conclusion)

<a name="1-overview"></a>

## 1. Overview

<a name="11-introduction"></a>

### 1.1 Introduction

This document describe strategies for implementing disaster-recovery and failover / high-availability capabilities for the Dataiku DSS design and automation nodes, when running on Azure.

This document distinguishes the following capabilities:

* High-availability relates to the capacity of an application to remain functional even though some specific adverse event occurs. Failover is a means to achieve high-availability through switch of the active service from one node to another. Failover is the primary means to achieve high-availability for the Dataiku DSS design and automation nodes.

* Disaster-recovery relates to the capacity to recover an application in the face of a major failure or catastrophe that may result in the inability of the application to perform (even if HA is implemented). Backups are the main ways to implement disaster recovery.

Please note that this document does not apply to the API node, which implements high-availability through replication rather than through failover. In the rest of the documentation, "DSS instance" or "DSS node" shall mean "Dataiku DSS design or automation node".

This document does not discuss scalability. Scalability for a DSS instance is achieved primarily through leveraging execution engines that allow spreading of the load of a cluster (Hadoop, Spark, Kubernetes, distributed SQL databases, ...)

HA and DR are separate concepts, and the answers to both requirements are independent and separate. Notably, some HA scenarios are incompatible with some DR scenarios.

This document assumes familiarity with the following concepts: 

* Azure-specific: Azure VMs, Azure Managed Disks, Azure Managed Disks Snapshots, Azure Files, AZ (Availablilty Zone)
* Generic: RPO (Recovery Point Objective), RTO (Recovery Time Objective)

<a name="12-notcovered"></a>

### 1.2 What is not covered?

It is important to understand what kind of issues are covered or not by these different terms.

The HA setups described in this document are meant to provide ability to continue service in the face of the following adverse events:

* Hardware failure of the Azure VMs instance running the DSS instance
* Persistent system-level software failure of the Azure VMs instance running the DSS instance
* (For some setups) Complete failure of the Azure AZ running the DSS instance

The DR setups described in this document are meant to provide ability to recover in the face of the following adverse events:

* Failure and loss of data of the Azure Managed Disks hosting the DSS data dir
* (For some setups) User error or hostile activity leading to loss of the data in the DSS data dir

DR almost always comes associated with a specific RPO.

In particular, it is important to understand that the HA/failover scenarios described in this document are not meant to provide protection against:

* Temporary DSS software failures, bugs in DSS, hangs or any kind of transitory software non-responsiveness that are fixed by a restart of the software. While performing a failover in this kind of situation would be technically possible, it is almost never the right answer when a restart solves the situation. This is because a failover operation (whether manual or automated) will entail disruption to users that are at least as large than a restart. This kind of situation manifests itself by a zero RPO.

* Temporary system software failures that are fixed by a reboot of the machine. The rationale is essentially the same.

* Permanent DSS software failures, bugs in DSS, that cause an inability to restart the DSS software after a failure that left corrupted data in the DSS data directory. All DSS failover scenarios imply a data directory that is shared between the active and passive instances, such that a persistent corruption (either caused by a software bug or a hardware failure) would manifest similarly on the passive instance. This kind of situation can be prevented by an appropriate DR strategy with a non-zero RPO.

* User error or hostile activity leading to loss of data in the data sources. Protecting data sources against these (by appropriate backup and archiving strategies) is out of DSS scope. This kind of situation can be prevented by an appropriate DR strategy with a non-zero RPO.

<a name="2-intra-az-ha"></a>

# 2. Intra-AZ HA / failover with Azure Managed Disks

When running on a cloud provider, compute and storage are natively separated (between Azure VMs and Azure Managed Disks in the case of Azure). 

Furthermore, apart from an extreme data loss case (which is covered as part of DR, not HA), the storage (Azure Managed Disks) is assumed to be itself highly available.

The basic intra-AZ failover scenario for DSS is therefore based on:

* Shutting down a malfunctioning (either software or hardware) Azure VMs instance 
* Restarting another Azure VMs instance which reattaches to the same Azure Managed Disks containing the DSS data directory.
* Moving an IP or DNS entry to the new Azure VMs instance

<a name="21-intra-az-ha-manual"></a>

## 2.1 Manual failover

The basic scenario, and the scenario which Dataiku generally recommends is to be prepared for a failure with a plan that is manually implemented.

The plan must include:

* Monitoring that provides early alerting to administrators

* Decision criteria to trigger the failover plan. For example, unresponsiveness of the Azure VMs instance that is not correct after trying to restart the Azure VMs instance, or Azure indicating a failure of the instance.

* Procedure, which can be either fully manual or scripted, to perform the switch (bringing up the new Azure VMs instance, attaching the Azure Managed Disks, starting DSS, moving the IP / DNS entry)

### RPO / RTO

* This scenario provides full failover, therefore it comes with a null RPO
* RTO would usually lie in the 15-60 minutes range, depending on the speed of reaction. Since this is a manual failover scenario, this assumes that an administrator remains ready to execute the plan at any time.


<a name="22-intra-az-ha-auto"></a>

## 2.2 Automated failover

Automated failover relies on software monitoring to automatically detect the presence of a condition that should trigger the failover, and automatically executing it.

The difficulty of automated failover relies in being able to properly identify the condition, and distinguishing it from other kind of issues like network difficulties of the monitoring stack.

We recommend using Amazon CloudWatch to automate the detection and the execution of the failover. The details of the probes and scripts is outside the scope of this document.

### RPO / RTO

* This scenario provides full failover, therefore it comes with a null RPO
* RTO would usually lie in the 5-15 minutes range, and would not require admin presence.

The difficulty of the scenario lies in avoiding both false positive and false negatives. Given the trickiness of this and the expected low frequency of events that would require triggering a failover, we generally recommend to have careful planning and **stick to manual failover rather than implementing automated failover**.

<a name="4-dr-ebs"></a>

# 3. DR with Azure Managed Disks snapshots

The main tool of DR is backups. Restoring the latest backup provides you with a controlled RPO. Another very important aspect is the ability to *historize* backups. It is crucial to maintain several historical snapshots of your DSS data directory and to be able to use any of these previous snapshots.

This way, if a data loss (due to software issue, user error or hostile activity) remains undetected for a few days, you'll still have the ability to revert to an older snapshot from before the disaster. If you only keep a single backup, and the backup occurs before the issue is detected, the backup would also contain the data loss with no possibility of recovery.

The recommended way to perform historized backups on Azure is to use Azure Managed Disks snapshots.

Azure Managed Disks snapshots:

* Are fully consistent, so you can take a snapshot while DSS is running, with high confidence over restoration capabilities.
* Are virtually immediate
* Are very cheap
* Are available cross-AZ, so you can base a cross-AZ recovery capability on them

<a name="41-dr-ebs-snapshot"></a>

## 3.1. Snapshot history strategy

In order to provide a good balance between RPO and ability to recover from a failure that went undetected for some time, we recommend implementing a tiered snapshot strategy.

For example:

* Take a snapshot every hour
* Keep all snapshots that are less than 24 hours old. 
* For snapshots between 24 hours and one week ago, keep a snapshot every 12 hours
* For snapshots between one week ago, and 15 days ago, keep a snapshot every 24 hours
* Drop snapshots older than 15 days ago.

With this strategy, you are able to maintain a low RTO (one hour) in the case of a disaster that is noticed immediately, while maintaining a granular RPO (hour by hour) for recent disasters, and less granular in case a disaster remains unnoticed for a long time

<a name="42-dr-ebs-complete"></a>

## 3.2 Complete restore strategy

Restoring a complete data directory from a Azure Managed Disks snapshot is fairly similar to the manual failover procedure described above:

* Shut down the Azure VMs instance running DSS
* Restore the snapshot to a new Azure Managed Disks volume
* Create a new Azure VMs instance attaching this Azure Managed Disks volume
* Move an IP or DNS entry to this new Azure VMs instance

<a name="43-dr-ebs-partial"></a>

## 3.3. Partial restore strategy

In some cases (this will generally be indicated by Dataiku Support), it may be possible that only a small part of the DSS data directory was affected and needs to be restored.

In that case, you can simply mount the Azure Managed Disks snapshot as a new Azure Managed Disks volume on the main Azure VMs instance running DSS, and copy files over from this restored volume to the DSS data directory.

This will allow you to repair the disaster without having to go back in time for the rest of the data directory. Beware that restoring parts of the DSS data directory may lead to inconsistencies. Partial restores should generally be requested by Dataiku Support.

<a name="5-conclusion"></a>

## 4. Conclusion and recommended setup

Overall, given its good complexity / constraints / RPO and RTO characteristics, Dataiku recommends the following setup for HA and DR on Azure:

* Use intra-AZ failover based on Azure Managed Disks reattachment. Have a script or written procedure for failover and perform manual failover in case of failure. Regularly test your failover capability.

* Use DR based on historized Azure Managed Disks snapshots. Have a written procedure for recovery after disaster and perform manual disaster recovery in case of failure. Regularly test your recovery capability.
