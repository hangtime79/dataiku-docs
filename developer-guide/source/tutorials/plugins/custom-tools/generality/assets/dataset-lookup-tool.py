from dataiku.llm.agent_tools import BaseAgentTool
import logging
import dataiku
from dataiku import SQLExecutor2
from dataiku.sql import Constant, toSQL, Dialects

class DatasetLookupTool(BaseAgentTool):
    def set_config (self, config, plugin_config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.plugin_config = plugin_config
        
    def get_descriptor(self, tool):
        return {
            "description": """Provide a name, job title and company of a customer, given the customer's ID""",
            "inputSchema": {
                "title": "Input for a customer id",
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The customer Id"
                    }
                }
            }

        }
    
    def invoke(self, input, trace):
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug(input)

        args = input["input"]
        customerId = args["id"]
        dataset = dataiku.Dataset("pro_customers_sql")
        table_name = dataset.get_location_info().get('info', {}).get('quotedResolvedTableName')
        executor = SQLExecutor2(dataset=dataset)
        cid = Constant(str(customerId))
        escaped_cid = toSQL(cid, dialect=Dialects.POSTGRES)  # Replace by your DB
        query_reader = executor.query_to_iter(
            f"""SELECT "name", "job", "company" FROM {table_name} WHERE "id" = {escaped_cid}""")
    
        for (name, job, company) in query_reader.iter_tuples():
            return {"output" : f"""The customer's name is "{name}", holding the position "{job}" at the company named "{company}"."""}
        return {"output" : f"No information can be found about the customer {customerId}"}

    def load_sample_query(self, tool):
        return {"id": "fdouetteau"}
