Public webapps
#################

Webapps are normally only available for logged-in DSS users who have at least:

* the "Read dashboards" permission on the DSS project if the webapp is accessible to dashboard users
* the "Read project content" permission on the DSS project if the webapp is not accessible to dashboard users.

It is also possible to make webapps public. When a webapp is public, being an authenticated user is not necessary in order to access the webapp, and no authorization control is performed. It is up to the webapp to implement its own authentication and authorization, if applicable.

Deciding whether a webapp can be made public is normally an administrator prerogative. In order to make a webapp public, an administrator must go to Administration > Settings > Security & Audit > Other security settings, and add the "PROJECTKEY.webappId" in the authentication whitelist.

The webappId is the first 8 characters (before the underscore) in the URL of the webapp. For example, if the webapp URL in DSS is ```/projects/BULLDOZER/webapps/kUDF1mQ_shiny/view```, the  webappId is ``kUDF1mQ``

.. warning::

	Please make sure to restart the webapp backend for these changes to take effect. 
