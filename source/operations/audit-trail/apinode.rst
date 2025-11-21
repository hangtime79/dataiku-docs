Configuration for API nodes
#############################

A major use case for audit centralization is to centralize logs of API node queries in order to perform ML Ops activities on these logs (analyzing predictions, performing input data drift, or model performance drift).


Automatic configuration through API deployer
==============================================


The API deployer can automatically configure the audit dispatcher in the API nodes (both static and K8S infrastructures). This allows automatically configuring the API nodes so that they centralize their audit to a central DSS location.


Automatic send to event server
-------------------------------

At the infrastructure or deployment level, you define the URL of the event server, and its authentication key
At the deployment level, you define a routing key for this deployment. 

The API node will then dispatch all ``apinode-query`` audit events with this routing key to this event server, which will in turn by default write it into a folder-per-routing key, hence reaching our goal of having clean access to the logs of this API node only.


Sample setup: easy case
=========================

This sample setup shows you the easiest way to perform centralization of API node logs. Use this for as-simple-as-possible setup, when you don't need strong security around the logs of a service (i.e. it is not a problem if the engineers of Service1 can see the logs of Service2).

The main advantage of this setup is that no admin intervention is required when new API services are created and deployed. Admin intervention is only required once at install time.


Setup once (as admin)
----------------------

 * Install a design node, enable the EventServer on it
 * Add a "files in connection" target on the event server
    * Set topics filtering to ``apinode-query``
    * Set routing keys filtering to ``All``
    * Enable creation of subfolders
    * Select any compatible file-like connection like S3
 * In the API deployer infrastructure, enable "auto-configure reporting to event server", enter just the URL of the event server

For each service (as user)
-----------------------------
       
 * Write your service, publish it to the API deployer
 * In the API deployer deployment, fill in the "routing key". Just the deployment id is an appropriate routing key. It just needs to be unique.
 * Start sending queries
 * In your MLOps project, create a new dataset on the connection that has been selected by the admin, browse to the ``path/apinode-query/your-routing-key``
 * Enable partitioning on this dataset
 * Voila, you have the partitioned logs of just this service, across all API node instances

Behind the scenes
------------------

* The API node emits audit events with ``apinode-query`` topic and with the routing key specified in the deployment settings 
* The audit log of each API node is configured to send apinode-query/this-routing-key to the eventserver
* The eventserver receives them, dispatches on the "files in connection" target which creates subfolders per topic and routing key

Sample setup: high-security API node centralization
=====================================================

Use this when you need to have differentiated security for accessing the nodes of individual API services. It also ensures that people who don't have access to the deployment cannot send "fake" events for this deployment

Setup once (as admin)
----------------------

 * Install a design node, enable the EventServer on it
 * Require authentication on events in the EventServer settings

For each service (as admin)
-----------------------------

 * Generate a new authentication key (random string)
 * Add a "files in connection" target on the event server
    * Set topics filtering to ``apinode-query``
    * Set routing keys filtering to only accept the routing key of the service
    * Enable creation of subfolders
    * Select any compatible file-like connection like S3
    * Add your authentication key to the list of valid authentication key for the events endpoint, and add it as the "required Auth key" for this event server destination
 * Give this service-specific authentication key to the developer of the service

For each service (as user)
----------------------------

 * Write your service, publish it to the API deployer
 * In the API deployer deployment settings, enable "override infrastructure settings" and enable "auto-configure reporting to event server", enter the URL of the event server and the auth key
 * In the API deployer deployment, fill in the "routing key". Just the deployment id is an appropriate routing key. It just needs to be unique.
 * Start sending queries
 * In your MLOps project, create a new dataset on the connection that has been selected by the admin, browse to the ``path/apinode-query/your-routing-key`` (you should not be able to browse other folders of course, this should be handled by connection security)
 * Enable partitioning on this dataset
 * Voila, you have the partitioned logs of just this service, across all API node instances

Manual usage
=============

Audit settings can be configured manually in the `config/server.json` file of the API node.

Here is a sample configuration:

.. code-block:: javascript

        "auditLog": {
            "settings": {
                "targets": [
                    {
                      "type": "EVENT_SERVER",
                      "url": "http://my-event-server:9999",
                      "routingKeyMode": "FROM_MESSAGE",
                      "topicsFiltering": "SELECTED",
                      "topics": [
                        "apinode-query"
                      ],
                      "routingKeysFiltering": "ALL",
                      "routingKeys": [
                        "rk-clvs-1"
                      ]
                    }
                ]
            }
        }
