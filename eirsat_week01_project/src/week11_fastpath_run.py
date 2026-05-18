from pathlib import Path
import subprocess
import sys


COMMANDS = [
    ["-m", "src.week10_make_figures"],
    ["-m", "src.week10_make_tables"],
    ["-m", "src.week10_clean_exports"],
    ["-m", "src.week10_dryrun_check"],
]


def main():
    root = Path(__file__).resolve().parents[1]
    summary_lines = []

    for cmd_suffix in COMMANDS:
        cmd = [sys.executable] + cmd_suffix
        summary_lines.append("RUN " + " ".join(cmd))
        subprocess.run(cmd, check=True, cwd=root)

    out = root / "docs" / "fastpath_summary.txt"
    out.write_text("\n".join(summary_lines), encoding="utf-8")

    print("Week11 fast-path run completed.")
    print("Summary written to:", out)


if __name__ == "__main__":
    main()