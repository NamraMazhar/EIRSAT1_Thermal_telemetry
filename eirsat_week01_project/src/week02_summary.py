import json
from pathlib import Path
import pandas as pd


def main():
    root = Path(__file__).resolve().parents[1]
    run_dir = root / "data" / "runs" / "R001"

    events_path = run_dir / "events.json"
    telemetry_path = run_dir / "telemetry_inj.csv"

    payload = json.loads(events_path.read_text(encoding="utf-8"))
    df = pd.read_csv(telemetry_path)

    events = payload["events"]
    events_df = pd.DataFrame(events)

    summary_file = run_dir / "week02_summary.txt"

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("WEEK 02 SUMMARY\n")
        f.write("----------------\n")
        f.write(f"Run ID: {payload['run_id']}\n")
        f.write(f"Seed: {payload['seed']}\n")
        f.write(f"Split Injected: {payload['split_to_inject']}\n")
        f.write(f"Events Generated: {payload['events_generated']}\n")
        f.write(f"Telemetry Rows: {len(df)}\n\n")

        f.write("Fault counts by type:\n")
        counts = events_df["event_type"].value_counts()
        for k, v in counts.items():
            f.write(f"- {k}: {v}\n")

        f.write("\nCounts by duration tier:\n")
        dcounts = events_df["duration_tier"].value_counts()
        for k, v in dcounts.items():
            f.write(f"- {k}: {v}\n")

    print("Summary written to:", summary_file)


if __name__ == "__main__":
    main()