# Limiting the ports used by DSS

## Introduction

DSS has the ability to scale horizontally by distributing heavy computations on other machines, in order to overcome limitations of the DSS server machine.
This is done by leveraging a variety of mechanisms and technologies (DBs, Kubernetes, Docker, Spark, Hadoop, etc).

Some of these remote processes need to communicate with DSS, usually through the network.
By default these ports are chosen randomly, and DSS expects all ports to be opened in order to be reachable from the other machines.

Since DSS 10.0.0 it is possible to force DSS to pick ports in a certain range.

## Enable the feature

On a designer or automation Node:

* Stop DSS
* Edit the `DATADIR/config/dip.properties` file
* Add a line `dku.feature.portRangeLimitation.enabled=true`
* Start DSS
* In DSS, go to Administration > Settings > Misc.

You can enable the feature on this page, and choose a port range that will be used to communicate with the backend.

* Restart DSS

### Spark (2.x and 3.x)

When `Auto configure Spark` is selected, DSS automatically overrides the following configuration entries for Spark jobs:

* `spark.blockManager.port`
* `spark.driver.port`
* `spark.port.maxRetries`

## Firewall settings

The firewall should at least allow static ports used by DSS (see the list below), along with the range of ports specified in the settings.

```
DKU_BASE_PORT
DKU_NGINX_PORT
DKU_BACKEND_PORT
DKU_IPYTHON_PORT
DKU_HPROXY_PORT
DKU_EVENTSERVER_PORT
```

This list can also be found in the `DATADIR/bin/env-default.sh` file.
