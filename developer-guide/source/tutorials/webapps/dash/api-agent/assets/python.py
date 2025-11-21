import dataiku, dataikuapi

API_KEY=""
DATAIKU_LOCATION = "" #http(s)://DATAIKU_HOST:DATAIKU_PORT
PROJECT_KEY = ""
WEBAPP_ID = ""


# If you are outside Dataiku use this function call
client = dataikuapi.DSSClient(DATAIKU_LOCATION, API_KEY)

# If you are inside Dataiku you can use this function call
client = dataiku.api_client()


project = client.get_project(PROJECT_KEY)
webapp = project.get_webapp(WEBAPP_ID)
backend = webapp.get_backend_client()

# To filter on one user
print(backend.session.get(backend.base_url + '/get_customer_info/fdouetteau').text)