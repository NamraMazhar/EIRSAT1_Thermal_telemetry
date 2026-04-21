from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def barplot(df, metric, out_name):
    plt.figure(figsize=(10, 5))
    pivot = df.pivot(index="fault_type", columns="Method", values=metric)
    pivot.plot(kind="bar")
    plt.ylabel(metric)
    plt.tight_layout()
    plt.savefig(out_name)
    plt.close()


def main():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "runs" / "week07_ablation_results.csv")

    barplot(df, "EventF1", root / "data" / "runs" / "week07_faulttype_eventf1.png")
    barplot(df, "MDD", root / "data" / "runs" / "week07_faulttype_mdd.png")
    barplot(df, "FAB", root / "data" / "runs" / "week07_faulttype_fab.png")

    print("Week07 summary plots generated.")


if __name__ == "__main__":
    main()