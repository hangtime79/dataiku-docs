## Base imports
from dataiku.code_env_resources import clear_all_env_vars
from dataiku.code_env_resources import set_env_path
from dataiku.code_env_resources import set_env_var
from dataiku.code_env_resources import grant_permissions

# Import torchvision models
import torchvision.models as models

# Clears all environment variables defined by previously run script
clear_all_env_vars()

## PyTorch
# Set PyTorch cache directory
set_env_path("TORCH_HOME", "pytorch")

# Download pretrained model: automatically managed by PyTorch,
# does not download anything if model is already in TORCH_HOME
resnet18 = models.resnet18(weights=True)

# Grant everyone read access to pretrained models in pytorch/ folder
# (by default, PyTorch makes them only readable by the owner)
grant_permissions("pytorch")
