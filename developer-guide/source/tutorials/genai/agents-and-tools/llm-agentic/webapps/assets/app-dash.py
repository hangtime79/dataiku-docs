import dataiku
from dash import html, dcc, no_update, set_props
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import json
from utils import get_customer_details, search_company_info, process_tool_calls, create_chat_session

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app.config.external_stylesheets = [dbc.themes.SUPERHERO, dbc_css]

# LLM setup
LLM_ID = ""  # LLM ID for the LLM Mesh connection + model goes here
client = dataiku.api_client()
project = client.get_default_project()
llm = project.get_llm(LLM_ID)

# Dash app layout
app.layout = html.Div([
    dbc.Row([html.H2("Using LLM Mesh with an agent in Dash")]),
    dbc.Row(dbc.Label("Please enter the ID of the customer:")),
    dbc.Row([
        dbc.Col(dbc.Input(id="customer_id", placeholder="Customer Id"), width=10),
        dbc.Col(dbc.Button("Search", id="search", color="primary"), width="auto")
    ], justify="between"),
    dbc.Row([dbc.Col(dbc.Textarea(id="result", style={"min-height": "500px"}), width=12)]),
    dbc.Toast(
        [html.P("Searching for information about the customer", className="mb-0"),
         dbc.Spinner(color="primary")],
        id="auto-toast",
        header="Agent working",
        icon="primary",
        is_open=False,
        style={"position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)"},
    ),
    dcc.Store(id="chat-state"),
    dcc.Store(id="step", data={"current_step": 0}),
], className="container-fluid mt-3")

@app.callback(
    [Output("result", "value"), Output("chat-state", "data")],
    Input("search", "n_clicks"),
    [State("customer_id", "value"), State("chat-state", "data")],
    prevent_initial_call=True,
    running=[(Output("auto-toast", "is_open"), True, False),
             (Output("search", "disabled"), True, False)]
)

def update_output(n_clicks, customer_id, chat_state):
    """Callback function that handles agent interactions"""
    if not customer_id:
        return no_update, no_update
    
    # Create new chat session
    chat = create_chat_session(llm, project)
    
    # Start conversation about customer
    content = f"Tell me about the customer with ID {customer_id}"
    chat.with_message(content, role="user")
    
    conversation_log = []
    while True:
        response = chat.execute()
        
        if not response.tool_calls:
            # Final answer received
            chat.with_message(response.text, role="assistant")
            conversation_log.append(f"Final Answer: {response.text}")
            break
            
        # Handle tool calls
        chat.with_tool_calls(response.tool_calls, role="assistant")
        tool_call_result = process_tool_calls(response.tool_calls)
        chat.with_tool_output(tool_call_result, tool_call_id=response.tool_calls[0]["id"])
        
        # Log the step
        tool_name = response.tool_calls[0]["function"]["name"]
        tool_args = response.tool_calls[0]["function"]["arguments"]
        conversation_log.append(f"Tool: {tool_name}\nInput: {tool_args}\nResult: {tool_call_result}\n{'-'*50}")
    
    return "\n".join(conversation_log), {"messages": chat.cq["messages"]}