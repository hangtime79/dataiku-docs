import os

from transformers import pipeline
from dataiku.core.model_provider import get_model_from_cache

model = get_model_from_cache("distilbert/distilbert-base-uncased")

# predict masked output
unmask = pipeline("fill-mask", model=model)
input_sentence = "Lend me your ears and I'll sing you a [MASK]"
resp = unmask(input_sentence)
for r in resp:
    print(f"{r['sequence']} ({r['score']})")