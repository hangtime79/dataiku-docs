import dataiku
import requests
import gzip
import json
import random


# URL & filenames to download & create
URL = 'http://jmcauley.ucsd.edu/data/amazon_v2/categoryFilesSmall/Luxury_Beauty_5.json.gz'
FILE_NAME = 'Luxury_Beauty_5.json.gz'
FILE_UNZIP = 'Luxury_Beauty_5.json'
PROD_CATEGORY = "Luxury Beauty"
SAMPLE_SIZE = 47
DATASET_NAME = "amznreviews-sample"

response = requests.get(URL)

with open(FILE_NAME, 'wb') as f:
    f.write(response.content)

# Unzip the archive
with gzip.open(FILE_NAME, 'rb') as gz_file:
     with open(FILE_UNZIP, "wb") as f_out:
        f_out.write(gz_file.read())

with open(FILE_UNZIP, "r", encoding="utf-8") as f:
    data = []
    for line in f:
        record = json.loads(line)
        review = {
            "product_category": PROD_CATEGORY,
            "text": record.get("reviewText", "")
        }
        data.append({
            "review": json.dumps(review),
            "sentiment_score": record.get("overall", ""),
            "sentiment": "negative" if record["overall"] in [1, 2] 
                        else "neutral" if record["overall"] == 3 
                        else "positive"
        })

# Get a random sample of records
sample_data = random.sample(data, SAMPLE_SIZE)

# Get the dataset object
dataset = dataiku.Dataset(DATASET_NAME)

# Define the schema for the dataset
schema = [{"name": "review", "type": "string"},
          {"name": "sentiment_score", "type": "int"},
          {"name": "sentiment", "type": "string"}]

# Write the schema to the dataset
dataset.write_schema(schema)

# Write the rows to the dataset
with dataset.get_writer() as writer:
    for row in sample_data:
        writer.write_row_dict(row)