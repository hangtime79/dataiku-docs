# Using Dask DataFrames in Dataiku

This article introduces distributed data manipulation in Dataiku using [Dask DataFrames](https://docs.dask.org/en/stable/dataframe.html).  
Specifically, it illustrates how to:

1. Deploy a Dask Cluster on a {doc}`Dataiku-managed Elastic AI cluster <refdoc:containers/managed-k8s-clusters>`.
2. Natively read a Dataiku dataset as a Dask DataFrame (i.e., without an intermediate step as a Pandas DataFrame).
3. Perform distributed, parallelized computations on the Dask DataFrame.

## Pre-requisites

* {doc}`Dataiku-managed Elastic AI cluster <refdoc:containers/managed-k8s-clusters>`
* A {doc}`code environment <refdoc:code-envs/index>` with a Python version 
  [supported by Docker Dask](https://github.com/dask/dask-docker)
  (which at the time of writing are 3.10, 3.11, and 3.12) and with the following packages:

  ```python
  dask[distributed]
  pyarrow
  s3fs
  ```

```{note}
The code environment only needs to be built locally, i.e., 
{doc}`containerized execution support <refdoc:containers/code-envs>` is not required.
```

### Deploying a Dataiku-managed Elastic AI cluster 
Before deploying the Dask Cluster,
a Dataiku administrator must deploy a {doc}`Dataiku-managed Elastic AI cluster <refdoc:containers/managed-k8s-clusters>`. 

A few things to keep in mind about the Elastic AI Cluster:
- Dataiku recommends creating a dedicated `nodegroup` to host the Dask Cluster; the `nodegroup` can be static or auto-scale.
- Dataiku recommends that each cluster node have at least 32 GB RAM for typical data processing workloads.

## Deploying a Dask Cluster

The procedure to deploy a Dask Cluster onto a Dataiku-managed Elastic AI cluster is as follows. 

::::{tabs}

:::{group-tab} By plugin


```{important}
Note that this procedure requires Dataiku Administrator privileges.
```

1. Install [this](https://github.com/dataiku/dss-plugin-daskcluster) plugin.
2. Navigate to the "Macros" section of a Dataiku project, search for the "Dask" macros,
   and select the "Start Dask Cluster" macro.

   ```{figure} ./assets/macros.png
   :align: center
   :class: with-shadow image-popup w500
   :alt: Figure 1.1 -- Macros for Dask

   Figure 1.1 -- Macros for Dask
   ```

3. Fill in the macro fields, keeping in mind the following information:

   - Dask image tag: this should be a valid tag from [Dask's Docker Registry](https://github.com/dask/dask-docker); 
     the Python version of the image tag should match the Python version
     of the Dataiku code environment created in the pre-requisites section.
   - The CPU / memory request should be at least 1 CPU / 2GB RAM per worker. 
   - The total worker resources should fit within the Elastic AI Cluster's default `nodegroup`. 

   Run the macro.

   ```{figure} ./assets/start-macro.png
   :align: center
   :class: with-shadow image-popup w500
   :alt: Figure 1.2 -- Start macro
 
   Figure 1.2 -- Start macro
   ```

4. Once the "Start Dask Cluster" macro is complete, run the "Inspect Dask Cluster" macro;
   this retrieves the Dask Cluster deployment status and provides the Dask Cluster endpoint once the cluster is ready. 


   ```{figure} ./assets/inspect-macro.png
   :align: center
   :class: with-shadow image-popup w500
   :alt: Figure 1.3 -- Inspect Dask Cluster
 
   Figure 1.3 -- Inspect Dask Cluster
   ```
    
5. Optionally, set up a port forwarding connection to the Dask Dashboard using the "Dask Dashboard Port-Forward" macro.

   ```{figure} ./assets/port-forward-macro.png
   :align: center
   :class: with-shadow image-popup w500
   :alt: Figure 1.4 -- Dask Dashboard Port-Forward
   
   Figure 1.4 -- Dask Dashboard Port-Forward
   ```

    
   The Dask Dashboard will then be accessible at `http://\<Dataiku instance domain>:8787` while the macro is running. 

If everything goes well, you should end up with something similar to:
```{figure} ./assets/cluster-up-and-running.png
:align: center
:class: with-shadow image-popup w500
:alt: Figure 1 -- Dask cluster is up and running

Figure 1: Dask cluster is up and running
```
     
:::

:::{group-tab} Advanced setup

```{important}
Note that this procedure requires SSH access to the Dataiku server.
```

1. SSH onto the Dataiku server and switch to the {doc}`dssuser <refdoc:user-isolation/index>`.
2. Point `kubectl` to the `kubeconfig` of the Elastic AI cluster onto which the Dask Cluster will be deployed:

    ```
    export KUBECONFIG=/PATH/TO/DATADIR/clusters/<cluster name>/exec/kube_config
    ```
    
    where `/PATH/TO/DATADIR` is the path to Dataiku's {doc}`data directory <refdoc:operations/datadir>`, and `<cluster name>` is the name of the Elastic AI cluster. 

3. Install the Dask Operator on the cluster:

    ```
    helm repo add dask https://helm.dask.org
    helm repo update
    helm install --create-namespace -n dask-operator --generate-name dask/dask-kubernetes-operator  
    ```

4. Deploy the Dask Cluster:

    ```
    kubectl apply -f dask-cluster.yaml 
    ```
    
    where `dask-cluster.yaml` is a file such as:
    
    ```yaml
    apiVersion: kubernetes.dask.org/v1
    kind: DaskCluster
    metadata:
      namespace: dask
      name: simple-dask-cluster
    spec:
      worker:
        replicas: 2
        spec:
          nodeSelector:
            label: value
          containers:
          - name: worker
            image: "ghcr.io/dask/dask:latest-py3.10"
            imagePullPolicy: "IfNotPresent"
            args:
              - dask-worker
              - --name
              - $(DASK_WORKER_NAME)
              - --dashboard
              - --dashboard-address
              - "8788"
            ports:
              - name: http-dashboard
                containerPort: 8788
                protocol: TCP
            resources:
              limits:
                cpu: "1"
                memory: "2G"
              requests:
                cpu: "1"
                memory: "2G"
      scheduler:
        spec:
          nodeSelector:
            labelkey: labelvalue 
          containers:
          - name: scheduler
            image: "ghcr.io/dask/dask:latest-py3.10"
            imagePullPolicy: "IfNotPresent"
            args:
              - dask-scheduler
            ports:
              - name: tcp-comm
                containerPort: 8786
                protocol: TCP
              - name: http-dashboard
                containerPort: 8787
                protocol: TCP
            readinessProbe:
              httpGet:
                port: http-dashboard
                path: /health
              initialDelaySeconds: 5
              periodSeconds: 10
            livenessProbe:
              httpGet:
                port: http-dashboard
                path: /health
              initialDelaySeconds: 15
              periodSeconds: 20
        service:
          type: NodePort
          selector:
            dask.org/cluster-name: simple
            dask.org/component: scheduler
          ports:
          - name: tcp-comm
            protocol: TCP
            port: 8786
            targetPort: "tcp-comm"
          - name: http-dashboard
            protocol: TCP
            port: 8787
            targetPort: "http-dashboard"
     ```
     
     ```{attention}
     - The `metadata.namespace` is optional and should correspond to a previously created namespace;
       Dataiku recommends using a dedicated namespace for each Dask cluster.
     - The `metadata.name` and `spec.scheduler.service.selector.dask.org/cluster-name` should be set to the desired Dask cluster name.
     - The `spec.worker.spec.nodeSelector` and `spec.scheduler.spec.nodeSelector` are optional.
     - The `spec.worker.replicas` should be set to the desired number of Dask workers.
     - The `spec.worker.spec.containers["worker"].name` and
       `spec.scheduler.spec.containers["scheduler"].name` fields should be the same and be valid tags 
       from one of [Dask's Docker Registry](https://github.com/dask/dask-docker) images.
     - The Python version of the `spec.worker.spec.containers["worker"].name` and
       `spec.scheduler.spec.containers["scheduler"].name` should match the Python version
       of the Dataiku code environment created in the pre-requisites section.
     - The `spec.worker.spec.containers["worker"].resources.limits` should be set to a **minimum** of 1 vCPU
       and 2GB RAM (although significantly more resources will likely be required depending on the specific data processing task).
     ```

     For the complete schema of the Dask Cluster YAML file, see the [Dask documentation](https://kubernetes.dask.org/en/latest/operator_resources.html#full-configuration-reference).
     
5. Watch the Dask Cluster pods being created:
    
    ```
    kubectl get pods -A -w -n <dask cluster namespace>
    ```

6. Once the `scheduler` pod has been successfully created, describe it and determine its IP:

    ```
    kubect describe pod <dask-cluster-scheduler-pod-name> -n <dask cluster namespace>
    ```
    
    The Dask Cluster endpoint is `<scheduler pod IP>:8786`.
    
7. Optionally, set up a port forwarding connection to the Dask Dashboard:

    ```
    kubectl port-forward service/<dask cluster name>-scheduler -n <dask cluster namespace> --address 0.0.0.0 8787:8787
    ```
    
    The Dask Dashboard will be accessible at `http://<Dataiku instance domain>:8787`. 
    Accessing it via a browser may require opening this port at the firewall.

If everything goes well, you should end up with something similar to:
```{figure} ./assets/cluster-up-and-running.png
:align: center
:class: with-shadow image-popup w500
:alt: Figure 1 -- Dask cluster is up and running

Figure 1: Dask cluster is up and running
```

:::
::::

     
For more information on this procedure and how to further customize the deployment of a Dask Cluster on Kubernetes
(e.g., writing custom Dask Operator plugins),
please refer to the relevant [Dask Kubernetes documentation](https://kubernetes.dask.org/en/latest/index.html). 

## Read and Manipulate a Dataiku Dataset as a Dask DataFrame
Now that the Dask cluster is running, users can manipulate Dataiku datasets in a distributed, parallelized fashion
using Dask DataFrames. All that is required is the Dask cluster endpoint determined above. 

First, you will need to create a {doc}`Project Library </concepts-and-examples/project-libraries>` 
called `dku_dask` (under the `python` folder) with one file, `utils.py`, with the following content:

````{dropdown} [utils.py](./assets/utils.py)
```{literalinclude} ./assets/utils.py
:language: python
:caption: utils.py
```
````

Second, you must create a dataset in the Flow, which will be read as a Dask DataFrame.
This example (and the code of the `dku_dask` project library) assumes that this dataset is:
- on S3
- in the parquet format
- on a Dataiku S3 connection that uses STS with AssumeRole as its authentication method
  and that the user running the code has "details readable by" access on the connection

```{note}
Modifying this example code to work with different connection and/or authentication types should be straightforward.
For help, see the [Dask DataFrame API documentation](https://docs.dask.org/en/stable/dataframe-create.html).
```

Finally, the following code illustrates how to load a Dataiku dataset as a Dask DataFrame,
apply a `groupby` transformation to the DataFrame (distributed over the cluster),
and then collect the results.
In this case, the `avocado_transactions` dataset is a slightly processed version of
[this Kaggle dataset](https://www.kaggle.com/datasets/neuromusic/avocado-prices).


```{literalinclude} assets/code.py
:language: python
```

If all goes well, you should end up with something similar to (assuming you've run the code in a notebook):
```{figure} ./assets/groupby-result.png
:align: center
:class: with-shadow image-popup 
:alt: Figure 1 -- Groupby result

Figure 1: Groupby result
```

## Conclusion

You now know how to set up a Dask cluster to achieve distributed, parallelized data manipulation using Dask DataFrames.
Adapting this tutorial to your specific ETL needs should be easy.

Here is the complete code for this tutorial:
````{dropdown} [code.py](./assets/code.py)
:open:
```{literalinclude} assets/code.py
:language: python
```
````
