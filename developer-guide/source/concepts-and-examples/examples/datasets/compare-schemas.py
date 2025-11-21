import json

def unpack_schema(s):
    return [json.dumps(x) for x in s]

dataset_names = ["ds_a", "ds_b"]
schemas = {}
for ds in dataset_names: 
    schemas[ds] = project.get_dataset(ds) \
        .get_schema() \
        .get("columns")
    
common_cols = set(unpack_schema(schemas["ds_a"])) \
    .intersection(unpack_schema(schemas["ds_b"]))