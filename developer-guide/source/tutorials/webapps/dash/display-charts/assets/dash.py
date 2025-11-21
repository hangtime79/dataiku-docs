from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import dataiku

# READ DATASET
dataset = dataiku.Dataset("Orders_by_Country_sorted")
df = dataset.get_dataframe()
df = df[df['campaign']]

# Create the layout of the app
app.layout = html.Div([
    html.Div([
        html.H1("Total Sales by Country", style={'backgroundColor': '#5473FF', 'color': '#FFFFFF', 'width': '98vw', 'margin': 'auto', 'textAlign': 'center'}),
        html.P("This graph allows you to compare the total sales amount and campaign influence by country.", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='country-select',
            options=[{'label': country, 'value': country} for country in sorted(df['country'].unique())],
            value=['United States', 'China', 'Japan', 'Germany', 'France', 'United Kingdom'],
            multi=True,
            style={'width': '50%', 'margin': 'auto'}
        ),
        dcc.Graph(id='sales-graph')
    ])
])

# Define the callback to update the graph
@app.callback(
    Output('sales-graph', 'figure'),
    [Input('country-select', 'value')]
)
def update_figure(selected_countries):
    """
    Update the bar chart whenever the user selects one country.
    Args:
        selected_countries: all selected countries

    Returns:
        the new bar chart
    """
    filtered_df = df[df['country'].isin(selected_countries)]
    fig = px.bar(filtered_df, x='country', y='total_amount', title='Total amount per campaign')
    fig.update_layout(xaxis_title='Country', yaxis_title='Total Amount')
    return fig

