import dataiku

client = dataiku.api_client()
project = client.get_default_project()
llm_list = project.list_llms(purpose="IMAGE_GENERATION")
for llm in llm_list:
    print(f"- {llm.description} (id: {llm.id})")

from dataiku import SQLExecutor2
from dataiku.sql import Constant, toSQL, Dialects

def search(title):
    """
    Search for information based on movie title
    Args:
        title: the movie title

    Returns:
        the image src, title, year, overview and genre of the movie.
    """
    dataset = dataiku.Dataset("movies")
    table_name = dataset.get_location_info().get('info', {}).get('quotedResolvedTableName')
    executor = SQLExecutor2(dataset=dataset)
    tid = Constant(str(title))
    escaped_tid = toSQL(tid, dialect=Dialects.POSTGRES)  # Replace by your DB
    query_reader = executor.query_to_iter(
        f"""SELECT "Poster_Link", "Series_Title", "Released_Year", "Overview", "Genre" FROM {table_name} WHERE "Series_Title" = {escaped_tid}""")
    for tupl in query_reader.iter_tuples():
        return tupl


LLM_ID = ""  # Replace with a valid LLM id

imagellm = dataiku.api_client().get_default_project().get_llm(LLM_ID)
movie = search('Citizen Kane')
img = imagellm.new_images_generation().with_prompt(f"""
Generate a poster movie. The size of the poster should be 120x120px. 
The title of the movie is: "{movie[1]}."
The year of the movie is: "{movie[2]}."
The summary is: "{movie[3]}."
The genre of the movie is: "{movie[4]}."
""")
resp = img.execute()

from IPython.display import display, Image

if resp.success:
    display(Image(resp.first_image()))
