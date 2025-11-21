# Datasets (reading and writing data)

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 19/09/2024
  
  this code samples has been verified on DSS: 14.1.0
  Date of check: 06/08/2025
```

Please see {doc}`index` for an introduction to interacting with datasets in Dataiku Python API

For a starting code sample, please see [Python Recipes](https://doc.dataiku.com/dss/latest/code_recipes/python.html).

## Basic usage


Reading a Dataiku dataset as a Pandas Dataframe: 

```py
import dataiku

mydataset = dataiku.Dataset("myname")

df = mydataset.get_dataframe()
```


Writing a Pandas Dataframe to a Dataiku dataset

```py
import dataiku

output_dataset = dataiku.Dataset("output_dataset")

output_dataset.write_with_schema(df)
```

Adding a dataframe to an input Dataiku dataset, or to any other dataset.

### Append Mode
When writing to a dataset, you must choose whether or not to use `appendMode`. By default, `appendMode` is disabled, and writing to a dataset will overwrite the data, meaning the dataset will be emptied and filled with the new data.

With `appendMode` enabled, you will instead add data to the existing dataset.

To enable `appendMode` you should go to the *Inputs/Outputs* tab on your coding recipe and enable `Append instead of overwrite` in the output section.

You can also enable `appendMode` in code by using the `spec_item` property, as shown in the sample below:

```python
import dataiku

df = ## The dataframe you want to add

input_append = dataiku.Dataset("input_dataset", ignore_flow=True)
input_append.spec_item["appendMode"] = True

input_append.write_with_schema(df)
```

## Accessing Dataset Connection Information

You generally want to avoid hard-coding connection information, table names, and other details in your recipe code.
Dataiku can provide you with some connection/location information about the datasets you are trying to read or write.

For all datasets, you can use the {meth}`~dataiku.Dataset.get_location_info` method. 
It returns a structure containing an ``info`` dict.
The keys in the ``info`` dict depend on the specific kind of dataset. 
Here are a few examples:

```python

# myfs is a Filesystem dataset
dataset = dataiku.Dataset("myfs")
location_info = dataset.get_location_info()
print(location_info)
```

```python
{
    'locationInfoType': 'UPLOADED',
    'info': {
        'path': '/data/input/PROJECTKEY/myfs',
        'isSingleFile': False
    }
}
```
```python
# sql is a Snowflake dataset
dataset = dataiku.Dataset("sql")
location_info = dataset.get_location_info()
print(location_info)
```
```python
{
    'locationInfoType': 'SQL', 
    'info': {
        'databaseType': 'Snowflake', 
        'schema': 'schema', 
        'quotedResolvedTableName': '"schema"."SQL"',
        'connectionName': 'snowflake', 
        'table': 'SQL'
    }
}
```

In addition, for filesystem-like datasets (Filesystem, HDFS, S3, etc.),
you can use the {meth}`~dataiku.Dataset.get_files_info` to get details about all files in a dataset (or partition).

```python
dataset = dataiku.Dataset("non_partitioned_fs")
files_info = dataset.get_files_info()

for filepath in files_info["globalPaths"]:
  # Returns a path relative to the root path of the dataset.
  # The root path of the dataset is returned by get_location_info
  print(filepath["path"])
  # Size in bytes of that file
  print(filepath["size"])
  
  
dataset = dataiku.Dataset("partitioned_fs")
files_info = dataset.get_files_info()

for (partition_id, partition_filepaths) in files_info["pathsByPartition"].items():
    print(partition_id)

    for filepath in partition_filepaths:
        # Returns a path relative to the root path of the dataset.
        # The root path of the dataset is returned by get_location_info
        print(filepath["path"])
        # Size in bytes of that file
        print(filepath["size"])      
```
## Typing and schema

### Type inference versus dataset-provided types

This applies when reading a dataframe.

By default, the data frame is created without explicit typing. This means that we let Pandas "guess" the proper Pandas type for each column. The main advantage of this approach is that even if your dataset only contains "string" columns (which is the default on a newly imported dataset from CSV, for example) if the column actually contains numbers, a proper numerical type will be used.

If you pass `infer_with_pandas=False` as an option to {meth}`~dataiku.Dataset.get_dataframe()`, the exact dataset types will be passed to Pandas. Note that if your dataset contains invalid values, the whole {meth}`~dataiku.Dataset.get_dataframe` call will fail.

```py
import dataiku

