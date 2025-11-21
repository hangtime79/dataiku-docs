from dash import html, Input, Output
from dash.exceptions import PreventUpdate
from flask import request
import logging
import dataiku

logger = logging.getLogger(__name__)

dataset_to_build = "web_history_prepared"

# build your Dash app
app.layout = html.Div([
    html.H1("Impersonation Demo", style={'text-align': 'center'}),
    html.H3([
        html.Span("Welcome: "),
        html.Span(id="identified_user")
    ]),
    html.Button('Build the dataset', id='submit-val', n_clicks=0)
])


@app.callback(
    Output('identified_user', 'children'),
    Input('identified_user', 'children')
)
def load_user_credentials(children):
    if children:
        raise PreventUpdate
    else:
        # Get user info from request (can be done with impersonation)
        request_headers = dict(request.headers)
        auth_info = dataiku.api_client().get_auth_info_from_browser_headers(request_headers)
        return auth_info.get("associatedDSSUser")

        #    with dataiku.WebappImpersonationContext() as ctx:
        #        # Using this context, your actions here will be impersonated.
        #        client = dataiku.api_client()
        #        user = client.get_own_user()
        #        settings = user.get_settings()
        #        return settings.get_raw().get('displayName')


@app.callback(
    Output('submit-val', 'n_clicks'),
    Input('submit-val', 'n_clicks'),
    prevent_initial_call=True
)
def update_output(n_clicks):
    logger.info("Impersonation begins...")
    with dataiku.WebappImpersonationContext() as context:
        # Each time your need to do impersonation, you need to obtain a client.
        # Dash cannot store objects that are not in JSON format.
        local_client = dataiku.api_client()
        project = local_client.get_default_project()
        outdataset = project.get_dataset(dataset_to_build)
        outdataset.build()

    logger.info("Impersonation ends...")
    raise PreventUpdate
