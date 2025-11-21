import dataiku

KB_ID = ""  # Replace with your KB id

client = dataiku.api_client()
project = client.get_default_project()
kb = dataiku.KnowledgeBank(id=KB_ID,
    project_key=project.project_key)
vector_store = kb.as_langchain_vectorstore()
query = "Summarize the current global status on inflation."
search_result = vector_store.similarity_search(query, include_metadata=True)

for r in search_result:
    print(r.json())
