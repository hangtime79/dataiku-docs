import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier


def split_and_train_pipeline(df: pd.DataFrame, test_size: float):
    """
    Return a tuple made of:
    - evaluation data in a df
    - sklearn estimator
    """

    # Split
    num_features = ["age", "balance", "duration", "previous", "campaign"]
    cat_features = [
        "job",
        "marital",
        "education",
        "default",
        "housing",
        "loan",
        "contact",
        "poutcome",
    ]
    target = "y"
    cols = num_features + cat_features
    cols.append(target)

    df_train, df_test = train_test_split(
        df[cols], test_size=test_size, random_state=42, shuffle=True
    )
    X_train = df_train.drop(target, axis=1)
    y_train = df_train[target]

    num_pipeline = Pipeline(
        [
            ("imp", SimpleImputer(strategy="median")),
            ("sts", StandardScaler()),
        ]
    )
    transformers = [
        ("num", num_pipeline, num_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
    ]
    preprocessor = ColumnTransformer(transformers, remainder="drop")

    clf = RandomForestClassifier(
        n_estimators=40, n_jobs=-1, max_depth=6, min_samples_leaf=20
    )
    pipeline = make_pipeline(preprocessor, clf)
    pipeline.fit(X_train, y_train)

    return pipeline, df_test