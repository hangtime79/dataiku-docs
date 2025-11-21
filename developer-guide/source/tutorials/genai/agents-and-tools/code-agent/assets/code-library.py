from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
import dataiku
from dataiku.llm.python import BaseLLM
from tools.tutorial import get_customer_details, search_company_info

OPENAI_CONNECTION_NAME = "REPLACE_WITH_YOUR_CONNECTION_NAME"  # example: "openAI"


@tool
def get_customer(customer: str) -> str:
    """Get customer name, position and company information from database.
    The input is a customer id (stored as a string).
    The ouput is a string of the form:
        "The customer's name is \"{name}\", holding the position \"{job}\" at the company named {company}"
    """
    return get_customer_details(customer)


@tool
def search_company(company: str) -> str:
    """
    Use this tool when you need to retrieve information on a company.
    The input of this tool is the company name.
    The ouput is either a small recap of the company or "No information ..." meaning that we couldn't find information about this company
    """
    return search_company_info(company)


tools = [get_customer, search_company]


class MyLLM(BaseLLM):
    def __init__(self):
        pass

    def process(self, query, settings, trace):
        project = dataiku.api_client().get_default_project()
        llm = project.get_llm(f"openai:{OPENAI_CONNECTION_NAME}:gpt-5-mini").as_langchain_chat_model(completion_settings=settings)
        llm_with_tools = llm.bind_tools(tools)

        messages = [m for m in query["messages"] if m.get("content")]
        iterations = 0
        while True:
            iterations += 1
            if iterations < 10:
                with trace.subspan("Invoke LLM with tools") as llm_invoke_span:
                    llm_response = llm_with_tools.invoke(messages)
            else:
                with trace.subspan("Invoke LLM without tools") as llm_invoke_span:
                    llm_response = llm.invoke(messages)

            if len(llm_response.tool_calls) == 0:
                return {"text": llm_response.content}

            with llm_invoke_span.subspan("Call the tools") as tools_subspan:
                messages.append(llm_response)
                for tool_call in llm_response.tool_calls:
                    with tools_subspan.subspan("Call a tool") as tool_subspan:
                        tool_subspan.attributes["tool_name"] = tool_call["name"]
                        tool_subspan.attributes["tool_args"] = tool_call["args"]
                        if tool_call["name"] == "get_customer":
                            tool_output = get_customer.invoke(tool_call["args"])
                        elif tool_call["name"] == "search_company":
                            tool_output = search_company.invoke(tool_call["args"])
                        else:
                            raise ValueError("unknown tool: " + tool_call["name"])
                    messages.append(ToolMessage(tool_call_id=tool_call["id"], content=tool_output))
