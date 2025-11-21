import dataiku
import pickle

from model_gen.sk_pipeliner import split_and_train_pipeline

df = dataiku.Dataset("bank") \
    .get_dataframe()

pipeline, df_test = split_and_train_pipeline(df, test_size=0.2)

bank_test = dataiku.Dataset("bank_test") \
    .write_with_schema(df_test)

FOLDER_ID = ""  # Enter your managed folder id here

model_folder = dataiku.Folder(FOLDER_ID)

with model_folder.get_writer("/pipeline.pkl") as writer:
    pickle.dump(pipeline, writer)
