import gradio as gr
import os
import re

import dataiku
from dataiku.langchain.dku_llm import DKUChatModel
from dataiku import SQLExecutor2
from dataiku.sql import Constant, toSQL, Dialects
from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import BaseTool, StructuredTool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional, Type

from duckduckgo_search import DDGS


LLM_ID = "" # Fill in with a valid LLM ID
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

    name:str = "GetCompanyInfo"
    description:str = "Provide general information about a company, given the company's name."
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


async def search_V2(customer_id):
    """
    Search information about a customer
    Args:
        customer_id: customer ID

    Returns:
        the agent result
    """
    iterator = agent_executor.stream({
        "input": f"""Give all the professional information you can about the customer with ID: {customer_id.strip()}. 
        Also include information about the company if you can.""",
        "tools": tools,
        "tool_names": tool_names
    })
    for i in iterator:
        if "output" in i:
            yield i['output']
        else:
            yield i


async def search_V3(customer_id):
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


if VERSION == "V1":
    demo = gr.Interface(
        fn=search_V1,
        inputs=gr.Textbox(label="Enter a customer ID to get more information", placeholder="ID Here..."),
        outputs="text"
    )

if VERSION == "V2":
    demo = gr.Interface(
        fn=search_V2,
        inputs=gr.Textbox(label="Enter a customer ID to get more information", placeholder="ID Here..."),
        outputs="text"
    )

if VERSION == "V3":
    demo = gr.Interface(
        fn=search_V3,
        inputs=gr.Textbox(label="Enter a customer ID to get more information", placeholder="ID Here..."),
        outputs=[
            gr.Textbox(label="Agent thought"),
            gr.Textbox(label="Tool Result"),
            gr.Textbox(label="Final result")]
    )

browser_path = os.getenv("DKU_CODE_STUDIO_BROWSER_PATH_7860")
# replacing env var keys in browser_path with their values
env_var_pattern = re.compile(r'(\${(.*)})')
env_vars = env_var_pattern.findall(browser_path)
for env_var in env_vars:
    browser_path = browser_path.replace(env_var[0], os.getenv(env_var[1], ''))

# WARNING: make sure to use the same params as the ones defined below when calling the launch method,
# otherwise you app might not be responding!
demo.queue().launch(server_port=7860, root_path=browser_path)
