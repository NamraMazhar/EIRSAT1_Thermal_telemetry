import numpy as np
import pandas as pd


def fit_periodic_template(train_df: pd.DataFrame, orbit_period_samples: int):
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


def apply_periodic_template(df: pd.DataFrame, template: pd.Series, orbit_period_samples: int):
    df = df.copy().reset_index(drop=True)
    df["sample_idx"] = np.arange(len(df))
    df["phase"] = df["sample_idx"] % orbit_period_samples
    df["periodic_baseline"] = df["phase"].map(template)
    return df


def fit_expected_residual_model(train_df: pd.DataFrame, orbit_period_samples: int, smoothing_window: int):
    train_applied = apply_periodic_template(
        train_df,
        fit_periodic_template(train_df, orbit_period_samples),
        orbit_period_samples
    )
    train_applied["residual_base"] = train_applied["value"] - train_applied["periodic_baseline"]

    expected = (
        train_applied["residual_base"]
        .rolling(window=smoothing_window, min_periods=1, center=True)
        .mean()
    )

    return {
        "template": fit_periodic_template(train_df, orbit_period_samples),
        "expected_residual_mean": expected.mean(),
        "expected_residual_std": expected.std(),
    }


def detect_proposed(df_train_ch, df_eval_ch, orbit_period_samples: int, smoothing_window: int, threshold: float):
    model = fit_expected_residual_model(df_train_ch, orbit_period_samples, smoothing_window)

    eval_df = apply_periodic_template(df_eval_ch, model["template"], orbit_period_samples)
    eval_df["residual"] = eval_df["value"] - eval_df["periodic_baseline"]

    mu = model["expected_residual_mean"]
    sigma = model["expected_residual_std"]

    if pd.isna(sigma) or sigma == 0:
        sigma = 1e-6

    eval_df["z_resid"] = (eval_df["residual"] - mu) / sigma
    eval_df["alarm"] = eval_df["z_resid"].abs() > threshold

    return eval_df