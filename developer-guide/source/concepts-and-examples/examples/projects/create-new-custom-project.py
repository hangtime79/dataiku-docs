import dataiku
from datetime import datetime

def create_checklist(author, items):
    checklist = {
        "title": "To-do list",
        "createdOn": 0,
        "items": []
    }
    for item in items:
        checklist["items"].append({
            "createdBy": author,
            "createdOn": int(datetime.now().timestamp()),
            "done": False,
            "stateChangedOn": 0,
            "text": item
        })
    return checklist

def create_custom_project(client,
                          project_key,
                          name,
                          custom_tags,
                          description,
                          checklist_items):
    current_user = client.get_auth_info()["authIdentifier"]
    project = client.create_project(project_key=project_key,
                                    name=name,
                                    owner=current_user,
                                    description=description)
    # Add tags                                 
    tags = project.get_tags()
    tags["tags"] = {k: {} for k in custom_tags}
    project.set_tags(tags)

    # Add checklist
    metadata = project.get_metadata()
    metadata["checklists"]["checklists"].append(create_checklist(author=current_user,
                                                                 items=checklist_items))
    project.set_metadata(metadata)

    # Set default status to "Draft"
    settings = project.get_settings()
    settings.settings["projectStatus"] = "Draft"
    settings.save()

    return project

# Example 
client = dataiku.api_client()
tags = ["work-in-progress", "machine-learning", "priority-high"]
checklist = [
    "Connect to data sources",
    "Clean, aggregate and join data",
    "Train ML model",
    "Evaluate ML model",
    "Deploy ML model to production"
    ]
            
project = create_custom_project(client=client,
                                project_key="MYPROJECT",
                                name="A custom Project",
                                custom_tags=tags,
                                description="This is a cool Project",
                                checklist_items=checklist)
