from pathlib import Path
import pandas as pd

RUNS = {
    "R101": "configs/ablation_A_bias.yaml",
    "R102": "configs/ablation_A_drift.yaml",
    "R103": "configs/ablation_A_lag.yaml",
    "R104": "configs/ablation_A_stuck_at.yaml",
    "R105": "configs/ablation_A_dropout.yaml",
}


def main():
    root = Path(__file__).resolve().parents[1]

    rows = []
    for run_id, cfg in RUNS.items():
        rows.append({
            "run_id": run_id,
            "config_file": cfg,
            "telemetry_file": f"data/runs/{run_id}/telemetry_inj.csv",
            "events_file": f"data/runs/{run_id}/events.json"
        })

    df = pd.DataFrame(rows)
    df.to_csv(root / "data" / "runs" / "week07_results_index.csv", index=False)
    print("Week07 results index created.")


if __name__ == "__main__":
    main()