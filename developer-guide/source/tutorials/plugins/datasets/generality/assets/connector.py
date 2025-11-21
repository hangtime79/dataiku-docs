import string

from dataiku.connector import Connector
import random


def generate_random_data(param):
    if param == "string":
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for i in range(random.randrange(1, 100)))
    if param == "number":
        return random.randrange(0, 100)
    if param == "boolean":
        return random.choice([True, False])


class MyConnector(Connector):
    """
    Generate random data
    """

    def __init__(self, config, plugin_config):
        """
        Initializes the dataset
        Args:
            config:
            plugin_config:
        """
        Connector.__init__(self, config, plugin_config)  # pass the parameters to the base class

        # perform some more initialization
        self.size = self.config.get("size", 100)
        self.columns = self.config.get("columns", ["first_col", "my_string"])
        self.types = [col.lower() for col in self.config.get("column_types", ["string", "string"])]

        # If we do not have enough types for the specified columns, complete with "string"
        len_col = len(self.columns)
        len_types = len(self.types)
        if (len_types < len_col):
            self.types.extend(["string"] * (len_col - len_types))

    def get_read_schema(self):
        """
        Returns the schema that this dataset generates when returning rows.
        """

        types = [{"name": val[0], "type": val[1]} for val in zip(self.columns, self.types)]
        return {"columns": types}

    def generate_rows(self, dataset_schema=None, dataset_partitioning=None,
                      partition_id=None, records_limit=-1):
        """
        The main reading method.

        Returns a generator over the rows of the dataset (or partition)
        Each yielded row must be a dictionary, indexed by column name.

        The dataset schema and partitioning are given for information purpose.
        """
        for i in range(0, self.size):
            data = {}
            for j in zip(self.columns, self.types):
                data[j[0]] = generate_random_data(j[1])
            yield data
