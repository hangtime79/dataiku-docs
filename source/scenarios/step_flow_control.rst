Step-based execution control
############################

The default behavior in step-based scenarios is to run all steps in order, until one fails or until all the steps are done. 


On failure, proceed with scenario
=================================

Some steps, among which the *Build/train* one, can treat errors as mere warnings. This means that if some error occurs during the execution of the step, which should normally stop the execution of the whole scenario, the error is downgraded to a warning and subsequent steps in the scenario are run.

An example is the *Kill another scenario* step: if a scenario `A` has a *Kill another scenario* step where it attempts to abort another scenario `B`, the run of scenario `A` will fail if scenario `B` has not started or has already finished running. It may then be useful to activate the *Ignore failure* on the *Kill another scenario* step so that scenario `A` can always run subsequent steps.


Run step conditionally
======================

The behavior of step-based scenarios to stop at the first failing step can be overridden by using the *Run this step* options of each step.


Never
-----

To disable a step, but keep it around, one should use the `Never` option


Always
------

The step is always run, regardless of whether previous steps failed or not. This is equivalent to a `finally` block. For example a step that frees computational resources taken before in the scenario need to run regardless of the state of the previous step, so that resources are properly freed.


If no prior step failed
-----------------------

This is the default behavior of steps. 


If some prior step failed
-------------------------

This mode lets the user run steps only in case of a failure in the preceding steps, like a `catch` clause. For example to deactivate a report or send a message if a build did not succeed.


If current outcome is
---------------------

This mode is a more generic version of the above modes.


If condition satisfied
----------------------

This mode is the most generic of all, and lets the user decide to run a step based on the current outcome of the scenario or on the value of variables set before in the scenario or in the project.

The expression is a :doc:`formula  <../formula/index>`. The variables available in the formula are:

* `outcome` : the current outcome of the scenario; possible values are 'SUCCESS', 'WARNING', 'FAILED', 'ABORTED'
* `stepOutcome_stepName` : the outcome of the step named 'stepName', if the step defined one
* `stepResult_stepName` : the result of the step named 'stepName', if the step defined one
* `stepOutput_stepName` : the output of the step named 'stepName', if the step defined one
* project-level variables, scenario-level variables
* `scenarioTriggerParams` : the parameters of the trigger that initiated the scenario run, if the trigger defined some. If not empty, the fields of `scenarioTriggerParams` are also accessible as `scenarioTriggerParam_fieldName`


