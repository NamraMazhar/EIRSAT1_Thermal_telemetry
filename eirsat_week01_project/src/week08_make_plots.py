from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def plot_eventf1_vs_magnitude(df, out_path):
    plt.figure(figsize=(10, 5))
    sub = df.groupby(["magnitude", "Method"])["EventF1"].mean().unstack()
    sub = sub.reindex(["small", "medium", "large"])
    sub.plot(marker="o")
    plt.ylabel("EventF1")
    plt.title("EventF1 vs Magnitude")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_mdd_vs_duration(df, out_path):
    plt.figure(figsize=(10, 5))
    sub = df.groupby(["duration", "Method"])["MDD"].mean().unstack()
    sub = sub.reindex(["short", "medium", "long"])
    sub.plot(marker="o")
    plt.ylabel("MDD")
    plt.title("MDD vs Duration")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_fab_vs_threshold(df, out_path):
    plt.figure(figsize=(10, 5))
    for method in df["Method"].unique():
        sub = df[df["Method"] == method]
        plt.scatter(sub["val_threshold"], sub["test_fab"], label=method)
    plt.xlabel("Validation threshold")
    plt.ylabel("Test FAB")
    plt.title("FAB vs Threshold")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def main():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "runs" / "week08_grid_results.csv")
    tune = pd.read_csv(root / "data" / "runs" / "week08_threshold_tuning.csv")

    plot_eventf1_vs_magnitude(df, root / "data" / "runs" / "week08_eventf1_vs_magnitude.png")
    plot_mdd_vs_duration(df, root / "data" / "runs" / "week08_mdd_vs_duration.png")
    plot_fab_vs_threshold(tune, root / "data" / "runs" / "week08_fab_vs_threshold.png")

    print("Week08 sensitivity plots generated.")


if __name__ == "__main__":
    main()