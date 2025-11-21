(scenarios-inside)=

# Scenarios (in a scenario)

This is the documentation of the API for use in scenarios.

:::{warning}
This API can only be used within a scenario in order to run steps and report on progress of the current scenario.

If you want to control scenarios, please see {doc}`scenarios`
:::

These functions can be used both for "Execute Python code" steps in steps-based scenarios, and for full Python scenarios

A quick description of Python scenarios can be found in [Definitions](https://doc.dataiku.com/dss/latest/scenarios/definitions.html). More details and usage samples are also available in [Custom scenarios](https://doc.dataiku.com/dss/latest/scenarios/custom_scenarios.html)

The Scenario is the main class you'll use to interact with DSS in your "Execute Python code" steps and Python scenarios.

## Detailed examples

### Set Scenario step timeout

There is no explicit timeout functionality for a Build step within a Scenario. A common question is how to setup a timeout for a scenario or scenario step to avoid situations where a scenario gets stuck/hung in a running state indefinitely.

You can implement it using the Dataiku Python API. The same scenario step can be re-written as a custom Python step, in which case you can add additional Python code to implement a timeout.

Here is a code sample that you can try:

```{literalinclude} examples/scenarios/set-scenario-timeout.py
```


## Reference documentation

```{eval-rst}
.. autosummary::
        dataiku.scenario.scenario.Scenario
        dataiku.scenario.scenario.BuildFlowItemsStepDefHelper
```
