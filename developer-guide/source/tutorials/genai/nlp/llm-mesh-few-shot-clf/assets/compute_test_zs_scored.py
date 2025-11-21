import dataiku
from utils.chat import predict_sentiment

LLM_ID = "" # Fill with your LLM-Mesh id
chat = dataiku.api_client().get_default_project().get_llm(LLM_ID).as_langchain_chat_model(temperature=0)

input_dataset = dataiku.Dataset("reviews_mag_test")
new_cols = [
    {"type": "string", "name": "llm_sentiment"},
    {"type": "int", "name": "nb_tokens"}
]
output_schema = input_dataset.read_schema() + new_cols
output_dataset = dataiku.Dataset("test_zs_scored")
output_dataset.write_schema(output_schema)

# Run prompts on test dataset
with output_dataset.get_writer() as w:
    for i, r in enumerate(input_dataset.iter_rows()):
        print(f"{i+1}")
        out_row = {}
        # Keep columns from input dataset
        out_row.update(dict(r))
        # Add LLM output
        out_row.update(predict_sentiment(chat=chat,
                                         review=r.get("reviewText")))
        w.write_row_dict(out_row)