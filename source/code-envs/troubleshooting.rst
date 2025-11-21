Troubleshooting
################

Where to look for logs
========================

All logs of operations are in the "Logs" tab of the code environment. If the error happens while you are not in a code environment, you may need to look in the backend logs. See :doc:`/troubleshooting/diagnosing`

Creation or package installation fails with gcc error
=======================================================

In most cases, this kind of error is due to missing system development headers.

Python.h not found
-------------------

If you get this error, you need to install the Python development headers system package which matches the version of Python for this code env.

.. note::

	System packages can only be installed by system administrators. The following instructions require shell access to the machine hosting DSS with **sudo** privileges.

In most cases, the name of the development package for a given version of Python can be obtained by appending "-devel" (for RHEL-like systems)
or "-dev" (for Debian-like systems) to the name of the system package which provides Python itself.

The following examples provide the corresponding instructions for the standard versions of Python 3.x which are installed by the DSS installer.

RHEL / CentOS / AlmaLinux / Rocky Linux / Oracle Linux
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.. code-block:: bash

    # System development tools
    sudo yum groupinstall "Development Tools"

    # RHEL/CentOS/Oracle Linux/AlmaLinux 8.x
    sudo yum install python39-devel

    # RHEL/CentOS/Oracle Linux/AlmaLinux 9.x
    sudo yum install python3.9-devel

Debian / Ubuntu
%%%%%%%%%%%%%%%

.. code-block:: bash

    # System development tools
    sudo apt-get install build-essential

    # Ubuntu 20.04 / Debian 11 (Python 3.9)
    sudo apt-get install python3.9-dev

    # Ubuntu 22.04 / Debian 11 (Python 3.10)
    sudo apt-get install python3.10-dev


SUSE Linux Enterprise Server 15
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.. code-block:: bash

    # System development tools
    sudo zypper install -t pattern devel_basis

    # Python 3.6
    sudo zypper install python3-devel

macOS
%%%%%%%%%%%%%%

First, download and install `Xcode <https://developer.apple.com/xcode/>`_ and then its Command Line Tools on the terminal.

.. code-block:: bash

    xcode-select --install

If you need a specific Python version, you will need to install it.
Several options are possible such as `Python.org <https://www.python.org/downloads/mac-osx/>`_ or `Pyenv <https://github.com/pyenv/pyenv#homebrew-on-macos>`_.

Other .h file not found
-------------------------

This error generally means that you need to install the development headers system package for the mentioned library. This package can only be installed by your system administrator. The name of the package is generally ``libsomething-dev`` or ``something-devel``

Creation of code environments fails with : No module named 'distutils.spawn'
============================================================================

On some Ubuntu systems, the "distutils.spawn" Python module, which is a standard part of Python (though considered "legacy"
in Python 3) is packaged independently of Python 3 itself.

This module is required by virtualenv however. If it is not present, creation of virtualenv-based code environments will 
fail with: ``ModuleNotFoundError: No module named 'distutils.spawn'``

You need to install the ``python3-distutils`` system package:

.. code-block:: bash
	
	# apt-get install python3-distutils

MXNet does not support numpy 2
==============================
MXNet is a library used by GluonTS, which is used by Dataiku for deep time series models.

MXNet doesn't support numpy 2, so installing it will downgrade numpy to 1.26.
You can choose to avoid installing MXNet so that you can install numpy 2. In this case, you still have access to the statistical timeseries models.

