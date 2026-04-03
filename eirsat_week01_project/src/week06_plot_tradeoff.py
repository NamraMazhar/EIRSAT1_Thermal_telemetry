from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "runs" / "week06_consolidated_results.csv")

    plt.figure()

    for method in df["Method"].unique():
        sub = df[df["Method"] == method]
        plt.scatter(sub["FAB"], sub["EventF1"], label=method)

        for _, row in sub.iterrows():
            plt.annotate(row["run_id"], (row["FAB"], row["EventF1"]))

    plt.xlabel("FAB")
    plt.ylabel("EventF1")
    plt.title("Week06 trade-off: FAB vs EventF1")
    plt.legend()
    plt.tight_layout()
    plt.savefig(root / "data" / "runs" / "week06_tradeoff_plot.png")
    plt.close()

    print("Week06 trade-off plot generated.")


if __name__ == "__main__":
    main()