
def get_best_model(project, analysis_id, ml_task_id, metric):
    analysis = project.get_analysis(analysis_id)
    ml_task = analysis.get_ml_task(ml_task_id)
    trained_models = ml_task.get_trained_models_ids()
    trained_models_snippets = [ml_task.get_trained_model_snippet(m) for m in trained_models]
    # Assumes that for your metric, "higher is better"
    best_model_snippet = max(trained_models_snippets, key=lambda x:x[metric])
    best_model_id = best_model_snippet["fullModelId"]
    return ml_task, best_model_id


def deploy_with_best_model(project,
    analysis_id,
    ml_task_id,
    metric,
    saved_model_name,
    training_dataset):
    """Create a new Saved Model in the Flow with the 'best model' of a MLTask.
    """

    ml_task, best_model_id = get_best_model(project,
                                            analysis_id,
                                            ml_task_id,
                                            metric)
    ml_task.deploy_to_flow(best_model_id,
                           saved_model_name,
                           training_dataset)

def update_with_best_model(project,
                           analysis_id,
                           ml_task_id,
                           metric,
                           saved_model_name,
                           activate=True):
    """Update an existing Saved Model in the Flow with the 'best model' 
       of a MLTask.
    """
    ml_task, best_model_id = get_best_model(project,
                                            analysis_id,
                                            ml_task_id,
                                            metric)
    training_recipe_name = f"train_{saved_model_name}"
    ml_task.redeploy_to_flow(model_id=best_model_id,
                             recipe_name=training_recipe_name,
                             activate=activate)