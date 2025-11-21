Operations (R)
#########################

.. note::

	* You need to have specific permissions to create, modify and use code environments. If you do not have these permissions, contact your DSS administrator.
	* See :doc:`/collaboration/requests` for more details on how users without these permissions can request a new code environment.

Create a code environment
===========================

* Go to Administration > Code envs
* Click on "New R env"
* Give an identifier to your code environment. Only use A-Z, a-z, digits and hyphens

.. note::

	Code environment identifiers must be globally unique to the DSS instance, so you should use a complete and descriptive identifier.


* Click on **CREATE**
* DSS creates the code environment and installs the minimal set of packages
* You are taken to the new environment page

Given that compiling R packages from source takes time, it is advised to use Conda when available for code environment, and benefit from pre-compiled packages.

Manage packages
=================

You can manage the list of packages to install by clicking on the "Packages to install" tab.

You see here two lists:

* A non-editable list of the "base packages". These are packages that are required by your current settings. These packages cannot be removed, and you cannot modify their version constraints. For more information, see :doc:`base-packages`

* An editable list of "Requested packages". This is where you write the list of packages that you want in your virtual environment.

.. image:: img/list_of_packages.png

The list of requested packages is a table where the first column is the package name, and an optional second column may specify a minimum
version number for this package:

* If the version is not specified, DSS will install this package if not already present.

* If the version is specified, DSS will (re-)install this package if not already present, or if the currently installed version is lower than
  the requested minimum version.

.. note::

  In both cases, installing a package will pull the latest version currently available in the configured repository (as determined by the
  standard ``install.packages()`` R function). In particular, it is not possible to specify that a given version of a package should be
  installed, nor that a version older than the latest should be installed.

For example:

* ``"dplyr",`` will install the latest version of dplyr if dplyr is not yet installed, and keep any existing version otherwise
* ``"RJSONIO","1.3"`` will install the latest version of RJSONIO, if RJSONIO is not yet installed or is installed in a version older
  than "1.3"

Once you have written the packages you want, click on **Save and update**. DSS downloads and installs the newly required packages

Afterwards, you can inspect the exact installed versions in the "Actually installed packages" tab.

Using different package repositories
===============================================

R packages not installed via Conda are pulled from repositories that mirror CRAN, and there is regularly a need to use a particular mirror (most often because of the availability of older versions). When DSS is installed on a machine without outgoing internet access, there is also a need to use a packaged CRAN repository hosting on the internal network.

To work with both these cases, the user can override the default CRAN mirror in Administration > Settings > Misc, and even override it on a per-code environment basis in the Extra Options, by unchecking "Inherit global settings". This lets the user pass an URL to point to the R packages repository.
