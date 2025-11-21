import dataiku

DATAIKU_HOST = ""  # Fill in your Dataiku instance's URL
API_KEY = "" # Fill in your personal API key to access that instance

# connect to your instance
dataiku.set_remote_dss(f"http://{DATAIKU_HOST}", API_KEY)
client = dataiku.api_client()

# list all the projects of the instance 
project_keys = client.list_project_keys()
print(f"N-projects on instance: {len(project_keys)}")

# work with a specific sample project
PROJECT_KEY = "DKU_TUT_VARCOD"
project = client.get_project(PROJECT_KEY)

USERNAME = "" # Fill in your username
REPO = "" # Fill in your repo

# get the project git!
project_git = project.get_project_git()

# .. and set the remote
project_git.set_remote(f"{USERNAME}@{REPO}:{PROJECT_KEY}")

# create a new branch
project_git.create_branch('definitely-not-master')
project_git.checkout('definitely-not-master')

# add these variables
project.update_variables({
   "country_name": "Germany",
   "merchant_url": "lidl"})

# commit & push
project_git.get_status()
project_git.commit(message="add project vars")
project_git.push()

# fetch & pull
project_git.fetch()
project_git.pull()
