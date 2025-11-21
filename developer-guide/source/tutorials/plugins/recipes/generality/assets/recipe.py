# import the classes for accessing Dataiku objects from the recipe
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config

# To retrieve the datasets of an input role named 'dataset_to_copy' as an array of dataset names:
datasets_to_copy = get_input_names_for_role('dataset_to_copy')
# The two lines below show two different ways to access to the wanted dataset
# dataset_to_copy = [dataiku.Dataset(name) for name in datasets_to_copy][0]
dataset_to_copy = dataiku.Dataset(datasets_to_copy[0])

# For outputs, the process is the same:
copied_datasets = get_output_names_for_role('copied_dataset')
copied_dataset = [dataiku.Dataset(name) for name in copied_datasets][0]

# Using the input dataset
dataset_to_copy_df = dataset_to_copy.get_dataframe()

# Your algorithm
copied_dataset_df = dataset_to_copy_df

# Using the output dataset
copied_dataset.write_with_schema(copied_dataset_df)
