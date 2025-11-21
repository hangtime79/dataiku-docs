scenario = project.get_scenario(scenario_id)
last_run = scenario.get_last_finished_run()
data = {
    "scenario_id": scenario_id,
    "outcome": last_run.outcome,
    "start_time": last_run.start_time.isoformat(),
    "end_time": last_run.end_time.isoformat()
}
print(data)