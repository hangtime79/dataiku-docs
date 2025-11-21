Create templates in Blueprint Designer
**************************************

.. contents::
	:local:

Summary 
=======
To create a template for an artifact, you must know how to design a **blueprint version**.

When designing blueprint versions, you can start by defining how many steps are in the workflow (if a workflow is desired).

The next step is to define which **Fields** you would like to include on that blueprint version. These will be the fields that Govern users will fill in or view information about the objects to which this template has been applied.

Next, you will define **Views**, which are the collection of fields that the users will see and interact with. For example, you might create a ``Project Description`` field and a ``Status Update`` field. Then you create a **Overview** view which includes ``Project Description`` and a **Step 1** view that includes ``Status Update``.

Finally, to add a View to the relevant place, you can add the **View ID** to either the **Overview** page or the steps you've created in the workflow, for instance.

Configuration
=============

General settings
----------------
The **General** tab allows you to define some key information for your blueprint version. 

Under the **Main section**, you can: 

- Add some instructions for other users.
- Define the Parent which is used to define the hierarchy of your govern items for breadcrumbs for users.
- Set which View should be used on the **Overview** page of any item using this blueprint version.

.. _custom.workflow:

Under the **Workflow section**, you can:

- Create steps for a workflow. Leave this empty if you want to make a blueprint version with no workflow. 
- Name and re-order your steps. Specify which View ID should be used for each step.
- Assign one or more of the steps to require a formal sign-off. You can use the sign-off editor to define who is responsible for signing off in that step for any Govern item created with this template.

.. _custom.sign-off:

While not included by default, Dataiku Govern was built to support extensive customization, providing more flexibility for clients with complex governance requirements for which the predefined templates aren't sufficient. For example, you may want to customize:

  .. list-table:: 
    :header-rows: 1
    :widths: 30 70
    
    * - Feature
      - Advanced capabilities
    * - **Sign-off workflow**
      - * Add or remove a sign-off on each workflow step. 
        * Choose if the sign-off approval is mandatory to continue the workflow process.
        * Note : Mandatory sign-offs defined on workflow steps having specific visibility conditions can be bypassed if the step was not visible when advancing the workflow. 
          It still applies even if the step becomes visible afterwards. In such case, a warning will be displayed on the workflow step, but the workflow won't be blocked from going forward, unless that step becomes ongoing again.
    * - **Sign-off assignment**
      - * Create multiple feedback groups. 
        * Assign who can give a review. You can add several roles, Users, Groups and/or Global API Keys.
    * - **Sign-off reset**
      - * Setup recurrence to automatically reset an approved sign-off. It can also be scheduled manually on each sign-off.

Fields
------
Fields can be defined which contain information and can accept user inputs. Fields can be of the following types:

.. list-table:: 
  :widths: 30 70
  :header-rows: 1

  * - Field type
    - Description
  * - Number
    - User inputs an integer or decimal value.
  * - Boolean
    - This creates a checkbox in the artifact that a user can select or leave unselected.
  * - Text
    - User inputs a string value.
  * - Category
    - Users choose items from a dropdown list.
  * - Date
    - Users input a date value.
  * - Reference
    - Provides other artifacts in Dataiku Govern, for example a specific governed Project.
  * - File
    - Allows users to upload a file.
  * - Time series
    - Mainly used for models metrics graphs. A field from this type cannot be edited directly from the GUI, only through the public API or in a hook.

Some constraints may be defined on fields depending on their type. For instance: 

- A Number field can be constrained for its value to be only on an allowed range. 
- A Reference field can be constrained on which allowed blueprints the reference item must be. 
- Fields can also be marked as ``required``. 
- The "is List" checkbox allows users to add multiple values in a single field.

.. note:: 
    To edit (or view) these fields, users will need to have Write (or Read) permission for that blueprint or field.

.. _views view components:

Views
-----
Views are essential components for defining the content and structure of a Govern item page. They are composed of various view components, which can be **containers**, **subcontainers**, or **fields**.

Key Concepts
^^^^^^^^^^^^

- **Containers and Fields:** Containers act as sections to group related fields. Fields must be placed within a view to be visible on an item page. A single field can be included in multiple views. When a shared field is updated in one view, the changes are automatically reflected in all other views where it is present.
- **Content Display:** Views determine the content shown on Govern item pages, such as **Overview**, **Workflow steps**, and **Reference fields**. They also define how rows are displayed in tables.

Creating and Customizing Views
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Adding Components:** You can add individual fields or containers to organize fields. Containers can be nested to create further subsections.
- **Arranging and Editing:** You can easily rearrange view components using a drag-and-drop interface and copy/paste, or add or delete components as needed.
- **Configurable Properties:** The following options can be managed from the right panel menu.

.. list-table:: 
  :header-rows: 1

  * - Properties
    - Description
  * - Label
    - You can define a label for sections and fields.
  * - Description
    - You can add a description, which will be displayed in a tooltip next to the label.
  * - Documentation
    - You can add inline documentation written in HTML.
  * - View type
    - You can define if you want to display the content as a card or a table.
  * - Conditional views
    - You can define rules based on another field value to conditionally display a field or a container.

.. note:: 
    Once these views are created, saved, and published, they will appear in the associated item. Users with appropriate permissions will then be able to read and write information in the fields of those views.

.. seealso::
    To practice configuring views, visit this `tutorial <https://knowledge.dataiku.com/latest/mlops-o16n/govern/tutorial-blueprint-designer.html#configure-views>`_.


Hooks
-----

Hooks are used to automate actions related to artifacts in Dataiku Govern. They are written in Python and will be run during the artifacts lifecycle phases: CREATE, UPDATE, or DELETE. Which phases are selected to run a hook is configurable.

When you first create a hook, sample code will be included to demonstrate the available functionality. Some examples of how hooks can be used include calculating a field based on other fields (for example, if you want to calculate a "risk score" based on inputs in a few different fields), or changing the owner of a project based on some criteria.

.. warning::

    Hooks are executed before the actual action is committed, which means that the item action (save/create/delete) may fail after the hook is run. For this reason, it is not recommended to have external side-effects on other items such as using the API client to save/create/delete an item in Govern because there may be inconsistent results.

    In addition, saving/creating/deleting an external item via the API client may also trigger another hook execution which is not supported at the moment and will fail the action.

    If there is a need to trigger a hook on a neighbor item for syncing reasons (ie. compute a sum from children items), you may fill the handler.artifactIdsToUpdate list with artifacts IDs to schedule the execution of their UPDATE hooks after the action has completed on the initial artifact.

