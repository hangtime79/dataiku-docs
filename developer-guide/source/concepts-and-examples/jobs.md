(jobs)=

```{eval-rst}
..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 24/09/2024
  
  this code samples has been verified on DSS: 14.2.0
  Date of check: 15/09/2025
```

# Jobs

The API offers methods to retrieve the list of jobs and their status, so that they can be monitored. Additionally, new jobs can be created to build datasets.

## Reading the jobs' status

The list of all jobs, finished or not, can be fetched with the {py:meth}`dataikuapi.dss.project.DSSProject.list_jobs` method. For example, to retrieve job failures posterior to a given date:

```python
import dataiku
import datetime


date = '2015/09/24'
date_as_timestamp = int(datetime.datetime.strptime(date, "%Y/%m/%d").strftime('%s')) * 1000
client = dataiku.api_client()
project = client.get_default_project()
jobs = project.list_jobs()
failed_jobs = [job for job in jobs if job['state'] == 'FAILED' and job['def']['initiationTimestamp'] >= date_as_timestamp]
```

The method {py:meth}`~dataikuapi.dss.project.DSSProject.list_jobs` returns all job information for each job, as a JSON object. Important fields are:

```python
{
        'def': {   'id': 'build_cat_train_hdfs_NP_2015-09-28T09-17-37.455',    # the identifier for the job
                'initiationTimestamp': 1443431857455,                      # timestamp of when the job was submitted
                'initiator': 'API (aa)',
                'mailNotification': False,
                'name': 'build_cat_train_hdfs_NP',
                'outputs': [   {   'targetDataset': 'cat_train_hdfs',      # the dataset(s) built by the job
                                    'targetDatasetProjectKey': 'IMPALA',
                                    'targetPartition': 'NP',
                                    'type': 'DATASET'}],
                'projectKey': 'IMPALA',
                'refreshHiveMetastore': False,
                'refreshIntermediateMirrors': True,
                'refreshTargetMirrors': True,
                'triggeredFrom': 'API',
                'type': 'NON_RECURSIVE_FORCED_BUILD'},
    'endTime': 0,
    'stableState': True,
    'startTime': 0,
    'state': 'ABORTED',                                                    # the stable state of the job
    'warningsCount': 0}
```

The `id` field is needed to get a handle of the job and call {py:meth}`~dataikuapi.dss.job.DSSJob.abort` or {py:meth}`~dataikuapi.dss.job.DSSJob.get_log` on it.

## Starting new jobs

Datasets can be built by creating a job of which they are the output. A job is created by building a job definition and starting it. For a simple non-partitioned dataset, this is done with:

```python
import dataiku
import time

client = dataiku.api_client()
project = client.get_default_project()

definition = {
        "type" : "NON_RECURSIVE_FORCED_BUILD",
        "outputs" : [{
            "id" : "dataset_to_build",
            "type": "DATASET",
            "partition" : "NP"
        }]
    }
job = project.start_job(definition)
state = ''
while state != 'DONE' and state != 'FAILED' and state != 'ABORTED':
        time.sleep(1)
        state = job.get_status()['baseStatus']['state']
# done!
```

The example above uses {py:meth}`~dataikuapi.dss.project.DSSProject.start_job` to start a job, and then checks the job state every second until it is complete. Alternatively, the method {py:meth}`~dataikuapi.dss.project.DSSProject.start_job_and_wait()` can be used to start a job and return only after job completion.

The {py:meth}`~dataikuapi.dss.project.DSSProject.start_job` method returns a job handle that can be used to later abort the job. Other jobs can be aborted once their id is known. For example, to abort all jobs currently being processed:

```python
import dataiku

client = dataiku.api_client()
project = client.get_default_project()
for job in project.list_jobs():
    if job['stableState'] == False:
        project.get_job(job['def']['id']).abort()
```

Here's another example of using {meth}`~dataikuapi.dss.project.DSSProject.new_job` to build a managed folder and the `with_output` method as an alternative to creating a dictionary job definition:

```python
import dataiku

client = dataiku.api_client()
project = client.get_default_project()
# where O2ue6CX3 is the managed folder id
job = project.new_job('RECURSIVE_FORCED_BUILD').with_output('O2ue6CX3', object_type='MANAGED_FOLDER')
res = job.start_and_wait()
print(res.get_status())
```

## Aborting jobs 

Jobs can be individually be aborted using the {py:meth}`~dataikuapi.dss.job.DSSJob.abort` method. The following example shows how to extend it to abort all jobs of a given Project.


```{literalinclude} examples/jobs/abort-all.py
```

## Reference documentation

### Classes

```{eval-rst}
.. autosummary::
        dataikuapi.dss.job.DSSJob
        dataikuapi.dss.job.DSSJobWaiter
        dataikuapi.dss.project.JobDefinitionBuilder
```

### Functions
```{eval-rst}
.. autosummary::
    ~dataikuapi.dss.job.DSSJob.get_status
    ~dataikuapi.dss.project.DSSProject.list_jobs
    ~dataikuapi.dss.project.DSSProject.new_job
    ~dataikuapi.dss.project.JobDefinitionBuilder.start_and_wait
    ~dataikuapi.dss.project.DSSProject.start_job
```