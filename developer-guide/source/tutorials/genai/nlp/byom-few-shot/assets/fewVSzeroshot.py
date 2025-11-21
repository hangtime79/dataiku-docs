import dataiku
import pandas as pd

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
print("Running script ...\n\n\n")
BATCH_SIZE = 8
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"DEVICE: {DEVICE}, processing batches of {BATCH_SIZE}\n\n")
print("Loading model ..\n\n" )

tokenizer = AutoTokenizer.from_pretrained(
    "databricks/dolly-v2-3b",
    padding_side="left"
)
model = AutoModelForCausalLM.from_pretrained(
    "databricks/dolly-v2-3b",
    device_map="auto",
    torch_dtype=torch.bfloat16
).eval()

DATASET_NAME = "beauty_product_reviews"
df = dataiku.Dataset(DATASET_NAME).get_dataframe()

print(df.info())

## Zero-shot
print("\n\nZero-shot \n")

# Build the zero-shot prompt
prompt0 = "Decide whether the following product review's sentiment is positive, neutral, or negative.\n\nProduct review:\n{}\nSentiment:"

target_tokens = ['positive', 'neutral', 'negative']
target_token_ids = [tokenizer.encode(k)[0] for k in target_tokens]

# target_tokens, target_token_ids

results0 = None

for i in range(0, len(df), BATCH_SIZE):
    print(i)
    # Instantiate the prompts
    prompts = [prompt0.format(txt) for txt in df["text"][i:i+BATCH_SIZE]]
    
    # Tokenize the prompts and compute the next token probabilities with the model
    input_ids = tokenizer(prompts, return_tensors="pt", padding=True).input_ids
    with torch.no_grad():
        outputs = model(input_ids.to(DEVICE))
    result = torch.nn.Softmax(dim=-1)(outputs.logits[:, -1, target_token_ids])
    
    if results0 is None:
        results0 = result
    else:
        results0 = torch.cat((results0, result), axis=0)

predicted_token_ids = torch.argmax(results0, axis=1)
predictions0 = [target_tokens[i] for i in predicted_token_ids]

scores0_df = pd.DataFrame(
    results0.float().cpu().numpy(),
    columns=[f"proba_{k}" for k in target_tokens]
)

df_zeroshot = pd.concat([df, pd.Series(predictions0, name='prediction'), scores0_df], axis=1)

## Few-shot
print("\n\nFew-shot \n")

# Build the prompt with examples
prompt = "Decide whether the following product reviews' sentiment is positive, neutral, or negative."
examples = [
    (
        "I love my new chess board!",
        "positive"
    ),
    (
        "Not what I expected but I guess it'll do",
        "neutral"
    ),
    (
        "I'm so disappointed. The product seemed much better on the website",
        "negative"
    )
]
for example in examples:
    prompt += f"\n\nProduct review:\n{example[0]}\nSentiment:\n{example[1]}"
prompt += "\n\nProduct review:\n{}\nSentiment:\n"


results = None

for i in range(0, len(df), BATCH_SIZE):
    print(i)
    # Instantiate the prompts
    prompts = [prompt.format(txt) for txt in df["text"][i:i+BATCH_SIZE]]
    # Tokenize the prompts and compute the next token probabilities with the model
    input_ids = tokenizer(prompts, return_tensors="pt", padding=True).input_ids
    with torch.no_grad():
        outputs = model(input_ids.to(DEVICE))
    result = torch.nn.Softmax(dim=-1)(outputs.logits[:, -1, target_token_ids])
    if results is None:
        results = result
    else:
        results = torch.cat((results, result), axis=0)

predicted_token_ids = torch.argmax(results, axis=1)
predictions = [target_tokens[i] for i in predicted_token_ids]
scores_df = pd.DataFrame(
    results.float().cpu().numpy(),
    columns=[f"proba_{k}" for k in target_tokens]
)

df_fewshot = pd.concat([df, pd.Series(predictions, name='prediction'), scores_df], axis=1)

from sklearn.metrics import accuracy_score
acc_zeroshot = accuracy_score(df_zeroshot["sentiment"], df_zeroshot["prediction"])
acc_fewshot = accuracy_score(df_fewshot["sentiment"], df_fewshot["prediction"])
acc_zeroshot, acc_fewshot
print("Classification completed! And now calculating the results you've been waiting for ..")

import random
print("".join(str(random.randint(0, 9)) for _ in range(50)))
print("".join(str(random.randint(0, 9)) for _ in range(30)))
print("".join(str(random.randint(0, 9)) for _ in range(20)))
print ("ALL DONE\n\n")

from sklearn.metrics import f1_score
f1_zeroshot = f1_score(df_zeroshot["sentiment"], df_zeroshot["prediction"], average="weighted")
f1_fewshot = f1_score(df_fewshot["sentiment"], df_fewshot["prediction"], average="weighted")
print("Zero-shot accuracy:", acc_zeroshot)
print("Few-shot accuracy:", acc_fewshot)
print("Zero-shot F1 score:", f1_zeroshot)
print("Few-shot F1 score:", f1_fewshot)