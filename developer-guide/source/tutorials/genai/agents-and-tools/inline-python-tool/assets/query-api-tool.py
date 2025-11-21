import dataiku
from dataiku.llm.agent_tools import BaseAgentTool
import logging


class ApiAgentTool(BaseAgentTool):
    """A code-based agent tool that queries a headless API"""

    def set_config(self, config, plugin_config):
        self.logger = logging.getLogger(__name__)

    def get_descriptor(self, tool):
        """
        Returns the descriptor of the tool, as a dict containing:
           - description (str)
           - inputSchema (dict, a JSON Schema representation)
        """
        return {
            "description": "Provide a prompt to use to query the headless API",
            "inputSchema" : {
                "$id": "",
                "title": "",
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to use in the API call"
                    }
                }
            }
        }


    def invoke(self, input, trace):
        """
        Invokes the tool.

        The arguments of the tool invocation are in input["input"], a dict
        """
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug(input)

        WEBAPP_ID = "cpxmkji"
        client = dataiku.api_client()
        project = client.get_default_project()
        webapp = project.get_webapp(WEBAPP_ID)
        backend = webapp.get_backend_client()
        backend.session.headers['Content-Type'] = 'application/json'
        prompt = input['input']['prompt']

        # Query the LLM
        response = backend.session.post(backend.base_url + '/query', json={'message':prompt})
        if response.ok:
            return { "output": response.text }
        else:
            return { "output": f"An error occured: {response.status_code} {response.reason}" }