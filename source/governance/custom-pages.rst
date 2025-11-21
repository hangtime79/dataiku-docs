Build Custom Pages
##################

.. contents::
	:local:

.. note::
    Note that this feature is not available in all Dataiku licenses. You may need to reach out to your Dataiku Account Manager or Customer Success Manager.


Overview
========
The Custom Page Designer is available from the Applications menu. It allows administrators to create as many custom pages as needed beyond the standard pages. 

Using the Custom Pages Designer, you can present your own selection of items with the option to display a Matrix as well. Custom and standard pages can be reordered and hidden in the navigation bar.

In the Custom Pages Designer, you will be able to:

* Choose which items to show.
* Utilize both standard and custom :doc:`blueprints <blueprint-designer/blueprint-designer>`.
* Select the Row Views you want to use.
* Create additional visualizations.


General settings
================
The administrator defines a custom page by an ID, name, and an icon. The ID is prefixed by ``cp.``. Once created, the ID cannot be changed.

Saving creates a preview of the page which is hidden from all non-admin users. Once the content is validated, you can set the page as **visible**.   

From the left tab, you will be able to:

* Search standard and custom pages.
* Hide or unhide standard and custom pages.
* Reorder standard and custom pages by dragging and dropping.
* Delete custom pages.


.. note::
   Standard pages cannot be deleted from Dataiku Govern. They can only be hidden from the navigation menu.

Custom Page content
===================

After creating a page, the user must select the **Custom Page content** of the page.

There are three types:

* **Item table**, which is the default.
* **Item table and matrix**.
* **Custom HTML**.

This choice will trigger different settings to configure.

Page settings
=============

By default all items are displayed, and you can dynamically filter items using rules on:

- Field value
- Item type
- Template
- Item
- Archived status
- Name
- Workflow step
- Sign-off
- Item contents


Table settings
==============
The administrator defines the column to display by default within the table. The columns directly available are:

- the **Name** of the item, 
- the **Workflow** status, 
- and the **Edit row button**.

For other column definition, select **View** and choose the blueprint in the first dropdown and fill-in the corresponding view ID in the View field. The field will suggest Row Views associated with the blueprint, as you can only select a row view ID.

.. seealso:: 
    To learn more about views please refer to :ref:`Views and view components section <views view components>`.

Matrix view settings
====================
The administrator defines a Matrix View by filling in the following fields:

* **Matrix Label**, which will override the dynamic title (optional).
* X and Y Axes, which define the default matrix axes.

Matrix zones
------------
The user can also choose the color gradient of the matrix zones.

Dataiku provides three preset color themes: **Business Value theme**, **Risk Matrix theme** and **Business Initiative theme**. 

It is also possible to create a **Custom theme**. Custom theme options include the background colors and the point border colors.

Custom HTML settings
====================
There is also an option to create a page defined by HTML code. For example, you can embed dashboards and videos from external tools, or even from Dataiku DSS.


.. seealso:: 
    To practice using the Custom Pages Designer, visit `this tutorial <https://knowledge.dataiku.com/latest/mlops-o16n/govern/tutorial-custom-pages.html>`_.