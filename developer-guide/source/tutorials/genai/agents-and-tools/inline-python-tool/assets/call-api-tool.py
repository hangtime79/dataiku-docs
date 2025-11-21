import dataiku

client = dataiku.api_client()
project = client.get_default_project()

tool =  project.get_agent_tool('rmESZYL')
result = tool.run({"prompt": "Do you know Dataiku?"})

print(result['output'])