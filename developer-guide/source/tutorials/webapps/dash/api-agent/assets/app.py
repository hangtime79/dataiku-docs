from dash import html

import dataiku
from dataiku.langchain.dku_llm import DKUChatModel

from langchain.tools import BaseTool
from dataiku import SQLExecutor2
from dataiku.sql import Constant, toSQL, Dialects
from langchain.pydantic_v1 import BaseModel, Field
from typing import Type
from duckduckgo_search import DDGS

from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_react_agent

LLM_ID = "<A valid LLM ID>"  # Replace with a valid LLM id

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
        dataset = dataiku.Dataset("pro_customers_sql")
        table_name = dataset.get_location_info().get('info', {}).get('quotedResolvedTableName')
        executor = SQLExecutor2(dataset=dataset)
        cid = Constant(str(id))
        escaped_cid = toSQL(cid, dialect=Dialects.POSTGRES)  # Replace by your DB
        query_reader = executor.query_to_iter(
            f"""SELECT "name", "job", "company" FROM {table_name} WHERE "id" = {escaped_cid}""")
        for (name, job, company) in query_reader.iter_tuples():
            return f"The customer's name is \"{name}\", holding the position \"{job}\" at the company named {company}"
        return f"No information can be found about the customer {id}"

    def _arun(self, name: str):
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


# Initializes the agent
# Link the tools
tools = [GetCustomerInfo(), GetCompanyInfo()]
tool_names = [tool.name for tool in tools]

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


@app.server.route("/get_customer_info/<customer_id>")
def get_customer_info(customer_id):
    """
    Ask the agent to retrieve information about the customer

    Args:
        customer_id: the customer ID

    Returns:
        Information about the customer
    """
    return agent_executor.invoke(
        {
            "input": f"""Give all the professional information you can about the customer with ID: {customer_id}. Also include information about the company if you can.""",
            "tools": tools,
            "tool_names": tool_names
        })["output"]


# build your Dash app
app.layout = html.Div()
