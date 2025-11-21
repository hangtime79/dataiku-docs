import dataiku
import ipywidgets as widgets
import json
import os
from utils import get_customer_details, search_company_info, process_tool_calls, create_chat_session

# LLM setup
LLM_ID = ""  # LLM ID for the LLM Mesh connection + model goes here
client = dataiku.api_client()
project = client.get_default_project()
llm = project.get_llm(LLM_ID)

def process_agent_response(chat, query):
    """Process the agent's response and handle any tool calls"""
    chat.with_message(query, role="user")
    
    while True:
        response = chat.execute()
        
        if not response.tool_calls:
            # Final answer received
            chat.with_message(response.text, role="assistant")
            chat = create_chat_session(llm, project) # refresh chat
            return response.text
            
        # Handle tool calls
        chat.with_tool_calls(response.tool_calls, role="assistant")
        tool_name = response.tool_calls[0]["function"]["name"]
        tool_args = response.tool_calls[0]["function"]["arguments"]
        
        # Process tool call and get result
        tool_call_result = process_tool_calls(response.tool_calls)
        chat.with_tool_output(tool_call_result, tool_call_id=response.tool_calls[0]["id"])


# Create widgets
label = widgets.Label(value="Enter your query about a customer")
query_input = widgets.Text(
    placeholder="Tell me about customer fdouetteau",
    continuous_update=False,
    layout=widgets.Layout(width='50%')
)
result = widgets.HTML(value="")
button = widgets.Button(description="Ask")

# Create the chat session
chat = create_chat_session(llm, project)

def on_button_click(b):
    """Handle button click event"""
    query = query_input.value
    if query:
        try:
            response = process_agent_response(chat, query)
            result.value = f"<div style='white-space: pre-wrap;'>{response}</div>"
        except Exception as e:
            result.value = f"<div style='color: red'>Error: {str(e)}</div>"
            
button.on_click(on_button_click)

# Layout
display(widgets.VBox([
    widgets.HBox([label]),
    widgets.HBox([query_input, button]),
    widgets.HBox([result])
], layout=widgets.Layout(padding='20px')))
