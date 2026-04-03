from pathlib import Path
import yaml
import pandas as pd
import matplotlib.pyplot as plt


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    root = Path(__file__).resolve().parents[1]
    cfg = load_yaml(root / "configs" / "week05_ml.yaml")

    run_dir = root / "data" / "runs" / cfg["run_id"]

    train_df = pd.read_csv(run_dir / "ml_scores_train.csv")
    test_df = pd.read_csv(run_dir / "ml_scores_test.csv")

    ch = cfg["score_plot_channel"]

    train_ch = train_df[train_df["channel"] == ch]["score"]
    test_ch = test_df[test_df["channel"] == ch]["score"]

    plt.figure()
    plt.hist(train_ch, bins=50, alpha=0.6, label="train")
    plt.hist(test_ch, bins=50, alpha=0.6, label="test")
    plt.legend()
    plt.title(f"Score distribution: {ch}")
    plt.tight_layout()
    plt.savefig(run_dir / "score_distribution_train_vs_test.png")
    plt.close()

    print("Week05 plot generated.")


if __name__ == "__main__":
    main()