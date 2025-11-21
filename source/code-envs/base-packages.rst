Base packages
##############

Two sets of packages can be pre-installed in environments (both Python and R)

* "Core packages". These are the absolute minimal requirements for the ``dataiku`` package to work. If you don't install these packages (or change their versions), the ``dataiku`` package cannot work. While it is possible to create virtual environments without core packages, their functionality will be strongly decreased

* "Jupyter packages". These packages are required to be able to use the Jupyter notebook with this code environment. If you choose not to install these packages, you will not be able to use the Jupyter notebook with this environment (but you can still use recipes, scenarios, ...)