from pathlib import Path
import shutil


def copy_if_exists(src: Path, dst: Path):
    if not src.exists():
        raise FileNotFoundError(f"Missing required artifact: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "FINAL" / "artifacts"
    out.mkdir(parents=True, exist_ok=True)

    # final headline run data
    copy_if_exists(root / "data" / "runs" / "R001" / "telemetry_inj.csv", out / "final_telemetry_inj.csv")
    copy_if_exists(root / "data" / "runs" / "R001" / "events.json", out / "final_events.json")

    # main results
    copy_if_exists(root / "data" / "runs" / "week09_main_results_table.csv", out / "final_main_results_table.csv")

    # key plots
    copy_if_exists(root / "docs" / "paper_fig_tradeoff.png", out / "final_tradeoff_plot.png")
    copy_if_exists(root / "docs" / "paper_fig_faulttype_sweep.png", out / "final_faulttype_plot.png")
    copy_if_exists(root / "docs" / "paper_fig_sensitivity.png", out / "final_sensitivity_plot.png")

    # optional supporting files for declared final runs
    copy_if_exists(root / "data" / "runs" / "R102" / "events.json", out / "support_R102_events.json")
    copy_if_exists(root / "data" / "runs" / "R205" / "events.json", out / "support_R205_events.json")
    copy_if_exists(root / "data" / "runs" / "RS01" / "events.json", out / "support_RS01_events.json")

    print("Week12 final artifacts exported to FINAL/artifacts/")


if __name__ == "__main__":
    main()