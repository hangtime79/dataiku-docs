import dataiku
import gradio as gr
import os
import re
import json
from utils import get_customer_details, search_company_info, process_tool_calls, create_chat_session

# LLM setup
LLM_ID = ""  # LLM ID for the LLM Mesh connection + model goes here
client = dataiku.api_client()
project = client.get_default_project()
llm = project.get_llm(LLM_ID)

def chat_with_agent(message, history):
    """Chat function that handles agent interactions"""
    chat = create_chat_session(llm, project)
    
    # Add history to chat context
    for user_msg, assistant_msg in history:
        chat.with_message(user_msg, role="user")
        chat.with_message(assistant_msg, role="assistant")
    
    chat.with_message(message, role="user")
    
    while True:
        response = chat.execute()
        
        if not response.tool_calls:
            # Final answer received
            chat.with_message(response.text, role="assistant")
            return response.text
            
        # Handle tool calls
        chat.with_tool_calls(response.tool_calls, role="assistant")
        tool_name = response.tool_calls[0]["function"]["name"]
        tool_args = response.tool_calls[0]["function"]["arguments"]
        
        # Process tool call and get result
        tool_call_result = process_tool_calls(response.tool_calls)
        chat.with_tool_output(tool_call_result, tool_call_id=response.tool_calls[0]["id"])
    

# Gradio interface setup
browser_path = os.getenv("DKU_CODE_STUDIO_BROWSER_PATH_7860")
env_var_pattern = re.compile(r'(\${(.*)})')
env_vars = env_var_pattern.findall(browser_path)
for env_var in env_vars:
    browser_path = browser_path.replace(env_var[0], os.getenv(env_var[1], ''))

# Create Gradio chat interface
app = gr.ChatInterface(
    fn=chat_with_agent,
    title="Customer Information Assistant",
    description="Ask me about customers using their ID ...",
    examples=["The id is fdouetteau", 
            "Find out about id wcoyote",
             "who is customer tcook"]
)

app.launch(server_port=7860, root_path=browser_path)
