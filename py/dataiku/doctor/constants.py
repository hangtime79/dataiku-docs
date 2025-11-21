def register_string_constant(s):
    globals()[s.upper()] = s

# Preprocessing states
STATE_LOADING_SRC = "Loading source dataset"
STATE_DEDUPLICATING = "Deduplicating"

ALL_PREPROCESSING_STATES = [
    STATE_LOADING_SRC,
    STATE_DEDUPLICATING,
]



STATE_FITTING = "Fitting model"
STATE_SAVING = "Saving model"
STATE_SCORING = "Scoring model"

ALL_PREDICTION_TRAIN_STATES = [
    STATE_FITTING,
    STATE_SAVING,
    STATE_SCORING
]

ALL_CLUSTERING_TRAIN_STATES = [
    STATE_FITTING,
    STATE_SAVING,
    STATE_SCORING
]

CLUSTER_OUTLIERS = 'cluster_outliers'

STRING_CONSTANTS = [
    "CATEGORY",
    "NUMERIC",
    "TEXT",
    "FLAG",
    "IMPUTE",
    "DROP_ROW",
    "DUMMIFY",
    "IMPACT",
    "TERM_HASH",
    "category_handling",
    "text_handling",
    "target_variable",
    "prediction_type",
    "category_possible_values",
    "category_need_others",
    "rescaling",
    "rescaling_method",
    "term_hash_size",
    "minmax",
    "avgstd",
    "multiclass",
    "regression",
    "classification",
    "missing_handling",
    "per_feature",
    "stats",
]

map(register_string_constant, STRING_CONSTANTS)
