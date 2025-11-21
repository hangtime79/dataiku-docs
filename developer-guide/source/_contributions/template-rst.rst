:orphan:

Template for writing a tutorial (Your title here)
*************************************************
.. note::
    A small introduction/summary text

Prerequisites
=============

* Dataiku version, a disclaimer if the tutorial doesn't work on Dataiku Cloud
* User permissions (both connection and project level)
* Python version and packages version
* Expected initial state, e.g.:
  * existing project
  * dataset
  * models
  * knowledge

Introduction/context (you can change the title if you need)
===========================================================

.. note::
    What problems solve in your tutorial?

Step 1
======


Sub-step if needed.
-------------------

Step 2
======


.../...
=======


Complete code (if applicable)
=============================


Wrapping up/Conclusion
======================

Reference documentation
=======================

Classes
-------

.. note::
    Classes used in this tutorial (alphabetically sorted)

.. autosummary::
    dataikuapi.DSSClient

Functions
---------
.. note::
    Functions used in this tutorial (alphabetically sorted by name of the function)
    ex: ~dataikuapi.DSSClient.get_default_project

.. autosummary::
  ~dataikuapi.DSSClient.get_default_project