mydataset = dataiku.Dataset("myname")
# The dataframe will have the types specified by the storage types in the dataset "myname"
df = mydataset.get_dataframe(infer_with_pandas=False)
```

### Nullable integers

This applies when reading a dataframe.

By default, when using ``infer_with_pandas=False``, DSS uses the regular integer types for pandas, i.e. ``np.int64`` and others.

These types do not support null values, which mean that if a column contains a single missing value, reading will fail. To avoid this, you can use the pandas "nullable integer" types, i.e. ``pd.Int64DType`` and others.

To use these, use ``use_nullable_integers=True``

```py
import dataiku

mydataset = dataiku.Dataset("myname")
# The dataframe will have the types specified by the storage types in the dataset "myname", even if an integer column contains null values
df = mydataset.get_dataframe(infer_with_pandas=False, use_nullable_integers=True)
```

Using nullable integers also causes DSS to use the exact type size (8 bits for tinyint, 16 bits for smallint, ...)

### Using categoricals

This applies when reading a dataframe.

For alphanumerical columns with a small number of values, pandas provides a ``Categorical`` type that improves memory consumption by storing references in a dictionary of possible values.

DSS does not automatically use categoricals, but you can request to use categoricals, either for explicitly-selected columns or for string columns.


```py
import dataiku

mydataset = dataiku.Dataset("myname")

# Read columns A and B as categoricals. Other string columns will be read as regular strings
df = mydataset.get_dataframe(infer_with_pandas=False, categoricals=["A", "B"])

# Read all string columns as categoricals (beware, if your columns have many values, this will be less efficient)
df = mydataset.get_dataframe(infer_with_pandas=False, categoricals="all_strings")
```

## Writing the output schema


When you use the {meth}`~dataiku.Dataset.write_with_schema()` method, this is what happens: the schema of the dataframe is used to modify the schema of the output dataset, each time the Python recipe is run. This must obviously be used with caution, as mistakes could lead the "next" parts of your Flow to fail if your schema changes.

You can also select to only write the schema (not the data):
```py
import dataiku

# Set the schema of ‘myoutputdataset’ to match the columns of the dataframe
output_ds = dataiku.Dataset("myoutputdataset")
output_ds.write_schema_from_dataframe(my_dataframe)
```

And you can write the data in the dataframe without changing the schema:

```py
# Write the dataframe without touching the schema
output_ds.write_dataframe(my_dataframe)
```

## Fast path reading

When using the universal {meth}`~dataiku.Dataset.get_dataframe()` API, all data goes through DSS, to be handled in a unified way.

In addition, Dataiku has the ability to read the dataset as a Pandas dataframe, using fast-path access (without going through DSS), if possible.


The fast path method provides better performance than the usual {meth}`~dataiku.Dataset.get_dataframe()` method, but is only compatible with some dataset types and formats.

Fast path requires the "permission details readable" to be granted on the connection.

Dataframes obtained using this method may differ from those using {meth}`~dataiku.Dataset.get_dataframe()`, notably around schemas and data.

At the moment, this fast path is available for:

* S3 datasets using Parquet. This requires the additional `s3fs` package, as well as `fastparquet` or `pyarrow`
* Snowflake datasets. This requires the additional `snowflake-connector-python[pandas]` package

```py
import dataiku

ds = dataiku.Dataset("my_s3_parquet_dataset")
df = ds.get_fast_path_dataframe() # will usually be much faster than get_dataframe

# fast path dataframe on S3+parquet is especially efficient when only selecting some columns
df = ds.get_fast_path_dataframe(columns=["A", "B", "C"])


ds = dataiku.Dataset("my_snowflake_dataset")
df = ds.get_fast_path_dataframe() # will usually be much faster than get_dataframe

# fast path dataframe on Snowflake is especially efficient when only selecting some columns
df = ds.get_fast_path_dataframe(columns=["A", "B", "C"])
```

## Improving read performance

When not using fast path reading, you can get improved reading performance by adding the `skip_additional_data_checks` option.

```py
import dataiku

ds = dataiku.Dataset("my_s3_parquet_dataset")
df = ds.get_dataframe(skip_additional_data_checks=True)
```

While this option is not enabled by default to ensure backwards compatibility, it can almost always be used.

If you know data is good, read performance on CSV datasets can also be strongly improved by going to the format settings and setting "Bad data type behavior (read)" to "Ignore"


## Chunked reading and writing with Pandas

When using {meth}`~dataiku.Dataset.get_dataframe()`, the whole dataset (or selected partitions) is read into a single Pandas dataframe, which must fit in RAM on the DSS server.

This is sometimes inconvenient and DSS provides a way to do this in chunks:

```py
import dataiku

