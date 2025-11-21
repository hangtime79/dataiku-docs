import dataiku
import json

# Get Dataiku client and get project
client = dataiku.api_client()
project = client.get_default_project()

# Get the LLM from the project
LLM_ID = ""  # Set your LLM ID here
llm = project.get_llm(LLM_ID)

# Set up datasets
ds_in = dataiku.Dataset("amznreviews-sample")
ds_out = dataiku.Dataset("amznreviews-sample-llm-scored")

# Define the JSON schema
SCHEMA = {
    "type": "object",
    "properties": {
        "llm_sentiment": {
            "type": "string",
            "enum": ["positive", "negative", "neutral"]
        },
        "llm_explanation": {
            "type": "string"
        },
        "llm_confidence": {
            "type": "number"
        }
    },
    "required": ["llm_sentiment", "llm_explanation", "llm_confidence"],
    "additionalProperties": False
}

# Outline the prompt
PROMPT = """
You are an assistant that classifies reviews in JSON format according to their sentiment. 
Respond with a JSON object containing the following fields:
    - llm_explanation: a very short explanation for the sentiment
    - llm_sentiment: should only be either "positive" or "negative" or "neutral" without punctuation
    - llm_confidence: a float between 0-1 showing your confidence in the sentiment score
"""

# Use a multi-completion query
completions = llm.new_completions()
completions.with_json_output(schema=SCHEMA)
for row in ds_in.iter_rows():
    # Load review JSON
    review_data = json.loads(row["review"])
    comp = completions.new_completion()
    comp.with_message(PROMPT, role="system")
    comp.with_message(json.dumps(review_data), role="user")

# Execute all completions in batch 
responses = completions.execute()
results = [r.json for r in responses.responses]

# Write the results to the output dataset
df_in = ds_in.get_dataframe()
df_out = df_in.copy()

df_out["llm_json_output"] = [json.dumps(r) for r in results]
df_out["llm_sentiment"] = [r.get("llm_sentiment") for r in results]
df_out["llm_explanation"] = [r.get("llm_explanation") for r in results]
df_out["llm_confidence"] = [r.get("llm_confidence") for r in results]
ds_out.write_with_schema(df_out)
