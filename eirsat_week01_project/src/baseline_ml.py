import time
import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor


def build_wide(df: pd.DataFrame, channels):
    """
    Convert long telemetry (timestamp, channel, value) into wide matrix:
    index = timestamp, columns = channels
    """
    temp = df[df["channel"].isin(channels)].copy()
    temp["timestamp"] = pd.to_datetime(temp["timestamp"])

    wide = (
        temp.pivot_table(
            index="timestamp",
            columns="channel",
            values="value",
            aggfunc="mean"
        )
        .sort_index()
    )

    # Ensure exact column order
    wide = wide.reindex(columns=channels)

    return wide


def fit_ml_reconstruction(train_wide: pd.DataFrame, hidden_layers, max_iter, solver, seed):
    """
    Fit an unsupervised reconstruction model using train split only.
    """
    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()

    x_train = imputer.fit_transform(train_wide)
    x_train_scaled = scaler.fit_transform(x_train)

    model = MLPRegressor(
        hidden_layer_sizes=tuple(hidden_layers),
        activation="relu",
        solver=solver,
        random_state=seed,
        max_iter=max_iter,
        shuffle=False
    )

    t0 = time.perf_counter()
    model.fit(x_train_scaled, x_train_scaled)
    train_time_sec = time.perf_counter() - t0

    bundle = {
        "imputer": imputer,
        "scaler": scaler,
        "model": model,
        "train_time_sec": train_time_sec
    }

    return bundle


def reconstruct_scores(bundle, wide_df: pd.DataFrame):
    """
    Reconstruct data and compute absolute reconstruction error scores.
    """
    imputer = bundle["imputer"]
    scaler = bundle["scaler"]
    model = bundle["model"]

    x = imputer.transform(wide_df)
    x_scaled = scaler.transform(x)

    t0 = time.perf_counter()
    pred_scaled = model.predict(x_scaled)
    infer_time_sec = time.perf_counter() - t0

    pred = scaler.inverse_transform(pred_scaled)

    err = np.abs(pred - x)

    score_wide = pd.DataFrame(
        err,
        index=wide_df.index,
        columns=wide_df.columns
    )

    return score_wide, infer_time_sec


def threshold_scores(train_score_wide: pd.DataFrame, eval_score_wide: pd.DataFrame, threshold: float):
    """
    Convert reconstruction scores into per-channel alarm dataframe.
    """
    rows = []

    for ch in eval_score_wide.columns:
        mu = train_score_wide[ch].mean()
        sigma = train_score_wide[ch].std()

        if pd.isna(sigma) or sigma == 0:
            sigma = 1e-6

        z = (eval_score_wide[ch] - mu) / sigma

        temp = pd.DataFrame({
            "timestamp": eval_score_wide.index,
            "channel": ch,
            "score": eval_score_wide[ch].values,
            "zscore": z.values,
            "alarm": (z.values > threshold)
        })

        rows.append(temp)

    out = pd.concat(rows, ignore_index=True)
    out["timestamp"] = pd.to_datetime(out["timestamp"])

    return out.sort_values(["channel", "timestamp"]).reset_index(drop=True)


def choose_threshold_on_validation(train_score_wide, val_score_wide, candidates, target_alarm_rate=0.01):
    """
    Choose threshold on validation only.
    Strategy: pick first threshold with alarm rate <= target value.
    If none satisfy, choose maximum threshold.
    """
    records = []
    chosen = None

    for thr in candidates:
        val_alarm_df = threshold_scores(train_score_wide, val_score_wide, thr)
        alarm_rate = float(val_alarm_df["alarm"].mean())

        records.append({
            "threshold": float(thr),
            "val_alarm_rate": alarm_rate
        })

        if chosen is None and alarm_rate <= target_alarm_rate:
            chosen = float(thr)

    if chosen is None:
        chosen = float(max(candidates))

    return chosen, records