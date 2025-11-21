# This file is the actual code for the Python runnable project-creation
import random
import string
from datetime import datetime
import dataiku
import json
from dataiku.runnables import Runnable


class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.config = config
        self.plugin_config = plugin_config
        self.project_name = self.config.get('project_name')
        # project_key should not contain any space
        self.project_key = ''.join([char.upper() for char in self.project_name if char.isalpha()])
        self.code_envs = self.config.get('code_envs')
        self.default_cluster = self.config.get('default_cluster')
        self.tags = self.config.get('tags')
        self.additional_wiki = self.config.get('additional_wiki')
        self.wiki_content = self.config.get('wiki_content')

    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def create_checklist(self, author, items):
        """
        Generate a checklist from a list of items

        :param author: Author of the checklist
        :param items: list of items
        :return: the checklist
        """
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

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """

        # Create a (Dataiku) client for interacting with Dataiku and collect the connected user.
        user_client = dataiku.api_client()
        user_auth_info = user_client.get_auth_info()

        # Generate a unique project_key
        while self.project_key in user_client.list_project_keys():
            self.project_key = self.project_name.upper() + '_' + ''.join(random.choices(string.ascii_uppercase, k=10))

        # Create the project
        new_project = user_client.create_project(self.project_key, self.project_name,
                                                 user_auth_info.get('authIdentifier'))

        # Set the default code env and cluster
        settings = new_project.get_settings()
        settings.set_python_code_env(self.code_envs)
        settings.set_k8s_cluster(self.default_cluster)
        settings.save()

        # Add tags to the project settings
        tags = new_project.get_tags()
        tags["tags"] = {t: {} for t in self.tags}
        new_project.set_tags(tags)

        # Create the checklist and add tags to the projects
        to_dos = ["Import some datasets",
                  "Create your first recipe/notebook",
                  "Enjoy coding"]
        metadata = new_project.get_metadata()
        metadata["checklists"]["checklists"].append(self.create_checklist(user_auth_info.get('authIdentifier'),
                                                                          items=to_dos))
        metadata['tags'] = [t for t in self.tags]
        new_project.set_metadata(metadata)

        # Create the wiki if the user wants it.
        if self.additional_wiki:
            wiki = new_project.get_wiki()
            article = wiki.create_article("Home page",
                                          content=self.wiki_content)
            settings = wiki.get_settings()
            settings.set_home_article_id(article.article_id)
            settings.save()
        
        return json.dumps({"projectKey": self.project_key})