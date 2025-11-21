import dataiku
from langchain_core.messages import HumanMessage, SystemMessage

client = dataiku.api_client()
project = client.get_default_project()
llm_list = project.list_llms()
for llm in llm_list:
    print(f"- {llm.description} (id: {llm.id})")

LLM_ID = ""  # Fill with a valid LLM_ID
llm = project.get_llm(LLM_ID)
lcllm = llm.as_langchain_llm()
lcllmResp = lcllm.invoke("When was the movie Citizen Kane released?")
print(lcllmResp)

question = "When was the movie Citizen Kane released?"
system_msg = """You are an expert in the history of American cinema.
You always answer questions with a lot of passion and enthusiasm.
"""

messages = [
    SystemMessage(content=system_msg),
    HumanMessage(content=question)
]

lcllmResp = lcllm.invoke(messages)
print(lcllmResp)