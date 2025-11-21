Creating a bundle
##########################

A bundle can be roughly seen as a snapshot of the project together with the data that are also needed for the recomputation of the tasks.
A bundle differs from a mere project export because its purpose is not to move a project with all its contents from one node to another but to move the metadata and the data needed to replay the tasks that should be performed on the production environment.

Bundles are used to transfer projects from the Design node to the Automation node. For example in a simple staged deployment workflow, bundles will be created on the Design Node, then transferred to a first Automation node where some tests will be performed, and then finally to the Automation node where the actual production batch recomputing will happen.
Transferring bundles between nodes can either be done :doc:`manually </deployment/manually-importing-bundles>` or via the :doc:`Project Deployer </deployment/deploying-bundles>`.

To create a bundle on a Design Node, go to the bundle list page (Project > Bundles). You need :doc:`Write project content privilege </security/permissions>` for this.

Bundle contents
===============

Metadata
---------

A bundle always contains a snapshot of the corresponding project's metadata at the time of its creation, which includes the following:

- Project settings
- Notebooks
- Analysis
- Recipes
- Scenarios
- Datasets metadata
- Saved Models metadata
- Managed Folders metadata
- Model Evaluation Store metadata
- :ref:`Project shared code<project-lib>`

Note that this does not include the actual data nor the persisted models lying under the flow. 
It also does not include :ref:`Global shared code<global-lib>`. 

Additional Data
----------------
Optionally, you can add to the bundle the actual data of some limited datasets, managed folders or saved models depending on what should be transferred to the production environment :

- *Datasets:* for example for static datasets containing enrichment or reference data that are not recomputed in production.
- *Saved Models:* for example when you plan to score data with a model that has been trained in the Design node.
- *Managed Folders:* Managed folders can contain all sorts of things (images, serializations, pdfs, etc). Adding managed folders is a convenient way to move their contents to the production environment together with the projects metadata.


Bundle release notes
---------------------
Upon creation, you can see the differences between the bundle under creation and the previous one  and add the appropriate release notes. This helps

- the tracking of high level changes between bundles
- the communications between the teams responsible for putting bundles in production when they differ from those designing the bundles.


Bundles that include shared objects
------------------------------------

If a bundle contains any objects that were shared to it from other projects, it will be reliant on those upstream projects. As a result, upstream bundles should always be published and activated prior to publishing and activating downstream bundles. If upstream bundles are not published prior to downstream bundles, any updates to shared objects in upstream projects will not be reflected in the downstream projects.
    

Publishing the bundle on the Project Deployer
=============================================

You then publish the bundles to the Project Deployer. Please see :ref:`bundles.deploying-projectdeployer.publishing` for more information.

Downloading a bundle
====================

All successfully created bundles are available for download as zip archives, which you can transfer to an Automation node in order to import them.



Reverting a bundle on the design node
=====================================
You can revert a project to a given bundle version. This will replace the current state of this project with the metadata stored into the bundle. If the bundles also contains data, the data will be imported as well and override current data.

If you made changes to the :doc:`/schemas/user-defined-meanings` since the bundle creation, you will see warnings before the bundle is reverted and will be able to choose whether you want to keep these changes or restore the UDMs from the bundle.
