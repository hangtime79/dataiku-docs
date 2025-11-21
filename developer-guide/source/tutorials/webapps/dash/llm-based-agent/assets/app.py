from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State
from dash import no_update
from dash import set_props

import dataiku
from dataiku.langchain.dku_llm import DKUChatModel
from dataiku import SQLExecutor2
from dataiku.sql import Constant, toSQL, Dialects
from duckduckgo_search import DDGS
from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import BaseTool, StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Type

from textwrap import dedent

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app.config.external_stylesheets = [dbc.themes.SUPERHERO, dbc_css]

LLM_ID = ""  # Fill in with a valid LLM ID
DATASET_NAME = "pro_customers_sql"
VERSION = "V3"

llm = DKUChatModel(llm_id=LLM_ID, temperature=0)


class CustomerInfo(BaseModel):
    """Parameter for GetCustomerInfo"""
    id: str = Field(description="customer ID")


class GetCustomerInfo(BaseTool):
    """Gathering customer information"""

    name: str = "GetCustomerInfo"
    description: str = "Provide a name, job title and company of a customer, given the customer's ID"
    args_schema: Type[BaseModel] = CustomerInfo

    def _run(self, id: str):
        dataset = dataiku.Dataset(DATASET_NAME)
        table_name = dataset.get_location_info().get('info', {}).get('quotedResolvedTableName')
        executor = SQLExecutor2(dataset=dataset)
        cid = Constant(str(id))
        escaped_cid = toSQL(cid, dialect=Dialects.POSTGRES)  # Replace by your DB
        query_reader = executor.query_to_iter(
            f"""SELECT "name", "job", "company" FROM {table_name} WHERE "id" = {escaped_cid}""")
        for (name, job, company) in query_reader.iter_tuples():
            return f"The customer's name is \"{name}\", holding the position \"{job}\" at the company named {company}"
        return f"No information can be found about the customer {id}"

    def _arun(self, id: str):
        raise NotImplementedError("This tool does not support async")


class CompanyInfo(BaseModel):
    """Parameter for the GetCompanyInfo"""
    name: str = Field(description="Company's name")


class GetCompanyInfo(BaseTool):
    """Class for gathering in the company information"""

    name: str = "GetCompanyInfo"
    description: str = "Provide general information about a company, given the company's name."
    args_schema: Type[BaseModel] = CompanyInfo

    def _run(self, name: str):
        results = DDGS().text(name + " (company)", max_results=1)
        result = "Information found about " + name + ": " + results[0]["body"] + "\n" \
            if len(results) > 0 and "body" in results[0] \
            else None
        if not result:
            results = DDGS().text(name, max_results=1)
            result = "Information found about " + name + ": " + results[0]["body"] + "\n" \
                if len(results) > 0 and "body" in results[0] \
                else "No information can be found about the company " + name
        return result

    def _arun(self, name: str):
        raise NotImplementedError("This tool does not support async")


tools = [GetCustomerInfo(), GetCompanyInfo()]
tool_names = [tool.name for tool in tools]

# Initializes the agent
prompt = ChatPromptTemplate.from_template(
    """Answer the following questions as best you can. You have only access to the following tools:
{tools}
Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
Begin!
Question: {input}
Thought:{agent_scratchpad}""")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools,
                               verbose=True, return_intermediate_steps=True, handle_parsing_errors=True)

# build your Dash app
v1_layout = html.Div([
    dbc.Row([html.H2("Using LLM-based agent with Dash"), ]),
    dbc.Row(dbc.Label("Please enter the login of the customer:")),
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
    dcc.Store(id="step", data=[{"current_step": 0}]),
], className="container-fluid mt-3")

app.layout = v1_layout


def search_V1(customer_id):
    """
    Search information about a customer
    Args:
        customer_id: customer ID
    Returns:
        the agent result
    """
    return agent_executor.invoke({
        "input": f"""Give all the professional information you can about the customer with ID: {customer_id}. 
        Also include information about the company if you can.""",
        "tools": tools,
        "tool_names": tool_names
    })['output']


def search_V2(customer_id):
    """
    Search information about a customer
    Args:
        customer_id: customer ID
    Returns:
        the agent result
    """
    iterator = agent_executor.iter({
        "input": f"""Give all the professional information you can about the customer with ID: {customer_id.strip()}. 
        Also include information about the company if you can.""",
        "tools": tools,
        "tool_names": tool_names
    })
    return iterator


def search_V3(customer_id):
    """
    Search information about a customer
    Args:
        customer_id: customer ID
    Returns:
        the agent result
    """
    actions = ""
    steps = ""
    output = ""
    iterator = agent_executor.stream({
        "input": f"""Give all the professional information you can about the customer with ID: {customer_id.strip()}. 
        Also include information about the company if you can.""",
        "tools": tools,
        "tool_names": tool_names
    })
    for i in iterator:
        if "output" in i:
            output = i['output']
        elif "actions" in i:
            for action in i["actions"]:
                actions = action.log
        elif "steps" in i:
            for step in i['steps']:
                steps = step.observation
        yield [actions, steps, output]




@app.callback(
    Output("result", "value", allow_duplicate=True),
    Input("search", "n_clicks"),
    State("customer_id", "value"),
    prevent_initial_call=True,
    running=[(Output("auto-toast", "is_open"), True, False),
             (Output("search", "disabled"), True, False)],
)
def search(_, customer_id):
    if VERSION == "V1":
        return search_V1(customer_id)
    elif VERSION == "V2":
        iterator = list(search_V2(customer_id))
        actions = ""
        for value in iterator:
            if 'intermediate_step' in value:
                for action in value['intermediate_step']:
                    actions = f"{actions}\n{action[0].log}\n{'*' * 80}"
            if 'output' in value:
                actions = f"{actions}\nFinal Result:\n\n{value['output']}"
        return actions
    else:
        global generator
        generator = search_V3(customer_id)
        value = next(generator)
        set_props("step", {"current_step": 1})
        return value[0]


@app.callback(
    Output("result", "value", allow_duplicate=True),
    Input("step", "current_step"),
    State("result", "value"),
    prevent_initial_call=True,
    running=[(Output("auto-toast", "is_open"), True, False),
             (Output("search", "disabled"), True, False)],
)
def next_value(n, old_text):
    value = next(generator, None)
    if value:
        new_text = f"""Action: {dedent(value[0])}
        Tool Result: {dedent(value[1])}
        ## Final Result: {dedent(value[2])}
        {'-' * 80}
        {old_text}
        """
        new_text = dedent(new_text)
        set_props("step", {"current_step": n + 1})

        return new_text
    else:
        return no_update