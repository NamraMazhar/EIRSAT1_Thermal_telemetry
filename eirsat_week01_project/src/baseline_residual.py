import pandas as pd
import numpy as np
from src.orbit_baseline import fit_orbit_template, apply_orbit_template


def detect_residual_alarms(df_train_ch, df_eval_ch, orbit_period_samples, phase_bins, threshold):
    """
    Fit periodic baseline on train only, then threshold residual on eval.
    """
    template = fit_orbit_template(
        df_train_ch,
        orbit_period_samples=orbit_period_samples,
        phase_bins=phase_bins
    )

    train_applied = apply_orbit_template(df_train_ch, template, orbit_period_samples)
    eval_applied = apply_orbit_template(df_eval_ch, template, orbit_period_samples)

    mu = train_applied["residual"].dropna().mean()
    sigma = train_applied["residual"].dropna().std()

    eval_applied["z_resid"] = (eval_applied["residual"] - mu) / sigma
    eval_applied["alarm"] = eval_applied["z_resid"].abs() > threshold

    return eval_applied, template