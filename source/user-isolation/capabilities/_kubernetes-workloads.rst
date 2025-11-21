
Running regular workloads
===========================

When you run non-Spark workloads on Kubernetes, the Kubernetes job is always started by the ``dssuser``. The ``dssuser`` requires the ability to connect and create pods and secrets on your Kubernetes cluster.

However, once the user's code has been started, a fundamental property of Kubernetes is that each container is independent and cannot access others. Thus, code running in one container is *isolated* from code running in another container without a specific need for impersonation.

No further setup is thus required for running regular workloads securely on Kubernetes.

Running Spark workloads
========================

When you run Spark workloads on Kubernetes, DSS uses the *sudo* mechanism of the local code isolation capability to start the ``spark-submit`` process running the Spark driver under the identity of the end-user. This driver process then sends control orders to Kubernetes in order to start pods for the Spark executor.

In other words, the Spark driver requires access to the Kubernetes API but runs untrusted code. This requires that each impersonated end-user has credentials to access Kubernetes. While this deployment is completely possible, it is not typically the case (each user needs to have a ``~/.kube/config`` file with proper credentials for the Kubernetes cluster).

To make it easier to run Spark on Kubernetes with UIF, DSS features a "managed Spark on Kubernetes" mode. In that mode, DSS can automatically generate temporary service accounts for each job, pass these temporary credentials to the Spark job, and delete the temporary service account after the job is complete.

In Kubernetes, the granularity of security is the namespace: if a service account has the right to create pods in a namespace, it is theoretically possible for it to gain all privileges on that namespace. Therefore, it is recommended to use one namespace per user (or one namespace per team). The "managed Spark on Kubernetes" mode can automatically create dynamic namespaces, and associate service accounts to namespaces. This requires that the account running DSS has credentials on the Kubernetes cluster that allow it to create namespaces.
