import datasets
import torch
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer

from dataiku import recipe
from dataiku.llm.finetuning import formatters

base_model_name = "mistralai/Mistral-7B-Instruct-v0.2"
assert base_model_name, ("please specify a base LLM, it must be available"
                         " on HuggingFace hub")

connection_name = "a_huggingface_connection_name"
assert connection_name, ("please specify a connection name, the fine-tuned"
                         " LLM will be available from this connection")

##################
# Initial setup
##################
# Here, we're assuming that your training dataset is composed of 2 columns:
# the input (user message) and expected output (assistant message).
# If using a validation dataset, format should be the same.
user_message_column = "input"
assistant_message_column = "output"
columns = [user_message_column, assistant_message_column]

system_message_column = ""  # optional
static_system_message = ""  # optional
if system_message_column:
    columns.append(system_message_column)

# Turn Dataiku datasets into SFTTrainer datasets. 
training_dataset = recipe.get_inputs()[0]
df = training_dataset.get_dataframe(columns=columns)
train_dataset = datasets.Dataset.from_pandas(df)

validation_dataset = None
eval_dataset = None
if len(recipe.get_inputs()) > 1:
    validation_dataset = recipe.get_inputs()[1]
    df = validation_dataset.get_dataframe(columns=columns)
    eval_dataset = datasets.Dataset.from_pandas(df)

saved_model = recipe.get_outputs()[0]

##################
# Model loading
##################
# Here, we are quantizing the Mistral model. It means that the weights
# are represented with lower-precision data types (like "Normal Float 4"
# from the [QLoRA paper](https://arxiv.org/pdf/2305.14314)) to optimize
# memory usage.
# We also change the data type used for matrix multiplication to speed
# up compute.
# One can of course use double (/nested) quantization, but with inevitable
# important precision loss.
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=False,
)

model = AutoModelForCausalLM.from_pretrained(base_model_name,
                                             quantization_config=bnb_config)
tokenizer = AutoTokenizer.from_pretrained(base_model_name)

tokenizer.pad_token = tokenizer.unk_token
tokenizer.padding_side = "right"

# It is mandatory to define a formatting function for fine-tuning,
# because ultimately, the model is fed with only one string:
# the concatenation of your input columns, in a specific format.
# Here, we leverage the apply_chat_template method, which depends
# on the tokenizer. For more information,
# see https://huggingface.co/docs/transformers/v4.43.3/chat_templating

formatting_func = formatters.ConversationalPromptFormatter(tokenizer.apply_chat_template,
                                                           *columns)

##################
# Fine-tune using SFTTrainer
##################
with saved_model.create_finetuned_llm_version(connection_name) as finetuned_llm_version:
    # feel free to customize, the only requirement is for a transformers model
    # to be created in finetuned_model_version.working_directory

    # TRL package offers many possibilities to configure the training job. 
    # For the full list, see
    # https://huggingface.co/docs/transformers/v4.43.3/en/main_classes/trainer#transformers.TrainingArguments
    train_conf = SFTConfig(
        output_dir=finetuned_llm_version.working_directory,
        save_safetensors=True,
        gradient_checkpointing=True,
        num_train_epochs=1,
        logging_steps=5,
        eval_strategy="steps" if eval_dataset else "no",
    )

    # LoRA is one of the most popular adapter-based methods to reduce memory-usage
    # and speed up fine-tuning
    peft_conf = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        task_type="CAUSAL_LM",
        target_modules="all-linear",
    )

    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        formatting_func=formatting_func,
        args=train_conf,
        peft_config=peft_conf,
    )
    trainer.train()
    trainer.save_model()

    # Finally, we are logging training information to the Saved Model version
    config = finetuned_llm_version.config
    config["trainingDataset"] = training_dataset.short_name
    if validation_dataset:
        config["validationDataset"] = validation_dataset.short_name
    config["userMessageColumn"] = user_message_column
    config["assistantMessageColumn"] = assistant_message_column
    config["systemMessageColumn"] = system_message_column
    config["staticSystemMessage"] = static_system_message
    config["batchSize"] = trainer.state.train_batch_size
    config["eventLog"] = trainer.state.log_history
