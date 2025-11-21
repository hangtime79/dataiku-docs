# ---------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
import pprint
from IPython.display import display, Image

client = dataiku.api_client()
project = client.get_default_project()
llm_list = project.list_llms(purpose="IMAGE_GENERATION")
for llm in llm_list:
    # pprint.pp(llm)
    print(f"- {llm.description} (id: {llm.id})")

# ---------------------------------------------------------------- NOTEBOOK-CELL: CODE
LLM_ID = "" # FILL WITH YOUR LLM ID
imagellm = dataiku.api_client().get_default_project().get_llm(LLM_ID)

# ---------------------------------------------------------------- NOTEBOOK-CELL: CODE
FOLDER_ID = "bean_images_train"
folder = dataiku.Folder(FOLDER_ID)

# ---------------------------------------------------------------- NOTEBOOK-CELL: CODE
with folder.get_download_stream("/healthy/healthy_30.jpg") as img:
    img_data = img.read()

Image(img_data)

# ---------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Example: load a Dataiku dataset as a Pandas dataframe
mydataset = dataiku.Dataset("bean_images_test_files_scored")
mydataset_df = mydataset.get_dataframe()
test_folder = dataiku.Folder("bean_images_test")
data = mydataset_df.iloc[0]

# ---------------------------------------------------------------- NOTEBOOK-CELL: CODE
with test_folder.get_download_stream(data.path) as img:
    img_data = img.read()

Image(img_data)

# ---------------------------------------------------------------- NOTEBOOK-CELL: CODE
with folder.get_download_stream("image.png") as img:
    black_mask_image_data = img.read()

generation = imagellm.new_images_generation()
generation.with_original_image(img_data, mode="INPAINTING", weight=1)
generation.with_mask("MASK_IMAGE_BLACK", image=black_mask_image_data)
generation.with_prompt(f"""Add the text "{data.prediction}" to the image""", weight=1)
generation.fidelity = 1
resp = generation.execute()

# ---------------------------------------------------------------- NOTEBOOK-CELL: CODE
Image(resp.first_image())
