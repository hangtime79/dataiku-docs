Dataiku Applications
####################

.. toctree::

   tiles
   application-as-recipe


Introduction
============
You can design and package your project as a reusable application with:

* customizable inputs (datasets, managed folders, project variables, ...)
* pre-defined actions allowing you for example to build the results
* access to pre-defined results (datasets, file/folder downloads, dashboards, ...)

Using a Dataiku application
===========================
A **Dataiku application** can be configured to allow instances to be created by any user. In this case any user will be able
to access the application and create a new instance.
If the **Dataiku application** is configured to allow instantiation only for users with execute permission the specific
:doc:`Execute app </security/permissions>` permission must be configured on the project containing the application.

**Dataiku applications** are listed on the main home page in a dedicated **Dataiku Apps** section or from the applications
menu.

From the application home page, you will:

* see the existing instances;
* be able to create a new instance;
* access one of the existing instances by clicking on the corresponding instance tile.

Developing a Dataiku application
================================
Only users that are :doc:`administrator of the project </security/permissions>` can contribute to the development of
an application. But only users with the **Develop plugins** permission are allowed to configure project variable tiles with
custom code.

To convert a project into a **Dataiku application**, click on **Application designer** from the project menu. A project can
be converted either into a **Dataiku application** or into an :doc:`/applications/application-as-recipe`. Once the project is converted, the
project menu will open the **Application designer** directly.

Application header
++++++++++++++++++
The **Application header** panel allows to configure:

* the application image;
* the application title and description;
* the application version;
* which user can instantiate the application;
* whether users without the permission to instantiate the application should still be able to discover it;
* the tags.

The application version is represented as a string that developers update to inform users of created app instances
about the availability of a new version, enabling them to update their instance. 
Typically, changes such as updates in the application flow or the addition of a new tile would prompt an application version update.

Application features
++++++++++++++++++++
The **Application features** panel allows toggling the display of some items on the application instances. The impacted
sections are:

* Flow top menu
* Lab top menu
* Code top menu
* Version control top menu
* "Switch back to project view" button (present on the instance's home)

Note that these options only apply to instances that are created from now on. If you want to apply any change to an existing instance, you'll have to delete and re-create the instance.

Included content
++++++++++++++++
The **Included content** panel allows to configure the additional data — from the original project containing the
application — to include into the application instances.

Application instance home
+++++++++++++++++++++++++
The **Application instance home** panel allows you to configure the user interface of the application instances.
It is possible to add many tiles in many sections.

You can find more information about the available tiles in :doc:`tiles`.

Advanced settings
+++++++++++++++++
From the **Advanced** tab in an **Application designer** you can:

* convert a **Dataiku application** into an **Application-as-recipe** and vice versa
* map connection and code environment
* visualize the raw JSON manifest corresponding to the application (for advanced usage)

Application instance names
++++++++++++++++++++++++++

When using a **Dataiku application**, the user can choose any name for the instance they create.
But since the name is arbitrary, some applications can meet trouble if they use it in places where the name is constrained,
such as names of tables in SQL databases, since these often enforce maximum lengths on identifiers.
Same with application-as-recipe, because the name of the project created by a run of the recipe is built from the recipe name.

To alleviate this issue, all application instances receive a project variable named `projectRandomKey` which is a short (8 characters)
random string of alphanumerical characters. This can for example be used to build table names for SQL datasets.
To use it in your application, first define a `projectRandomKey` variable in your application, then use it wherever it is needed.
This way you can still execute your application flow while building the application content while the variable content
will be overwritten when the application is instantiated.
 
Note that, as `projectRandomKey` is a random alphanumerical string, it can start with a number: since many SQL databases
reject identifiers starting with numbers, it is advised to prefix `${projectRandomKey}` with some letters if this variable
is used to prefix a table name. E.g. `p${projectRandomKey}_table_name`.

Application-as-recipe
=====================
You can instead build a reusable recipe: see :doc:`application-as-recipe`.

Sharing a Dataiku application
=============================
You can share a **Dataiku application** either by :doc:`copying this project </concepts/projects/duplicate>` or by creating a
plugin component from your application. To create a plugin component from your application, click on the
**Create or update plugin application** action from the **Actions** menu in the **Application designer**.

Plugin component
++++++++++++++++
From the component descriptor you can configure :

* the application name with the **meta.label** field
* the application description with the **meta.description** field
* the application image with **appImageFilename** field referring to an image uploaded in the **resource** folder of the plugin (at the root of the plugin)

Connection and code environment mapping
+++++++++++++++++++++++++++++++++++++++
It is possible to specify connection and code environment mapping.

For an application inside a project
-----------------------------------
Go to the **Advanced** tab in the application designer.

For an application inside a plugin
----------------------------------
Go to the **Settings** tab of the plugin: for each application, a tab to configure these mappings will be available.

For an application inside a bundle
----------------------------------
Go to the **Activation settings** tab in the bundles management. See :doc:`/deployment/index`.

Initiating an application instantiation request
===============================================

Only users without any permissions on the application will be able to initiate an application instantiation request. They will be able to do so through a modal that will be displayed when landing on the application URL.
For example, for discoverable applications, users can discover applications through the interface and request access.
In the case of private applications, this will most likely happen if one of the application contributors shares the application URL with another user.

Managing an application execution request
=========================================

Application administrators can manage execution requests from within the project's security section or by handling the request in the requests inbox.

If they manage the request via the requests inbox, they will be able to select which user or group they are granting the `Execute App` permission.

.. note::

	Automatic updates of the request:

	In the requests inbox, the request status can be automatically updated in the following cases:
	
	* Request is considered approved if the requester is given "Execute App" right via the app's project security page
	* Request is rejected if the requester is deleted
	* Request is deleted if the project is deleted
