import dataiku
from dataiku import SQLExecutor2
from dataiku.sql import Constant, toSQL, Dialects
from flask import request, make_response
import logging

logger = logging.getLogger(__name__)

DATASET_NAME = 'pro_customers_sql'


@app.route('/get_customer_info')
def get_customer_info():
    dataset = dataiku.Dataset(DATASET_NAME)
    table_name = dataset.get_location_info().get('info', {}).get('quotedResolvedTableName')
    executor = SQLExecutor2(dataset=dataset)

    id = request.args.get('id', None)
    if id:
        cid = Constant(str(id))
        escaped_cid = toSQL(cid, dialect=Dialects.POSTGRES)  # Replace by your DB
        query_reader = executor.query_to_iter(
            f"""SELECT "name", "job", "company" FROM {table_name} WHERE "id"={escaped_cid}""")
        for (name, job, company) in query_reader.iter_tuples():
            result = {"name": name, "job": job, "company": company}
        response = make_response(json.dumps(result))
        response.headers['Content-type'] = 'application/json'
        return response
    else:
        query_reader = executor.query_to_iter(
            f"""SELECT "name", "job", "company" FROM {table_name}""")
        result = ""
        for (name, job, company) in query_reader.iter_tuples():
            result += f"""{name}, {job}, {company}
"""

        response = make_response(result)
        response.headers['Content-type'] = 'text/plain'
        return response