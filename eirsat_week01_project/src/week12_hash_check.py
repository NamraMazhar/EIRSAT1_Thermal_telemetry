from pathlib import Path
import hashlib
import pandas as pd


FILES_TO_HASH = [
    "FINAL/configs/final_injection_config.yaml",
    "FINAL/configs/final_eval_config.yaml",
    "FINAL/configs/final_proposed_config.yaml",
    "FINAL/artifacts/final_telemetry_inj.csv",
    "FINAL/artifacts/final_events.json",
    "FINAL/artifacts/final_main_results_table.csv",
    "FINAL/artifacts/final_tradeoff_plot.png",
    "FINAL/artifacts/final_faulttype_plot.png",
    "FINAL/artifacts/final_sensitivity_plot.png",
]


def sha256_of_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    rows = []

    for rel in FILES_TO_HASH:
        p = root / rel
        if not p.exists():
            raise FileNotFoundError(f"Missing final file: {rel}")
        rows.append({
            "path": rel,
            "sha256": sha256_of_file(p),
        })

    df = pd.DataFrame(rows)
    out = root / "FINAL" / "artifacts" / "final_hashes.csv"
    df.to_csv(out, index=False)

    print("Week12 final hashes written to:", out)


if __name__ == "__main__":
    main()