import pandas as pd
from datetime import datetime

# Useful to de-normalize tenperature.
# Check https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset for more details
TEMP_MIN_C = -8.0
TEMP_MAX_C = 39.0

def with_temp_fahrenheit(df: pd.DataFrame, temp_col: str) -> pd.DataFrame:
    """
    Denormalize temperature then convert it to Fahrenheit degrees.

    Args:
        df (pd.DataFrame): Input pandas DataFrame to chain on.
        temp_col (str): DataFrame column name for normalized temperature.
    
    Returns:
        A pandas DataFrame with a new column called "temp_F" containing
        de-normalized temperature in Fahrenheit degrees.
    """
    df["temp_F"] = 1.8 * (TEMP_MIN_C+df[temp_col].astype(float) * (TEMP_MAX_C-TEMP_MIN_C)) + 32.0
    return df

def with_datetime(df: pd.DataFrame,
                  date_col: str,
                  hour_col: str) -> str:
    """
    Create a proper datetime column.

    Args:
        df (pd.DataFrame): Input pandas DataFrame to chain on.
        date_col (str) : column name in df containing date value (e.g. 2023-04-29)
        hour_col (str): column name in df containing hour value (e.g. 21)
    
    Returns:
        A pandas DataFrame with a new column called "datetime" containing
        date + hour information in ISO8601 format.
    """

    df["datetime"] = (df[date_col] + ' ' + df[hour_col].astype(str)) \
        .apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H")) \
        .apply(datetime.isoformat)
    return df

