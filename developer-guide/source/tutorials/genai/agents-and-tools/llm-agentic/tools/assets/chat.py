import dataiku
import json
from dataiku import SQLExecutor2
from duckduckgo_search import DDGS
from dataiku.sql import Constant, toSQL, Dialects

PROJECT = "" # Dataiku project key goes here
client = dataiku.api_client()
project = client.get_project(PROJECT)
LLM_ID = "" # LLM ID for the LLM Mesh connection + model goes here
llm = project.get_llm(LLM_ID)
chat = llm.new_completion()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_info",
            "description": "Get customer details from the database given their ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The unique identifier for the customer",
                    },
                },
                "required": ["customer_id"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_company_info",
            "description": "Get company information from internet search",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "Name of the company to search for",
                    },
                },
                "required": ["company_name"],
            },
        }
    }
]

chat.settings["tools"] = tools

CONTEXT = '''
  You are a helpful assistant with access to customer and company information.
  You have two tools available:
  - get_customer_info: retrieves customer details from our database
  - get_company_info: searches the internet for company information
  Use these tools to provide comprehensive responses about customers and their companies.
'''

CONTENT = 'Who are you and what is your purpose?'

chat.with_message(CONTEXT, role="system")
chat.with_message(CONTENT, role="user")

response = chat.execute()
response.text

# I am an AI assistant designed to help you gather information about customers
# and companies. My main functions include retrieving customer details from our
# database and searching the internet for company information. If you have
# specific questions or tasks related to customers or companies, feel free to
# ask!

chat.with_message(response.text, role="assistant")

customer_id = "fdouetteau"
CONTENT = f"The customer's id is {customer_id}"
chat.with_message(CONTENT, role="user")
response = chat.execute()

tool_calls = response.tool_calls
tool_calls

# [{'type': 'function',
#   'function': {'name': 'get_customer_info',
#    'arguments': '{"customer_id":"fdouetteau"}'},
#   'id': 'call_cQECgVOCgU7OLLb5mrBOZrg5'}]

chat.with_tool_calls(tool_calls, role="assistant")

def get_customer_details(customer_id):
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
    tool_name = tool_calls[0]["function"]["name"]
    llm_args = json.loads(tool_calls[0]["function"]["arguments"])
    if tool_name == "get_customer_info":
        return get_customer_details(llm_args["customer_id"])
    elif tool_name == "get_company_info":
        return search_company_info(llm_args["company_name"])

tool_call_result = process_tool_calls(tool_calls)

chat.with_tool_output(tool_call_result, tool_call_id=tool_calls[0]["id"])

# Continue the conversation
CONTENT = "Find more information about the company from a search."

chat.with_message(CONTENT, role="user")
response = chat.execute()

tool_calls = response.tool_calls
tool_calls

# [{'type': 'function',
#   'function': {'name': 'get_company_info',
#    'arguments': '{"company_name":"Dataiku"}'},
#   'id': 'call_4lg3yspLrMdJvISnL2aBtzfn'}]

chat.with_tool_calls(tool_calls, role="assistant")

tool_call_result = process_tool_calls(tool_calls)

chat.with_tool_output(tool_call_result, tool_call_id=tool_calls[0]["id"])

# Chat history
from pprint import pprint
pprint(chat.cq["messages"], indent=2, width=80)

# [ { 'content': '\n'
#                '  You are a helpful assistant with access to customer and '
#                'company information.\n'
#                '  You have two tools available:\n'
#                '  - get_customer_info: retrieves customer details from our '
#                'database\n'
#                '  - get_company_info: searches the internet for company '
#                'information\n'
#                '  Use these tools to provide comprehensive responses about '
#                'customers and their companies.\n',
#     'role': 'system'},
#   {'content': 'Who are you and what is your purpose?', 'role': 'user'},
#   { 'content': 'I am an AI assistant designed to help you retrieve information '
#                'about customers and companies. My purpose is to provide '
#                'comprehensive and accurate responses based on the data '
#                'available in our database and from online resources. Whether '
#                "you need customer details or company information, I'm here to "
#                'assist you. How can I help you today?',
#     'role': 'assistant'},
#   {'content': "The customer's id is fdouetteau", 'role': 'user'},
#   { 'role': 'assistant',
#     'toolCalls': [ { 'function': { 'arguments': '{"customer_id":"fdouetteau"}',
#                                    'name': 'get_customer_info'},
#                      'id': 'call_OoXImpZSMNYEqe5w1QT8eFUy',
#                      'type': 'function'}]},
#   { 'role': 'tool',
#     'toolOutputs': [ { 'callId': 'call_OoXImpZSMNYEqe5w1QT8eFUy',
#                        'output': 'The customer\'s name is "Florian Douetteau", '
#                                  'holding the position "CEO" at the company '
#                                  'named Dataiku'}]},
#   { 'content': 'Find more information about the company from a search.',
#     'role': 'user'},
#   { 'role': 'assistant',
#     'toolCalls': [ { 'function': { 'arguments': '{"company_name":"Dataiku"}',
#                                    'name': 'get_company_info'},
#                      'id': 'call_9KerL9juzQMJG3s8FN31yOdo',
#                      'type': 'function'}]},
#   { 'role': 'tool',
#     'toolOutputs': [ { 'callId': 'call_9KerL9juzQMJG3s8FN31yOdo',
#                        'output': 'Information found about Dataiku: Dataiku is '
#                                  'the leading platform for Everyday AI ... '
#                                  "We're pioneering “Everyday AI,” helping "
#                                  'everyone in an organization — from technical '
#                                  'teams to business leaders\xa0...'}]}]