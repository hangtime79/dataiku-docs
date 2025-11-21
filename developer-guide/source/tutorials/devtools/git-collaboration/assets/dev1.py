import dataiku
import yahooquery as yq

def find_symbol(name):
    """
    Searches for a stock ticker symbol using the yahooquery package.

    Args:
        name (str): The company name or search term.

    Returns:
        str: The ticker symbol if found, 'NA' if not found, or 'ERROR' on exception.
    """
    try:
        data = yq.search(name)
    except ValueError:
        return "ERROR"
    else:
        quotes = data['quotes']
        if len(quotes) == 0:
            return 'NA'

        symbol = quotes[0]['symbol']

        return symbol

# Read recipe input
pro_customers_sql = dataiku.Dataset("pro_customers_sql")
customers_companies = pro_customers_sql.get_dataframe(columns=['company'])

# Write recipe outputs
companies = dataiku.Dataset("companies")
companies_df = customers_companies.copy()

# For each company name, find the corresponding stock symbol
symbols = []
for company in companies_df['company']:
    symbol = find_symbol(company)
    if symbol not in ["ERROR", "NA"]:
        symbols.append(symbol)
    else:
        symbols.append(None)
# Add the list of symbols as a new column 'symbol' in the DataFrame
companies_df['symbol'] = symbols

# writes the result to the dataset
companies.write_with_schema(companies_df)