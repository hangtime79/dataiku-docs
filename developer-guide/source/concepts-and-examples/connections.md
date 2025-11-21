(connections)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 26/09/2024
  
  this code samples has been verified on DSS: 14.2.0
  Date of check: 18/09/2025
```
# Connections

The API exposes DSS connections, which can be created, modified and deleted through the API. These operations are restricted to API keys with the "admin rights" flag.

## Getting the list of connections

A list of the connections can by obtained with the {meth}`~dataikuapi.DSSClient.list_connections` method:

```python
client = DSSClient(host, apiKey)
dss_connections = client.list_connections()
prettyprinter.pprint(dss_connections)
```

outputs

```
{   'filesystem_managed': {   'allowManagedDatasets': True,
                               'allowMirror': False,
                               'allowWrite': True,
                               'allowedGroups': [],
                               'maxActivities': 0,
                               'name': 'filesystem_managed',
                               'params': {   'root': '${dip.home}/managed_datasets'},
                               'type': 'Filesystem',
                               'usableBy': 'ALL',
                               'useGlobalProxy': True},
    'hdfs_root':                  {    'allowManagedDatasets': True,
                                   'allowMirror': False,
                                   'allowWrite': True,
                                   'allowedGroups': [],
                                   'maxActivities': 0,
                                   'name': 'hdfs_root',
                                   'params': {'database': 'dataik', 'root': '/'},
                                   'type': 'HDFS',
                                   'usableBy': 'ALL',
                                   'useGlobalProxy': False},
    'local_postgress':    {    'allowManagedDatasets': True,
                               'allowMirror': False,
                               'allowWrite': True,
                               'allowedGroups': [],
                               'maxActivities': 0,
                               'name': 'local_postgress',
                               'params': { 'db': 'testdb',
                                           'host': 'localhost',
                                           'password': 'admin',
                                           'port': '5432',
                                           'properties': {   },
                                           'user': 'admin'},
                            'type': 'PostgreSQL',
                            'usableBy': 'ALL',
                            'useGlobalProxy': False},
    ...
}
```

## Creating a connection

Connections can be added:

```python
new_connection_params = {'db':'mysql_test', 'host': 'localhost', 'password': 'admin', 'properties': [{'name': 'useSSL', 'value': 'true'}], 'user': 'admin'}
new_connection = client.create_connection('test_connection', type='MySql', params=new_connection_params, usable_by='ALLOWED', allowed_groups=['administrators','data_team'])
prettyprinter.pprint(client.list_connections()['test_connection'])
```

outputs

```
{   'allowManagedDatasets': True,
    'allowMirror': True,
    'allowWrite': True,
    'allowedGroups': ['data_scientists'],
    'maxActivities': 0,
    'name': 'test_connection',
    'params': {   'db': 'mysql_test',
                   'host': 'localhost',
                   'password': 'admin',
                   'properties': {   },
                   'user': 'admin'},
    'type': 'MySql',
    'usableBy': 'ALLOWED',
    'useGlobalProxy': True}
```

## Modifying a connection

To modify a connection, it is advised to first retrieve the connection definition with a {py:meth}`~dataikuapi.dss.admin.DSSConnection.get_definition` call, alter the definition, and set it back into DSS:

```python
connection_definition = new_connection.get_definition()
connection_definition['usableBy'] = 'ALL'
connection_definition['allowWrite'] = False
new_connection.set_definition(connection_definition)
prettyprinter.pprint(new_connection.get_definition())
```

outputs

```
{   'allowManagedDatasets': True,
    'allowMirror': True,
    'allowWrite': False,
    'allowedGroups': ['data_scientists'],
    'maxActivities': 0,
    'name': 'test_connection',
    'params': {   'db': 'mysql_test',
                   'host': 'localhost',
                   'password': 'admin',
                   'properties': {   },
                   'user': 'admin'},
    'type': 'MySql',
    'usableBy': 'ALL',
    'useGlobalProxy': True}
```

## Deleting a connection

Connections can be deleted through their handle:

```python
connection = client.get_connection('test_connection')
connection.delete()
```

## Detailed examples

This section contains more advanced examples on Connections. 

### Mass-change filesystem Connections

You can programmatically switch all Datasets of a Project from a given filesystem Connection to a different one, thus reproducing the "Change Connection" action available in the Dataiku Flow UI.

```{literalinclude} examples/connections/mass-change-fs.py
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
        dataikuapi.dss.admin.DSSConnection
        dataikuapi.dss.admin.DSSConnectionDetailsReadability
        dataikuapi.dss.admin.DSSConnectionInfo
        dataikuapi.dss.admin.DSSConnectionListItem
        dataikuapi.dss.admin.DSSConnectionSettings
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.DSSClient.create_connection
    ~dataikuapi.DSSClient.get_connection
    ~dataikuapi.dss.admin.DSSConnection.get_definition
    ~dataikuapi.DSSClient.list_connections
    ~dataikuapi.dss.admin.DSSConnection.set_definition
```
