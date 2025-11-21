"Editable" dataset
##########################

An Editable Dataset is a special dataset stored on the DSS server that can be edited manually. Editable Datasets are limited to 100 000 rows and can only be modified from the UI. They can't be edited from the dataiku Python API.

It is possible create an editable dataset from any other dataset with the Push to Editable recipe, see :doc:`/other_recipes/push-to-editable` for more information, or from the Python API with pythproject.create_dataset("my_editable", "Inline"). 
