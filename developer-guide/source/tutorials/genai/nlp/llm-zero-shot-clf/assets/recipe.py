import dataiku
import ast

LLM_ID = ""  # Fill with a valid LLM_ID
SSIZE = 10

client = dataiku.api_client()
project = client.get_default_project()
llm = project.get_llm(LLM_ID)

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
        completion = llm.new_completion()
        llm_out = completion.with_message(role="system", message=system_msg).with_message(r.get("text")).execute()
        w.write_row_dict({**dict(r), **(ast.literal_eval(llm_out.text))})
        cnt += 1
        if cnt == SSIZE:
            break
