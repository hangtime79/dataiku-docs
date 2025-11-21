import os
from sentence_transformers import SentenceTransformer

# Load pre-trained model
sentence_transformer_home = os.getenv('SENTENCE_TRANSFORMERS_HOME')
model_path = os.path.join(sentence_transformer_home, 'DataikuNLP_average_word_embeddings_glove.6B.300d')
model = SentenceTransformer(model_path)

sentences = ["I really like Ice cream", "Brussels sprouts are okay too"]

# get sentences embeddings
embeddings = model.encode(sentences)
embeddings.shape