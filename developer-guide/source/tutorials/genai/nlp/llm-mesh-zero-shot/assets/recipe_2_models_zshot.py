import dataiku
from review_code.models import zshot_clf

GPT_35_LLM_ID = ""  # Fill with your gpt-3.5-turbo LLM id
GPT_4_LLM_ID = ""  # Fill with your gpt-4 LLM id
N_MAX_OUTPUT_ROWS = 100  # Change this value to increase the number of rows to use

# Create new schema for the output dataset
reviews = dataiku.Dataset("reviews")
schema = reviews.read_schema()
reviews_scored = dataiku.Dataset("reviews_2_models_scored")
for c in [f"pred_{GPT_35_LLM_ID}", f"pred_{GPT_4_LLM_ID}"]:
    schema.append({"name": c, "type": "string"})
reviews_scored.write_schema(schema)

# Retrieve the LLM handle
client = dataiku.api_client()
project = client.get_default_project()
gpt_35 = project.get_llm(GPT_35_LLM_ID)
gpt_4 = project.get_llm(GPT_4_LLM_ID)

# Iteratively classify reviews with both models
with reviews_scored.get_writer() as w_out:
    for i, row in enumerate(reviews.iter_rows()):
        if i == N_MAX_OUTPUT_ROWS-1:
            break
        print(i)
        gpt = {}
        gpt[f"pred_{GPT_35_LLM_ID}"] = zshot_clf(gpt_35, row).get('prediction')
        gpt[f"pred_{GPT_4_LLM_ID}"]  = zshot_clf(gpt_4, row).get('prediction')
        w_out.write_row_dict({**row, **gpt})
