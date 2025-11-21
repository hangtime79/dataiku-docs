import dataiku
from dataiku.llm.python import BaseLLM


class MyLLM(BaseLLM):
    def __init__(self):
        pass

    def process_stream(self, query, settings, trace):
        pass

    def process(self, query, settings, trace):
        prompt = query["messages"][0]["content"]

        project = dataiku.api_client().get_default_project()

        # call concept extractor
        EXTRACTOR_AGENT_ID = "<YOUR EXTRACTOR AGENT ID>"
        agent_extractor = project.get_llm(EXTRACTOR_AGENT_ID)

        completion = agent_extractor.new_completion()
        completion.with_message(prompt)
        resp = completion.execute()
        extractor_answer = resp.text

        # call web writer
        WEB_AGENT_ID = "<YOUR WEB WRITER AGENT ID>"
        agent_webwriter = project.get_llm(WEB_AGENT_ID)

        completion = agent_webwriter.new_completion()
        completion.with_message(extractor_answer)
        resp = completion.execute()
        webwriter_answer = resp.text

        return {"text": webwriter_answer}
