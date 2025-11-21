# This file is the implementation of custom LLM custom-chat-plugin
from dataiku.llm.python import BaseLLM
from openai import OpenAI


class MyLLM(BaseLLM):
    def __init__(self):
        pass

    def set_config(self, config: dict, plugin_config: dict) -> None:
        self.config = config
        self.model = config.get("model", None)
        self.api_key = config.get('api_key').get('param_set_api_key')
        self.client = OpenAI(api_key=self.api_key)

    def process(self, query, settings, trace):
        prompt = query["messages"][-1]["content"]

        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.json()
