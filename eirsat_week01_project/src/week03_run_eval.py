import pandas as pd
import json
from pathlib import Path

from src.baseline_threshold import run_baseline
from src.eval_events import alarms_to_events, compute_metrics


root = Path(__file__).resolve().parents[1]

telemetry = pd.read_csv(root / "data/runs/R001/telemetry_inj.csv")
events_json = json.load(open(root / "data/runs/R001/events.json"))

true_events = pd.DataFrame(events_json["events"])

train = telemetry.iloc[:180000]
test = telemetry.iloc[180000:]

alarms = run_baseline(train, test)

pred_events = alarms_to_events(alarms)

precision, recall, f1, mdd, fp = compute_metrics(pred_events, true_events)

metrics = pd.DataFrame([{
    "Precision": precision,
    "Recall": recall,
    "EventF1": f1,
    "MDD": mdd,
    "FAB": fp
}])

metrics.to_csv(root / "data/runs/R001/metrics_table.csv", index=False)

print(metrics)