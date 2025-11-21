---
title: "Cloud Stacks: Disaster Recovery with Fleet Manager"
---

This section deals with disaster recovery using Fleet Manager (FM) following the fall of an availability zone in Azure or AWS.

# Azure
## Recover the FM instance
### Requirements
* FM is deployed in a region with availability zones
* FM snapshots are activated

### Procedure
* In Azure portal, open the resource group where FM is deployed and find the last snapshot of the FM data disk and note its resource ID
* In the same resource group, use the instance template to deploy a new FM instance
	* Reuse the region, Virtual Network, Subnet, Instance Identity
	* Provide the resource ID of the snapshot in the *Snapshot* field
* *Review + create*
* Wait for the FM machine to startup

## Recover DSS instances with FM
### Requirements
* FM is up and running
* DSS instances are deployed in a region with availability zones
* DSS snapshots are activated

### Procedure
* Enable feature flag on FM instance that will allow to create an instance from any snapshot:


	dku.fm.azure.instancecreatefromexternalsnapshot.enabled=true

* Restart your FM instance
* Create an API key for your user on the FM instance


	sudo su dataiku
	/data/dataiku/fmhome/bin/fmadmin create-personal-api-key {{yourUser}}

* Encode `keyId:keySecret` as Base64 to have your Basic Auth token
* Retrieve the information about the fallen DSS instance through the API


	curl --location 'https://{{fmUrl}}/api/public/tenants/main/instances/{{logicalInstanceIdFromFm}}' \
	--header 'Authorization: Basic {{basicAuth}}'

* Retrieve the snapshots taken for this instance through the API


	curl --location 'https://{{fmUrl}}/api/public/tenants/main/instances/{{logicalInstanceIdFromFm}}/snapshots' \
	--header 'Authorization: Basic {{basicAuth}}'

* Prepare a call to create a DSS instance with the information from the response


	curl --location 'https://{{fmUrl}}/api/public/tenants/main/instances' \
	--header 'Content-Type: application/json' \
	--header 'Authorization: Basic {{basicAuth}}' \
	--data-raw '{{dataRetrievedFromTheFallenInstance}}'

* In `data-raw` JSON:
	* change the `label` to differentiate the new machine from the old one
	* in `azureAvailabilityZone`, provide the number of an available availability zone
	* in `azureSnapshotId`, provide the ID of the last snapshot taken from the fallen DSS instance
* Create and provision the new instance

# AWS
## Recover the FM instance
### Requirements
* FM is deployed in a region with availability zones
* FM snapshots are activated

### Procedure
* In AWS console online, find the Cloudformation stack corresponding to the fallen FM instance
* Find the last snapshot corresponding to it and note its ID
* Create a new stack with new resources and use the instance template to deploy a new FM instance
	* Reuse the VPC, VPC CIDR
	* Use a subnet in an available availability zone
	* Provide the snapshot ID in the *(Optional) Restore from this Snapshot ID* field
* Create the stack and wait for its deployment
* Wait for the FM machine to startup

## Recover DSS instances with FM
### Requirements
* FM and DSS instances are deployed in a region with availability zones
* There are different subnets on multiple availability zones in the VPC
* FM is up and running
* DSS snapshots are activated

### Procedure
* In FM, create a new Virtual Network specifying the subnet from an available availability zone
* Enable feature flag on FM instance that will allow to create an instance from any snapshot:


	dku.fm.feature.awsinstancecreatefromexternalsnapshot.enabled=true

* Restart your FM instance
* Create an API key for your user on the FM instance


	sudo su dataiku
	/data/dataiku/fmhome/bin/fmadmin create-personal-api-key {{yourUser}}

* Encode `keyId:keySecret` as Base64 to have your Basic Auth token
* Retrieve the information about the fallen DSS instance through the API


	curl --location 'https://{{fmUrl}}/api/public/tenants/main/instances/{{logicalInstanceIdFromFm}}' \
	--header 'Authorization: Basic {{basicAuth}}'

* Retrieve the snapshots taken for this instance through the API


	curl --location 'https://{{fmUrl}}/api/public/tenants/main/instances/{{logicalInstanceIdFromFm}}/snapshots' \
	--header 'Authorization: Basic {{basicAuth}}'

* Prepare a request to create a DSS instance with the information from the response


	curl --location 'https://{{fmUrl}}/api/public/tenants/main/instances' \
	--header 'Content-Type: application/json' \
	--header 'Authorization: Basic {{basicAuth}}' \
	--data-raw '{{dataRetrievedFromTheFallenInstance}}'

* In `data-raw` JSON:
	* in `virtualNetworkId`, provide the ID of the newly created Virtual Network in FM
	* change the `label` to differentiate the new machine from the old one
	* in `awsSnapshotId`, provide the ID of the last snapshot taken from the fallen DSS instance
* Create and provision the new instance

## After availability zone recovery
* There is no automatic data reconciliation mechanism. Once the availability zone is back, the data recuperation can be done manually
* When restored, the fallen DSS instance will be able to communicate with FM again and thus be part of the fleet. It is up to the administrator to get the necessary data and then delete the fallen instances
