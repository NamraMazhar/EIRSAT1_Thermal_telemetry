from pathlib import Path
import json
import pandas as pd


def main():
    root = Path(__file__).resolve().parents[1]

    checks = []

    # Check final configs exist
    checks.append(("final_config_set", (root / "FINAL" / "configs" / "final_injection_config.yaml").exists()))
    checks.append(("final_eval_config", (root / "FINAL" / "configs" / "final_eval_config.yaml").exists()))

    # Check artifacts exist
    checks.append(("final_telemetry", (root / "FINAL" / "artifacts" / "final_telemetry_inj.csv").exists()))
    checks.append(("final_events", (root / "FINAL" / "artifacts" / "final_events.json").exists()))
    checks.append(("final_results", (root / "FINAL" / "artifacts" / "final_main_results_table.csv").exists()))

    # Check definitions file exists
    checks.append(("final_definitions", (root / "docs" / "final_definitions.md").exists()))

    # Check hashes file exists
    checks.append(("final_hashes", (root / "FINAL" / "artifacts" / "final_hashes.csv").exists()))

    # Check main results has expected columns
    results_path = root / "FINAL" / "artifacts" / "final_main_results_table.csv"
    if results_path.exists():
        df = pd.read_csv(results_path)
        required = {"run_id", "method", "EventF1", "MDD", "FAB"}
        checks.append(("final_results_columns", required.issubset(df.columns)))
    else:
        checks.append(("final_results_columns", False))

    failures = [name for name, ok in checks if not ok]

    out = root / "docs" / "final_qa_summary.txt"
    lines = [f"{name}: {'PASS' if ok else 'FAIL'}" for name, ok in checks]
    if failures:
        lines.append("STATUS=FAIL")
        out.write_text("\n".join(lines), encoding="utf-8")
        print("\n".join(lines))
        raise SystemExit(1)

    lines.append("STATUS=PASS")
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()