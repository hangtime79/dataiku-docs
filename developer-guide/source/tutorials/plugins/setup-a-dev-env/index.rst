Setting up a dedicated instance for developing plugins
***********************************************************

This tutorial helps you to set a development environment for developing Dataiku plugins.
From a very minimal setup to a complete setup,
this tutorial will help you understand the requirements
and the best practices we recommend to develop a plugin for Dataiku.


Prerequisites
#############

The minimal prerequisites are:

* "Manage all code-envs" permission.
* "Develop plugins" permission.
* Dataiku.

It would be best to have:

* A dedicated Dataiku instance with admin rights (you can rely on the
  `community Dataiku instance <https://www.dataiku.com/product/get-started/>`_).

* Git access.
* Pycharm or Visual Code studio.


Best practices
##############

We recommend reading **this introduction first** (:doc:`Foreword<../foreword>`).

Developing a plugin is an important task that requires careful consideration.
It is highly recommended to have a dedicated instance when developing a plugin.
This will ensure that your plugin development does not interfere with other projects.

You can install one of the many plugins already published in the Plugin Store to gain inspiration
or see how certain functionalities were implemented.
By opening it in dev mode and examining the source code, you can learn how to implement similar features in your plugin.
You can also inspect the source code on GitHub for publicly published plugins.

When developing your plugin, paying attention to naming your variables and functions is essential.
Ensure that they are meaningful and descriptive.
This will make it easier for other developers to understand your code.
Using comprehensive wording in your code and user interface is also important.
The component/plugin naming should never contain the word plugin or custom.
It would be best if you had consistent wording throughout your company.

Before running any processing, it's essential to validate all input parameters.
If possible, read them and validate output parameters.
Implementing error handling at any point can help prevent issues and make your plugin more reliable and safe to use.

To ensure the reliability and security of your code,
it is advised to use the ``my_dict.get('smth', default_value)`` method instead of ``my_dict['smth']``.
This is because the former method allows you to provide a default value if the key ``smth`` is not present in the dictionary,
thus preventing potential errors.

It is also crucial to sanitize user inputs before usage, especially regarding strings.
Untrusted or malicious inputs could cause security vulnerabilities and
lead to data breaches in the project where the plugin is used.
Furthermore, dates and time zones must be handled with particular care.
Incorrect time zone conversions or date calculations can result in serious issues.


Separating the logic of your component in plugin libraries is a good practice.
Doing so lets you keep the code in the plugin libraries independent of dataiku.
Avoid importing ``dataiku``, as this will simplify testing the plugin logic outside of Dataiku.


Preparing your development environment
######################################

Before developing a plugin, you must prepare your development environment.
You can use your preferred Integrated Development Environment (IDE), such as PyCharm or VSCode.
If you use VSCode,
you can install the VSCode extension by following :doc:`these instructions</tutorials/devtools/vscode-extension/index>`.
Similarly, if you choose to use PyCharm,
you can install the PyCharm plugin by following :doc:`these instructions</tutorials/devtools/pycharm-plugin/index>`.

Interacting with Git
####################

As a developer, you can use Git to synchronize your plugin between your Dataiku instance and IDE.
To enable Git communication between your instance and repository, make sure they can communicate with each other.

To connect your Dataiku instance to an external Git repository,
copy your Dataiku user's public SSH key and add it to the list of accepted SSH keys in your GitHub account.
This means that you must have access to the public key of your Dataiku users.

If you need to generate SSH keys, use the command ``ssh-keygen`` and follow the corresponding prompts.

For further help, you can refer to GitHub's documentation.
Suppose you face difficulty establishing communication between your Dataiku instance and your GitHub account.
In that case, you can try running the command ``ssh -vT git@github.com`` from your Dataiku instance's shell command line.
This command provides a detailed description of the various connection steps used to connect to your GitHub account.

Always ensure no components with the same name are present in the existing instance when synchronizing.
If any such components exist, your plugin will be loaded only after you fix this error.

Wrapping up
###########

Congratulations! Setting up a developer environment for plugin development is a significant milestone.
It means you have taken the first crucial step towards easily creating plugins.
By adhering to best practices, you will develop plugins confidently and quickly,
knowing you are following proven methods that produce high-quality results.
