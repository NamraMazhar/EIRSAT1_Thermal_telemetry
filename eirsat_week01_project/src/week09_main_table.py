from pathlib import Path
import pandas as pd


def main():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "runs" / "week09_stress_results.csv")

    stress_map = {
        "RS01": "timing_orbit_phase",
        "RS02": "missingness",
        "RS03": "noise",
    }
    df["stress_dimension"] = df["run_id"].map(stress_map)

    df.to_csv(root / "data" / "runs" / "week09_main_results_table.csv", index=False)
    df.to_csv(root / "data" / "runs" / "week09_stress_matrix.csv", index=False)

    print("Week09 main results table generated.")


if __name__ == "__main__":
    main()