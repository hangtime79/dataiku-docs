import dataiku
import json
from dataiku import SQLExecutor2
from dataiku.sql import Constant, toSQL, Dialects
from duckduckgo_search import DDGS

def create_chat_session(llm, project):
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
    
    When looking up customer info, you will:
    1. First get customer details
    2. Then look up their company
    3. Summarize in a single paragraph with details on both"""
    
    chat.with_message(SYSTEM_PROMPT, role="system")
    return chat


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
