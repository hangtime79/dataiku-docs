import os

from transformers import pipeline
from transformers import DistilBertTokenizer, DistilBertForMaskedLM


# Define which pre-trained model to use
model = {"name": "distilbert-base-uncased",
         "revision": "1c4513b2eedbda136f57676a34eea67aba266e5c"}

# Load pre-trained model
hf_home_dir = os.getenv("HF_HOME")
model_path = os.path.join(hf_home_dir,
                          f"transformers/models--{model['name']}/snapshots/{model['revision']}")
unmasker = DistilBertForMaskedLM.from_pretrained(model_path, local_files_only=True)
tokenizer = DistilBertTokenizer.from_pretrained(model_path, local_files_only=True)

# predict masked output
unmask = pipeline("fill-mask", model=unmasker, tokenizer=tokenizer)
input_sentence = "Lend me your ears and I'll sing you a [MASK]"
resp = unmask(input_sentence)
for r in resp:
    print(f"{r['sequence']} ({r['score']})")