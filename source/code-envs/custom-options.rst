Custom options and environment
################################

In many cases, it may be needed to customize options passed to the various system commands used in the management of the code environment system (``virtualenv``, ``pip``, ``R`` and ``conda``)

One of the main use cases for doing so is if your DSS server does not have outgoing Internet access. In that case, you will not be able to install packages from the main repositories, and will need to pass additional arguments for custom repositories.

Custom options for virtualenv, pip, R and conda can be configured in Administration > Settings > Misc. These settings can only be configured by the DSS administrator.

These options can also be overridden on a per-code-environment basis by unchecking "Inherit global settings" in the "General > Extra options" configuration section for the code environment.

Examples
========

The options for pip, virtualenv, R and conda can be found in the relevant documentation. 

    * For pip, the relevant custom options can be found in the `pip install documentation <https://pip.pypa.io/en/stable/cli/pip_install/>`_. 
    * For virtualenv, the relevant custom options can be found in the `virtualenv documentation <https://virtualenv.pypa.io/en/latest/cli_interface.html>`_
    * For conda, you can customize the `conda create <https://docs.conda.io/projects/conda/en/latest/commands/create.html#>`_ and `conda install <https://docs.conda.io/projects/conda/en/latest/commands/install.html>`_ options. 
    * For R, you can customize the `CRAN mirror URL <https://cran.r-project.org/mirrors.html>`_

You can apply regular pip, virtualenv or conda install flags to a code environment by adding the respective option flags. The syntax for all options is an entry line for the option, followed by a separate entry line for the option value.  

Adding a trusted host for pip installs
---------------------------------------

Trust the following hosts even without valid HTTPS. This will run the equivalent of ``pip install --trusted-host pypi.python.org --trusted-host file.pythonhosted.org [...]``

.. code-block:: bash 

    --trusted-host 
    pypi.python.org
    --trusted-host
    file.pythonhosted.org


Adding a proxy for pip installs
---------------------------------------

Apply a proxy to your pip installations. This will run the equivalent of ``pip install --proxy [user:passwd@]proxy.server:port [...]``

.. code-block:: bash 

    --proxy 
    [user:passwd@]proxy.server:port 


Point to a custom python package repository for pip installs
--------------------------------------------------------------

Use an alternative python package repository for pip installs (not PyPI). This will run the equivalent of ``pip install --index-url http://index.example.com/simple/ [...]``

.. code-block:: bash 
    
    --index-url
    http://index.example.com/simple/


Install from a local directory without scanning remote package indexes
-----------------------------------------------------------------------

If you are installing packages on a system with limited connectivity, you can set pip not to scan remote package indexes when installing a package, and provide a local path to install from. This will run the equivalent of ``pip install --no-index --find-links /full/path/to/package-folder/ [...]`` 

.. code-block:: bash 

    --no-index 
    --find-links
    /full/path/to/package-folder/
        

Add a conda channel for packages install
--------------------------------------------------------------

Adds an additional channel to search for packages. Runs the equivalent of ``conda install --channel conda-forge [...]``

.. code-block:: bash

    --channel
    conda-forge
