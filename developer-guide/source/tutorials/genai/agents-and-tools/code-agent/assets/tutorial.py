import dataiku
from dataiku import SQLExecutor2
from duckduckgo_search import DDGS
from dataiku.sql import Constant, toSQL, Dialects


def get_customer_details(customer_id: str) -> str:
    """Get customer name, position and company information from database.
    The input is a customer id (stored as a string).
    The ouput is a string of the form:
        "The customer's name is \"{name}\", holding the position \"{job}\" at the company named \"{company}\""
    """
    dataset = dataiku.Dataset("pro_customers_sql")
    table_name = dataset.get_location_info().get('info', {}).get('quotedResolvedTableName')
    executor = SQLExecutor2(dataset=dataset)
    cid = Constant(str(customer_id))
    escaped_cid = toSQL(cid, dialect=Dialects.POSTGRES)  # Replace by your DB
    query_reader = executor.query_to_iter(
        f"""SELECT * FROM {table_name}  where "id"={escaped_cid}""")
    for (user_id, name, job, company) in query_reader.iter_tuples():
        return f"The customer's name is \"{name}\", holding the position \"{job}\" at the company named \"{company}\""
    return f"No information can be found about the customer {customer_id}"


def search_company_info(company_name: str) -> dict:
    """
    Use this tool when you need to retrieve information on a company.
    The input of this tool is the company name.
    The ouput is either a small recap of the company or "No information ..." meaning that we couldn't find information about this company
    """
    with DDGS() as ddgs:
        results = list(ddgs.text(f"{company_name} (company)", max_results=1))
        result = "Information found about " + company_name + ": " + results[0]["body"] + "\n" \
            if len(results) > 0 and "body" in results[0] \
            else None
        if not result:
            results = DDGS().text(company_name, max_results=1)
            result = "Information found about " + company_name + ": " + results[0]["body"] + "\n" \
                if len(results) > 0 and "body" in results[0] \
                else "No information can be found about the company " + company_name
    return {"messages": result}
