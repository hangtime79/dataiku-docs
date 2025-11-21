Deploying bundles with the Project Deployer
############################################

This page will guide you through the process of taking a bundle that you've created of an existing project on your Design node, publishing the bundle on the Project Deployer, and then deploying and activating this bundle on an Automation node.

.. warning::

	This section assumes that you already have installed and configured the DSS Project Deployer, and already have an infrastructure connected to it. Please see :doc:`setup` and :doc:`project-deployment-infrastructures` if that's not yet the case.

Creating the bundle
===================

The first step is to create a bundle for an existing project. Please see :doc:`creating-bundles` for more information.

.. _bundles.deploying-projectdeployer.publishing:

Publishing the bundle on the Project Deployer
=============================================

With your created bundle selected on the project's Bundles list, click the "Publish on Deployer" action.

This will create a project on the Project Deployer and then import the bundle into that project. Note that a project on the Project Deployer is not the same as a Design node project, it's just a collection of bundles that in most cases all come from the same Design node project.

Click on the link that appears, which takes you to the uploaded bundle on the Project Deployer.

Deploying the bundle
====================

In the Project Deployer, you now need to actually deploy your bundle to your infrastructure (Automation node).

* From the left column of the Project Deployer, click on the bundle that was just uploaded, and select "Deploy"
* Select the infrastructure you wish to deploy to
* Give an identifier to your deployment. This identifier will not appear on the Automation node. It is only used on the Project Deployer
* Optionally, choose a different "Target Project Key" and "Target Project Folder"

    * The "Target Project Key" allows you to choose the project key of the created project on the Automation node
    * By default, projects on the Automation node will be created in the root folder

* Create

Your deployment is ready. You can either modify its settings, or start it.

When you click on the "Deploy" (or the "Update") button, DSS sends your bundle to the Automation node and activates it. When this process completes, you can see:

* The health status of the deployment, visible on both the main Deployments dashboard and the deployment's status page
* A timeline of recent scenario runs with their outcomes
* Stored update information, available in the **Last Updates** tab of the deployment

Modifying deployment settings
=============================

The Project Deployer also allows you to modify the settings of a deployment without having to actually log in to the Automation node. From the Settings tab of a deployment, you are able to modify settings such as the project's local variables, connection remapping, and current active bundle.

Whenever you modify a deployment setting, you must click the "Update" button for the new settings to be sent over to the Automation node project, even if you haven't changed the bundle. If not, you may see the deployment enter an "Out of sync" state, which means the settings on the Automation node project do not match what you have configured on the deployment.

Note that you can also change the active bundle of a deployment by clicking on one of the "Deploy" buttons associated with a bundle that has already been published on the Project Deployer. These "Deploy" buttons are found either on the bundle page on the Project Deployer, or the left sidebar of the Project Deployer's Deployments dashboard. If a deployment already exists for the project that the bundle belongs to, you have the option of updating that existing deployment (or creating a brand new deployment).

Scenarios
---------
You can also control which scenarios will be enabled or disabled on the Automation node project from the "Scenarios" section of the "Settings" tab. In this section, you can see all the scenarios located in the deployment's current active bundle. For each scenario, you are able to select whether you want the scenario's triggers to be enabled, disabled, or left alone when activating a bundle. "Automation local" scenarios (scenarios that were created directly in the Automation node project) cannot be controlled from here.

You can also disable all automatic triggers on the Automation node project from this section.
