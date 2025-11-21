import dataiku
import random

LLM_ID = "" # Fill with your LLM-Mesh id
lc_llm = dataiku.api_client().get_default_project().get_llm(LLM_ID).as_langchain_llm()


def bin_score(x):
    return 'pos' if float(x) >= 4.0 else ('ntr' if float(x) == 3.0 else 'neg')


random.seed(1337)

input_dataset = dataiku.Dataset("reviews_magazines")

output_schema = [
    {"type": "string", "name": "reviewText"},
    {"type": "int", "name": "nb_tokens"},
    {"type": "string", "name": "sentiment"}
]
train_dataset = dataiku.Dataset("reviews_mag_train")
train_dataset.write_schema(output_schema)
w_train = train_dataset.get_writer()

test_dataset = dataiku.Dataset("reviews_mag_test")
test_dataset.write_schema(output_schema)
w_test = test_dataset.get_writer()

for r in input_dataset.iter_rows():
    text = r.get("reviewText")
    if len(text) > 0:
        out_row = {
            "reviewText": text,
            "nb_tokens": lc_llm.get_num_tokens(text),
            "sentiment": bin_score(r.get("overall"))
        }
        rnd = random.random()
        if rnd < 0.5:
            w_train.write_row_dict(out_row)
        else:
            w_test.write_row_dict(out_row)

w_train.close()
w_test.close()
