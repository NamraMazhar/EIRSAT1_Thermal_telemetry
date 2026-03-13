import pandas as pd
import numpy as np


def compute_zscore(series):
    mean = series.mean()
    std = series.std()
    return (series - mean) / std


def run_baseline(df_train, df_test, threshold=3.0):

    alarms = []

    for ch in df_test["channel"].unique():

        train_vals = df_train[df_train["channel"] == ch]["value"].dropna()

        mu = train_vals.mean()
        sigma = train_vals.std()

        ch_test = df_test[df_test["channel"] == ch].copy()

        z = (ch_test["value"] - mu) / sigma

        ch_test["alarm"] = (z.abs() > threshold)

        alarms.append(ch_test)

    alarms_df = pd.concat(alarms)

    return alarms_df