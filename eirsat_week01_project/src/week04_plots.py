from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def main():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "runs" / "R001" / "baseline2_detected_test.csv")

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Plot 1: raw vs residual for representative channel
    ch = "TEMP_CPU"
    ch_df = df[df["channel"] == ch].iloc[:1500].copy()

    plt.figure()
    plt.plot(ch_df["timestamp"], ch_df["value"], label="raw")
    plt.plot(ch_df["timestamp"], ch_df["residual"], label="residual")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(root / "data" / "runs" / "R001" / f"raw_vs_residual_{ch}.png")
    plt.close()

    # Plot 2: false alarm timeline over time blocks
    ch_alarm = df[df["channel"] == ch].copy()
    ch_alarm["time_block"] = (range(len(ch_alarm)))
    ch_alarm["alarm_int"] = ch_alarm["alarm"].astype(int)

    plt.figure()
    plt.plot(ch_alarm["time_block"], ch_alarm["alarm_int"])
    plt.title("False alarm timeline")
    plt.tight_layout()
    plt.savefig(root / "data" / "runs" / "R001" / "false_alarm_timeline.png")
    plt.close()

    print("Plots generated.")


if __name__ == "__main__":
    main()