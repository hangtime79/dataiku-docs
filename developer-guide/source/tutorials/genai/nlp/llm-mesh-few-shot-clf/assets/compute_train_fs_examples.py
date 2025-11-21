import dataiku
from utils.chat import predict_sentiment

SIZE_EX_MIN = 20
SIZE_EX_MAX = 100
NB_EX_MAX = 10

LLM_ID = "" # Fill with your LLM-Mesh id
chat = dataiku.api_client().get_default_project().get_llm(LLM_ID).as_langchain_chat_model(temperature=0)

input_dataset = dataiku.Dataset("reviews_mag_train")
input_schema = input_dataset.read_schema()

output_dataset = dataiku.Dataset("train_fs_examples")
new_cols = [
    {"type": "string", "name": "llm_sentiment"}
]
output_schema = input_schema + new_cols
output_dataset.write_schema(output_schema)

nb_ex = 0
with output_dataset.get_writer() as w:
    for r in input_dataset.iter_rows():
        # Check token-base length
        nb_tokens = r.get("nb_tokens")
        if nb_tokens > SIZE_EX_MIN and nb_tokens < SIZE_EX_MAX:
            pred = predict_sentiment(chat, r.get("reviewText"))

            # Keep prediction only if it was mistaken
            if pred["llm_sentiment"] != r.get("sentiment"):
                out_row = dict(r)
                out_row["llm_sentiment"] = pred["llm_sentiment"]
                w.write_row_dict(out_row)
                nb_ex += 1
                if nb_ex == NB_EX_MAX:
                    break
