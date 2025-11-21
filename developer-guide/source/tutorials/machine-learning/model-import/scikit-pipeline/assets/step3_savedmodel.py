import dataiku
import pickle
import mlflow

# Fill the models managed folder id below
MODEL_FOLDER_ID = ""
# Use name of the code environment from prerequisites
MLFLOW_CODE_ENV_NAME = ""

client = dataiku.api_client()
project = client.get_default_project()

# Use for Dataiku Cloud
# client._session.verify = False

# use or create SavedModel
SAVED_MODEL_NAME = "clf"
SAVED_MODEL_ID = None

for sm in project.list_saved_models():
    if SAVED_MODEL_NAME != sm["name"]:
        continue
    else:
        SAVED_MODEL_ID = sm["id"]
        print(
            "Found SavedModel {} with id {}".format(
                SAVED_MODEL_NAME, SAVED_MODEL_ID))
        break
if SAVED_MODEL_ID:
    sm = project.get_saved_model(SAVED_MODEL_ID)
else:
    sm = project.create_mlflow_pyfunc_model(
        name=SAVED_MODEL_NAME,
        prediction_type="BINARY_CLASSIFICATION")
    SAVED_MODEL_ID = sm.id
    print(
        "SavedModel not found, created new one with id {}".format(
            SAVED_MODEL_ID))

# Load model from pickle file
folder = dataiku.Folder(MODEL_FOLDER_ID)
with folder.get_download_stream("/pipeline.pkl") as f:
    model = pickle.load(f)

# Create MLflow model via a dummy experiment run
folder_api_handle = project.get_managed_folder(MODEL_FOLDER_ID)
mlflow_extension = project.get_mlflow_extension()
with project.setup_mlflow(managed_folder=folder_api_handle) as mf:
    mlflow.set_experiment("dummy_xpt")
    with mlflow.start_run(run_name="dummy_run") as run:
        mlflow.sklearn.log_model(sk_model=model, artifact_path="dummy_model")
        mlflow_extension.set_run_inference_info(
            run_id=run._info.run_id,
            prediction_type='BINARY_CLASSIFICATION',
            classes=list(model.classes_),
            code_env_name=MLFLOW_CODE_ENV_NAME)

# Deploy MLflow model as a saved model version
mlflow_extension.deploy_run_model(
    run_id=run._info.run_id,
    sm_id=SAVED_MODEL_ID,
    version_id="v01",
    evaluation_dataset="bank_test",
    target_column_name="y")
