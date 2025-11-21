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


backend.session.headers['Content-Type'] = 'application/json'

# Query the LLM
print(backend.session.post(backend.base_url + '/query', json={'message':'Coucou'}).text)