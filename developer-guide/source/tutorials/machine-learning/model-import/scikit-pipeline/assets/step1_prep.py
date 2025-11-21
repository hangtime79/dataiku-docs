# Libraries
import io
import requests
import zipfile
import pandas as pd
import dataiku

BANK_DATA_URL = 'https://archive.ics.uci.edu/static/public/222/bank+marketing.zip'

with requests.get(BANK_DATA_URL, stream=True) as r:
    archive = zipfile.ZipFile(io.BytesIO(r.content))
    archive.extractall()

bank_zip = [archive.open(name) for name in archive.namelist() \
    if name == 'bank.zip']

with zipfile.ZipFile(bank_zip[0]) as z:
    for filename in z.namelist():
        if filename == 'bank.csv':
            df = pd.read_csv(z.open(filename), sep=';')

DATASET = 'bank'
ds = dataiku.Dataset(DATASET)
ds.write_with_schema(df)