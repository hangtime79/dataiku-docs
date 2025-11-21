import dataiku

import requests
import gzip
import json
import csv
import random

# URL & filenames to download & create
URL = 'http://jmcauley.ucsd.edu/data/amazon_v2/categoryFilesSmall/Luxury_Beauty_5.json.gz'
FILE_NAME = 'Luxury_Beauty_5.json.gz'
FILE_UNZIP = 'Luxury_Beauty_5.json'
PROD_CATEGORY = "Luxury Beauty"
SAMPLE_SIZE = 256 # GPU provisioned :fingers-crossed:
SAMPLE_SIZE = 32 # in case no GPU :warning:
DATASET_NAME = "beauty_product_reviews"

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
        text = record.get("reviewText", "")
        category = PROD_CATEGORY
        sentiment = record.get("overall", "")
        if sentiment in [1, 2]:
            sentiment = "negative"
        elif sentiment == 3:
            sentiment = "neutral"
        elif sentiment in [4, 5]:
            sentiment = "positive"
        data.append({"text": text, "product_category": category, "sentiment": sentiment})
        


# Get a random sample of 1000 records
sample_data = random.sample(data, SAMPLE_SIZE)

# Get the dataset object
dataset = dataiku.Dataset(DATASET_NAME)

# Define the schema for the dataset
schema = [{"name": "text", "type": "string"},
          {"name": "product_category", "type": "string"},
          {"name": "sentiment", "type": "string"}]

# Write the schema to the dataset
dataset.write_schema(schema)

# Write the rows to the dataset
with dataset.get_writer() as writer:
    for row in sample_data:
        writer.write_row_dict(row)