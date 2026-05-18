from pathlib import Path
import pandas as pd


def main():
    root = Path(__file__).resolve().parents[1]

    rows = [
        {
            "artifact_type": "figure",
            "path": "docs/paper_fig_tradeoff.png",
            "description": "Week09 trade-off figure"
        },
        {
            "artifact_type": "figure",
            "path": "docs/paper_fig_faulttype_sweep.png",
            "description": "Week07 fault-type sweep"
        },
        {
            "artifact_type": "figure",
            "path": "docs/paper_fig_sensitivity.png",
            "description": "Week08 sensitivity figure"
        },
        {
            "artifact_type": "table",
            "path": "docs/paper_table_main_results.csv",
            "description": "Week09 main results table"
        },
        {
            "artifact_type": "table",
            "path": "docs/paper_table_ablation_summary.csv",
            "description": "Week07 ablation summary"
        },
        {
            "artifact_type": "table",
            "path": "docs/paper_table_robustness_summary.csv",
            "description": "Week09 robustness summary"
        },
        {
            "artifact_type": "data",
            "path": "data/runs/R001/telemetry_inj.csv",
            "description": "Injected telemetry run R001"
        },
        {
            "artifact_type": "data",
            "path": "data/runs/R001/events.json",
            "description": "Event labels run R001"
        },
        {
            "artifact_type": "data",
            "path": "data/runs/week09_main_results_table.csv",
            "description": "Paper-use main results table"
        },
    ]

    df = pd.DataFrame(rows)
    df.to_csv(root / "docs" / "repro_manifest.csv", index=False)
    print("Week10 repro manifest generated.")


if __name__ == "__main__":
    main()