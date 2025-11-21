import warnings
warnings.filterwarnings('ignore')

###
import dataiku
from utils.evaluate import get_classif_metrics

df = dataiku.Dataset("test_zs_scored") \
    .get_dataframe(columns=["sentiment", "llm_sentiment"])
metrics_zs = get_classif_metrics(df, "llm_sentiment", "sentiment")
print(metrics_zs)
###


###
import dataiku
from utils.evaluate import get_classif_metrics

df = dataiku.Dataset("test_fs_scored") \
    .get_dataframe(columns=["sentiment", "llm_sentiment"])
metrics_fs = get_classif_metrics(df, "llm_sentiment", "sentiment")
print(metrics_fs)
###