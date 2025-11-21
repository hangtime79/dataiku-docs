import dataiku
from dataiku.llm.python import BaseLLM
from dataikuapi.dss.llm import DSSLLMStreamedCompletionChunk, DSSLLMStreamedCompletionFooter

OPENAI_CONNECTION_NAME = "toto"


class MyLLM(BaseLLM):
    def __init__(self):
        pass

    def process_stream(self, query, settings, trace):
        prompt = query["messages"][0]["content"]

        llm = dataiku.api_client().get_default_project().get_llm(f"openai:{OPENAI_CONNECTION_NAME}:gpt-4o-mini")
        completion = llm.new_completion().with_message("You are an helpful assitant.", "system") \
            .with_message(prompt)
        completion.settings.update(settings)

        for chunk in completion.execute_streamed():
            if isinstance(chunk, DSSLLMStreamedCompletionChunk):
                yield {"chunk": {"text": chunk.text}}
            elif isinstance(chunk, DSSLLMStreamedCompletionFooter):
                yield {"footer": chunk.data}

    def process(self, query, settings, trace):
        prompt = query["messages"][0]["content"]

        resp_text = prompt

        llm = dataiku.api_client().get_default_project().get_llm(f"openai:{OPENAI_CONNECTION_NAME}:gpt-4o-mini")
        completion = llm.new_completion().with_message("You are an helpful assitant.", "system") \
            .with_message(prompt)
        completion.settings.update(settings)
        llm_resp = completion.execute()

        resp_text = llm_resp.text
        return {"text": resp_text}
