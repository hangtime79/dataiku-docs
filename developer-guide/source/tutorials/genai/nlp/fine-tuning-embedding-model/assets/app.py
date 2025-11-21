import dataiku
import os
import tempfile

from datasets import Dataset, concatenate_datasets

from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import InformationRetrievalEvaluator
from sentence_transformers.losses import MultipleNegativesRankingLoss
from sentence_transformers import SentenceTransformerTrainingArguments, SentenceTransformerTrainer
from sentence_transformers.training_args import BatchSamplers


# Load the Dataiku datasets as Pandas dataframes
sci_qa_train_df = dataiku.Dataset("sci_q_and_a_train").get_dataframe()
sci_qa_test_df = dataiku.Dataset("sci_q_and_a_test").get_dataframe()

# And then from Pandas dataframes to Datasets (to be used by the trainer)
sci_qa_train = Dataset.from_pandas(sci_qa_train_df)
sci_qa_test = Dataset.from_pandas(sci_qa_test_df)

model_id = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_id)

sci_qa_corpus = concatenate_datasets([sci_qa_train, sci_qa_test])
# Convert the datasets to dictionaries
corpus = dict(
    zip(sci_qa_corpus["_id"], sci_qa_corpus["positive"])
)  # Our corpus (cid => document)
queries = dict(
    zip(sci_qa_test["_id"], sci_qa_test["anchor"])
)  # Our queries (qid => question)

# Create a mapping of relevant document for each query
relevant_docs = {}  # Query ID to relevant documents (qid => set([relevant_cids])
for q_id in queries:
    relevant_docs[q_id] = [q_id] # The only revelant document, 
                                 # in our case, has the same id as the query

# Given queries, a corpus and a mapping with relevant documents,
# the InformationRetrievalEvaluator computes different IR metrics.
ir_evaluator = InformationRetrievalEvaluator(
    queries=queries,
    corpus=corpus,
    relevant_docs=relevant_docs,
)
results = ir_evaluator(model)
# print(f"cosine_ndcg@10: {results['cosine_ndcg@10']}")
#   --> this gave use a baseline of ~0.67

training_loss = MultipleNegativesRankingLoss(model)

# Managed folder to store the fine-tuned model
folder = dataiku.Folder("a_valid_managed_folder_id")

with tempfile.TemporaryDirectory() as temp_dir:
    
    # Define training arguments
    args = SentenceTransformerTrainingArguments(
        # Required parameter:
        output_dir=temp_dir,
        
        # Optional training parameters:
        num_train_epochs=2,                        # number of epochs
        per_device_train_batch_size=8,             # train batch size
        gradient_accumulation_steps=8,             # for a global batch size of 64 (= 8 * 8)
        per_device_eval_batch_size=8,              # evaluation batch size
        learning_rate=2e-5,                        # learning rate
        warmup_ratio=0.1,                          # warmup ratio
        fp16=True,                                 # use fp16 precision (set to False if your GPU can't run on FP16)
        bf16=False,                                # use bf16 precision (set to True if your GPU can run on BF16)
        batch_sampler=BatchSamplers.NO_DUPLICATES, # losses that use "in-batch negatives" benefit from no duplicates
        
        # Optional tracking/debugging parameters:
        eval_strategy="epoch",                     # evaluate after each epoch
        save_strategy="no",                        # save after each epoch
        save_total_limit=2,                        # save the last 2 models
        save_only_model=True,                      # for each checkpoints, save only the model (no optimizer.pt/scheduler.pt) 
        logging_steps=100,                         # log every 100 steps
    )
    
    # Create a trainer & train. 
    embedding_trainer = SentenceTransformerTrainer(
        model=model,
        args=args,
        train_dataset=sci_qa_train.select_columns(
            ["anchor", "positive"]
        ),  # training dataset,
        loss=training_loss,
        evaluator=ir_evaluator,
    )
    embedding_trainer.train()
    
    # Save the fine-tuned model in the managed folder
    embedding_trainer.save_model(output_dir=temp_dir)
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            source_path = os.path.join(root, file)
            target_path = os.path.relpath(source_path, temp_dir)
            folder.upload_file(target_path, source_path)

results_ft = ir_evaluator(embedding_trainer.model)
# print(f"cosine_ndcg@10: {results['cosine_ndcg@10']}") 
#   --> this gave use a baseline of ~0.77, which represents a 15% performance increase !