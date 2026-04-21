from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "runs" / "week09_stress_results.csv")

    # EventF1 vs FAB
    plt.figure()
    for method in df["method"].unique():
        sub = df[df["method"] == method]
        plt.plot(sub["FAB"], sub["EventF1"], marker="o", label=method)
    plt.xlabel("FAB")
    plt.ylabel("EventF1")
    plt.title("Week09 EventF1 vs FAB")
    plt.legend()
    plt.tight_layout()
    plt.savefig(root / "data" / "runs" / "week09_eventf1_vs_fab.png")
    plt.close()

    # MDD vs FAB
    plt.figure()
    for method in df["method"].unique():
        sub = df[df["method"] == method]
        plt.plot(sub["FAB"], sub["MDD"], marker="o", label=method)
    plt.xlabel("FAB")
    plt.ylabel("MDD")
    plt.title("Week09 MDD vs FAB")
    plt.legend()
    plt.tight_layout()
    plt.savefig(root / "data" / "runs" / "week09_mdd_vs_fab.png")
    plt.close()

    print("Week09 trade-off plots generated.")


if __name__ == "__main__":
    main()