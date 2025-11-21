Definitions
###########

A **scenario** in DSS is a set of actions to do, with condition(s) to run it. DSS automatically executes scenarios whose conditions are satisfied.

Types of scenarios
==================

There are 2 types of scenarios, which differ in the way the sequence of actions they take is defined:

* **step-based** scenarios are made of a fixed list of steps, parametrized by the user. The steps are all run, and always in the same order. Some level of flow control is possible (see :doc:`/scenarios/step_flow_control`).
* **custom python** scenarios consist in a python script, which is run in an environment allowing it to launch scenario steps on the DSS backend.

**Custom python** scenarios offer more flexibility when it comes to deciding whether a given step needs to be run or not. For example, a step to re-train a model could be conditioned on the last known performance of that model.


Triggers
========

A **trigger** is a condition attached to a scenario. A scenario can have one or more triggers attached to it.  The triggers are evaluated periodically, and when a trigger condition is met, it launches the scenario.


Reporters
=========

Since scenarios run in the background, there is a need for knowing whether a given run is finished or not, and whether failures were recorded. This information can be read by the user when he inspects the scenario's last runs or when he uses the monitoring plots, and can also be published on a variety of channels by **reporters**.

One or more reporters can be set up on a scenario to prepare messages and send them on **messaging channels**. These channels are configured by the DSS instance's administrator in the **Administration** section.

.. _def-test-in-dss:

Test in DSS
===========

This option is used to record future scenario runs as "test runs" and makes them available in the :doc:`Test Dashboard <./test_scenarios>`.