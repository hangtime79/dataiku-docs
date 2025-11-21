Items in Dataiku Govern
#######################

.. contents::
	:local:

Item is the generic way to describe the objects manipulated in Dataiku Govern. Items can be:

- **Synced items**: they are synced from Dataiku nodes and the hierarchical relationship between objects are represented in the way Dataiku Govern employs inheritance throughout its architecture. 
- **Govern items**: these can be pure Govern objects such as Business initiatives or the representation of the layer of governance added on synced items.

.. seealso:: 
	More information is available in `Concept | Governed items <https://knowledge.dataiku.com/latest/mlops-o16n/govern/concept-governed-items.html>`_

Items synced in Govern
======================
In Dataiku Govern, items created in Dataiku nodes and their associated metadata are automatically synchronized. Items from the Design node have a hierarchical structure, which is reflected in the Registry pages. 

Types of **governable items** include:

- Projects
- Bundles
- ML Saved Models and their versions
- GenAI Items, including:

	- Fine-tuned LLMs and their versions.
	- Agents and their versions.
	- Augmented LLMs and their versions.

.. seealso:: 
	More information is available in `Concept | Surfacing Dataiku items in the Govern node <https://knowledge.dataiku.com/latest/mlops-o16n/govern/concept-centralization-in-govern.html>`_

Dataiku Govern items
====================

Dataiku Govern enables users to add a governance layer with specific definitions, metrics, attachments, workflows, and sign-offs. You can create this governance layer in two ways:

- **By adding a layer** to existing synced items.
- **By independently creating** a layer, such as for Govern projects, Business initiatives, and custom items.

A **Govern project** can be started from the "Governed projects" page during the ideation phase, even before it is linked to a Dataiku project.

For better organization, you can group governed projects into **Business initiatives**, which are created in Dataiku Govern to link multiple projects with shared business goals.

.. seealso::
		More information is available in `Concept | Adding a governance layer to Dataiku items <https://knowledge.dataiku.com/latest/mlops-o16n/govern/concept-adding-governance.html>`_

.. _govern.item.content:

Govern item content
===================

Each Govern item page has detailed information that you can access in the left navigation menu.

Access the synced design and deployment metadata
------------------------------------------------

- The **Source objects** tab provides a view of the metadata connected from your **Dataiku Design node**. The information displayed is contextual, meaning it changes based on the item type.

	+--------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
	| Type of metadata         | Description                                                                                                                                             |
	+==========================+=========================================================================================================================================================+
	| General Information      | Essential details such as the Node ID, creation date, and author.                                                                                       |
	+--------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
	| Related Items            | A list of connected items like projects, models, bundles, LLMs, and Agents.                                                                             |
	+--------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
	| Specific to an item type | For example, when viewing a bundle, this section will also include specific details like `Release notes`, `Project standards` values and the `AI Types`.| 
	+--------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+

- The **Model metrics** tab is only available for *Dataiku Saved Model versions*. The information are related to the *Active version*, the *Data drift* and the *Performance metrics*.

- The **Deployments** tab provides updates on deployable items like *Saved Model versions* or *bundles*, including their deployment status and related infrastructure details.

	+--------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
	| Type of information      | Description                                                                                                                                             |
	+==========================+=========================================================================================================================================================+
	| Deployment Location      | The specific infrastructure and its type where the item is deployed.                                                                                    |
	+--------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
	| Governance Policy        | The specific Govern policy that is configured for the deployment.                                                                                       |
	+--------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
	| Deployment History       | The total number of times the item has been deployed.                                                                                                   | 
	+--------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+

.. seealso::
		More information is available in `Concept | Governed items <https://knowledge.dataiku.com/latest/mlops-o16n/govern/concept-governed-items.html>`_.

Add Governance metadata
-----------------------

- The **Overview** tab is a central location for enriching an item with additional metadata for governance purposes. The specific fields you can provide are contextual and vary by item type. 

.. _workflows:

- **Workflow**: Dataiku Govern provides a sequential *Standard workflow* for tracking and managing AI items, allowing users to monitor an item's status and its entire journey. For a clear record of progress, each item can have extra information and predefined workflows attached, with each step updated to a specific status.

	+------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+
	| Workflow Steps Status  | Description                                                                                                                                    |
	+========================+================================================================================================================================================+
	| Not Started            | The workflow process has not been initiated.                                                                                                   |
	+------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+
	| On Going               | The work on the step is active.                                                                                                                |
	+------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+
	| Finished               | The step is completed.                                                                                                                         | 
	+------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+

	.. seealso:: 
		More information is available in `Concept | Governed items - Advancing the status of Govern items through a workflow <https://knowledge.dataiku.com/latest/mlops-o16n/govern/concept-governed-items.html#advancing-the-status-of-govern-items-through-a-workflow.html>`_.

.. _sign-off:

- **Sign-off** is associated to a workflow steps. Reviews can be assigned to either roles, individuals or groups. In the *Standard workflow*, this sign-off occurs during the **Review step**, which includes **Feedback** and **Final Approval**. The Final Approval status is checked by Dataiku Deployer and the deployment authorization depends on the :doc:`Govern policy <deployment-policies>` set up on the infrastructure.

	+----------------+-------------------------------------------+------------------------------------------------------+
	| Review type    | Description                               | Possible statuses                                    |                                                                    
	+================+===========================================+======================================================+
	| Feedback       | Guide the final approver's decision.      | ``Approved`` / ``Minor issue`` or ``Major issue``.   |                                                     
	+----------------+-------------------------------------------+------------------------------------------------------+
	| Final approval | Only one final approval can be submitted. | ``Approved`` / ``Rejected`` / ``Abandoned``          |                                                                                                              
	+----------------+-------------------------------------------+------------------------------------------------------+

	.. seealso:: 
		More information is available in `Concept | Sign-offs in workflows of Govern items <https://knowledge.dataiku.com/latest/mlops-o16n/govern/concept-reviews-signoffs.html>`_.

- From the **Attachments** tab, references and files can be added.

Access your govern instance history
-----------------------------------

The **Timeline** records significant changes, including who made the change, a description, and a timestamp. A detailed table further shows the name of the updated attribute, its previous value, and its new value. To be able to easily find information about specific events, you can also filter the timeline.


Adapt governance policies to a specific item
--------------------------------------------

The **Governance settings** tab displays the :doc:`governance-policies`. From there, it is also possible to define specific rules that override the instance-level one.

Assign permissions to a specific item
-------------------------------------

**Role assignments** can be configured at the item level with the **artifact admin** permission. Permissions, inherited role assignment rules, and computed roles are not editable at the item level. To do this, go to the **Roles and Permissions** settings.

.. seealso:: 
	To learn more about role assignment rules settings, please refer to :doc:`/security/govern-permissions`.
