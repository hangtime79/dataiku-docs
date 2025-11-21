import pandas as pd

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from typing import Dict


def get_classif_metrics(df: pd.DataFrame,
                        pred_col: str,
                        truth_col: str) -> Dict[str, float]:
    metrics = {
        "precision": precision_score(y_pred=df[pred_col],
                                     y_true=df[truth_col],
                                     average="macro"),
        "recall": recall_score(y_pred=df[pred_col],
                               y_true=df[truth_col],
                               average="macro")
    }
    return metrics
