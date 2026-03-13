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