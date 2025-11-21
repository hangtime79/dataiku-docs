(clusters)=

```{eval-rst}
..
  this code samples has been verified on DSS: 14.2.0.alpha3
  Date of check: 11/09/2025

  this code samples has been verified on DSS: 13.2.0
  Date of check: 04/10/2024
```

# Clusters

The API offers methods to:

- Start, stop or delete clusters
- Read and write settings of clusters
- Get the status of clusters

Clusters may be listed, created and obtained using methods of the {py:class}`~dataikuapi.dssclient.DSSClient`:

- list clusters: {py:meth}`~dataikuapi.DSSClient.list_clusters`
- obtain a handle on a cluster: {py:meth}`~dataikuapi.DSSClient.get_cluster()`
- create a cluster: {py:meth}`~dataikuapi.DSSClient.create_cluster()`

{py:class}`~dataikuapi.dss.admin.DSSClusterSettings` is an opaque type and its content is specific to each cluster provider. It is therefore strongly advised to use scenario steps to create/start/delete clusters, as this will greatly help define a consistent configuration.

## Starting a managed cluster

```python
import logging
logger = logging.getLogger("my.package")

client = dataiku.api_client()

cluster_id = "my_cluster_id"

# Obtain a handle on the cluster
my_cluster = client.get_cluster(cluster_id)

# Start the cluster. This operation is synchronous. An exception is thrown in case of error
try:
    my_cluster.start()
    logger.info("Cluster {} started".format(cluster_id))
except Exception as e:
    logger.exception("Could not start cluster: {}".format(e))
```

## Getting the status of a cluster

```python
import logging
logger = logging.getLogger("my.package")

client = dataiku.api_client()

cluster_id = "my_cluster_id"

# Obtain a handle on the cluster
my_cluster = client.get_cluster(cluster_id)

# Get status
status = my_cluster.get_status()

logger.info("Cluster status is {}".format(status.status))
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataikuapi.dss.admin.DSSCluster
    dataikuapi.dss.admin.DSSClusterSettings
    dataikuapi.dss.admin.DSSClusterStatus
```

### Functions

```{eval-rst}
.. autosummary::
    ~dataikuapi.DSSClient.get_cluster
    ~dataikuapi.dss.admin.DSSCluster.get_status
    ~dataikuapi.dss.admin.DSSCluster.start
```
