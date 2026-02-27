import json
import pandas as pd
from pathlib import Path
from src.config import PROCESSED_FILE, SPLITS_FILE, RUN_ID


def summarize(df, name):
    lines = []
    lines.append(f"[{name}]")
    lines.append(f"Rows: {len(df)}")
    lines.append(f"Time: {df['timestamp'].min()} -> {df['timestamp'].max()}")
    lines.append(f"Channels: {df['channel'].nunique()}")

    grp = df.groupby("channel")["value"].agg(
        samples="size",
        missing_n=lambda s: s.isna().sum()
    ).reset_index()

    grp["missing_pct"] = grp["missing_n"] / grp["samples"] * 100.0
    grp = grp.sort_values("samples", ascending=False).head(5)

    lines.append("Top 5 channels missingness:")
    for _, r in grp.iterrows():
        lines.append(
            f"  - {r['channel']}: samples={int(r['samples'])}, "
            f"missing={r['missing_pct']:.2f}%"
        )

    lines.append("")
    return "\n".join(lines)


def main():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_parquet(root / PROCESSED_FILE)

    splits = json.loads((root / SPLITS_FILE).read_text(encoding="utf-8"))

    t1 = pd.to_datetime(splits["train"]["end"])
    t2 = pd.to_datetime(splits["val"]["end"])

    train = df[df["timestamp"] < t1]
    val = df[(df["timestamp"] >= t1) & (df["timestamp"] < t2)]
    test = df[df["timestamp"] >= t2]

    report = []
    report.append("=== WEEK 01 SPLIT REPORT ===\n")
    report.append(summarize(train, "TRAIN"))
    report.append(summarize(val, "VAL"))
    report.append(summarize(test, "TEST"))

    run_dir = root / "data" / "runs" / RUN_ID
    out_file = run_dir / "split_report.txt"
    out_file.write_text("\n".join(report), encoding="utf-8")

    print("Split report generated at:", out_file)


if __name__ == "__main__":
    main()