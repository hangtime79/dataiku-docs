import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html
import dataikuapi

# use the style of examples on the Plotly documentation
app.config.external_stylesheets = [dbc.themes.BOOTSTRAP]

# Content for entering API endpoint information
api_information = html.Div([
    dbc.Row([
        dbc.Label("Endpoint URL", html_for="endpoint_url", width=2),
        dbc.Col(dbc.Input(id="endpoint_url",
                          placeholder="Please enter the endpoint URL (http://<IP_Address>:<Port>)"),
                width=10)
    ]),
    dbc.Row([
        dbc.Label("Endpoint name", html_for="endpoint_name", width=2),
        dbc.Col(dbc.Input(id="endpoint_name",
                          placeholder="Please enter the name of the endpoint"),
                width=10)
    ])
])

# Content for entering feature values
data = dbc.Row([
    dbc.Label("Data to score", html_for="features", width=2),
    dbc.Col(dbc.Textarea(id="features", class_name="mb-3"), width=10)])

# Send button
send = dbc.Row([
    dbc.Col(dbc.Button("Score it", id="score_button", color="primary", n_clicks=0),
            width=2)],
    justify="end")

# Content for displaying the result
result = dbc.Row([
    dbc.Label("Prediction", width=2),
    dbc.Label(id="prediction_result", width=10),
])

# build your Dash app
app.layout = html.Div([
    api_information,
    data,
    send,
    result
], className="container-fluid mt-3")


@app.callback(
    Output("prediction_result", "children"),
    Input("score_button", "n_clicks"),
    State("endpoint_url", "value"),
    State("endpoint_name", "value"),
    State("features", "value"),
    prevent_initial_call=True
)
def score(_nclicks, url, name, data):
    if url and name:
        try:
            client = dataikuapi.APINodeClient(url, name)

            record_to_predict = eval(data)
            prediction = client.predict_record("predict_fraud", record_to_predict)
            return prediction \
                .get('result', {'prediction': 'No result was found'}) \
                .get('prediction', 'No prediction was made.')
        except SyntaxError:
            return "Parse error in feature"
        except Exception:
            return "Error"
    else:
        return "Unable to reach the endpoint"
