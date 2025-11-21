import dataiku
from bokeh.io import curdoc
from bokeh.models import Div, MultiSelect, ColumnDataSource, FactorRange
from bokeh.plotting import figure
from functools import partial
from bokeh.layouts import layout


def add_title():
    """
    Create the title for the application.
    :return: The title object.
    """
    title = Div(text="""<h1>Total Sales by Country</h1>""",
                style={'backgroundColor': '#5473FF',
                       'color': '#FFFFFF',
                       'width': '98vw',
                       'margin': 'auto',
                       'textAlign': 'center'})
    return title


def add_text():
    """
    Create a description of the application.
    :return: The text object.
    """
    text = Div(text="This graph allows you to compare the total sales amount and campaign influence by country.",
               sizing_mode="stretch_width",
               align="center")
    return text


def update_fig(_attr, _old, new, df, source, plot):
    """
    Callback for updating the plot with the new values.
    :param _attr: Unused: the attribute that is changed.
    :param _old: Unused: the old value.
    :param new: The new value.
    :param df: The dataframe to use.
    :param source: The columnSource to use.
    :param plot: The plot to update.
    """

    data = df[df['country'].isin(new)]
    source.data = dict(
        x=data.country,
        y=data.total_amount
    )
    plot.x_range.factors = list(source.data['x'])


def add_select(df, source, plot):
    """
    Create a Multi-select for the country selection.
    :param df: The dataframe to use.
    :param source: The columnSource to use.
    :param plot: The plot to update.
    :return: The multi-select object.
    """
    select = MultiSelect(title="Select countries:",
                         options=[i for i in sorted(df.country.unique())],
                         value=['United States', 'China', 'Japan', 'Germany', 'France', 'United Kingdom'],
                         size=10,
                         sizing_mode='stretch_width'
                         )
    select.on_change("value", partial(update_fig, df=df, source=source, plot=plot))
    return select


def application():
    """
    Create the application.
    """
    # READ DATASET
    dataset = dataiku.Dataset("Orders_by_Country_sorted")
    df = dataset.get_dataframe()
    # Only keep data where the campaign has been launched
    df = df[df['campaign']]

    source = ColumnDataSource(dict(x=[], y=[]))

    title = add_title()
    text = add_text()
    plot = add_plot(df, source)
    select = add_select(df, source, plot)

    update_fig("", "", select.value, df, source, plot)

    app = layout([title, text, select, plot])
    curdoc().add_root(app)


def add_plot(df, source):
    """
    Create a plot for rendering the selection
    :param df: The dataframe to use.
    :param source: The columnSource to use.
    :return: The plot object.
    """
    plot = figure(plot_width=600, plot_height=300,
                  x_axis_label='Country',
                  y_axis_label='Total Amount',
                  title='Total amount per campaign',
                  x_range=FactorRange(factors=list(df.country)),
                  sizing_mode='stretch_width'
                  )
    plot.left[0].formatter.use_scientific = False
    plot.xaxis.major_label_orientation = "vertical"
    plot.vbar(source=source, x='x', top='y', bottom=0, width=0.3)

    return plot


application()
