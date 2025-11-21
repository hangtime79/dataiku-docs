import os
import subprocess

PACKAGES = [
    {
        "name": "dataikuapi",
        "exclude": [
            "dss_plugin_mlflow/*",
            "fm/*",
            "dss/tools/*",
            "dss/analysis.py",
            "dss/codestudio.py",
            "dss/continuousactivity.py",
            "dss/macro.py",
            "apinode_client.py",
            "base_client.py",
            "fmclient.py",
            "utils.py",
            "module_utils/*",
            "setup.py"]
    },
    {
        "name": "dataiku",
        "exclude": [
            "base/*",
            "bigframes/*",
            "core/base.py",
            "core/connection.py",
            "core/continuous_write.py",
            "core/dataframe_preparation.py",
            "core/debugging.py",
            "core/dku_logging.py",
            "core/dku_pandas_csv.py",
            "core/dkuio.py",
            "core/dkujson.py",
            "core/doctor_constants.py",
            "core/export_model_charts_and_templates.py",
            "core/flow.py",
            "core/intercom.py",
            "core/message_sender.py",
            "core/pandasutils.py",
            "core/percentage_progress.py",
            "core/pig.py",
            "core/platform_exec.py",
            "core/plugin.py",
            "core/project.py",
            "core/schema_handling.py",
            "core/sql.py",
            "core/streaming_endpoint.py",
            "core/write_base.py",
            "cluster/*",
            "code_env_resources/*",
            "code_studio/*",
            "connector/*",
            "container/*",
            "continuous/*",
            "customformat/*",
            "customrecipe/*",
            "customstep/*",
            "customtrigger/*",
            "customui/*",
            "customwebapp/*",
            "doctor/*",
            "dsscli/*",
            "eda/*",
            "exporter/*",
            "externalml/*",
            "fsprovider/*",
            "metric/*",
            "modelevaluation/*",
            "notebook/*",
            "recipe/*",
            "runnables/*",
            "scenario/build_state.py",
            "scenario/messaging.py",
            "scenario/step.py",
            "scenario/trigger.py",
            "snowpark/*",
            "sql/*",
            "udf/*",
            "vendor/*",
            "webapps/*"
        ]
    }
]

SPHINX_APIDOC_DIR = "source/api-reference/python"

def generate_apidoc():
    # Retrieve path of dip
    dip_dir = os.environ.get("DKUINSTALLDIR", "")
    if dip_dir:
        # Check that directory exists
        if not os.path.isdir(dip_dir):
            raise ValueError(f"{dip_dir} is not a valid directory")
    else:
        raise ValueError(f"DKUINSTALLDIR is not defined")
    # Set SPHINX_APIDOC_OPTIONS env variable to override default automodule directives
    os.environ["SPHINX_APIDOC_OPTIONS"] = "members"

    # Generate .rst files
    python_path = os.path.join(dip_dir, "src/main/python")
    for package in PACKAGES:
        print(f"--Documenting {package['name']}...")
        package_path = os.path.join(python_path, package["name"])
        cmd = ["sphinx-apidoc", "-o", SPHINX_APIDOC_DIR, package_path]
        for excl in package["exclude"]:
            cmd.append(f"{package_path}/{excl}")
        subprocess.run(cmd)

# Delete the generated .rst files
def clean():
    print("-- Removing old files...")
    for item in os.listdir(SPHINX_APIDOC_DIR):
        if item != "index.md":
            item_path = os.path.join(SPHINX_APIDOC_DIR, item)
            print(f"Deleting file {item_path}")
            os.remove(item_path)

def main():
    clean()
    generate_apidoc()

if __name__ == "__main__":
    main()