Using Conda
############

In addition to the builtin mechanisms to create and manage code environments (ie, virtualenv for Python and custom mechanism for R), you can choose to use Conda.

Conda is a third-party packages management system which provides both Python and R packages.

.. warning::

    **Tier 2 support**: Conda code envs are covered by :doc:`Tier 2 support </troubleshooting/support-tiers>`

    conda packages repositories tend to be very bleeding-edge, and move quickly, with frequent backwards-incompatibles changes.

    Various incompatibilities may happen, and Dataiku can only provide limited support with setup and usage of conda-based code environments.

    For these reasons, Dataiku does not generally recommend using conda for code environments. We recommend that you only use conda
    if there are reasons for which you cannot use the native virtualenv and R packages systems.


.. warning::

    In most cases, using Conda repositories is **not free**, and you **must** have a paid license.

    Before using Conda in Dataiku, ensuring that you have a paid license and that you are compliant with Conda's licensing terms is **your responsibility**.


Prerequisites
==============

* For Custom or Cloud Stacks installations, you need to install miniconda or anaconda. The "conda" binary should be in the PATH of DSS.

* In Dataiku Cloud, enable the extension "Conda" in the Launchpad to install miniconda.

Using Conda environments
=========================

To use Conda for an environment instead of the builtin mechanisms, check the "Use conda" checkbox when creating the environment.

When managing the packages of a Conda-based environment, you actually need to manage two lists of packages:

* The list of Conda packages
* The "regular" list of language packages (either pip requirements or R packages)

This is due to the fact that not all packages are available through Conda. For packages not available through Conda, you need to put them in the "regular" list.

It is strongly recommended not to put the same packages in both lists. Various issues can also happen if a package in a list depends on one in another.