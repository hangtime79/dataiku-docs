import dataiku

client = dataiku.api_client()
project = client.get_default_project()

tool =  project.get_agent_tool('xg3bQfN')
result = tool.run({"id": "fdouetteau"})

print(result['output'])