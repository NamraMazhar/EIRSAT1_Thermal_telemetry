from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def make_tradeoff_figure(root: Path):
    df = pd.read_csv(root / "data" / "runs" / "week09_main_results_table.csv")

    plt.figure(figsize=(8, 5))
    for method in df["method"].unique():
        sub = df[df["method"] == method]
        plt.scatter(sub["FAB"], sub["EventF1"], label=method)
        for _, row in sub.iterrows():
            plt.annotate(row["run_id"], (row["FAB"], row["EventF1"]), fontsize=8)

    plt.xlabel("False Alarm Burden (FAB)")
    plt.ylabel("EventF1")
    plt.title("Trade-off: EventF1 vs FAB")
    plt.legend()
    plt.tight_layout()
    plt.savefig(root / "docs" / "paper_fig_tradeoff.png")
    plt.close()


def make_faulttype_figure(root: Path):
    df = pd.read_csv(root / "data" / "runs" / "week07_ablation_results.csv")

    pivot = df.pivot(index="fault_type", columns="Method", values="EventF1")

    plt.figure(figsize=(9, 5))
    pivot.plot(kind="bar")
    plt.ylabel("EventF1")
    plt.title("Fault-Type Sweep: EventF1 by Method")
    plt.tight_layout()
    plt.savefig(root / "docs" / "paper_fig_faulttype_sweep.png")
    plt.close()


def make_sensitivity_figure(root: Path):
    df = pd.read_csv(root / "data" / "runs" / "week08_grid_results.csv")

    sub = df.groupby(["magnitude", "Method"])["EventF1"].mean().unstack()
    sub = sub.reindex(["small", "medium", "large"])

    plt.figure(figsize=(8, 5))
    sub.plot(marker="o")
    plt.ylabel("Mean EventF1")
    plt.title("Sensitivity Sweep: EventF1 vs Magnitude")
    plt.tight_layout()
    plt.savefig(root / "docs" / "paper_fig_sensitivity.png")
    plt.close()


def main():
    root = Path(__file__).resolve().parents[1]
    (root / "docs").mkdir(parents=True, exist_ok=True)

    make_tradeoff_figure(root)
    make_faulttype_figure(root)
    make_sensitivity_figure(root)

    print("Week10 paper figures generated.")


if __name__ == "__main__":
    main()