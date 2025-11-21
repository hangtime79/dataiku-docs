# Basic workflow

```{eval-rst}
.. meta::
  :description: Dataiku provides a streamlined workflow for data projects, enabling users to connect to data storage,
                manipulate datasets, and build outputs through a data-driven approach.
                It facilitates easy dependency management and scheduling of tasks within a visual Flow,
                allowing programmers to focus on project goals rather than implementation details.
```
This section will provide you a programmer's view of how workloads are built and orchestrated in the Dataiku platform.
It is inspired by {doc}`this documentation page<refdoc:concepts/index>` but puts it in the perspective of a coder user.

## Connecting to your data 

When working on a data project, the first steps often involve connecting to the data storage platforms hosting your data,
like data warehouses or object storage buckets.
To do so, you should provide the location of those sources and a set of relevant credentials.
Handling this manually in your code can be a cumbersome and repetitive task,
so the Dataiku platform provides a simplified framework to speed up the work of data scientists. 

In practice, each data source is materialized within Dataiku as a "connection" object, 
which contains information on how to authenticate and follow a given path to read and write your data.
By doing so, Dataiku enforces a clear separation of responsibilities:
while platform administrators create and maintain connections, end users can focus on implementing their projects. 

Once you have access to the data storage, the next step is to retrieve specific data pieces that will be useful in your project.
For that, the concept of "dataset" provided by Dataiku comes in handy.
In short, a dataset acts as a *pointer* to tabular data sources living on a data storage platform
for which a connection has been defined.
In practice, when you write code in Dataiku, you manipulate dataset objects
that rely on the connection properties to authenticate against the data source and read/write data from/to it.
Dataset definitions include the underlying data schema, column names, and types.

To further facilitate data manipulation,
dataset objects have been designed to give end-users access to data through well-known programmatic interfaces,
such as SQL tables and pandas/PySPark DataFrames.
This way, the data storage type is abstracted away from the user,
who will only have to care about *what* to do with the data instead of *where* and *how* to find it.

In that same spirit, pointers to more generic (i.e., not necessarily tabular) data are also available in Dataiku as "managed folders."
They often handle unstructured data such as images or text documents.

```{seealso} 

* Connections {doc}`documentation page <refdoc:connecting/index>` and {doc}`API reference </api-reference/python/connections>`
* Datasets {doc}`documentation section <refdoc:concepts/index>` and {doc}`API reference </api-reference/python/datasets>`
* Managed folders {doc}`documentation page <refdoc:connecting/managed_folders>` and {doc}`API reference </api-reference/python/managed-folders>`

```

## Running code

In your project, your code will likely read data, process it, and then write the results.
In other words, your code's task will work with input items and produce output items.
In Dataiku, the reasoning is built so that you don't run tasks; instead, you build output items.
This so-called **data-driven** mindset takes inspiration from all standard build tools
in the software engineering ecosystem (e.g., make, Maven, Gradle),
where the developers focus on the target they want to build instead of the underlying code. 

In practice, to run code in a Dataiku project, you will write its logic into a recipe, and to execute this code,
you will build the recipe's output items.
Recipes can be written in Python or R and edited in various environments
(see the {ref}`getting-started/tool-for-coding` page).

While datasets are the most common type of *buildable items*, more items fall into this category,
like managed folders or ML models.
All in all, the entire logic of your project can be articulated by chaining buildable items and linking them with recipes,
forming a direct acyclic graph (DAG) called the Flow.

```{seealso}

* Recipes {doc}`documentation page <refdoc:code_recipes/index>` and {doc}`API reference </api-reference/python/recipes>`
```

## Building a Flow

Dataiku's Flow unveils the true power of a data-driven workflow: *dependency management*.
In a data project, the most critical parts are often materialized by the final elements of the workflow's DAG.
In Dataiku, you will focus on building the final item of your Flow.
Every upstream buildable item is then treated as a dependency, meaning it must also be built if it isn't already.
Dataiku's dependency resolver solves the recursion problem of determining which dependencies need to be built.
Then the scheduler takes care of running all tasks required for those builds, enforcing concurrency and parallelism when it's possible.

The user is free to define the level of granularity in their project,
which often translates to the number of intermediary states in a Flow.
Dataiku offers additional tooling to segment better the logic of a Flow
and flush unnecessary intermediary data when needed so that the flow's expressiveness is not sacrificed for conciseness.

```{seealso}

* Flow {doc}`documentation page <refdoc:flow/index>` and {doc}`API reference </api-reference/python/flow>`
* [Blog post](https://blog.dataiku.com/the-flow) providing more details on data-driven Flows in Dataiku.
```

## Scheduling and automating a Flow

Once your Flow has been developed, one important step towards its production-readiness is to define how its execution can be scheduled and automated.
In Dataiku, the most frequent patterns are:

* Using the native "scenario" feature to define *steps* to execute, *triggers* that will launch the execution,
  and *reports* to format the outcome of your runs.
* Using Dataiku's public API to connect to a third-party scheduler,
  which can either enforce its own scheduling rules or remotely start a Dataiku scenario.

```{seealso}
* Scenario {doc}`documentation page <refdoc:scenarios/index>` and {doc}`API reference </api-reference/python/scenarios>`
```
