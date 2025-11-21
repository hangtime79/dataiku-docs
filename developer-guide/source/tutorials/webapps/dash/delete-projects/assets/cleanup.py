from dash import html, dash_table, Input, Output, State, callback, dcc
import dataiku
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.info('start webapp')

client = dataiku.api_client()


def get_projects():
    """
    Returns a pandas dataframe containing the projects key, name and short description
    """
    projects = client.list_projects()
    keys = [proj['projectKey'] for proj in projects]
    names = [proj['name'] for proj in projects]
    desc = [proj['shortDesc'] for proj in projects]
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
    projects_table,
    dcc.ConfirmDialogProvider(
        children=html.Button('Delete', id='delete-button', n_clicks=0),
        id='warning-delete',
        message='Are you sure you want to delete the selected project(s)?'
    )
])


@callback(
    Output('projects_table', 'data'),
    Output('projects_table', 'selected_rows'),
    Input('warning-delete', 'submit_n_clicks'),
    State('projects_table', 'selected_rows'),
    prevent_initial_call=True
)
def delete_projects(submit_n_clicks, selected_rows):
    """
    Callback triggered when the user clicks on the delete button.
    This will delete all the selected projects.
    Returns the updated list of projects and resets the selection.
    """
    projects = get_projects()
    for key in projects.iloc[selected_rows]['key'].to_list():
        project = client.get_project(key)
        project.delete(clear_managed_datasets=True, clear_output_managed_folders=True, clear_job_and_scenario_logs=True)
        logger.info(f"project {key} deleted")
    updated_projects = projects.loc[~projects.index.isin(selected_rows)].to_dict('records')

    return updated_projects, []
