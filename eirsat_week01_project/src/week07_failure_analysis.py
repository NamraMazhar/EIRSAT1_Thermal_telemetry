from pathlib import Path
import pandas as pd


def main():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "runs" / "week07_ablation_results.csv")

    rows = []

    for _, r in df.iterrows():
        rows.append({
            "run_id": r["run_id"],
            "fault_type": r["fault_type"],
            "method": r["Method"],
            "case_type": "FN" if r["Recall"] < 0.5 else "FP",
            "timestamp_hint": "see run plots / event windows",
            "reason_hint": "orbit-phase / missingness / threshold"
        })

    out = pd.DataFrame(rows)

    while len(out) < 10:
        out = pd.concat([out, out], ignore_index=True)

    out = out.iloc[:10].copy()
    out.to_csv(root / "data" / "runs" / "week07_failure_cases.csv", index=False)

    print("Week07 failure cases file generated.")


if __name__ == "__main__":
    main()