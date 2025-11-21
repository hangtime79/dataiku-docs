# This file is the actual code for the Python runnable set-up-a-project
from dataiku.runnables import Runnable, ResultTable
import dataiku

class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.plugin_config = plugin_config
        self.datasets = config.get('datasets',[])
        self.text = config.get('text', '_copy')
        self.client = dataiku.api_client()
        self.project = self.client.get_default_project()

    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return (len(self.datasets), 'NONE')

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        rt = ResultTable()
        rt.add_column("1", "Original name", "STRING")
        rt.add_column("2", "Copied name", "STRING")

        for index, name in enumerate(self.datasets):
            record = []
            progress_callback(index+1)
            record.append(name)

            try:
                dataset = self.project.get_dataset(name)
                settings = dataset.get_settings().get_raw()
                params = settings.get('params')
                table = params.get('table','')
                path = params.get('path')
                if table:
                    params['table'] = "${projectKey}/" + name + self.text
                if path:
                    params['path'] = "${projectKey}/" + name + "__copy_from_notebook"

                copy = self.project.create_dataset(name + self.text,
                                                   settings.get('type'),
                                                   params,
                                                   settings.get('formatType'),
                                                   settings.get('formatParams')
                                                   )
                f = dataset.copy_to(copy, True, 'OVERWRITE')
                f.wait_for_result()
                record.append("copied to " + name + self.text)
                # Need better error handling
            except Exception:
                record.append("An error occured.")

            rt.add_record(record)

        return rt
