from bike_sharing.prepare import with_temp_fahrenheit
from bike_sharing.prepare import with_datetime
import datetime

import pandas as pd
import pytest

dummy_df = pd.DataFrame({
        "instant": "1",
        "dteday": "2023-01-01",
        "season": "1",
        "yr": "0",
        "mnth": "1",
        "hr": "13",
        "holiday": "0",
        "weekday": "1",
        "workingday": "0",
        "weathersit": "1",
        "temp": "1.0",
        "atemp": "0.5",
        "hum": "0.8",
        "windspeed": "0",
        "casual": "3",
        "registered": "10",
        "cnt": "13"
    }, index=[0])

def test_with_temp_fahrenheit():
    out = dummy_df.pipe(with_temp_fahrenheit,
                        temp_col="temp")
    assert out["temp_F"][0] == pytest.approx(102.2)

def test_with_datetime():
    out = dummy_df.pipe(with_datetime, date_col="dteday", hour_col="hr")
    expected_dt = datetime.datetime(2023, 1, 1, 13, 0)
    out_dt = datetime.datetime.fromisoformat(out["datetime"][0])
    assert out_dt == expected_dt
