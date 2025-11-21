import dataiku
from bike_sharing import prepare

cols = ["dteday",
        "hr",
        "temp",
        "casual",
        "registered",
        "cnt"]

df = dataiku.Dataset("BikeSharingData") \
    .get_dataframe() \
    [cols] \
    .pipe(prepare.with_temp_fahrenheit, temp_col="temp") \
    .pipe(prepare.with_datetime, date_col="dteday", hour_col="hr")

output_dataset = dataiku.Dataset("BikeSharingData_prepared")
output_dataset.write_with_schema(df)
