Installing R packages
###########################

Any R package can be used in DSS. There is no restriction to which package can be installed and used.

The recommend way to install your own R packages is to install them in a :doc:`code environment </code-envs/index>`.

Installing in a specific code environment (recommended)
========================================================

Please see :doc:`/code-envs/operations-r`


Installing in the root DSS environment (not recommended)
=============================================================

In addition to user-controlled code environments, DSS has its own builtin R environment, which contains a default set of packages.
It is possible, although not recommended to install your own packages in that builtin environment.

Installing packages in the builtin environment requires shell access on the host running DSS and can only be performed by DSS administrators.

A number of packages are preinstalled in the builtin environment. Modifying the version of these packages is **not supported** and may result in causing DSS to stop functioning.

* Go to the DSS data directory

* Run ``./bin/R``

.. warning::

	Beware: you must run ./bin/R, not the "R" binary on your PATH

* Run the regular ``install.packages()`` R command

In Dataiku Cloud, the built-in environment is managed so it is not possible to install your own packages. Please use a code environment to install non-default packages.

Installing without Internet access
-------------------------------------
