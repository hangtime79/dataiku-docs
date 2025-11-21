# Autoscaling of data, model training, and inference workloads

In today’s data-driven world, leveraging the full potential of an organization’s collected data is essential for businesses to stay competitive. As organizations increasingly rely on data to drive decision-making, their data workloads are growing exponentially. This surge in data volume, coupled with the demand for real-time insights, presents a significant challenge for traditional data processing systems. Scaling these systems to meet the growing demands of data preparation, model training and inference, and the emerging needs of Generative AI is no longer optional \- it became a necessity.

A robust AI Platform must be equipped to handle these scaling requirements efficiently. Dataiku offers a set of capabilities to automatically adjust computational resources based on workload demands. By leveraging these capabilities, businesses can avoid the bottlenecks that come with static infrastructure, ensuring that data pipelines, model training processes, and inference tasks are executed seamlessly, even as data volumes increase or fluctuate.

This article describes Dataiku’s capabilities to address the before mentioned challenges. 

# Data Workloads

## Avoiding Data Movement

As data volumes grow, it becomes inefficient to extract large datasets into external processing systems. Rather than moving the data, the data transformation instructions should be executed where the data is located. Dataiku enables its users to run data pipelines directly in the underlying SQL databases, avoiding unnecessary data movement and ensuring more efficient processing.

### Translating No-Code Actions into SQL Code

