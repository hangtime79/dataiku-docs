Non-managed code environments
#############################

When a completely custom Python or R installation is needed, DSS can let the user maintain code environment directly. In this case, the code environment is "non-managed" from the point of view of DSS. To create such an environment:

* go to Administration > Code envs
* create a new Python or R environment
* select "Non-managed path" as environment type
* Give an identifier to your code environment. Only use A-Z, a-z, digits and hyphens

.. note::

	Code environment identifiers must be globally unique to the DSS instance, so use a complete and descriptive identifier


A non-managed code environment is basically a folder created by DSS. Its path can be found on the code environment's General tab, as "Location of the environment".


Non-managed Python code environment
===================================

DSS requires the presence in the location of the non-managed code environment of the following files:

* `bin/python` : a python executable
* `bin/pip` : a script to list the packages, that will be called with the arguments "bin/python bin/pip freeze -l"


Non-managed R code environment
===================================

DSS requires the presence in the location of the non-managed code environment of the following files:

* `bin/R` : a R executable

