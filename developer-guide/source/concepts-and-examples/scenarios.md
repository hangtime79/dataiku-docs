(scenarios)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 23/09/2024
  
    this code samples has been verified on DSS: 14.1.0
  Date of check: 01/09/2025
```

# Scenarios

The scenario API can control all aspects of managing a scenario.

:::{note}
There is a dedicated API to use *within* a scenario to run steps and report on progress of the scenario. For that, please see {doc}`scenarios-inside`.
:::

## Example use cases

In all examples, `project` is a {class}`dataikuapi.dss.project.DSSProject` handle, obtained using {meth}`~dataikuapi.DSSClient.get_project()` or {meth}`~dataikuapi.DSSClient.get_default_project()`

### Run a scenario

#### Variant 1: Run and wait for it to complete

```python
scenario = project.get_scenario("MYSCENARIO")

scenario.run_and_wait()
```

#### Variant 2: Run, then poll while doing other stuff

```python
scenario = project.get_scenario("MYSCENARIO")

trigger_fire = scenario.run()

# When you call `run` a scenario, the scenario is not immediately
# started. Instead a "manual trigger" fires.
#
# This trigger fire can be cancelled if the scenario was already running,
# or if another trigger fires
# Thus, the scenario run is not available immediately, and we must "wait"
# for it

scenario_run = trigger_fire.wait_for_scenario_run()

# Now the scenario is running. We can wait for it synchronously with
# scenario_run.wait_for_completion(), but if we want to do other stuff
# at the same time, we can use refresh

while True:
    # Do a bit of other stuff
    # ...

    scenario_run.refresh()
    if scenario_run.running:
        print("Scenario is still running ...")
    else:
        print("Scenario is not running anymore")
        break

    time.sleep(5)
```

### Get information about the last completed run of a scenario

```python
scenario = project.get_scenario("MYSCENARIO")

last_runs = scenario.get_last_runs(only_finished_runs=True)

if len(last_runs) == 0:
    raise Exception("The scenario never ran")

last_run = last_runs[0]

# outcome can be one of SUCCESS, WARNING, FAILED or ABORTED
print(f"The last run finished with {last_run.outcome}")

# start_time and end_time are datetime.datetime objects
print(f"Last run started at {last_run.start_time} and finished at {last_run.end_time}")
```

### Disable/enable scenarios

#### Disable and remember

This snippet disables all scenarios in a project (i.e. prevents them from auto-triggering), and also keeps
a list of the ones that were active, so that you can selectively re-enable them later

```python
# List of scenario ids that were active
previously_active = []

for scenario in project.list_scenarios(as_type="objects"):
    settings = scenario.get_settings()

    if settings.active:
        previously_active.append(scenario.id)
        settings.active = False
        # In order for settings change to take effect, you need to save them
        settings.save()
```

#### Enable scenarios from a list of ids

```python
for scenario_id in previously_active:
    scenario = project.get_scenario(scenario_id)
    settings = scenario.get_settings()

    settings.active = True
    settings.save()
```

### List the "run as" user for all scenarios

This snippet allows you to list the identity under which a scenario runs:

```python
for scenario in project.list_scenarios(as_type="objects"):
    settings = scenario.get_settings()
    # We must use `effective_run_as` and not `run_as` here.
    # run_as contains the "configured" run as, which can be None - in that case, it will run
    # as the last modifier of the scenario
    # effective_run_as is always valued and is the resolved version.
    print(f"Scenario {scenario.id} runs as user {settings.effective_run_as}")
```

### Reassign scenarios to another user

If user "u1" has left the company, you may want to reassign all scenarios that ran under his identity to another
user "u2".

```python
for scenario in project.list_scenarios(as_type="objects"):
    settings = scenario.get_settings()

    if settings.effective_run_as == "u1":
        print(f"Scenario {scenario.id} used to run as u1, reassigning it")
        # To configure a run_as, we must use the run_as property.
        # effective_run_as is read-only
        settings.run_as = "u2"
        settings.save()
```

### Get the "next expected" run for a scenario

If the scenario has a temporal trigger enabled, this will return a datetime of the approximate next expected run

```python
scenario = project.get_scenario("MYSCENARIO")
# next_run is None if no next run is scheduled
print(f"Next run is at {scenario.get_status().next_run}")
```

### Get the list of jobs started by a scenario

"Build/Train" or Python steps in a scenario can start jobs. This snippet will give you the list of job ids
that a particular scenario run executed.

These job ids can then be used together with {meth}`~dataikuapi.dss.project.DSSProject.get_job`

```python
scenario = project.get_scenario("MYSCENARIO")
# Focusing only on the last completed run. Else, use get_last_runs() and iterate
last_run = scenario.get_last_finished_run()

