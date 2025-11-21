import dataiku
from dataiku import SQLExecutor2
from dataiku.sql import Constant, toSQL, Dialects
from fastapi import Query
from fastapi.responses import JSONResponse, PlainTextResponse
import logging
from typing import Optional

logger = logging.getLogger(__name__)

DATASET_NAME = 'pro_customers_sql'


@app.get("/get_customer_info")
async def get_customer_info(id: Optional[str] = Query(default=None)):
    dataset = dataiku.Dataset(DATASET_NAME)
    table_name = dataset.get_location_info().get('info', {}).get('quotedResolvedTableName')
    executor = SQLExecutor2(dataset=dataset)

    if id:
        cid = Constant(str(id))
        escaped_cid = toSQL(cid, dialect=Dialects.POSTGRES)  # Replace by your DB
        query_reader = executor.query_to_iter(
            f"""SELECT "name", "job", "company" FROM {table_name} WHERE "id"={escaped_cid}"""
        )
        result = None
        for (name, job, company) in query_reader.iter_tuples():
            result = {"name": name, "job": job, "company": company}
        
        if result:
            return JSONResponse(content=result)
        else:
            return JSONResponse(content={"error": "Customer not found"}, status_code=404)
    
    else:
        query_reader = executor.query_to_iter(
            f"""SELECT "name", "job", "company" FROM {table_name}"""
        )
        result = ""
        for (name, job, company) in query_reader.iter_tuples():
            result += f"""{name}, {job}, {company}\n"""
        
        return PlainTextResponse(content=result)
