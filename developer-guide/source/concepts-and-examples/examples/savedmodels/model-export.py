import dataiku

PROJECT_KEY = 'YOUR_PROJECT_KEY'
METRIC = 'auc' # or any classification metrics of interest.
SAVED_MODEL_ID = 'YOUR_SAVED_MODEL_ID'
FILENAME = 'path/to/model-archive.zip'


def get_best_classifier_version(project, saved_model_id, metric):
    """
    This function returns the best version id of a
    given Dataiku classifier model in a project.
    """

    model = project.get_saved_model(saved_model_id)
    outcome = []
    
    for version in model.list_versions():    
        version_id = version.get('id')
        version_details = model.get_version_details(version_id)
        perf = version_details.get_raw_snippet().get(metric)
        outcome.append((version_id, perf))
    
    # get the best version id. User reverse=False if 
    # lower metric means better
    best_version_id = sorted(
        outcome, key = lambda x: x[1], reverse=True)[0][0]
    
    return best_version_id
        


client = dataiku.api_client()
project = client.get_project(PROJECT_KEY)
model = project.get_saved_model(SAVED_MODEL_ID)
best_version_id = get_best_classifier_version(project, SAVED_MODEL_ID, METRIC)
version_details = model.get_version_details(best_version_id)

# Export in Python
version_details.get_scoring_python(FILENAME)

# Export in MLflow format
version_details.get_scoring_mlflow(FILENAME)

