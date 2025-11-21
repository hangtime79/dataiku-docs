(tables-import)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 25/09/2024
  
  this code samples has been verified on DSS: 14.2.0
  Date of check: 16/09/2025  
```

# Importing tables as datasets

The "import tables as datasets" feature is available through the API, both for Hive and SQL tables

## Importing SQL tables

```python
import dataiku

client = dataiku.api_client()
project = client.get_default_project()

import_definition = project.init_tables_import()
import_definition.add_sql_table("my_sql_connection", "schema_of_the_databse", "name_of_the_table")

prepared_import = import_definition.prepare()
future = prepared_import.execute()

import_result = future.wait_for_result()
```

## Importing Hive tables

```python
import dataiku

client = dataiku.api_client()
project = client.get_default_project()

import_definition = project.init_tables_import()
import_definition.add_hive_table("hdfs_managed", "hive_table_name")

prepared_import = import_definition.prepare()
future = prepared_import.execute()

import_result = future.wait_for_result()
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataikuapi.dss.project.TablesImportDefinition
    dataikuapi.dss.project.TablesPreparedImport
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.project.TablesImportDefinition.add_hive_table
    ~dataikuapi.dss.project.TablesImportDefinition.add_sql_table
    ~dataikuapi.dss.project.TablesPreparedImport.execute
    ~dataikuapi.dss.project.DSSProject.init_tables_import
    ~dataikuapi.dss.project.TablesImportDefinition.prepare
```