from dash import html, dash_table
import dataiku
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.info('start webapp')

client = dataiku.api_client()


def get_projects():
    """
    Returns a pandas dataframe containing the key, name, and short description for each project
    """
    projects = client.list_projects()
    keys = [proj['projectKey'] for proj in projects]
    names = [proj['name'] for proj in projects]
    desc = [proj.get('shortDesc', 'No description found.') for proj in projects]
    data = {
        "key": keys,
        "name": names,
        "description": desc
    }

    return pd.DataFrame(data)


projects_table = dash_table.DataTable(
    id='projects_table',
    columns=[{"name": i, "id": i, "selectable": True} for i in get_projects().columns],
    data=get_projects().to_dict('records'),
    row_selectable='multi',
    selected_rows=[],
    editable=True
)

# build your Dash app
app.layout = html.Div([
    html.H1("List of projects"),
    projects_table
])
