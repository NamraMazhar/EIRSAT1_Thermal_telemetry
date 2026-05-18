from pathlib import Path
import importlib


REQUIRED_MODULES = [
    "pandas",
    "numpy",
    "yaml",
    "matplotlib",
    "sklearn",
]


def main():
    missing = []

    for mod in REQUIRED_MODULES:
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append(mod)

    if missing:
        print("Missing modules:", missing)
        raise SystemExit(1)

    root = Path(__file__).resolve().parents[1]
    needed_files = [
        root / "docs" / "paper_fig_tradeoff.png",
        root / "docs" / "paper_fig_faulttype_sweep.png",
        root / "docs" / "paper_fig_sensitivity.png",
        root / "docs" / "paper_table_main_results.csv",
        root / "docs" / "paper_table_ablation_summary.csv",
        root / "docs" / "paper_table_robustness_summary.csv",
        root / "docs" / "RUNBOOK.md",
        root / "docs" / "repro_manifest.csv",
    ]

    missing_files = [str(p) for p in needed_files if not p.exists()]

    if missing_files:
        print("Missing files:")
        for f in missing_files:
            print(f)
        raise SystemExit(1)

    print("Week10 dry-run check passed.")


if __name__ == "__main__":
    main()