In Dataiku, data transformations are defined in so called Recipes. No-Code users can define these transformations in [Visual Recipes](https://doc.dataiku.com/dss/latest/other_recipes/index.html). Dataiku translates these actions, such as filtering, transforming, and aggregating data, into optimized SQL queries. Users can interact with the platform through an intuitive, graphical interface, while the platform handles the SQL code generation in the background. This allows users, even those without deep SQL knowledge, to perform complex data preparation tasks directly within the database, improving speed and efficiency.

### Writing SQL Queries for Advanced Users

For advanced users, the platform offers the flexibility to write custom [SQL queries in Code Recipes](https://doc.dataiku.com/dss/latest/code_recipes/sql.html). This capability is ideal for complex data manipulations or specific transformations that go beyond the built-in functionality. Whether using the graphical interface or writing SQL directly, users can work with data in the most efficient way possible.

### Reducing Data Movement and Improving Performance

In both cases, the data transformation tasks are pushed down to the database, thus eliminating the need for data extraction, processing, and reloading. This minimizes data movement, saving time and resources. Additionally, databases are optimized for query execution, meaning that data preparation tasks like filtering, joins, and aggregations are performed faster and more efficiently, leading to better performance and scalability.

### Scalability and Flexibility

This approach scales effortlessly as data volumes grow. By executing tasks within the database, the platform adapts to increasing data sizes without sacrificing performance. Furthermore, it works with a variety of SQL-compliant databases, whether on-premises or in the cloud, ensuring flexibility and seamless integration across different data environments.

By pushing down data preparation tasks into the database, the platform reduces inefficiencies, enhances performance, and ensures scalability. This allows users to focus on more meaningful tasks, like building and deploying machine learning models, while leaving complex data transformations to the database itself.

## Offloading to Elastic AI Compute  

In addition to directly leveraging underlying databases, Dataiku can offload resource-intensive tasks to attached cluster technology. To achieve this, many operations within Dataiku can be [containerized](https://doc.dataiku.com/dss/latest/containers/concepts.html#containerized-execution-configurations) and executed externally, ensuring efficient use of computational resources. This capability, called [Elastic AI Compute](https://doc.dataiku.com/dss/latest/containers/concepts.html#concepts), utilizes [Kubernetes](https://doc.dataiku.com/dss/latest/containers/managed-k8s-clusters.html) as execution engine. The complexities of creating and managing these clusters is handled by Dataiku itself, allowing the platform to seamlessly distribute compute-heavy data transformation tasks to a cluster that scales horizontally based on demand.

### Scalable Clusters

With Elastic AI Compute, heavy computational workloads are offloaded from the central platform node to one or multiple clusters. Kubernetes manages the cluster’s resources, automatically scaling out by adding more nodes when demand increases, and scaling back in once the workload subsides. This ensures that tasks are completed efficiently without overburdening the central infrastructure.

### Dynamic Scaling for Efficiency

The core benefit of Elastic AI Compute is its ability to scale out during peak demand and scale back in afterward, optimizing resource usage. This dynamic scaling ensures that the platform can handle intensive data transformations tasks quickly and cost-effectively, releasing resources when they are no longer needed.

Elastic AI Compute empowers data scientists to perform large-scale data transformations with ease, without introducing the complexities of managing Kubernetes based clusters. This approach offers cost-effective, scalable compute that meets the demands of modern data science workflows.

## Spark workloads on Elastic AI Compute

While many data science and machine learning tasks can be efficiently handled directly by the platform or through SQL pushdown, certain complex workloads require more advanced computational power. For these scenarios, [the platform can leverage the attached Elastic AI Compute cluster to run Spark workloads](https://blog.dataiku.com/why-you-should-be-using-apache-spark-kubernetes-to-process-data-1). This capability is particularly useful when data is stored in object storage systems, such as Amazon S3, Azure Data Lake Storage,  Google Cloud Storage, or Hadoop Distributed File System (HDFS), where large-scale data processing is necessary.

### When Spark is Needed

Spark is used for large-scale data processing where tasks require distributed computing power. It is particularly necessary when datasets are too large to fit into memory on a single node or when computations need to be parallelized across multiple resources. The platform seamlessly integrates Spark with Elastic AI Compute, using Kubernetes for orchestration.

Similar to SQL-based transformations, Spark workloads can be defined either through code or using Visual Recipes, where Dataiku automatically translates the transformation steps into the corresponding Spark code.

### Spark on Kubernetes: Task Distribution and Scaling

When running Spark on Kubernetes, tasks are automatically divided into smaller units and distributed across the cluster. Kubernetes manages the orchestration, ensuring that tasks are assigned to the appropriate nodes based on resource availability. This horizontal scaling allows Spark to process large datasets more efficiently by parallelizing workloads. Kubernetes also automatically manages the lifecycle of Spark pods, adding more resources when demand increases and scaling back when the workload decreases. This ensures optimal resource usage and cost efficiency.

Running Spark workloads on the Elastic AI Compute cluster enables efficient processing of large-scale data transformations, particularly when using object storage. As with other Elastic AI Compute capabilities, end users do not need to concern themselves with the implementation details of the cluster or the execution of Spark jobs. This allows users to focus solely on defining the desired transformations, without managing the underlying infrastructure.

# Machine Learning \- Model Training and Inference 

## Training Models

In addition to supporting users during the data preparation process, training machine learning models is another critical function of an AI platform. This process is resource-intensive and requires a platform capable of scaling compute resources on demand. To address these challenges, Dataiku leverages the previously introduced concept of Elastic AI Compute, offloading workloads to an attached cluster as needed.

### Training in parallel

One of the key advantages of using an attached cluster for model training is the ability to train multiple models in parallel. Instead of training models sequentially, which can be time-consuming, Dataiku distributes each model's training process across different nodes in the cluster. This parallelization accelerates the overall training process, allowing data scientists to experiment [with different algorithms](https://doc.dataiku.com/dss/latest/machine-learning/algorithms/in-memory-python.html), hyperparameters, and datasets simultaneously.

For example, a data scientist might train multiple models to compare performance across various machine learning algorithms such as decision trees, support vector machines, and deep learning models. By utilizing the attached cluster, the platform can handle the simultaneous execution of these different models, reducing the time required for experimentation and model selection.

In most cases, training machine learning models is not a continuous task. It is typically performed at specific stages during a data science project, such as model development, experimentation, or retraining. These tasks occur at distinct intervals, rather than constantly throughout the project. As a result, compute resources are not always needed. Dataiku’s universal AI platform efficiently scales resources up when required for training and scales them back down during idle periods, optimizing costs by only using resources when necessary.

### Distributed Hyperparameter Search

Hyperparameter tuning is a crucial part of building effective machine learning models, but it can be computationally expensive, especially when exploring large search spaces. Dataiku provides a distributed hyperparameter search feature to address this challenge. Just as with model training, Elastic AI Compute is leveraged to achieve the desired scalability effects.

In traditional hyperparameter tuning, the search process can be slow, as it requires training multiple models with different hyperparameter combinations. Dataiku’s distributed hyperparameter search allows this process to be parallelized across multiple compute nodes, significantly speeding up the search. By offloading these tasks to an attached cluster, users can explore a broader set of hyperparameters in less time, without being constrained by the resources of a single machine.  
The ability to distribute hyperparameter search across a scalable cluster allows data scientists to experiment more freely and efficiently, exploring a wider range of hyperparameters in less time. By leveraging Kubernetes for automatic scaling, Dataiku ensures that compute resources are only allocated when needed, optimizing both performance and cost.

A more in-depth explanation of these aspects can be found on this [blog post](https://blog.dataiku.com/distributed-hyperparameter-search-how-its-done-in-dataiku).

## Model Inference

After training, models can be utilized in various ways within Dataiku. They can be used directly within the platform to score new data through large batch prediction jobs. Alternatively, models can be [deployed and exposed](https://doc.dataiku.com/dss/latest/apinode/index.html) to business applications via a REST API, making them accessible for real-time predictions.

### Models as Java Objects

In Dataiku, models are typically trained using Python, leveraging popular libraries like scikit-learn. However, when these models are deployed and exposed to external applications for inference, they are converted into Java code to optimize scoring performance. This conversion enhances the speed and efficiency of model inference, particularly in high-throughput, low-latency environments where Java's performance advantages are crucial. By using Java for model deployment, Dataiku ensures that models can handle production-scale demands while maintaining high responsiveness and scalability.

### Deploying Models to Elastic AI Compute clusters

The previously introduced [concept of Elastic AI Compute can also be used to expose models](https://doc.dataiku.com/dss/latest/apinode/kubernetes/index.html) as REST APIs. Built on Kubernetes, Elastic AI Compute allows models to be deployed as Kubernetes Services. These services are backed by pods that handle the inference requests. Kubernetes manages the lifecycle of these pods, ensuring high availability and fault tolerance for deployed models.

Elastic AI Compute takes advantage of Kubernetes' native horizontal scaling capabilities. The deployment can be configured to automatically scale based on resource utilization metrics such as CPU usage. When demand increases, Kubernetes can add new pods to distribute the inference workload, ensuring that the service can handle higher traffic volumes. Conversely, when demand decreases, Kubernetes can scale down the number of active pods, optimizing resource usage and reducing operational costs.

The scaling conditions and boundaries are configurable, allowing users to set thresholds. Kubernetes continuously monitors these metrics, adjusting the number of pods in the deployment to ensure the model’s performance remains optimal under varying load conditions.

### Deploying Models to External Platforms

In addition to exposing models on the attached Elastic AI Compute cluster, [Dataiku's Deploy Anywhere](https://blog.dataiku.com/redefining-flexibility-in-mlops-deploy-anywhere-with-dataiku) capability offers users the flexibility to export and deploy machine learning models on a wide range of [external platforms](https://doc.dataiku.com/dss/latest/apinode/deploy-anywhere.html), including Amazon SageMaker, Azure ML, Vertex AI, Databricks, and Snowflake. 

This approach allows organizations to take advantage of the scalability and infrastructure provided by these platforms, enabling seamless model deployment in cloud-native environments. By exporting models to these platforms, Dataiku ensures that models can leverage the unique scaling options available, such as automated scaling on SageMaker. 

These integrations also simplify the process of managing and serving models in production, as users can tap into platform-specific features like managed services, high availability, and auto-scaling capabilities. With Deploy Anywhere, Dataiku empowers teams to deploy models where it makes the most sense for their business needs, all while maintaining a consistent workflow and maximizing performance across various cloud environments.

While models are deployed to external platforms, Dataiku retains its built-in functionality for managing the entire lifecycle of these models. The platform provides similar functionailty for models hosted on its own infrastructure and those deployed externally, ensuring seamless management across both scenarios. Essential features, such as [monitoring the health status and detecting potential data or performance drift](https://blog.dataiku.com/ensuring-smooth-mlops-with-unified-monitoring), are available for models regardless of where they are hosted.