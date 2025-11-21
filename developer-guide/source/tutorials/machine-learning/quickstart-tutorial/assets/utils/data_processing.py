"""data_processing.py

This file contains data preparation functions to process the heart measures dataset.
"""

import pandas as pd

def transform_heart_categorical_measures(df, chest_pain_colname, resting_ecg_colname, 
                                         exercise_induced_angina_colname, st_slope_colname, sex_colname):
    """
    Transforms each category from the given categorical columns into int value, using specific replacement rules for each column.
    
    :param pd.DataFrame df: the input dataset
    :param str chest_pain_colname: the name of the column containing information relative to chest pain type
    :param str resting_ecg_colname: the name of the column containing information relative to the resting electrocardiogram results
    :param str exercise_induced_angina_colname: the name of the column containing information relative to exercise-induced angina
    :param str st_slope_colname: the name of the column containing information relative to the slope of the peak exercise ST segment
    :param str sex_colname: the name of the column containing information relative to the patient gender
    
    :returns: the dataset with transform categorical columns
    :rtype: pd.DataFrame
    """
    df[chest_pain_colname].replace({'TA':1, 'ATA':2, 'NAP': 3, 'ASY': 4}, inplace=True)
    df[resting_ecg_colname].replace({'Normal':0, 'ST':1, 'LVH':2}, inplace=True)
    df[exercise_induced_angina_colname].replace({'N':0, 'Y':1}, inplace=True)
    df[st_slope_colname].replace({'Down':0, 'Flat':1, 'Up':2}, inplace=True)
    df[sex_colname].replace({'M': 0, 'F': 1}, inplace=True)
    return df