mydataset = dataiku.Dataset("myname")

for df in mydataset.iter_dataframes(chunksize=10000):
        # df is a dataframe of at most 10K rows.
```

By doing this, you only need to load a few thousand rows at a time.

Writing in a dataset can also be made by chunks of data frames. For that, you need to obtain a writer:

```py
import dataiku

inp = dataiku.Dataset("myname")
out = dataiku.Dataset("output")

with out.get_writer() as writer:

        for df in inp.iter_dataframes():
                # Process the df dataframe ...

                # Write the processed dataframe
                writer.write_dataframe(df)
```

:::{note}
When using chunked writing, you cannot set the schema for each chunk, you cannot use {meth}`~dataiku.Dataset.write_with_schema()`.

Instead, you should set the schema first on the dataset object, using {meth}`~dataiku.Dataset.write_schema_from_dataframe()`, with the first chunked dataframe.
:::

## Using the streaming API

If the dataset does not fit in memory, it is also possible to stream the rows. This is often more complicated, so we recommend using Pandas for most use cases.

### Reading

Dataset object's:

* ``iter_rows`` method are iterating over the rows of the dataset, represented as dictionary-like objects.
* ``iter_tuples`` method are iterating over the rows of the dataset, represented as tuples. Values are ordered according to the schema of the dataset.

```py
import dataiku
from collections import Counter

cars = dataiku.Dataset("cars")

origin_count = Counter()

# iterate on the dataset. The row object is a dict-like object
# the dataset is "streamed" and it is not required to fit in RAM.
for row in cars.iter_rows():
    origin_count[row["origin"]] += 1
```
    
### Writing the output schema

Generally speaking, it is preferable to declare the schema of the output dataset prior to running the Python code. However, it is often impractical to do so, especially when you write data frames with many columns (or columns that change often). In that case, it can be useful for the Python script to actually modify the schema of the dataset.

The Dataset API provides a method to set the schema of the output dataset. When doing that, the schema of the dataset is modified each time the Python recipe is run. This must obviously be used with caution.

```py
output.write_schema([
{
  "name": "origin",
  "type": "string",
},
{
  "name": "count",
  "type": "int",
}
])
```

### Writing the data

Writing the output dataset is done via a writer object returned by {meth}`~dataiku.Dataset.get_writer`

```py
with output.get_writer() as writer:
    for (origin,count) in origin_count.items():
        writer.write_row_array((origin,count))
```

Don't forget to close your writer. If you don't, your data will not get fully written. In some cases (like SQL output datasets), no data will get written at all.

We strongly recommend that you use the ``with`` keyword in Python to ensure that the writer is closed.


## Sampling

All calls to iterate the dataset ({meth}`~dataiku.Dataset.get_dataframe`, {meth}`~dataiku.Dataset.iter_dataframes`, {meth}`~dataiku.Dataset.iter_rows`, and {meth}`~dataiku.Dataset.iter_tuples`) take several arguments to set sampling.

Sampling lets you only retrieve a selection of the rows of the input dataset. It's often useful when using Pandas if your dataset does not fit in RAM.

For more information about sampling methods, please see [Sampling](https://doc.dataiku.com/dss/latest/preparation/sampling.html).

The `sampling` argument takes the following values: `head`, `random`, `random-column`

* `head` returns the first rows of the dataset. Additional arguments:

    * `limit=X` : number of rows to read

* `random` returns a random sample of the dataset. Additional arguments:

    * `ratio=X`: ratio (between 0 and 1) to select.
    * OR: `limit=X`: number of rows to read.

* `random-column` return a column-based random sample. Additional arguments:

    * `sampling_column`: column to use for sampling
    * `ratio=X`: ratio (between 0 and 1) to select


Examples:

```py
# Get a Dataframe over the first 3K rows
dataset.get_dataframe(sampling='head', limit=3000)

# Iterate over a random 10% sample
dataset.iter_tuples(sampling='random', ratio=0.1)

# Iterate over 27% of the values of column 'user_id'
dataset.iter_tuples(sampling='random-column', sampling_column='user_id', ratio=0.27)

