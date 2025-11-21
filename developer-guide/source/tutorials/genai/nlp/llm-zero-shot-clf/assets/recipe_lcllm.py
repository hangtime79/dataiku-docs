import dataiku
import ast
from langchain_core.messages import HumanMessage, SystemMessage

LLM_ID = ""  # Fill with a valid LLM_ID
SSIZE = 10

client = dataiku.api_client()
project = client.get_default_project()
llm = project.get_llm(LLM_ID).as_langchain_llm()

input_dataset = dataiku.Dataset("reviews")
new_cols = [
    {"type": "string", "name": "llm_sentiment"},
    {"type": "string", "name": "llm_explanation"}
]
output_schema = input_dataset.read_schema() + new_cols
output_dataset = dataiku.Dataset("reviews_sample_llm_scored")
output_dataset.write_schema(output_schema)

system_msg = f"""
You are an assistant that classifies reviews according to their sentiment. \
Respond in json format with the keys: llm_sentiment and llm_explanation. \
The value for llm_sentiment should only be either pos or neg without punctuation: pos if the review is positive, neg otherwise.\
The value for llm_explanation should be a very short explanation for the sentiment.
"""

cnt = 0
with output_dataset.get_writer() as w:
    for r in input_dataset.iter_rows():
        messages = [
            SystemMessage(content=system_msg),
            HumanMessage(content=r.get("text"))
        ]
        llm_out = llm.invoke(messages)
        w.write_row_dict({**dict(r), **(ast.literal_eval(llm_out))})
        cnt += 1
        if cnt == SSIZE:
            break
