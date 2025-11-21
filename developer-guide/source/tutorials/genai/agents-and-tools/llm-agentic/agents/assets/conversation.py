import dataiku
import json
from dataiku import SQLExecutor2
from dataiku.sql import Constant, toSQL, Dialects
from duckduckgo_search import DDGS

def get_customer_details(customer_id):
    """Get customer information from database"""
    dataset = dataiku.Dataset("pro_customers_sql")
    table_name = dataset.get_location_info().get('info', {}).get('quotedResolvedTableName')
    executor = SQLExecutor2(dataset=dataset)
    cid = Constant(str(customer_id))
    escaped_cid = toSQL(cid, dialect=Dialects.POSTGRES)  # Replace by your DB
    query_reader = executor.query_to_iter(
        f"""SELECT "name", "job", "company" FROM {table_name} WHERE "id" = {escaped_cid}""")
    for (name, job, company) in query_reader.iter_tuples():
        return f"The customer's name is \"{name}\", holding the position \"{job}\" at the company named {company}"
    return f"No information can be found about the customer {customer_id}"

def search_company_info(company_name):
    """Search for company information online"""
    with DDGS() as ddgs:
        results = list(ddgs.text(f"{company_name} (company)", max_results=1))
        if results:
            return f"Information found about {company_name}: {results[0]['body']}"
        return f"No information found about {company_name}"

def process_tool_calls(tool_calls):
    """Process tool calls and return results"""
    tool_name = tool_calls[0]["function"]["name"]
    llm_args = json.loads(tool_calls[0]["function"]["arguments"])
    if tool_name == "get_customer_info":
        return get_customer_details(llm_args["customer_id"])
    elif tool_name == "get_company_info":
        return search_company_info(llm_args["company_name"])

def create_chat_session():
    """Create a new chat session with tools and prompt"""
    chat = llm.new_completion()
    
    # Import tools from JSON file
    library = project.get_library()
    tools_file = library.get_file("/python/tools.json")
    tools_str = tools_file.read()
    tools_dict = json.loads(tools_str)

    chat.settings["tools"] = tools_dict["tools"]
    
    SYSTEM_PROMPT = """You are a customer information assistant. You can:
    1. Look up customer information in our database
    2. Search for additional information about companies online

    When asked about a customer:
    1. First look up their basic information
    2. If company information is requested, search for additional details
    3. Combine the information into a coherent, single-paragraph response"""
    
    chat.with_message(SYSTEM_PROMPT, role="system")
    return chat

def process_query(query):
    """Process a user query using the agent"""
    chat = create_chat_session()

    chat.with_message(query, role="user")

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
    
    return "\n".join(conversation_log)

PROJECT = ""  # Dataiku project key goes here
client = dataiku.api_client()
project = client.get_project(PROJECT)
LLM_ID = ""  # LLM ID for the LLM Mesh connection + model goes here
llm = project.get_llm(LLM_ID)

CONTENT = "Give me all the information you can find about customer with id fdouetteau"
print(process_query(CONTENT))

# Tool: get_customer_info
# Input: {"customer_id":"fdouetteau"}
# Result: The customer's name is "Florian Douetteau", holding the position "CEO" at the company named Dataiku
# --------------------------------------------------
# Tool: get_company_info
# Input: {"company_name":"Dataiku"}
# Result: Information found about Dataiku: Our Story. Dataiku is the leading platform for Everyday AI · 
# Leadership and Team · Over 1000 people work hard to ensure the quality of our product and company as ...
# --------------------------------------------------
# Final Answer: The customer, Florian Douetteau, is the CEO of Dataiku, a leading platform for Everyday AI. 
# Dataiku employs over 1,000 people dedicated to ensuring the quality of their products and services 
# in the AI domain.
