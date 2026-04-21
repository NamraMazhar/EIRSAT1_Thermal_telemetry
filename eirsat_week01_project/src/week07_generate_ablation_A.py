from pathlib import Path
import subprocess
import sys

CONFIGS = [
    "configs/ablation_A_bias.yaml",
    "configs/ablation_A_drift.yaml",
    "configs/ablation_A_lag.yaml",
    "configs/ablation_A_stuck_at.yaml",
    "configs/ablation_A_dropout.yaml",
]

def main():
    root = Path(__file__).resolve().parents[1]

    for cfg in CONFIGS:
        print(f"Generating run from {cfg} ...")
        cmd = [sys.executable, "-m", "src.thermal_fault_injector_v2", cfg]
        subprocess.run(cmd, check=True, cwd=root)

if __name__ == "__main__":
    main()