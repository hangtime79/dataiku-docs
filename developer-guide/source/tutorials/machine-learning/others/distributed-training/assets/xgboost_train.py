# Inspired by from:
#    https://github.com/ray-project/ray/blob/master/release/train_tests/xgboost_lightgbm/train_batch_inference_benchmark.py

import json
import numpy as np
import os
import pandas as pd
import time
from typing import Dict

import xgboost as xgb
from pyarrow import fs

import ray
from ray import data
from ray.train.xgboost.v2 import XGBoostTrainer # https://github.com/ray-project/ray/blob/master/python/ray/train/xgboost/v2.py#L13
from ray.train.xgboost import RayTrainReportCallback as XGBoostReportCallback
from ray.train import RunConfig, ScalingConfig


def xgboost_train_loop_function(config: Dict):
    # 1. Get the dataset shard for the worker and convert to a `xgboost.DMatrix`
    train_ds_iter = ray.train.get_dataset_shard("train")
    train_df = train_ds_iter.materialize().to_pandas()

    label_column, params = config["label_column"], config["params"]
    train_X, train_y = train_df.drop(label_column, axis=1), train_df[label_column]

    dtrain = xgb.DMatrix(train_X, label=train_y)

    # 2. Do distributed data-parallel training.
    # Ray Train sets up the necessary coordinator processes and
    # environment variables for your workers to communicate with each other.
    report_callback = config["report_callback_cls"]
    xgb.train(
        params,
        dtrain=dtrain,
        num_boost_round=10,
        callbacks=[report_callback()],
    )


def train_xgboost(data_path: str,
                  data_filesystem,
                  data_label: str,
                  storage_path: str,
                  storage_filesystem,
                  num_workers: int,
                  cpus_per_worker: int,
                  run_name: str) -> ray.train.Result:
    
    print(storage_path)
    ds = data.read_parquet(data_path, filesystem=data_filesystem)

    train_loop_config= {
        "params": {
            "objective": "binary:logistic",
            "eval_metric": ["logloss", "error"]
        },
        "label_column": data_label,
        "report_callback_cls": XGBoostReportCallback
    }
    
    trainer = XGBoostTrainer(
        train_loop_per_worker=xgboost_train_loop_function,
        train_loop_config=train_loop_config,
        scaling_config=ScalingConfig( # https://docs.ray.io/en/latest/train/api/doc/ray.train.ScalingConfig.html
            num_workers=num_workers,
            resources_per_worker={"CPU": cpus_per_worker},
        ),
        datasets={"train": ds},
        run_config=RunConfig( # https://docs.ray.io/en/latest/train/api/doc/ray.train.RunConfig.html
            storage_path=storage_path, 
            storage_filesystem=storage_filesystem,
            name=run_name
        ),
    )
    result = trainer.fit()
    return result


def main(args):
    # Build pyarrow filesystems with s3 credentials
    #  https://arrow.apache.org/docs/python/generated/pyarrow.fs.S3FileSystem.html#pyarrow.fs.S3FileSystem
    s3_ds = fs.S3FileSystem(
        access_key=args.data_s3_access_key,
        secret_key=args.data_s3_secret_key,
        session_token=args.data_s3_session_token
    )
    
    s3_mf = fs.S3FileSystem(
        access_key=args.storage_s3_access_key,
        secret_key=args.storage_s3_secret_key,
        session_token=args.storage_s3_session_token
    )
    
    print(f"Running xgboost training benchmark...")
    training_start = time.perf_counter()
    result = train_xgboost(
        args.data_s3_path, 
        s3_ds,
        args.data_label_column,
        args.storage_s3_path,
        s3_mf,
        args.num_workers, 
        args.cpus_per_worker, 
        args.run_name
    )
    training_time = time.perf_counter() - training_start

    print("Training result:\n", result)
    print("Training time:", training_time)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    
    # Train dataset arguments
    parser.add_argument("--data-s3-path", type=str)
    parser.add_argument("--data-s3-access-key", type=str)
    parser.add_argument("--data-s3-secret-key", type=str)
    parser.add_argument("--data-s3-session-token", type=str)
    parser.add_argument("--data-label-column", type=str)
    
    # storage folder arguments
    parser.add_argument("--storage-s3-path", type=str)
    parser.add_argument("--storage-s3-access-key", type=str)
    parser.add_argument("--storage-s3-secret-key", type=str)
    parser.add_argument("--storage-s3-session-token", type=str)
    
    # compute arguments
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--cpus-per-worker", type=int, default=1)
    parser.add_argument("--run-name", type=str, default="xgboost-train")
    
    args = parser.parse_args()

    main(args)