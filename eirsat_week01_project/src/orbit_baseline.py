import pandas as pd
import numpy as np


def fit_orbit_template(train_df: pd.DataFrame, orbit_period_samples: int, phase_bins: int):
    """
    Fit periodic baseline using training split only.
    """
    train_df = train_df.copy().reset_index(drop=True)
    train_df["sample_idx"] = np.arange(len(train_df))
    train_df["phase"] = train_df["sample_idx"] % orbit_period_samples

    template = (
        train_df.groupby("phase")["value"]
        .mean()
        .reindex(range(orbit_period_samples))
    )

    template = template.interpolate().bfill().ffill()

    return template


def apply_orbit_template(df: pd.DataFrame, template: pd.Series, orbit_period_samples: int):
    df = df.copy().reset_index(drop=True)
    df["sample_idx"] = np.arange(len(df))
    df["phase"] = df["sample_idx"] % orbit_period_samples
    df["periodic_baseline"] = df["phase"].map(template)
    df["residual"] = df["value"] - df["periodic_baseline"]
    return df