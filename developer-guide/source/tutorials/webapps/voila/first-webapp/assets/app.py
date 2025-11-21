import dataiku
from dataiku import SQLExecutor2
from dataiku.sql import Constant, toSQL, Dialects

DATASET_NAME = "pro_customers_sql"


def get_customer_info(id):
    dataset = dataiku.Dataset(DATASET_NAME)
    table_name = dataset.get_location_info().get('info', {}).get('quotedResolvedTableName')
    executor = SQLExecutor2(dataset=dataset)
    cid = Constant(str(id))
    escaped_cid = toSQL(cid, dialect=Dialects.POSTGRES)  # Replace by your DB
    query_reader = executor.query_to_iter(
        f"""SELECT "name", "job", "company" FROM "{table_name}" WHERE "id" = {escaped_cid}""")
    for (name, job, company) in query_reader.iter_tuples():
        return f"""The customer's name is "{name}", holding the position "{job}" at the company named "{company}" """
    return "No information can be found"


import ipywidgets as widgets
import os

label = widgets.Label(value="Enter the customer ID")
text = widgets.Text(placeholder="fdouetteau", continuous_update=False)

result = widgets.Label(value="")


def callback(customerId):
    result.value = get_customer_info(customerId.get('new', ''))


text.observe(callback, 'value')

display(widgets.VBox([widgets.HBox([label, text]), result]))
