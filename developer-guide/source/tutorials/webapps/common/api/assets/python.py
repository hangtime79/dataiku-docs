import dataiku, dataikuapi

API_KEY=""
DATAIKU_LOCATION = "" #http(s)://DATAIKU_HOST:DATAIKU_PORT
PROJECT_KEY = ""
WEBAPP_ID = ""


# Depending on your case, use one of the following

#client = dataikuapi.DSSClient(DATAIKU_LOCATION, API_KEY)
client = dataiku.api_client()


project = client.get_project(PROJECT_KEY)
webapp = project.get_webapp(WEBAPP_ID)
backend = webapp.get_backend_client()

# To retrieve all users
print(backend.session.get(backend.base_url + '/get_customer_info').text)

# To filter on one user
print(backend.session.get(backend.base_url + '/get_customer_info?id=fdouetteau').text)