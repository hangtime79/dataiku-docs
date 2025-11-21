import dataiku

from functools import partial

from bokeh.io import curdoc
from bokeh.models import Div, Button
from bokeh.layouts import layout
from dataiku.webapps.run_bokeh import get_session_headers

import logging

logger = logging.getLogger(__name__)

dataset_to_build = "web_history_prepared"


def build_dataset(dataset):
    logger.info('impersonation')
    with dataiku.WebappImpersonationContext() as ctx:
        local_client = dataiku.api_client()
        project = local_client.get_default_project()
        outdataset = project.get_dataset(dataset)
        outdataset.build()


def application():
    title = Div(text="""<h1>Impersonation Demo</h1>""")

    # Get user form http request (can be done with user impersonation)
    headers = get_session_headers(curdoc().session_context.id)
    auth_info = dataiku.api_client().get_auth_info_from_browser_headers(headers)
    user = auth_info.get('associatedDSSUser')
    subtitle = Div(text=f"""<h2>Welcome: <span id="identified_user">{user}</span></h2>""")

    button = Button(label="Build the dataset")
    button.on_event('button_click', partial(build_dataset, dataset=dataset_to_build))

    app = layout([title, subtitle, button])
    curdoc().add_root(app)

    curdoc().title = "Impersonation"


application()
