import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import json

import dataiku
import logging

logger = logging.getLogger(__name__)

from streamlit.scriptrunner.script_run_context import get_script_run_ctx
from streamlit.server.server import Server

dataset_to_build = "web_history_prepared"


def get_headers():
    # Get headers
    session_id = get_script_run_ctx().session_id
    server = Server.get_current()
    session_info = server._get_session_info(session_id)
    if session_info.ws is None:
        # At first page load, this is None (at least until #4099 is fixed)
        st.markdown("Unable to get session websocket. Please refresh the page.")
        st.stop()
    headers = dict(session_info.ws.request.headers)
    logger.info(headers)
    return headers


def build_dataset(dataset):
    user = dataiku.api_client().get_user(auth_info.get('authIdentifier'))
    client_as_user = user.get_client_as()
    project = client_as_user.get_default_project()
    outdataset = project.get_dataset(dataset_to_build)
    outdataset.build()


st.title('Impersonation Demo')
request_headers = get_headers()
auth_info = dataiku.api_client().get_auth_info_from_browser_headers(request_headers)
st.subheader(f"Welcome: {auth_info.get('authIdentifier')}")

st.button("Build the dataset", on_click=build_dataset, args=[dataset_to_build])
