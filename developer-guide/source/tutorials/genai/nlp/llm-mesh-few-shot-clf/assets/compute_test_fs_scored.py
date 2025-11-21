import dataiku
from utils.chat import predict_sentiment_fs
from utils.chat import build_example_msg

MIN_EX_LEN = 5
MAX_EX_LEN = 200
MAX_NB_EX = 10

LLM_ID = "" # Fill with your LLM-Mesh id
chat = dataiku.api_client().get_default_project().get_llm(LLM_ID).as_langchain_chat_model(temperature=0)

input_dataset = dataiku.Dataset("reviews_mag_test")
new_cols = [
    {"type": "string", "name": "llm_sentiment"},
]

# Retrieve a few examples from the training dataset
examples_dataset = dataiku.Dataset("train_fs_examples")
ex_to_add = []
tot_tokens = 0
for r in examples_dataset.iter_rows():
    nb_tokens = r.get("nb_tokens")
    if (nb_tokens > MIN_EX_LEN and nb_tokens < MAX_EX_LEN):
        ex_to_add += build_example_msg(dict(r))
        tot_tokens += nb_tokens
        if len(ex_to_add) == MAX_NB_EX:
            print(f"Total tokens = {tot_tokens}")
            break

output_schema = input_dataset.read_schema() + new_cols
output_dataset = dataiku.Dataset("test_fs_scored")
output_dataset.write_schema(output_schema)

# Run prompts on test dataset
with output_dataset.get_writer() as w:
    for i, r in enumerate(input_dataset.iter_rows()):
        out_row = {}
        # Keep columns from input dataset
        out_row.update(dict(r))
        # Add LLM output
        result = predict_sentiment_fs(chat=chat,
                                      review=r.get("reviewText"),
                                      examples=ex_to_add)
        if result:
            out_row.update(result)
        w.write_row_dict(out_row)
