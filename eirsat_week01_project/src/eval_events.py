import pandas as pd
import numpy as np


# -------------------------------------------------------
# Convert point alarms into event windows
# -------------------------------------------------------

def alarms_to_events(df):

    events = []

    for ch in df["channel"].unique():

        ch_df = df[df["channel"] == ch].sort_values("timestamp")

        active = False
        start = None

        for _, row in ch_df.iterrows():

            if row["alarm"] and not active:
                start = row["timestamp"]
                active = True

            elif not row["alarm"] and active:
                end = row["timestamp"]

                events.append({
                    "channel": ch,
                    "start": start,
                    "end": end
                })

                active = False

        # close event if still active at end
        if active:
            end = ch_df.iloc[-1]["timestamp"]
            events.append({
                "channel": ch,
                "start": start,
                "end": end
            })

    return pd.DataFrame(events, columns=["channel", "start", "end"])


# -------------------------------------------------------
# Compute detection metrics
# -------------------------------------------------------

def compute_metrics(pred_events, true_events):

    # Handle events.json naming
    if "start_time" in true_events.columns:
        true_events = true_events.rename(
            columns={"start_time": "start", "end_time": "end"}
        )

    # Ensure datetime format
    true_events["start"] = pd.to_datetime(true_events["start"])
    true_events["end"] = pd.to_datetime(true_events["end"])

    if len(pred_events) > 0:
        pred_events["start"] = pd.to_datetime(pred_events["start"])
        pred_events["end"] = pd.to_datetime(pred_events["end"])

    TP = 0
    FN = 0
    delays = []

    for _, gt in true_events.iterrows():

        match = pred_events[
            (pred_events["channel"] == gt["channel"]) &
            (pred_events["end"] >= gt["start"]) &
            (pred_events["start"] <= gt["end"])
        ]

        if len(match) > 0:

            TP += 1

            det_time = match.iloc[0]["start"]
            delay = (det_time - gt["start"]).total_seconds()
            delays.append(delay)

        else:
            FN += 1

    FP = max(len(pred_events) - TP, 0)

    precision = TP / (TP + FP + 1e-6)
    recall = TP / (TP + FN + 1e-6)

    f1 = 2 * precision * recall / (precision + recall + 1e-6)

    mdd = np.mean(delays) if len(delays) > 0 else None

    return precision, recall, f1, mdd, FP

def alarms_to_events_minlen(df, min_len=1):
    events = alarms_to_events(df)

    if len(events) == 0:
        return events

    events = events.copy()
    events["start"] = pd.to_datetime(events["start"])
    events["end"] = pd.to_datetime(events["end"])

    durations = (events["end"] - events["start"]).dt.total_seconds()

    # assuming 60-second cadence; min_len=3 means >= 2 intervals = 120 sec
    min_seconds = max(0, (min_len - 1) * 60)

    events = events[durations >= min_seconds].copy()
    return events.reset_index(drop=True)

def smooth_alarm_series(df, window=5):
    """
    Apply per-channel median-like smoothing to boolean alarms.
    Uses rolling mean > 0.5 as a simple denoising step.
    """
    df = df.copy()
    out_frames = []

    for ch in df["channel"].unique():
        ch_df = df[df["channel"] == ch].sort_values("timestamp").copy()
        alarm_num = ch_df["alarm"].astype(int)
        smooth = alarm_num.rolling(window=window, min_periods=1, center=True).mean()
        ch_df["alarm"] = smooth > 0.5
        out_frames.append(ch_df)

    out = pd.concat(out_frames, ignore_index=True)
    return out.sort_values(["channel", "timestamp"]).reset_index(drop=True)