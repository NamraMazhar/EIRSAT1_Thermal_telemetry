from pathlib import Path
import pandas as pd


def main():
    root = Path(__file__).resolve().parents[1]

    artifacts = [
        ("config", "configs/injection_v2_R001.yaml"),
        ("config", "configs/injection_v2_R002.yaml"),
        ("config", "configs/injection_v2_R003.yaml"),
        ("config", "configs/eval_config.yaml"),
        ("figure", "docs/paper_fig_tradeoff.png"),
        ("figure", "docs/paper_fig_faulttype_sweep.png"),
        ("figure", "docs/paper_fig_sensitivity.png"),
        ("table", "docs/paper_table_main_results.csv"),
        ("table", "docs/paper_table_ablation_summary.csv"),
        ("table", "docs/paper_table_robustness_summary.csv"),
        ("doc", "docs/RUNBOOK.md"),
        ("doc", "docs/repro_manifest.csv"),
        ("doc", "docs/repro_metadata.json"),
        ("doc", "docs/final_definitions.md"),
        ("data", "data/runs/week09_main_results_table.csv"),
    ]

    rows = []
    for art_type, rel_path in artifacts:
        p = root / rel_path
        rows.append({
            "artifact_type": art_type,
            "path": rel_path,
            "exists": p.exists(),
        })

    df = pd.DataFrame(rows)
    out = root / "docs" / "repro_audit.csv"
    df.to_csv(out, index=False)

    print("Week11 repro audit written to:", out)


if __name__ == "__main__":
    main()