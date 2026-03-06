import numpy as np
import pandas as pd


def apply_bias(series: pd.Series, magnitude: float) -> pd.Series:
    return series + magnitude


def apply_drift(series: pd.Series, magnitude: float) -> pd.Series:
    n = len(series)
    drift = np.linspace(0, magnitude, n)
    return series + drift


def apply_lag(series: pd.Series, alpha: float = 0.2) -> pd.Series:
    # simple slow response / low-pass effect
    out = series.copy().astype(float)
    for i in range(1, len(out)):
        if pd.notna(out.iloc[i]) and pd.notna(out.iloc[i - 1]):
            out.iloc[i] = alpha * out.iloc[i] + (1 - alpha) * out.iloc[i - 1]
    return out


def apply_stuck_at(series: pd.Series, stuck_value: float = None) -> pd.Series:
    if len(series) == 0:
        return series
    if stuck_value is None:
        stuck_value = series.iloc[0]
    return pd.Series([stuck_value] * len(series), index=series.index)


def apply_dropout(series: pd.Series) -> pd.Series:
    out = series.copy()
    out[:] = np.nan
    return out


def apply_noise_increase(series: pd.Series, std: float = 1.0, seed: int = 0) -> pd.Series:
    rng = np.random.default_rng(seed)
    noise = rng.normal(0, std, len(series))
    return series + noise