Automation nodes
######################################

Like projects, code environments on an automation node come from bundles created on a design node and imported in the automation node. Unlike projects, code environments can also be created directly in the Administration section, and will be found and used when a bundle requiring them is imported.


Versioning
==========

The code environments existing on an automation node can be versioned. A versioned code environment actually holds several code environments, each with its own independent list of requirements. Only the permissions and installation command overrides are shared. 

Each bundle can then link to a specific version of a code environment, and versions of a given code environment are not removed, allowing for rolling back to a previous version of a project without risking to not be able to rebuild the exact same code environment. Once a bundle is preloaded and activated, all items inside the project only see one version of a versioned code environment, the version that matches the bundled requirements.

.. note::

	The kernels in Python and R notebooks can be changed at runtime, and the scoping to the relevant version of a versioned code environment for the project is not enforced.


Code environments from bundles
==============================

Before activating a bundle of a project using non-builtin code environments, a new action is required:

* go to the Bundles management page
* select the desired bundle of the project
* use the "Preload" button in the action bar on the right
* once preloading is complete, the bundle can be activated

Preloading the bundle scans it for needed code environments, compares to the ones available on the automation node, and if needed and parametrized as such, creates new code environments or code environments versions, or updates existing ones.


Comparison between bundled and existing
---------------------------------------

Code environments are identified by their language (Python or R) and by their name. When a code environment exists with the right language and name, the requirements of the bundled code environment are compared to the definition of the existing one, or to the definition of its versions in case it is a versioned code environment. A (version of a) code environment matches if its definition is the same, and "definition" can be :

* the requirements of the code environment, i.e. the lists of user-required packages (Conda packages if relevant, and Pip or R packages)
* the actual lists of packages of the code environment

The mode for defining a code environments contents can be selected in the Activation Settings part of the Bundles management page.


Preloading code environments
----------------------------

The behavior when faced with a missing or outdated code environment in the Preloading phase can be selected in the Activation settings of the Bundles management page :

* do nothing
* stop preloading if a code environment used by the project is flat-out missing (i.e. no code environment with the same language and name exists) or not up-to-date (with requirements differing)
* ensure existence of an appropriate code environment by either creating a new one if no code environment with the same language and name exists, or updating an existing non-versioned code environment, or adding a version to a versioned code environment

Code environments created in the preloading have their type defined by the type of the code environment in the design node they need to correspond to:

* managed code environments on the design node become versioned code environments on the automation node
* non-managed code environments on the design node become non-managed code environments on the automation node
* external Conda code environments on the design node become external Conda code environments on the automation node


Managing code environments directly
====================================

Creating code environments manually can be done in Administration > Code envs, and code environments created this way will be considered by preloading of bundles when their language and name match. Versions of versioned code environments or non-versioned code environment can be imported, their packages lists modified.

.. note::

	Modifying the package list of a code environment and updating it is very likely to prevent it from matching requirements in bundled code environments, meaning these modified code environments will not be used by the bundle preloading.
