from dash import Dash, dcc, html, dash_table, Input, Output
from dash.exceptions import PreventUpdate
import logging
import dataiku

logger = logging.getLogger(__name__)

project = dataiku.api_client().get_default_project()
datasets_name = list(map((lambda x: x.get("name", "")), project.list_datasets()))

# build your Dash app
app.layout = html.Div([
    html.H1("How to display a dataset"),
    dcc.Dropdown(datasets_name, placeholder="Choose a dataset to display.", id='dropdown'),
    dash_table.DataTable(id='table')
])


@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('dropdown', 'value')
)
def update(value):
    # If there is no value, do nothing (this is the case when the webapp is launched)
    if value is None:
        raise PreventUpdate
    # Take only the 100 first rows
    dataset = dataiku.Dataset(value).get_dataframe(limit=100)
    return dataset.to_dict('records'), [{"name": i, "id": i} for i in dataset.columns]
