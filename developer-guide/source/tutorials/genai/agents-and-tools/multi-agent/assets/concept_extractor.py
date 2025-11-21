import dataiku
from dataiku.llm.python import BaseLLM

LLM_ID = "REPLACE_WITH_YOUR_LLM_ID"

class MyLLM(BaseLLM):
    def __init__(self):
        pass

    def process(self, query, settings, trace):
        llm = dataiku.api_client().get_default_project().get_llm(LLM_ID)

        user_query = query["messages"][0]["content"]

        concept_extractor = """You are working in a marketing team.
        Your role is to read a product description and find the key features, target audience, and unique selling points.
        Start with the product name mentioned as PRODUCT"""

        extract = llm.new_completion()
        extract.settings["temperature"] = 0.1
        extract.with_message(message=concept_extractor, role='system')
        extract.with_message(message=user_query, role='user')
        resp = extract.execute()


        return {"text": resp.text}
