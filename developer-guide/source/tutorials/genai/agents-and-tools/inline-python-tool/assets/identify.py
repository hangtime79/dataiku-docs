import dataiku

client = dataiku.api_client()
project = client.get_default_project()

project.list_agent_tools()
