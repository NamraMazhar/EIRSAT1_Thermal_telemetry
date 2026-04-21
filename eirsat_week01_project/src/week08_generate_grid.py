from pathlib import Path
import subprocess
import sys
import pandas as pd


def main():
    root = Path(__file__).resolve().parents[1]
    idx = pd.read_csv(root / "data" / "runs" / "week08_config_index.csv")

    for _, row in idx.iterrows():
        cfg = row["config_file"]
        print(f"Generating {row['run_id']} from {cfg} ...")
        cmd = [sys.executable, "-m", "src.thermal_fault_injector_v2", cfg]
        subprocess.run(cmd, check=True, cwd=root)


if __name__ == "__main__":
    main()