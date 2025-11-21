Installing STAN or Prophet
############################

.. warning::
    
    **Tier 2 support**: These instructions installation are provided "as-is" and are covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

The STAN and prophet packages for time series forecasting are challenging to install, because they require very recent C++ compilers that most Linux distributions do not provide, in particular the "C++14" features.

Common errors
==============

You will often see the following error in the code environment build log:

.. code-block::

	Error in .shlib_internal(args) :
		C++14 standard requested but CXX14 is not defined

Installing on RedHat 7 or Centos 7
====================================

On a CentOS 7.6 system, you could for example proceed as follows:
 
1. As root, install the "software collection library" (SCL)

.. code-block:: bash

    yum install centos-release-scl
 
2. As root, install the latest Developer Toolset (which contains a recent version of the GCC suite)

.. code-block:: bash

    yum install devtoolset-8-toolchain
 
3. Activate the developer toolset in the DSS user session by adding the following to the session initialization file for the DSS user account (ie .bash_profile or equivalent):

.. code-block:: bash

    source /opt/rh/devtoolset-8/enable
 
4. Logout and login from your shell on the DSS user account, to pick up the new definition above, and restart DSS from it so it also picks the updated environment.
 
5. Create a file named $HOME/.R/Makevars, where $HOME is the homedir of the DSS user, containing:

.. code-block:: bash
  
  CXX14 = g++
  CXX14FLAGS = -O3 -march=native -mtune=native -fPIC

This declares to R that there is a C++ 14 compiler available, named "g++"
 
You should now be able to build R packages containing C++14 code from DSS.

6. If UIF is enabled on your DSS instance, you also need to tell UIF to use system sudo, because devtoolset-8 includes a non-compatible sudo. Follow :doc:`these steps </user-isolation/troubleshooting>` to edit the ``install.ini`` file and add a line:

.. code-block:: bash

	[mus]
	custom_root_sudo = ["/usr/bin/sudo"]