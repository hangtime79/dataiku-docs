import dataiku
import yahooquery as yq
import yfinance as yf


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

# For each company name, find the corresponding last stock value
last_stocks = []
for company in companies_df['company']:
    symbol = find_symbol(company)
    if symbol not in ["ERROR", "NA"]:
        try:
            ticker_obj = yf.Ticker(symbol)
            price = ticker_obj.history(period="1d")['Close']
            latest_price = price.iloc[-1] if not price.empty else None
            last_stocks.append(latest_price)
        except Exception as e:
            last_stocks.append(None)
    else:
        last_stocks.append(None)
# Add the list of last_stocks as a new column 'last_stock' in the DataFrame
companies_df['last_stock'] = last_stocks

# writes the result to the dataset
companies.write_with_schema(companies_df)