from pathlib import Path
import subprocess
import sys
import time


COMMANDS = [
    ["-m", "src.week12_freeze_final_set"],
    ["-m", "src.week12_make_final_artifacts"],
    ["-m", "src.week12_hash_check"],
]


def main():
    root = Path(__file__).resolve().parents[1]
    lines = []
    t0 = time.perf_counter()

    for cmd_suffix in COMMANDS:
        cmd = [sys.executable] + cmd_suffix
        lines.append("RUN " + " ".join(cmd))
        subprocess.run(cmd, check=True, cwd=root)

    elapsed = time.perf_counter() - t0
    lines.append(f"TOTAL_RUNTIME_SEC={elapsed:.4f}")
    lines.append("STATUS=SUCCESS")

    out = root / "docs" / "final_release_candidate_log.txt"
    out.write_text("\n".join(lines), encoding="utf-8")

    print("Week12 release candidate completed.")
    print("Log written to:", out)


if __name__ == "__main__":
    main()