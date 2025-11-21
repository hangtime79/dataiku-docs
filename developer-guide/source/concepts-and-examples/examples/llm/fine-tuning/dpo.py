import dataiku
from dataiku import recipe
from datasets import Dataset
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import huggingface_hub
from trl import DPOTrainer, DPOConfig
from peft import LoraConfig

#################################
# Model & Tokenizer Preparation #
#################################

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
MODEL_REVISION = "c72e5d1908b1e2929ec8fc4c8820e9706af1f80f"
connection_name = "a_huggingface_connection_name"

saved_model = recipe.get_outputs()[0]

# Here, we're assuming that your training dataset is composed of 3 columns:  
# a question (we'll make it a prompt later), the chosen response and rejected response.  
# If using a validation dataset, format should be the same.  
train_dataset = Dataset.from_pandas(
    dataiku.Dataset("po_train").get_dataframe()
)
validation_dataset = Dataset.from_pandas(
    dataiku.Dataset("po_validation").get_dataframe()
)

auth_info = dataiku.api_client().get_auth_info(with_secrets=True)
for secret in auth_info["secrets"]:
    if secret["key"] == "hf_token":
        huggingface_hub.login(token=secret["value"])
        break

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    revision=MODEL_REVISION,
    device_map="auto",
    quantization_config=quantization_config,
    use_cache=False # Because the model will change as it is fine-tuned
)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    revision=MODEL_REVISION
)
tokenizer.pad_token = tokenizer.eos_token

####################
# Data Preparation #
####################

def return_prompt_and_responses(samples):
    """
    Transform a batch of examples in a format suitable for DPO.
    """
    return {
        "prompt": [
            f'[INST] Answer the following question in a concise manner: "{question}" [/INST]'
            for question in samples["question"]
        ],
        "chosen": samples["chosen"],
        "rejected": samples["rejected"]
    }

def transform(ds):
    """
    Prepare the datasets in a format suitable for DPO.
    """
    return ds.map(
        return_prompt_and_responses,
        batched=True,
        remove_columns=ds.column_names
    )

train_dataset = transform(train_dataset)
validation_dataset = transform(validation_dataset)

#####################
# Fine Tuning Model #
#####################

with saved_model.create_finetuned_llm_version(connection_name) as finetuned_llm_version:

    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
    )
    # Define the training parameters
    training_args = DPOConfig(
        per_device_train_batch_size=4,
        num_train_epochs=1,
        output_dir=finetuned_llm_version.working_directory,
        gradient_checkpointing=True
    )

    dpo_trainer = DPOTrainer(
        model,
        None, # The reference model is the base model (without LoRA adaptation)
        peft_config=peft_config,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=validation_dataset,
        tokenizer=tokenizer,
    )

    # Fine-tune the model
    dpo_trainer.train()

    dpo_trainer.save_model()
    config = finetuned_llm_version.config
    config["batchSize"] = dpo_trainer.state.train_batch_size
    config["eventLog"] = dpo_trainer.state.log_history