last_run_details = last_run.get_details()

all_job_ids = []
for step in last_run_details.steps:
    all_job_ids.extend(step.job_ids)

print(f"All job ids started by scenario run {last_run.id} : {all_job_ids}")
```

### Get the first error that happened in a scenario run

This snippet retrieves the first error that happened during a scenario run.

```python
scenario = project.get_scenario("MYSCENARIO")

last_run = scenario.get_last_finished_run()

if last_run.outcome == "FAILED":
    last_run_details = last_run.get_details()
    print(f"Error was: {last_run_details.first_error_details}")
```

### Start multiple scenarios and wait for all of them to complete

This code snippet starts multiple scenarios and returns when all of them have completed, returning
the updated DSSScenarioRun for each

```python
import time

scenarios_ids_to_run = ["s1", "s2", "s3"]

scenario_runs = []

for scenario_id in scenarios_ids_to_run:
    scenario = project.get_scenario(scenario_id)

    trigger_fire = scenario.run()
    # Wait for the trigger fire to have actually started a scenario
    scenario_run = trigger_fire.wait_for_scenario_run()
    scenario_runs.append(scenario_run)

# Poll all scenario runs, until all of them have completed
while True:
    any_not_complete = False
    for scenario_run in scenario_runs:
        # Update the status from the DSS API
        scenario_run.refresh()
        if scenario_run.running:
            any_not_complete = True

    if any_not_complete:
        print("At least a scenario is still running...")
    else:
        print("All scenarios are complete")
        break

    # Wait a bit before checking again
    time.sleep(30)

print(f"Scenario run ids and outcomes: {[(sr.id, sr.outcome) for sr in scenario_runs]}")
```

### Change the "from" email for email reporters

Note that usually, we would recommend using variables for "from" and "to" email. But you can also modify them with the API.

```python
scenario = project.get_scenario("MYSCENARIO")

settings = scenario.get_settings()

for reporter in settings.raw_reporters:
    # Only look into 'email' kind of reporters
    if reporter["messaging"]["type"] == "mail-scenario":
        messaging_configuration = reporter["messaging"]["configuration"]
        messaging_configuration["sender"] = "new.email.address@company.com"
        print(f"Updated reporter {reporter['id']}")

settings.save()
```

## Detailed examples

This section contains more advanced examples on Scenarios.

### Get last run results

You can programmatically get the outcome of the last finished run for a given Scenario.

```{literalinclude} examples/scenarios/get-last-scenario-runs.py
```

From there, you can easily extend the same logic to loop across all Scenarios within a Project.


## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
    dataikuapi.dss.scenario.DSSScenario
    dataikuapi.dss.scenario.DSSScenarioListItem
    dataikuapi.dss.scenario.DSSScenarioSettings
    dataikuapi.dss.scenario.DSSScenarioRun
    dataikuapi.dss.scenario.DSSScenarioRunDetails
    dataikuapi.dss.scenario.DSSScenarioStatus
    dataikuapi.dss.scenario.DSSStepRunDetails
    dataikuapi.dss.scenario.DSSTriggerFire
```

### Functions
```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.scenario.DSSScenarioSettings.active
    ~dataikuapi.dss.scenario.DSSScenarioSettings.effective_run_as
    ~dataikuapi.dss.scenario.DSSScenarioRun.end_time
    ~dataikuapi.dss.scenario.DSSStepRunDetails.first_error_details
    ~dataikuapi.dss.scenario.DSSScenarioRun.get_details
    ~dataikuapi.dss.scenario.DSSScenarioRun.id
    ~dataikuapi.dss.scenario.DSSStepRunDetails.job_ids
    ~dataikuapi.dss.scenario.DSSScenarioStatus.next_run
    ~dataikuapi.dss.scenario.DSSScenarioRun.outcome
    ~dataikuapi.dss.scenario.DSSScenarioSettings.raw_reporters
    ~dataikuapi.dss.scenario.DSSScenarioRun.refresh
    ~dataikuapi.dss.scenario.DSSScenario.run
    ~dataikuapi.dss.scenario.DSSScenario.run_and_wait
    ~dataikuapi.dss.scenario.DSSScenarioSettings.run_as
    ~dataikuapi.dss.scenario.DSSScenarioRun.running
    ~dataikuapi.dss.scenario.DSSScenarioSettings.save
    ~dataikuapi.dss.scenario.DSSScenarioRun.start_time
    ~dataikuapi.dss.scenario.DSSScenarioRunDetails.steps
    ~dataikuapi.dss.scenario.DSSTriggerFire.wait_for_scenario_run
```