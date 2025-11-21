import gradio as gr
import os
import re
import dataiku

LLM_ID = "YOUR_LLM_ID"

browser_path = os.getenv("DKU_CODE_STUDIO_BROWSER_PATH_7860")
env_var_pattern = re.compile(r'(\${(.*)})')
env_vars = env_var_pattern.findall(browser_path)
for env_var in env_vars:
    browser_path = browser_path.replace(env_var[0], os.getenv(env_var[1], ''))

client = dataiku.api_client()
project = client.get_default_project()
llm = project.get_llm(LLM_ID)

def chat_function(message, history):
    completion = llm.new_completion()
    completion.with_message(message="You are a helpful assistant.")
    for msg in history:
        completion.with_message(message=msg[0], role="user")
        completion.with_message(message=msg[1], role="assistant")
    completion.with_message(message=message, role="user")
    resp_text = completion.execute().text
    return resp_text


demo = gr.ChatInterface(fn=chat_function)
demo.launch(server_port=7860, root_path=browser_path)