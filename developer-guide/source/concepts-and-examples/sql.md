(sql)=

# Performing SQL, Hive and Impala queries

You can use the Python APIs to execute SQL queries on any SQL connection in DSS (including Hive and Impala).

:::{note}
There are three capabilities related to performing SQL queries in Dataiku's Python APIs:

- {class}`dataiku.SQLExecutor2`, {class}`dataiku.HiveExecutor` and {class}`dataiku.ImpalaExecutor` in the `dataiku` package. It was initially designed for usage within DSS in recipes and Jupyter notebooks. These are used to perform queries and retrieve results, either as an iterator or as a pandas dataframe
- "partial recipes". It is possible to execute a "partial recipe" from a Python recipe, to execute a Hive, Impala or SQL query. This allows you to use Python to dynamically generate a SQL (resp Hive, Impala) query and have DSS execute it, as if your recipe was a SQL query recipe. This is useful when you need complex business logic to generate the final SQL query and can't do it with only SQL constructs.
- {meth}`dataikuapi.DSSClient.sql_query` in the `dataikuapi` package. This function was initially designed for usage outside of DSS and only supports returning results as an iterator. It does not support pandas dataframe

We recommend the usage of the `dataiku` variants.

For more details on the two packages, please see {doc}`index`
:::

## Executing queries

You can retrieve the results of a SELECT query as a Pandas dataframe.

```py
from dataiku import SQLExecutor2

executor = SQLExecutor2(connection="db-connection") # or dataset="dataset_name"
df = executor.query_to_df("SELECT col1, COUNT(*) as count FROM mytable")
# df is a Pandas dataframe with two columns : "col1" and "count"
```

Alternatively, you can retrieve the results of a query as an iterator.

```py
from dataiku import SQLExecutor2

executor = SQLExecutor2(connection="db-connection")
query_reader = executor.query_to_iter("SELECT * FROM mytable")
query_iterator = query_reader.iter_tuples()
```

### Queries with side-effects

For databases supporting commit, the transaction in which the queries are executed is rolled back at the end, as is the default in DSS.

In order to perform queries with side-effects such as INSERT or UPDATE, you need to add `post_queries=['COMMIT']` to your `query_to_df` call.

Depending on your database, DDL queries such as `CREATE TABLE` will also need a `COMMIT` or not.

## Partial recipes

It is possible to execute a "partial recipe" from a Python recipe, to execute a Hive, Impala or SQL query.

This allows you to use Python to dynamically generate a SQL (resp Hive, Impala) query and have DSS execute it, as if your recipe was a SQL query recipe.

This is useful when you need complex business logic to generate the final SQL query and can't do it with only SQL constructs.

:::{note}
Partial recipes are only possible when you are running a Python recipe. It is not available in the notebooks nor outside of DSS.

The partial recipe behaves like the corresponding SQL (resp Hive, Impala) recipe w.r.t. the inputs and outputs. Notably, a Python recipe in which a partial Hive recipe is executed can only have HDFS datasets as inputs and outputs. Likewise, a Impala or SQL partial recipe having only one ouput, the output dataset has to be specified for the partial recipe execution.
:::

In the following example, we make a first query in order to dynamically build the larger query that runs as the "main" query of the recipe.

```py
from dataiku import SQLExecutor2

# get the needed data to prepare the query
# for example, load from another table
executor = SQLExecutor2(dataset=my_auxiliary_dataset)
words = executor.query_to_df(
"SELECT word FROM word_frequency WHERE frequency > 0.01 AND frequency < 0.99")

# prepare a query dynamically
sql = 'SELECT id '
for word in words['word']:
    sql = sql + ", (length(text) - length(regexp_replace(text, '" + word + "', ''))) / " + len(word) + " AS count_" + word
sql = sql + " FROM reviews"

# execute it
# no need to instantiate an executor object, the method is static
my_output_dataset = dataiku.Dataset("my_output_dataset_name")
SQLExecutor2.exec_recipe_fragment(my_output_dataset, sql)
```

## Executing queries (dataikuapi variant)

:::{note}
We recommend using {class}`~dataiku.SQLExecutor2` rather, especially inside DSS.
:::

Running a query against DSS is a 3-step process:

> - create the query
> - run it and fetch the data
> - verify that the streaming of the results wasn't interrupted

The verification will make DSS release the resources taken for the query's execution, so the {meth}`~dataikuapi.dss.sqlquery.DSSSQLQuery.verify()` call has to be done once the results have been streamed.

An example of a SQL query on a connection configured in DSS is:

```python
streamed_query = client.sql_query('select * from train_set', connection='local_postgres', type='sql')
row_count = 0
for row in streamed_query.iter_rows():
        row_count = row_count + 1
streamed_query.verify() # raises an exception in case something went wrong
print('the query returned %i rows' % count)
```

Queries against Hive and Impala are also possible. In that case, the type must be set to 'hive' or 'impala' accordingly, and instead of a connection it is possible to pass a database name:

```python
client = DSSClient(host, apiKey)
streamed_query = client.sql_query('select * from train_set', database='test_area', type='impala')
...
```

In order to run queries before or after the main query, but still in the same session, for example to set variables in the session, the API provides 2 parameters `pre_queries` and `post_queries` which take in arrays of queries:

```python
streamed_query = client.sql_query('select * from train_set', database='test_area', type='hive', pre_queries=['set hive.execution.engine=tez'])
...
```

## Detailed examples

This section contains more advanced examples on executing SQL queries.

### Remap Connections between Design and Automation for SQLExecutor2

When you deploy a project from a Design Node to an Automation Node, you may have to remap the Connection name used as a parameter in [SQLExecutor2](https://doc.dataiku.com/dss/latest/python-api/sql.html#executing-queries) to the name of the connection used on the Automation node.

```{literalinclude} examples/sql/sqlexec2-conn-remap.py
```


## Reference documentation

```{eval-rst}
.. autosummary::
        dataiku.SQLExecutor2
        dataiku.HiveExecutor
        dataiku.ImpalaExecutor
        dataikuapi.dss.sqlquery.DSSSQLQuery
```
