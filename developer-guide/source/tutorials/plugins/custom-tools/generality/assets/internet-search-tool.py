from dataiku.llm.agent_tools import BaseAgentTool
import logging
import dataiku
from duckduckgo_search import DDGS

class InternetSearchTool(BaseAgentTool):
    def set_config (self, config, plugin_config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.plugin_config = plugin_config
        
    def get_descriptor(self, tool):
        return {
            "description": """Provide general information about a company, given the company's name.""",
            "inputSchema": {
                "title": "Input for a company",
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string",
                        "description": "The company you need info on"
                    }
                }
            }
        }
    
    def invoke(self, input, trace):
        self.logger.info(input)
        
        args = input["input"]
        company_name = args["company"]

        with DDGS() as ddgs:
            results = list(ddgs.text(f"{company_name} (company)", max_results=1))
            if results:
                return {"output" : f"Information found about {company_name}: {results[0]['body']}"}
            return {"output": f"No information found about {company_name}"}

    def load_sample_query(self, tool):
        return {"company": "Dataiku"}
