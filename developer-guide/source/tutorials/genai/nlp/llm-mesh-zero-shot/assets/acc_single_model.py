import dataiku
from sklearn.metrics import accuracy_score

client = dataiku.api_client()
project = client.get_default_project()

review_scored_df = dataiku.Dataset("reviews_scored").get_dataframe()
acc = accuracy_score(review_scored_df["polarity"],
                     review_scored_df["prediction"])
print(f"ACC = {acc:.2f}")