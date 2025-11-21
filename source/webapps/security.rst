Webapps and security
#####################

.. contents::
	:local:

Authentication of webapp users
================================

By default, webapps require users to be authenticated. For more details and options, please see :doc:`public`.

Run-as-user
============

The code of the webapp itself always runs as a single user, the "run-as-user" of the webapp. By default, a webapp runs as the identity of the last DSS user who modified the webapp.

An administrator can modify the DSS user name under which the webapp runs. This is done in the settings of each individual webapp.

Identifying users from within a webapp
========================================

When a logged-in DSS user accesses a webapp, the webapp's code can identify which user is accessing the webapp. The webapp can use this information in order to customize the behavior for the user, to access user-specific information, or to deny access to some features, for example.

The exact way to do that depends on the webapp kind:

Standard webapp
-----------------

Please see https://github.com/dataiku/dss-code-samples/tree/master/webapps/flask/authenticate-calls

Bokeh webapp
-------------

Please see :doc:`devguide:api-reference/python/authinfo`. In order to retrieve the request headers, you need the following:

.. code-block:: python

    from bokeh.io import curdoc as bokeh_curdoc
    session_id = bokeh_curdoc().session_context.id
    from dataiku.webapps.run_bokeh import get_session_headers as get_bokeh_session_headers
    request_headers = get_bokeh_session_headers(session_id)

    auth_info = dataiku.api_client().get_auth_info_from_browser_headers(request_headers)

Dash webapp
-------------

This work the same as standard webapp. Just be careful to only access the `request.header` in a callback, because there's no active HTTP request initialization code.

.. code-block:: python

    from flask import request
    @app.callback(
        Output(component_id='my-output', component_property='children'),
        [Input(component_id='my-input', component_property='value')]
    )
    def update_output_div(input_value):
        request_headers = dict(request.headers)
        auth_info_brower = dataiku.api_client().get_auth_info_from_browser_headers(request_headers)
        return auth_info_brower["authIdentifier"]

Shiny webapp
------------

Please see :doc:`/R-api/authinfo`

Access to secrets
-----------------

The ``get_auth_info_from_browser_headers`` can be called with ``with_secrets=True`` in order to get decrypted user secrets (Please see :doc:`/security/user-secrets` for more details). 

This is possible because the end-user who is browsing the webapp has a DSS session cookie that the ``get_auth_info_from_browser_headers`` calls reads to retrieve information and secrets. If you want to block that behavior, you need to enable "Hide access tokens" in the Webapps security settings (Administration > Settings > Login & Security).

Impersonating users from within a webapp
=========================================

As indicated earlier, the backend code of a webapp runs as single user. However, the backend will very often perform calls to the Dataiku API, in order to read datasets, set variables, run scenarios, ...

It is possible for these calls to the Dataiku API to be *impersonated* in the name of the user currently viewing the webapp.

In order for a webapp to be able to impersonate other users in the Dataiku API, the run-as-user of the webapp must be granted the "Impersonation in webapps" permission to impersonate the *target* users, i.e. end-users.

These settings are done at the group level. If the webapp runs as user RU1 (which belongs to group G1), and the end-users to impersonate, EU1 and EU2, who belong to group G2, you need to:

* Go to the settings of G1
* In "Impersonation in webapps", put G2 as the allowed group.

This now allows webapps running as users of the G1 group to perform impersonated API calls in the name of users of the G2 group.

To actually perform impersonated calls, you need to modify your code this way:

Standard webapps
----------------

.. code-block:: python


    @app.route('/example')
    def example_call():

        # Calls performed using this client will be done as the run-as-user
        client = dataiku.api_client()

        # D1 will be read as the run-as-user
        df = dataiku.Dataset("d1").get_dataframe()
   
        with dataiku.WebappImpersonationContext() as ctx:
            # Calls performed using this client will be done as the end-user
            end_user_client = dataiku.api_client()

            # D2 will be read as the end-user
            df = dataiku.Dataset("d2").get_dataframe()

Bokeh webapps
--------------

.. code-block:: python


    def update_data(attrname, old, new):

        # Calls performed using this client will be done as the run-as-user
        client = dataiku.api_client()

        # D1 will be read as the run-as-user
        df = dataiku.Dataset("d1").get_dataframe()
   
        with dataiku.WebappImpersonationContext() as ctx:
            # Calls performed using this client will be done as the end-user
            end_user_client = dataiku.api_client()

            # D2 will be read as the end-user
            df = dataiku.Dataset("d2").get_dataframe()

Dash webapps
--------------

.. code-block:: python


    @app.callback(
        Output(component_id='my-output', component_property='children'),
        [Input(component_id='my-input', component_property='value')]
    )
    def update_output_div(input_value):
        # Calls performed using this client will be done as the run-as-user
        client = dataiku.api_client()

        # D1 will be read as the run-as-user
        df = dataiku.Dataset("d1").get_dataframe()
   
        with dataiku.WebappImpersonationContext() as ctx:
            # Calls performed using this client will be done as the end-user
            end_user_client = dataiku.api_client()

            # D2 will be read as the end-user
            df = dataiku.Dataset("d2").get_dataframe()

Shiny webapps
--------------

.. code-block:: R

    output$myPlot <- renderPlot({
        # D1 will be read as the run-as-user
        dkuReadDataset("d1")
      
        dkuImpersonateShinyCalls(session$request, {
            # D2 will be read as the end-user
            dkuReadDataset("d2")
        })
        ...
    })


Access to static resources from webapps
========================================

Webapps may require static resources accessible from the frontend client to function correctly (css, additional javascript resources...).
There are multiple ways to make those resources available through project / global code libraries.


Project-level private resources
-------------------------------

In the *Project library* two directory are automatically exposed as static resources:

- the `static` directory in the *Libraries* tab is exposed under ``http(s)://host:port/local/projects/PROJECT_KEY/static/``
- the `static` directory in the *Resources* tab is exposed under ``http(s)://host:port/local/projects/PROJECT_KEY/resources/``

These resources will be directly available for users who have the authorization to read the project content.
Editing these resources requires write permission on the project, and the *Write isolated code* global permission (or *Write unisolated code* if impersonation is disabled).


Project-level public resources
-------------------------------

In the *Project library* any file in the `local-static` directory in the *Resources* tab is exposed under ``http(s)://host:port/local/projects/PROJECT_KEY/public-resources/``

These resources will be available for any user, even users that are not authenticated to the Dataiku DSS instance.
Editing these resources requires write permission on the project, and the *Write isolated code* global permission (or *Write unisolated code* if impersonation is disabled).


Global public resources
-------------------------------

In the *Global shared code* any file in the *Static Web Resources* tab is exposed as public static resource under ``http://host:port/local/static/``

These resources will be available for any user, even users that are not authenticated to the Dataiku DSS instance.
Editing these resources requires the *Edit lib folders* global permission.
