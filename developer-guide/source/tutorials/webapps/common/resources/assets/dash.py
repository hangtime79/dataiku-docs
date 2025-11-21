import dash
from dash import html
from dash import dcc
from dash.dependencies import Input
from dash.dependencies import Output
import dataiku
import base64

import logging

logger = logging.getLogger(__name__)

folder_name = "Resources"
image_name = "/image.png"
pdf_name = "/document.pdf"
css_name = "/my-css.css"

# use the style of examples on the Plotly documentation
app.config.external_scripts = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"]
app.config.external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css",
                                   "/local/static/my-css.css",
                                   f"/local/projects/{dataiku.default_project_key()}/resources/my-css.css"
                                   ]


def make_accordion_item(parent_name, name, title, content):
    """ Helper to make an accordion object

    Args:
        parent_name (str): id of the accordion parent
        name (str): name of the accordion (must be unique)
        title (str): title for the accordion item
        content (object): the content of the accordion

    Returns:
        an html.Div containing the accordion item
    """
    return html.Div([
        html.H2([html.Button([title],
                             className="accordion-button", type="button",
                             **{"data-bs-toggle": "collapse", "data-bs-target": f"#collapse{name}",
                                "aria-expanded": "false", "aria-controls": f"collapse{name}"}
                             )], className="accordion-header", id=f"{name}"),
        html.Div([html.Div([content], className="accordion-body")],
                 id=f"collapse{name}", className="accordion-collapse collapse",
                 **{"aria-labelledby": f"{name}", "data-bs-parent": f"#{parent_name}"}
                 )], className="accordion-item")


def get_image_from_managed_folder():
    """ Read a Png image and return the encoded version

    Returns:
        a base64 encoded image
    """
    folder = dataiku.Folder(folder_name)

    with folder.get_download_stream(image_name) as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


@app.callback(
    Output("downloadManagedFolder", "data"),
    Input("btnImageManagedFolder", "n_clicks"),
    prevent_initial_call=True,
)
def download_file(_):
    """Serve a file

    Args:
        _ : not use

    Returns:
        the file
    """
    folder = dataiku.Folder(folder_name)

    with folder.get_download_stream(pdf_name) as f:
        file = f.read()
    return dcc.send_bytes(file, pdf_name[1:])


# build your Dash app
app.layout = html.Div(children=[
    html.H2("From external resources", className="display-2"),
    html.Div([
        make_accordion_item('externalURL', 'displayImage', "Display an image",
                            html.Div([html.Div(["You can use images coming from an URL by using the classical ",
                                                html.Code('html.Img(src="URL_TO_USE", alt="Alternate text")')]),
                                      html.Img(src="https://picsum.photos/200/300", alt="Image to display")])),
    ], className="accordion", id="externalURL"),

    html.H2("From managed folders", className="display-2"),
    html.Div([
        make_accordion_item('managedFolder', 'displayImageManagedFolder', "Display an image",
                            html.Div([html.Div([
                                "You can use images coming from a managed folder by using the classical, in conjunction with a python funtion ",
                                html.Code(
                                    'html.Img(src=function_that_returns_the_image, alt="Alternate text")')]),
                                html.Img(src=get_image_from_managed_folder(), alt="Image to display",
                                         className="container")])),
        make_accordion_item('managedFolder', 'downloadFileManagedFolder', "Download a file",
                            html.Div([html.P([
                                "For downloading a file, you should use the html.Download, and a button to activate the download"]),
                                html.Button("Get the file", className="btn btn-primary",
                                            id="btnImageManagedFolder"),
                                dcc.Download(id="downloadManagedFolder")])),
        make_accordion_item('managedFolder', 'cssFromManagedFolder', "Use your own CSS",
                            html.Div([html.P(["You can not use a CSS file defined in a managed folder"]),
                                      ])),
    ], className="accordion", id="managedFolder"),

    html.H2("From resources in project library ", className="display-2"),
    html.Div([
        make_accordion_item('projectLib', 'displayImageProjectLib', 'Display an image',
                            html.Div([html.Div(
                                ["You use images coming from resources in the project library by using the classical:",
                                 html.Code("""html.Img(src="URLOfTheResources", alt="Alternate text)""")]),
                                html.Img(
                                    src=f"/local/projects/{dataiku.default_project_key()}/resources/image.jpg"),
                            ])
                            ),
        make_accordion_item('projectLib', 'downloadFileProjectLib', 'Download a file',
                            html.Div([html.P(
                                "To be able to use the resources folder in project library, you need to fallback to the usage of the A tag. "),
                                html.A(children=[
                                    html.Span("Get the PDF", className="btn btn-primary")
                                ], href=f"/local/projects/{dataiku.default_project_key()}/resources/file.pdf",
                                    download="file.pdf")])),
        make_accordion_item('projectLib', 'cssFromProjectLib', "Use your own CSS",
                            html.Div([html.P(
                                ["You just need to adapt the app.config.external_stylesheets to your needs"],
                                className="devadvocate-alert2"),
                            ])),
    ], className="accordion", id="projectLib"),

    html.H2("Global shared Code", className="display-2"),
    html.Div([
        make_accordion_item('managedFolder', 'displayImageGlobalSharedCode', "Display an image",
                            html.Div([html.Div([
                                "You can use images coming from the Global shared Code by using the classical path ('/local/static/...') ",
                                html.Code('html.Img(src="URL_TO_USE", alt="Alternate text")')]),
                                html.Img(src="/local/static/image.jpg", alt="Image to display",
                                         className="container")])),
        make_accordion_item('managedFolder', 'downloadFileGlobalSharedCode', "Download a file",
                            html.Div([html.P(
                                "To be able to use the global shared code folder, you need to fallback to the usage of the A tag. "),
                                html.A(children=[
                                    html.Span("Get the PDF", className="btn btn-primary")
                                ], href="/static/local/file.pdf", download="file.pdf")])),
        make_accordion_item('managedFolder', 'cssFromGlobalSharedCode', "Use your own CSS",
                            html.Div([html.P(
                                ["You just need to adapt the app.config.external_stylesheets to your needs"],
                                className="devadvocate-alert"),
                            ])),
    ], className="accordion", id="globalSharedCode")

], className="container")