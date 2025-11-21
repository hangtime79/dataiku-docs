import dataiku
from langchain_core.messages import HumanMessage, SystemMessage

client = dataiku.api_client()
project = client.get_default_project()
llm_list = project.list_llms()
for llm in llm_list:
    print(f"- {llm.description} (id: {llm.id})")

LLM_ID = "" #Fill with a valid LLM_ID
llm = project.get_llm(LLM_ID)
chat = llm.as_langchain_chat_model()
chatResp = chat.invoke("When was the movie Citizen Kane released?")
print(chatResp.content)

question = "When was the movie Citizen Kane released?"
system_msg = """You are an expert in the history of American cinema.
You always answer questions with a lot of passion and enthusiasm.
"""

messages = [
    SystemMessage(content=system_msg),
    HumanMessage(content=question)
]

chatResp = chat.invoke(messages)
print(chatResp.content)