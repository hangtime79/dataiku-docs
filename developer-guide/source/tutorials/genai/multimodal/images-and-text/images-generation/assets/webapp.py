from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash import no_update

import base64
import dataiku
from dataiku import SQLExecutor2
from dataiku.sql import Constant, toSQL, Dialects

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app.config.external_stylesheets = [dbc.themes.SUPERHERO, dbc_css]

IMG_LLM_ID = ""
DATASET_NAME = "movies"

USE_TITLE = 1
USE_YEAR = 2
USE_OVERVIEW = 3
USE_GENRE = 4

imagellm = dataiku.api_client().get_default_project().get_llm(IMG_LLM_ID)

# build your Dash app
v1_layout = html.Div([
    dbc.Row([html.H2("Using LLM Mesh to generate of Poster movie."), ]),
    dbc.Row(dbc.Label("Please enter a name of a movie:")),
    dbc.Row([
        dbc.Col(dbc.Input(id="movie", placeholder="Citizen Kane", debounce=True), width=10),
        dbc.Col(dbc.Button("Search", id="search", color="primary"), width=2)
    ], justify="between", class_name="mt-3 mb-3"),
    dbc.Row([
        dbc.Col(dbc.Label("Select features you want to use for genrating an image:")),
        dbc.Col(dbc.Row([
            dbc.Checklist(
                options=[
                    {"label": "Use Title", "value": USE_TITLE},
                    {"label": "Use Year", "value": USE_YEAR},
                    {"label": "Use Overview", "value": USE_OVERVIEW},
                    {"label": "Use Genre", "value": USE_GENRE}
                ],
                value=[USE_OVERVIEW],
                id="features",
                inline=True,
            ),
        ]), width=6),
        dbc.Col(dbc.Button("Generate", id="generate", color="primary"), width=2)
    ], align="center", class_name="mt-3 mb-3"),
    dbc.Row([
        dbc.Col([
            dbc.Row([html.H2("Movie information")]),
            dbc.Row([
                html.H3(children="", id="title")
            ], align="center", justify="around"),
            dbc.Row([
                html.H4(children="", id="year")
            ]),
            dbc.Row([
                html.H4(children="", id="genre")
            ]),
            dbc.Textarea(id="overview", style={"min-height": "500px"})
        ], width=4),
        dbc.Col(html.Img(id="image", src="", width="95%"), width=4),
        dbc.Col(html.Img(id="generatedImg", src="", width="95%"), width=4),
    ], align="center"),
    dbc.Toast(
        [html.P("Searching for information about the movie", className="mb-0"),
         dbc.Spinner(color="primary")],
        id="search-toast",
        header="Querying the database",
        icon="primary",
        is_open=False,
        style={"position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)"},
    ),
    dbc.Toast(
        [html.P("Generating an image", className="mb-0"),
         dbc.Spinner(color="primary")],
        id="generate-toast",
        header="Querying the LLM",
        icon="primary",
        is_open=False,
        style={"position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)"},
    ),

    dcc.Store(id="step", data=[{"current_step": 0}]),
], className="container-fluid mt-3")

app.layout = v1_layout


def search(movie_title):
    """
    Search information about a movie
    Args:
        movie_title: title of the movie
    Returns:
        Information of the movie
    """
    dataset = dataiku.Dataset(DATASET_NAME)
    table_name = dataset.get_location_info().get('info', {}).get('quotedResolvedTableName')
    executor = SQLExecutor2(dataset=dataset)
    tid = Constant(str(movie_title))
    escaped_tid = toSQL(tid, dialect=Dialects.POSTGRES)  # Replace by your DB
    query_reader = executor.query_to_iter(
        f"""SELECT "Poster_Link", "Series_Title", "Released_Year", "Overview", "Genre" FROM {table_name} WHERE "Series_Title" = {escaped_tid}""")
    for tupl in query_reader.iter_tuples():
        return tupl
    return None


@app.callback([
    Output("image", "src"),
    Output("title", "children"),
    Output("year", "children"),
    Output("genre", "children"),
    Output("overview", "value")
],
    Input("search", "n_clicks"),
    State("features", "value"),
    Input("movie", "value"),
    prevent_initial_call=True,
    running=[(Output("search-toast", "is_open"), True, False),
             (Output("search", "disabled"), True, False),
             (Output("generate", "disabled"), True, False)
             ]
)
def gather_information(_, value, title):
    info = search(title)
    if info:
        return [info[0], info[1], info[2], info[4], info[3]]
    else:
        return ["", "", "", "", f"""No information concerning the movie: "{title}" """]


@app.callback([
    Output("generatedImg", "src"),
],
    Input("generate", "n_clicks"),
    State("title", "children"),
    State("year", "children"),
    State("genre", "children"),
    State("overview", "value"),
    State("features", "value"),
    prevent_initial_call=True,
    running=[(Output("generate-toast", "is_open"), True, False),
             (Output("search", "disabled"), True, False),
             (Output("generate", "disabled"), True, False)
             ],
)
def generate_image(_, title, year, genre, overview, features):
    prompt = "Generate a poster movie."
    if USE_TITLE in features:
        prompt = f"""${prompt} The title of the movie is: "{title}." """
    if USE_YEAR in features:
        prompt = f"""${prompt} The film was released in: "{year}." """
    if USE_GENRE in features:
        prompt = f"""${prompt} The film genre is: "{year}." """
    if USE_OVERVIEW in features:
        prompt = f"""${prompt} The film synopsis is: "{overview}." """

    img = imagellm.new_images_generation().with_prompt(prompt)
    response = img.execute()
    if response.success:
        return ['data:image/png;base64,' + base64.b64encode(response.first_image()).decode('utf-8')]
    return no_update
