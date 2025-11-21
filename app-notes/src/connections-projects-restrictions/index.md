# Connections/Projects restrictions plugin

In DSS, permissions on connections and projects are managed independently.

This strongly reduces the burden for administrators, who do not have to manage connections on a per-project basis, and also allows users with full access to connections to give access to datasets that other users can then leverage.

This can however in some cases allow "sharing" of data between connections, which can be unwanted.

For example:

* User U1 belongs to group G1, which has access to connections C1 and C2
* User U2 belongs to group G2, which only has access to connection C2
* Both G1 and G2 have access to project P1
* Thus, in project P1, user U1 can create a dataset D1 that uses connection C1, and then create a sync recipe that syncs to a dataset D2 that uses connection C2
* This has the effect of copying data from C1 to C2, and thereby granting access to this data to U2

While this ability is often desirable, it is not always, especially in some regulated cases.

The "Connections/Projects restrictions" plugin adds an additional security layer which forbids this kind of use case. The main goal of the plugin is to control in which projects a given connection can be used.

# Installation

Go to the plugin store and install the Connections/projects restrictions plugin.

Alternatively, download it from https://cdn.downloads.dataiku.com/public/dss-plugins/connections-projects-restrictions/ (make sure to select the correct DSS version) and upload it to DSS.

# Setup

Configure the plugin by going to the page of the plugin in your DSS, then to the "Settings" tab.

The plugin has two modes of operation.

In both cases, the plugin operates by restricting the ability to *create* or *save* datasets that don't respect the rules. *The plugin will not affect or restrict existing datasets or projects*

## Automatic mode

In automatic mode (called "Allow usage if connection is freely usable by all users who have access to the project"), the following rules is applied:

A dataset that uses a given a connection can only be created/saved if *all* users who have *any* access to the project *also* have the "Freely usable" permission on the connection.

## Explicit mode

In explicit mode (called "Allow usage if project is explicitly allowed by connection"), you must configure in each connection the exact list of project keys that may use this connection.

To do that:

* Go to the Connection settings
* In "Advanced connection properties" (not to be confused with "Advanced JDBC properties"), add a new entry, with:

   * key: `dku.security.allowedInProjects`
   * value: a comma-separated list of project keys (not names) in which this connection may be used. Use `*` as wildcard.

If using [Dataiku applications](https://doc.dataiku.com/dss/latest/applications/index.html#dataiku-applications), the permissions need to be granted on the app template, and are carried over to app instances built from the app template by adding another entry in "Advanced connection properties" :

   * key: `dku.security.allowedInApps`
   * value: a comma-separated list of project keys (not names) of the Dataiku app templates in which this connection may be used. Use `*` as wildcard.

If using [application-as-recipes](https://doc.dataiku.com/dss/latest/applications/application-as-recipe.html), the permissions need to be granted on the app template of the application-as-recipe, using `dku.security.allowedInApps`. This applies to connections used in the template, as well as connections used in the host projects of the application-as-recipe instances. That is, if connection `AAAA` is used in the app template, then the app template project key needs to be listed in `dku.security.allowedInApps`. If connection `BBBB` is used in a host project of an application-as-recipe instance, and one of the inputs of the recipe is on `BBBB`, then the app template needs to be listed in `dku.security.allowedInApps` for connection `BBBB` too.

For Dataiku apps or app-as-recipes installed as plugins, the value is not a project key but `PLUGIN_pluginId_elementId`, where `pluginId` is the plugin identifier (not name) and `elementId` is the app identifier (not name) inside the plugin, that is, the name of the folder of the app inside the plugin.

# Details

The rules are applied and checked upon the following operations:

* Creating a dataset
* Saving the settings of a dataset (including when editing schema)
* Creating a managed folder
* Saving the settings of a managed folder
* Sharing items to the project