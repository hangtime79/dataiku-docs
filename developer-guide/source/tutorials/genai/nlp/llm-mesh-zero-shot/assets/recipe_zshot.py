import dataiku
from review_code.models import zshot_clf

GPT_35_LLM_ID = ""  # Fill with your gpt-3.5-turbo LLM id
N_MAX_OUTPUT_ROWS = 100  # Change this value to increase the number of rows to use

# Create new schema for the output dataset
reviews = dataiku.Dataset("reviews")
schema = reviews.read_schema()
reviews_scored = dataiku.Dataset("reviews_scored")
for c in ["prediction", "llm_id"]:
    schema.append({"name": c, "type": "string"})
reviews_scored.write_schema(schema)


# Retrieve the LLM handle
client = dataiku.api_client()
project = client.get_default_project()
llm = project.get_llm(GPT_35_LLM_ID)

# Iteratively classify reviews
with reviews_scored.get_writer() as w_out:
    for i, row in enumerate(reviews.iter_rows()):
        if i == N_MAX_OUTPUT_ROWS-1:
            break
        w_out.write_row_dict(zshot_clf(llm, row))
