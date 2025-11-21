import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash.exceptions import PreventUpdate
import dataiku
import base64
import pandas as pd


def write_question_answer_sql(client, dataset_name, connection, connection_type, project_key, question, answer):
    """
    Save data into a SQL like dataset
    Args:
        client: the dataiku client
        dataset_name: name of the SQL dataset
        connection: name of the SQL connection used for saving
        connection_type: type of connection
        project_key: project key
        question: the question
        answer: the answer
    """
    dataset = dataiku.Dataset(dataset_name)
    table_name = dataset.get_location_info().get('info', {}).get('table')
    value_string = f"('{base64.b64encode(question.encode('utf-8')).decode('utf-8')}', '{base64.b64encode(answer.encode('utf-8')).decode('utf-8')}')"
    sql = f"""INSERT INTO "{table_name}" (question, answer) VALUES {value_string}"""
    client.sql_query(sql, connection=connection, type=connection_type, project_key=dataset.project_key,
                     post_queries=['COMMIT'])


def write_question_answer_csv(dataset_name, question, answer):
    """
    Save data into a CSV like dataset
    Args:
        dataset_name: the CSV dataset
        question: the question
        answer: the answer
    """
    dataset = dataiku.Dataset(dataset_name)
    row = {
        "question": [f"""{question}"""],
        "answer": [f"""{answer}"""]
    }
    df = dataset.get_dataframe()
    df = pd.concat([df, pd.DataFrame(row)])
    with dataset.get_writer() as writer:
        writer.write_dataframe(df)


# use the style of examples on the Plotly documentation
app.config.external_stylesheets = [dbc.themes.BOOTSTRAP, "/local/static/loading-state.css"]

search_text_layout = html.Div([
    dcc.Store(id='messages', data=[
        {"role": "system", "content": "You are a helpful assistant"}]),
    dbc.Row([
        dbc.Label("Max messages", html_for="max_messages", width=2),
        dbc.Col(dbc.Input(id="max_messages", value="5", type="number", min=1, max=10), width=2),
        dbc.Col(width=6),
        dbc.Col(dbc.Button("Reset conversation", id="flush_messages", n_clicks=0, class_name="btn-danger"), width=2,
                class_name="d-grid col-2 gap-2")
    ], class_name="mb-3", ),
    dbc.Row([
        dbc.Label("Ask your question", html_for="search_input", width=2),
        dbc.Col(html.Div(children=[
            dbc.Input(id="search_input", placeholder="What can I do for you?"),
            dcc.Loading(id="ls-loading-1", children=[html.Div(id="ls-loading-output-1")], type="default")]), width=10),
    ], className="mb-3", ),
])

# build your Dash app
app.layout = html.Div([
    search_text_layout,
    dbc.Row([
        dbc.Col(width=2),
        dbc.Col(dbc.Textarea(id="text_output", style={"height": "200px"}), width=10)], class_name="mb-3"),
    dbc.Row(
        [dbc.Col(dbc.Button("Save this answer", id="save_answer", n_clicks=0, class_name="btn-primary", size="lg"))],
        justify="end", className="d-grid gap-2 col-12 mx-auto", )
], className="container-fluid mt-3")

LLM_ID = "openai:toto:gpt-3.5-turbo"
client = dataiku.api_client()
project = client.get_default_project()
llm = project.get_llm(LLM_ID)


@app.callback(
    [Output("ls-loading-output-1", "children"),
     Output("text_output", "value"),
     Output("messages", "data")],
    Input("search_input", "n_submit"),
    State("search_input", "value"),
    State("max_messages", "value"),
    State("messages", "data"),
    running=[
        (Output("search_button", "disabled"), True, False),
    ],
    prevent_initial_call=True
)
def get_answer(_, question, max_messages, messages):
    """
    Ask a question to Chat GPT (with some context), and give back the response
    Args:
        _: number of enter pressed in the input text (not used)
        question: the question (with the context)
        max_messages: number of context messages to keep
        messages: the context

    Returns:
        the response, and an updated version of the context
    """
    if not (question) or not (max_messages) or not (messages):
        raise PreventUpdate

    while len(messages) > int(max_messages):
        messages.pop(1)

    messages.append({"role": "user", "content": question})
    try:
        completion = llm.new_completion()
        for message in messages:
            completion.with_message(message.get('content'), role=message.get('role'))
        answer = completion.execute()

        if answer.success:
            messages.append({"role": "assistant", "content": answer.text})
            return ["", answer.text, messages]
        else:
            return ["", "Something went wrong", messages]
    except:
        return ["", "Something went wrong", messages]


@app.callback(
    Output("messages", "data", allow_duplicate=True),
    Input("flush_messages", "n_clicks"),
    prevent_initial_call=True
)
def reset_conversation(_clicks):
    """
    Reset the conversation
    Args:
        _clicks: number of clicks on the flush button (unused)

    Returns:
        a new context for the conversation
    """
    return [{"role": "system", "content": "You are a helpful assistant"}]


@app.callback(
    Output("save_answer", "n_clicks"),
    Input("save_answer", "n_clicks"),
    State("search_input", "value"),
    State("text_output", "value"),
    prevent_initial_call=True
)
def save_answer(_clicks, question, answer):
    """
    Save the answer
    Args:
        _clicks: number of clicks on the flush button (unused)
        question: the question
        answer: the answer

    Returns:

    """
    ## Uncomment these lines if you need to save into an SQL dataset

    #    client =  dataiku.api_client()
    #dataset_name = "History_SQL"
    #connection = "PostgreSQL"
    #connection_type = "sql"
    #project_key = client.get_default_project()

    #write_question_answer_sql(client, dataset_name, connection, connection_type, project_key, question, answer)

    ## Saving into a CSV dataset

    dataset_name = "History"
    write_question_answer_csv(dataset_name, question, answer)
