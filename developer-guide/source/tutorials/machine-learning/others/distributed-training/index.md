# Distributed ML Training using Ray

This notebook provides an example of distributed ML training on [Ray](https://docs.ray.io/en/latest/cluster/getting-started.html). 
Specifically, it illustrates how to:

1. Deploy a Ray Cluster on a {doc}`Dataiku-managed Elastic AI cluster <refdoc:containers/managed-k8s-clusters>`
2. Train a binary classification *xgboost* model in a distributed fashion on the deployed Ray Cluster.

## Pre-requisites

* {doc}`Dataiku-managed Elastic AI cluster <refdoc:containers/managed-k8s-clusters>`
* A {doc}`code environment <refdoc:code-envs/index>` with a Python version [supported by Ray](https://docs.ray.io/en/latest/ray-overview/installation.html#docker-source-images) (which at the time of writing are 3.9, 3.10 and 3.11) and with the following packages:
  ```python
  ray[default, train, client]
  xgboost
  lightgbm
  pyarrow
  boto3
  tqdm
  mlflow==2.17.2
  scikit-learn==1.0.2
  statsmodels==0.13.5
  ```

```{note}
The code environment only needs to be built locally, i.e., {doc}`containerized execution support <refdoc:containers/code-envs>` is not required.
```

### Deploying a Dataiku-managed Elastic AI cluster 
Before deploying the Ray Cluster, a Dataiku administrator must deploy an {doc}`Dataiku-managed Elastic AI cluster <refdoc:containers/managed-k8s-clusters>`. 

A few things to keep in mind about the Elastic AI Cluster:
- Dataiku recommends creating a dedicated `nodegroup` to host the Ray Cluster; the `nodegroup` can be static or auto-scale.
- Ray [recommends](https://docs.ray.io/en/latest/cluster/kubernetes/getting-started/raycluster-quick-start.html#step-3-deploy-a-raycluster-custom-resource) sizing each Ray Cluster pod to take up an entire Kubernetes node.
- Dataiku recommends that each cluster node have at least 64 GB RAM for typical ML workloads.

(tutorials/ml/others/distributed-learning/deploying-ray-cluster)=
## Deploying a Ray Cluster

The procedure to deploy a Ray Cluster onto a Dataiku-managed Elastic AI cluster is as follows. 

::::{tabs}

:::{group-tab} By plugin


```{important}
Note that this procedure requires Dataiku Administrator privileges.
```

1. Install [this](https://github.com/dataiku/dss-plugin-raycluster) plugin.
2. Navigate to the "Macros" section of a Dataiku project, search for the "Ray" macros, and select the "Start Ray Cluster" macro.

  ```{figure} ./assets/macros.png
  :align: center
  :class: with-shadow image-popup w500
  :alt: Figure 1.1 -- Macros for Ray

  Figure 1.1 -- Macros for Ray
  ```

3. Fill in the macro fields, keeping in mind the following information:

  - KubeRay version: select the latest version from their [GitHub release](https://github.com/ray-project/kuberay/releases) page.
  - Ray image tag: should be a valid tag from [Ray's DockerHub](https://hub.docker.com/r/rayproject/ray) images; 
    the Python version of the image tag should match the Python version of the Dataiku code environment created in the pre-requisites section.
  - Ray version: must match the version on the Ray image tag.
  - The CPU / memory request should be at least 1 CPU / 1GB RAM less than the node's schedulable amount. 
  - The number of Ray Cluster agents (i.e., head + worker replicas) should be equal to (or smaller) than the max size of the default Kubernetes `nodegroup`.

  Run the macro.

  ```{figure} ./assets/start-macro.png
  :align: center
  :class: with-shadow image-popup w500
  :alt: Figure 1.2 -- Start macro

  Figure 1.2 -- Start macro
  ```

4. Once the "Start Ray Cluster" is macro complete, run the "Inspect Ray Cluster" macro; this retrieves the Ray Cluster deployment status and provides the Ray Cluster endpoint once the cluster is ready. 


  ```{figure} ./assets/inspect-macro.png
  :align: center
  :class: with-shadow image-popup w500
  :alt: Figure 1.3 -- Inspect Ray Cluster

  Figure 1.3 -- Inspect Ray Cluster
  ```
    
5. Optionally, set up a port forwarding connection to https://github.com/dataiku/dss-plugin-rayclustere Ray Dashboard using the "Ray Dashboard Port-Forward" macro.

```{figure} ./assets/port-forward-macro.png
:align: center
:class: with-shadow image-popup w500
:alt: Figure 1.4 -- Ray Dashboard Port-Forward

Figure 1.4 -- Ray Dashboard Port-Forward
```

    
  The Ray Dashboard will then be accessible at `http://\<Dataiku instance domain>:8265` while the macro is running. 
     
:::

:::{group-tab} Advanced setup

```{important}
Note that this procedure requires SSH access to the Dataiku server.
```

1. SSH onto the Dataiku server and switch to the {doc}`dssuser <refdoc:user-isolation/index>`.
2. Point `kubectl` to the `kubeconfig` of the Elastic AI cluster onto which the Ray Cluster will be deployed:

    ```
    export KUBECONFIG=/PATH/TO/DATADIR/clusters/<cluster name>/exec/kube_config
    ```
    
    where `/PATH/TO/DATADIR` is the path to Dataiku's {doc}`data directory <refdoc:operations/datadir>`, and `<cluster name>` is the name of the Elastic AI cluster. 

3. Install the Ray Operator on the cluster:

    ```
    helm repo add kuberay https://ray-project.github.io/kuberay-helm/
    helm repo update
    helm install kuberay-operator kuberay/kuberay-operator --version 1.2.2
    ```

4. Deploy the Ray Cluster:

    ```
    helm install -f ray-values.yaml --version 1.2.2 raycluster kuberay/ray-cluster
    ```
    
    where `ray-values.yaml` is a file such as:
    
    ```yaml
    image:
      tag: 2.40.0.22541c-py310

    head:
      rayVersion: 2.40.0
      nodeSelector:
        nodegroupName: rayNodegroup
      resources:
        limits:
          cpu: "7"
          memory: "30G"
        requests:
          cpu: "7"
          memory: "30G"

    worker:
      replicas: 2
      nodeSelector:
        nodegroupName: rayNodegroup
      resources:
        limits:
          cpu: "7"
          memory: "30G"
        requests:
          cpu: "7"
          memory: "30G"
     ```
     
     ```{attention}
     - The `image.tag` should be a valid tag from one of [Ray's DockerHub](https://hub.docker.com/r/rayproject/ray) images.
     - The Python version of the `image.tag` should match the Python version of the Dataiku code environment created in the pre-requisites section.
     - The `head.rayVersion` must match the version on the `image.tag`.
     - The `head.resources.limits` should match the `head.resources.requests` values (and the same for the worker resources and limits) as per [Ray's documentation](https://docs.ray.io/en/latest/cluster/kubernetes/user-guides/config.html#resources).
     - The CPU / memory request should be at least 1 CPU / 1GB RAM less than the node's schedulable amount. 
     - The number of Ray Cluster agents (i.e., head + worker replicas) should be equal to (or smaller) the max size of the Kubernetes `nodegroup` onto which they will be deployed (i.e., the `rayNodegroup`).
     ```

     For the complete schema of the Ray Cluster values file, see [Ray's GitHub repo](https://github.com/ray-project/kuberay-helm/blob/main/helm-chart/ray-cluster/values.yaml).
     
5. Watch the Ray Cluster pods being created:
    
    ```
    kubectl get pods -A -w
    ```
(tutorials/ml/others/distributed-learning/step6)=
6. Once the head pod has been successfully created, describe it and determine its IP:

    ```
    kubect describe pod <ray-cluster-head-pod-name>
    ```
    
    The Ray Cluster endpoint is `http://<head pod IP>:8265`.
    
7. Optionally, setup a port forwarding connection to the Ray Dashboard:

    ```
    kubectl port-forward service/raycluster-kuberay-head-svc --address 0.0.0.0 8265:8265
    ```
    
    The Ray Dashboard will be accessible at `http://<Dataiku instance domain>:8265`. 
    Accessing it via a browser may require opening this port at the firewall.

If everything goes well, you should end up with something similar to:
```{figure} ./assets/cluster-up-and-running.png
:align: center
:class: with-shadow image-popup w500
:alt: Figure 1 -- Ray cluster is up and running

Figure 1: Ray cluster is up and running
```

:::
::::

     
For more information on this procedure and how to further customize the deployment of a Ray Cluster on Kubernetes
(e.g., creating an auto-scaling Ray Cluster),
please refer to the relevant [Ray documentation](https://docs.ray.io/en/latest/cluster/kubernetes/index.html). 

## Train an XGBoost Model
Now that you have a running Ray Cluster, you can train ML models on it in a distributed fashion.
All they need to be provided with is the Ray Cluster endpoint, 
which was determined in {ref}`step 6 <tutorials/ml/others/distributed-learning/step6>` of the {ref}`tutorials/ml/others/distributed-learning/deploying-ray-cluster` section.

The following procedure illustrates how to train a binary classification *xgboost* model on a Ray Cluster using a data-parallel paradigm. The example draws inspiration from this [code sample](https://github.com/ray-project/ray/blob/master/release/train_tests/xgboost_lightgbm/train_batch_inference_benchmark.py) published in Ray's documentation. 

First, you will need to create a {doc}`Project Library </concepts-and-examples/project-libraries>` 
called `dku_ray` (under the `python` folder) with two files, `utils.py` and `xgboost_train.py`, with the following content:

````{dropdown} [utils.py](./assets/utils.py)
```{literalinclude} ./assets/utils.py
:language: python
:caption: utils.py
```
````

````{dropdown} [xgboost_train.py](./assets/xgboost_train.py)
```{literalinclude} ./assets/xgboost_train.py
:language: python
:caption: xgboost_train.py
```
````

Second, you must create a dataset in the Flow to be used as the model's training dataset.
This example (and the code of the `dku_ray` project library) assumes that this dataset is:
- on S3
- in the parquet format
- on a Dataiku S3 connection that uses STS with AssumeRole as its authentication method
  and that the user running the code has "details readable by" access on the connection

```{note}
Modifying the code with different connection and/or authentication types should be straightforward.
```

Third, you must create a managed folder in the Flow, where Ray will store the training process outputs.
Similar to the training dataset,
this example assumes the managed folder is on an S3 connection with the same properties listed above.

Finally, the following code can be used to train a model on the input dataset. 
In this case, the "avocado_transactions_train" is a slightly processed version of [this Kaggle dataset](https://www.kaggle.com/datasets/neuromusic/avocado-prices).

### Importing the required packages

```{literalinclude} assets/code.py
:language: python
:lines: 1-15
```

### Setting the default parameters

```{literalinclude} assets/code.py
:language: python
:lines: 17-37
```

### Setting the training script

```{literalinclude} assets/code.py
:language: python
:lines: 39-52
```

### Submitting the job to Ray

```{literalinclude} assets/code.py
:language: python
:lines: 54-
```

Once you've submitted the job, you can see it running in the Ray dashboard shown below:

```{figure} ./assets/jobs-submitted.png
:align: center
:class: with-shadow image-popup
:alt: Figure 2 -- Ray dashboard showing the running job

Figure 2 -- Ray dashboard showing the running job
```

Once the job succeeds, you should be able to find the `xgboost` object in the managed folder designated as the "output."

## Conclusion

You now know how to set up a Ray cluster to achieve distributed learning using the `xgboost` algorithm.
Adapting this tutorial to your preferred algorithm and/or cluster should be easy.

Here is the complete code for this tutorial:
````{dropdown} [code.py](./assets/code.py)
:open:
```{literalinclude} assets/code.py
:language: python
```
````

