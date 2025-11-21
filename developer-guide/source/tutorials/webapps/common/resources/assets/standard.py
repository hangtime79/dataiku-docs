import dataiku
import pandas as pd
from flask import request

# Definition of the various resources (This can be done programmatically)
# ## Name of the managed folder
folder = "Resources"
# ## Path name of the files
image = "/image.png"
pdf = "/document.pdf"
css = "/my-css.css"


def get_file_from_managed_folder(folder_name, file_name):
    """
    Retrieve the file from the managed folder
    Args:
        folder_name: name of the managed folder
        file_name: name of the file

    Returns:
        the file
    """
    folder = dataiku.Folder(folder_name)

    with folder.get_download_stream(file_name) as f:
        return (f.read())

@app.route('/get_image_from_managed_folder')
def get_image_from_managed_folder():
    return get_file_from_managed_folder(folder, image)

@app.route('/get_pdf_from_managed_folder')
def get_pdf_from_managed_folder():
    return get_file_from_managed_folder(folder, pdf)

@app.route('/get_css_from_managed_folder')
def get_css_from_managed_folder():
    return get_file_from_managed_folder(folder, css)