# Get a chunked stream of dataframes over 100K randomly selected rows
dataset.iter_dataframes(sampling='random', limit=100000)
```

## Getting a dataset as raw bytes

In addition to retrieving a dataset as Pandas Dataframes or iterator, you can also ask DSS for a streamed export, as formatted data.

Data can be exported by DSS in various formats: CSV, Excel, Avro, ...

```py
# Read a dataset as Excel, and dump to a file, chunk by chunk
#
# Very important: you MUST use a with() statement to ensure that the stream
# returned by raw_formatted is closed

with open(target_path, "wb") as ofl:
        with dataset.raw_formatted_data(format="excel") as ifl:
                while True:
                        chunk = ifl.read(32000)
                        if len(chunk) == 0:
                                break
                        ofl.write(chunk)
```

## Data interaction (dataikuapi variant)

This section covers reading data using the `dataikuapi` pacakge. We recommend that you rather use the `dataiku` package for reading data.
{doc}`/getting-started/dataiku-python-apis/index` explains how to use and connect to the `dataikuapi` package.

### Reading data (dataikuapi variant)

The data of a dataset can be streamed with the {meth}`~dataikuapi.dss.dataset.DSSDataset.iter_rows()` method.
This call returns the raw data, so that in most cases it is necessary to first get the dataset's schema with a call to {meth}`dataikuapi.dss.dataset.DSSDataset.get_schema()`. For example, printing the first 10 rows can be done with

```python
columns = [column['name'] for column in dataset.get_schema()['columns']]
print(columns)
row_count = 0
for row in dataset.iter_rows():
        print(row)
        row_count = row_count + 1
        if row_count >= 10:
                break
```

outputs

```
['tube_assembly_id', 'supplier', 'quote_date', 'annual_usage', 'min_order_quantity', 'bracket_pricing', 'quantity', 'cost']
['TA-00002', 'S-0066', '2013-07-07', '0', '0', 'Yes', '1', '21.9059330191461']
['TA-00002', 'S-0066', '2013-07-07', '0', '0', 'Yes', '2', '12.3412139792904']
['TA-00002', 'S-0066', '2013-07-07', '0', '0', 'Yes', '5', '6.60182614356538']
['TA-00002', 'S-0066', '2013-07-07', '0', '0', 'Yes', '10', '4.6877695119712']
['TA-00002', 'S-0066', '2013-07-07', '0', '0', 'Yes', '25', '3.54156118026073']
['TA-00002', 'S-0066', '2013-07-07', '0', '0', 'Yes', '50', '3.22440644770007']
['TA-00002', 'S-0066', '2013-07-07', '0', '0', 'Yes', '100', '3.08252143576504']
['TA-00002', 'S-0066', '2013-07-07', '0', '0', 'Yes', '250', '2.99905966403855']
['TA-00004', 'S-0066', '2013-07-07', '0', '0', 'Yes', '1', '21.9727024365273']
['TA-00004', 'S-0066', '2013-07-07', '0', '0', 'Yes', '2', '12.4079833966715']
```

### Reading data for a partition (dataikuapi variant)

The data of a given partition can be retrieved by passing the appropriate partition spec as parameter to {meth}`dataikuapi.dss.dataset.DSSDataset.iter_rows()`:

```python
row_count = 0
for row in dataset.iter_rows(partitions='partition_spec1,partition_spec2'):
        print(row)
        row_count = row_count + 1
        if row_count >= 10:
                break
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataiku.Dataset
    dataikuapi.dss.dataset.DSSDataset
    dataiku.core.dataset_write.DatasetWriter
```

### Functions
```{eval-rst}
.. autosummary::
    ~dataiku.Dataset.get_dataframe
    ~dataiku.Dataset.get_fast_path_dataframe
    ~dataikuapi.dss.dataset.DSSDataset.get_schema
    ~dataiku.Dataset.get_writer
    ~dataiku.Dataset.iter_dataframes
    ~dataikuapi.dss.dataset.DSSDataset.iter_rows
    ~dataiku.Dataset.iter_tuples
    ~dataiku.Dataset.raw_formatted_data
    ~dataiku.Dataset.write_dataframe
    ~dataiku.core.dataset_write.DatasetWriter.write_dataframe
    ~dataiku.core.dataset_write.DatasetWriter.write_row_array
    ~dataiku.Dataset.write_schema_from_dataframe
    ~dataiku.Dataset.write_with_schema
```