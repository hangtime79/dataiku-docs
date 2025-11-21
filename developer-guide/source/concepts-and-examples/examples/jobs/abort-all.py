import dataiku

client = dataiku.api_client()
project = client.get_default_project()
aborted_jobs = []
for job in project.list_jobs():
    if not job["stableState"]:
        job_id = job["def"]["id"]
        aborted_jobs.append(job_id)
        project.get_job(job_id).abort()
print(f"Deleted {len(aborted_jobs)} running jobs")