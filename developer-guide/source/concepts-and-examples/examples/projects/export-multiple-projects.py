
import dataiku
import os

from datetime import datetime

PROJECT_KEY = "BACKUP_PROJECTS"
FOLDER_NAME = "exports"
PROJECT_KEYS_TO_EXPORT = ["FOO", "BAR"]

# Generate timestamp (e.g. 20221201-123000)
ts = datetime \
    .now() \
    .strftime("%Y%m%d-%H%M%S")

client = dataiku.api_client()
project = client.get_project(PROJECT_KEY)
folder_path = dataiku.Folder(FOLDER_NAME, project_key=PROJECT_KEY) \
    .get_path()
for pkey in PROJECT_KEYS_TO_EXPORT:
    zip_name = f"{pkey}-{ts}.zip"
    pkey_project = client.get_project(pkey)
    with pkey_project.get_export_stream() as es:
        target = os.path.join(folder_path, zip_name)
        with open(target, "wb") as f:
            for chunk in es.stream(512):
                f.write(chunk)