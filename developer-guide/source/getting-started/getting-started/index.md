# Getting started

```{eval-rst}
.. meta::
    :description: Dataiku enables coders to create flexible and customizable data solutions using Python, R,
                  and SQL, allowing for advanced machine learning models and automation through its extensive API.
                  With features like code notebooks, recipes, and the ability to develop plugins,
                  coders can enhance their workflows and integrate Dataiku into their CI/CD processes effectively.
```

## Being a coder
As a coder using Dataiku, you can develop more powerful/adaptable data solutions.
While Dataiku is designed for users with varying technical expertise, it is also coder-friendly. 

### Enhanced Customization and Flexibility
Coders can create custom code recipes using Python, R, and SQL.
Custom recipes can offer alternatives to existing data transformations, algorithms, and execution contexts.
You're not limited to Dataiku's standard offerings.
You can build any logic required to meet your needs.

### Advanced usage of Generative AI
Dataiku provides a centralized and secure gateway to a wide range of LLMs.
Coders can test different LLMs without changing their code, but only by changing the connection.
Coders can define their personalized connection, allowing the usage of tailored or self-hosted LLMs.
You can define your code logic embedded into an agent, a tool, or any new emerging concepts of LLM,
and easily compare model performance and cost without changing the core logic.
Dataiku provides a complete integration for RAG, allowing you to create a dedicated chatbot.

### Advanced Machine Learning
Although Dataiku's visual machine learning tools are powerful,
you can code your own model or use external libraries to build custom machine learning models.
You'll use your model within Dataiku, allowing you to take full advantage of Dataiku's features.
These models will become part of the platform, allowing users to run them in Dataiku.

### Automation and Integration
Programmers can exploit Dataiku's API to control and automate almost every platform aspect;
from datasets to scenarios to Large Language Models, you can easily integrate Dataiku into your CI/CD workflow.
Dataiku also offers integrated CI/CD solutions that can be configured via code.
These capabilities allow you to envisage a rapid, stable, and automated production launch.
For example, you can write a script that automatically re-trains and deploys a model when new data becomes available.

### Extensibility with Plugins
One of the most significant benefits for coders is the ability to develop custom plugins.
These plugins can add new functionalities to Dataiku,
such as new dataset connectors, custom data preparation steps, or unique visualizations.
This allows you to extend the platform to meet your organization's specific needs
and share these new capabilities with other users, both technical and non-technical.



While Dataiku empowers everyone to work with data, coders can push the boundaries of what's possible,
creating more sophisticated, automated, and integrated data science solutions. 


This page briefly explains where the code is written and executed when working on a Dataiku instance.

(getting-started/tool-for-coding)=
## Tools for coding

### Notebooks

If you are looking for a way to interactively explore your data and experiment with small pieces of code,
then **notebooks** are the way to go.
They allow you to execute your code by consecutive blocks called *cells*, and visualize each cell's output. 

Dataiku offers the ability to spawn complete code notebook environments server-side:

* SQL notebooks to run interactive queries on your SQL databases.
* Code notebooks to execute Python or R code in a simple yet effective interface based on Jupyter notebooks.

All these solutions are natively embedded in the Dataiku web interface to facilitate navigation
and allow you to easily share your work with other users on the same instance.
Additionally, Python/R notebook sources (`.ipynb` files) can be synchronized from/to remote Git repositories.

```{seealso}

* {doc}`Documentation page on code notebooks <refdoc:notebooks/index>`.
* {doc}`kb:code/getting-started/concept-code-notebooks`.
* {doc}`kb:code/sql/concept-sql-notebooks`

```

### Code recipe

Once you have tested your code in a notebook or elsewhere, you may want to integrate it into Dataiku.
Code recipes provide a way to run code
on many different inputs/outputs (among datasets, managed folders, knowledge banks, and agents, for example).
This way, your workflow integrates your specific needs.
A code recipe can replace a visual recipe if you feel more comfortable using code.

```{seealso}

* {doc}`refdoc:code_recipes/index`
* {doc}`kb:code/getting-started/concept-code-recipes`
```

### IDE and Code Studio

If you already use an IDE like Visual Studio Code or PyCharm on your client machine,
installing the relevant extensions/plugins will allow you to connect it to your Dataiku instance 
and edit source code directly.

If you prefer editing your source code remotely, Dataiku can embed a Visual Studio Code editor directly in its interface.
This option is based on the platform's "Code Studios" feature
and does not require any setup on your client machine since the platform fully manages it.


```{seealso}

* {doc}`refdoc:code-studios/index`

**VSCode/IntelliJ  extension for Dataiku**

* The [Visual Studio marketplace page](https://marketplace.visualstudio.com/items?itemName=dataiku.dataiku-dss) to install and configure the extension
* The {doc}`tutorial explaining how to use the extension </tutorials/devtools/vscode-extension/index>`


**PyCharm plugin for Dataiku**

* The [JetBrains marketplace page](https://plugins.jetbrains.com/plugin/12511-dataiku-dss) to install and configure the plugin
* The {doc}`tutorial explaining how to use the plugin </tutorials/devtools/pycharm-plugin/index>`

**Code Studios**

* {doc}`Documentation page on Code Studios <refdoc:code-studios/index>`
* {doc}`Using VSCode for Code Studios tutorial </tutorials/devtools/using-vscode-for-code-studios/index>`
```

## Managing dependencies

Writing code often implies working with third-party packages that you must install separately.
For example, in the case of Python,
you would take advantage of **virtual environments** to create and import your dependencies.

In Dataiku, the equivalent of the virtual environment concept is called the **code environment**.
It lets you choose which Python version and custom packages you want to run your code with.
Once the code environment is set up, its dependencies can be imported from any code run by Dataiku. 

```{seealso}

* {doc}`Documentation page on code environments <refdoc:code-envs/index>`.
* {doc}`kb:code/work-environment/concept-code-environments`
```


### Building a shared code base

When writing code for a project, past a certain size and/or complexity threshold,
it is essential to modularize it into classes and functions.
By doing so, you also allow other users to import these items directly instead of re-implementing them.
This concept of **shared code repository** is materialized in Dataiku in the form of **project libraries**. 

Thanks to them, you can decouple your code's logic (containing business/domain expertise)
from the Dataiku-related code that handles workflow orchestration. 

```{seealso}

* {doc}`Documentation page on project libraries <refdoc:python/reusing-code>`.
* {doc}`kb:code/shared/concept-shared-code`
* {doc}`kb:code/shared/concept-project-libraries`

```


### Bringing an external code base

As a new Dataiku user, you have already worked on an existing code base living independently from the instance.
You can make the items of this code base directly importable in Dataiku
by using a special feature of project libraries called "Git references."
Provided the external code is hosted on a remote Git repository,
this feature allows you to pull a specific branch of that repository into Dataiku,
which will be materialized into a project library. 

By doing so, you can have your Dataiku workflows **operate hand-in-hand with any external code repository**.

```{seealso}

* {doc}`Documentation page on Git references <refdoc:collaboration/import-code-from-git>`.
* {doc}`kb:code/shared/concept-import-from-git`
```

## Git integration
Dataiku natively includes git operations.
There are several ways to interact with git, from managing your code to managing your project.
The documentation contains several guidelines for using git within Dataiku.

```{seealso}

* {doc}`refdoc:collaboration/git`
* {doc}`kb:code/shared/concept-import-from-git`
* {doc}`/tutorials/devtools/git-dss-setup/index`
* {doc}`/tutorials/devtools/using-api-with-git-project/index`
```