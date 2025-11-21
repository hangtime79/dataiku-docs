import dataiku


# Read recipe input
pro_customers_sql = dataiku.Dataset("pro_customers_sql")
customers_companies = pro_customers_sql.get_dataframe(columns=['company'])

# Write recipe outputs
companies = dataiku.Dataset("companies")
companies_df = customers_companies.copy()
companies.write_with_schema(companies_df)