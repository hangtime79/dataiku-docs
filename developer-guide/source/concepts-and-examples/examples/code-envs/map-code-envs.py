import dataiku


def get_instance_default_code_env(client):
    """Return the global default code envs (instance-level).
    """

    defaults = {}
    general_settings = client.get_general_settings()
    for rcp_type in [("python", "defaultPythonEnv"), ("r", "defaultREnv")]:
        code_env = general_settings.settings["codeEnvs"].get(rcp_type[1], None)
        if code_env:
            defaults[rcp_type[0]] = code_env
        else:
            defaults[rcp_type[0]] = "dss_builtin"
    return defaults
        

def get_code_env_mapping(client, project):
    """Return a dict mapping code-based items with their code envs.
    """

    rcp_types = ["python", "r"]
    mapping = {"python": [], "r": []}

    env_default = {}
    settings = project.get_settings()
    project_default_modes = settings.get_raw()["settings"]["codeEnvs"]
    all_recipes = project.list_recipes()
    for rcp_type in rcp_types:
        if project_default_modes[rcp_type]["mode"] == "USE_BUILTIN_MODE":
            env_default[rcp_type] = "dss_builtin"
        if project_default_modes[rcp_type]["mode"] == "INHERIT":
            env_default[rcp_type] = get_instance_default_code_env(client).get(rcp_type)
        if project_default_modes[rcp_type]["mode"] == "EXPLICIT_ENV":
            env_default[rcp_type] = project_default_modes[rcp_type]["envName"]
        recipes = [r for r in all_recipes if r["type"] == rcp_type]
        for r in recipes:
            name = r["name"]
            env_select = r["params"]["envSelection"]
            if env_select["envMode"] == "EXPLICIT_ENV":
                code_env = env_select["envName"]
            else:
                code_env = env_default[rcp_type]
            mapping[rcp_type].append({"name": name, "code_env": code_env})
    return mapping

client = dataiku.api_client()
project = client.get_default_project()
mapping = get_code_env_mapping(client, project)
print(mapping)