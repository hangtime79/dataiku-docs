import dataiku
from sklearn.metrics import accuracy_score

client = dataiku.api_client()
project = client.get_default_project()

GPT_35_LLM_ID = ""  # Fill with your gpt-3.5-turbo LLM id
GPT_4_LLM_ID = ""  # Fill with your gpt-4 LLM id

acc = []

review_scored_df = dataiku.Dataset("reviews_2_models_scored").get_dataframe()
for m in [GPT_35_LLM_ID, GPT_4_LLM_ID]:
    acc.append({"llm_id": m,
                "accuracy": accuracy_score(review_scored_df["polarity"],
                                           review_scored_df[f"pred_{m}"])})
                                           
for ac in acc:
    print(f"ACC({ac.get('llm_id')}) = {ac.get('accuracy'):.2f}")
