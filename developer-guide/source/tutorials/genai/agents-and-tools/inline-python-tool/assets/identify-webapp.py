import dataiku

client = dataiku.api_client()
project = client.get_default_project()

for webapp in project.list_webapps():
    print(f"WebApp id: {webapp['id']} name: {webapp['name']}")
