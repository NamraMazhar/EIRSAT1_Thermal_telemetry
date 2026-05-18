from pathlib import Path
import pandas as pd


def main():
    root = Path(__file__).resolve().parents[1]
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)

    # Table 1: main results
    main_df = pd.read_csv(root / "data" / "runs" / "week09_main_results_table.csv")
    main_df.to_csv(docs / "paper_table_main_results.csv", index=False)

    # Table 2: ablation summary (week07)
    ab_df = pd.read_csv(root / "data" / "runs" / "week07_ablation_results.csv")
    ab_summary = (
        ab_df.groupby(["fault_type", "Method"])[["EventF1", "MDD", "FAB"]]
        .mean()
        .reset_index()
    )
    ab_summary.to_csv(docs / "paper_table_ablation_summary.csv", index=False)

    # Table 3: robustness summary (week09)
    rb_df = pd.read_csv(root / "data" / "runs" / "week09_main_results_table.csv")
    robustness = (
        rb_df.groupby(["stress_dimension", "method"])[["EventF1", "MDD", "FAB"]]
        .mean()
        .reset_index()
    )
    robustness.to_csv(docs / "paper_table_robustness_summary.csv", index=False)

    print("Week10 paper tables generated.")


if __name__ == "__main__":
    main()