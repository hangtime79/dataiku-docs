import dataiku

client = dataiku.api_client()
project = client.get_default_project()
llm_list = project.list_llms()
for llm in llm_list:
    print(f"- {llm.description} (id: {llm.id})")

LLM_ID = ""  # Fill with a valid LLM_ID
llm = project.get_llm(LLM_ID)

completion = llm.new_completion()
resp = completion.with_message("Q1: When was the movie Citizen Kane released?").execute()
if resp.success:
    print(resp.text)
else:
    print("Something went wrong. Check you have the permission to use the LLM.")

completion = llm.new_completion()
question = "When was the movie Citizen Kane released?"
system_msg = """You are an expert in the history of American cinema.
You always answer questions with a lot of passion and enthusiasm.
"""

resp = completion.with_message(role="system", message=system_msg).with_message(role="user", message=question).execute()
if resp.success:
    print(resp.text)
else:
    print("Something went wrong. Check you have the permission to use the LLM.")
