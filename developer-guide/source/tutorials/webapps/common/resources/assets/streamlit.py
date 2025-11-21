import streamlit as st
import dataiku
import io

import logging

logger = logging.getLogger(__name__)

host = "http://<dataikuURL>:<port>/"
folder = "Resources"
image = "/image.jpg"
pdf = "/file.pdf"
css = "/my-css.css"


def get_file_from_managed_folder(folder_name, file_name):
    """
    Retrieves a file from a managed folder

    :param folder_name: name of the folder to retrieve the file from
    :param file_name: name of the file to retrieve
    Returns:
        the file.
    """
    folder = dataiku.Folder(folder_name)

    with folder.get_download_stream(file_name) as f:
        return (f.read())


def get_global_shared_file_url(file):
    """
    Retrieves a file from the static web resources
    Args:
        file: the file to retrieve.

    Returns:
        the URL to the static web resources file
    """
    return host + '/local/static/' + file


st.title('Uses resources')
st.markdown("""## From external URL""")
with st.container():
    st.write("### Display an image")
    st.image("https://source.unsplash.com/random/1920x1080/?cat=")

st.markdown("""## From managed folder""")
with st.container():
    st.write("### Display an image")
    st.image(get_file_from_managed_folder(folder, image))

with st.container():
    st.write("### Serving a file")
    st.download_button("Get the PDF", data=get_file_from_managed_folder(folder, pdf), file_name=pdf)

with st.container():
    st.write("### Use your own CSS")
    st.write("At the moment, there's no easy way to add an id/class to a streamlit element. However, if you want to use CSS, simply load it like any other file.")

st.markdown("""## From Global shared code""")

with st.container():
    st.write("### Display an image")
    st.image(get_global_shared_file_url(image))

with st.container():
    st.write("### Serving a file")
    st.download_button("Get the PDF", data=get_global_shared_file_url(pdf), file_name=pdf)

with st.container():
    st.write("### Use your own CSS")
    st.write("At the moment, there's no easy way to add an id/class to a streamlit element. However, if you want to use CSS, simply load it like any other file.")

st.markdown("""## From Code studios resources""")

with st.container():
    st.write("### Display an image")
    with open('../../code_studio-resources/image.jpg', 'rb') as f:
        st.image(image=io.BytesIO(f.read()))

with st.container():
    st.write("### Serving a file")
    with open('../../code_studio-resources/file.pdf', 'rb') as f:
        st.download_button("Get the PDF", data=io.BytesIO(f.read()), file_name="file.pdf")

with st.container():
    st.write("### Use your own CSS")
    st.write("At the moment, there's no easy way to add an id/class to a streamlit element. However, if you want to use CSS, simply load it like any other file.")

st.markdown("## From project resources")

with st.container():
    st.write("### Display an image (using URL)")
    st.image(f"{host}/local/projects/{dataiku.api_client().get_default_project().project_key}/resources/image.jpg")

    st.write("### Display an image (using the Code studio location)")
    with open('../../project-lib-resources/static/image.jpg', 'rb') as f:
        st.image(image=io.BytesIO(f.read()))


with st.container():
    st.write("### Serving a file")
    with open('../../project-lib-resources/static/file.pdf', 'rb') as f:
        st.download_button("Get the PDF", data=io.BytesIO(f.read()), file_name="file.pdf", key="download_button")

with st.container():
    st.write("### Use your own CSS")
    st.write("At the moment, there's no easy way to add an id/class to a streamlit element. However, if you want to use CSS, simply load it like any other file.")
