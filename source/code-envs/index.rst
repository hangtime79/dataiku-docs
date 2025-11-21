Code environments
#################

DSS allows you to create an arbitrary number of code environments. A code environment is a standalone and self-contained environment to run Python or R code.

Each code environment has its own set of packages. Environments are independent: you can install different packages or different versions of packages in different environments without interaction between them. In the case of Python environments, each environment may also use its own version of Python. You can for example have one environment running Python 3.8 and one running Python 3.9

In each location where you can run Python or R code, you can select which code environment to use.

.. toctree::

	operations-python
	operations-r
	base-packages
	conda
	automation
	non-managed
	plugins
	custom-options
	troubleshooting
	permissions
