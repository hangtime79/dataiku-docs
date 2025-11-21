import dataiku

PROJECT_KEY = "DKU_TSHIRTS"
GROUP = "readers"

client = dataiku.api_client()
project = client.get_project(PROJECT_KEY)
permissions = project.get_permissions()

new_perm = {
    "group": GROUP,
    "admin": False,
    "executeApp": False,
    "exportDatasetsData": False,
    "manageAdditionalDashboardUsers": False,
    "manageDashboardAuthorizations": False,
    "manageExposedElements": False,
    "moderateDashboards": False,
    "readDashboards": True,
    "readProjectContent": True,
    "runScenarios": False,
    "shareToWorkspaces": False,
    "writeDashboards": False,
    "writeProjectContent": False
}

permissions["permissions"].append(new_perm)
project.set_permissions(permissions)