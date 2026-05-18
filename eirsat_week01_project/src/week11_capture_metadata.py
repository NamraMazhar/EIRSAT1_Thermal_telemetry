from pathlib import Path
import json
import platform
import sys

import pandas as pd
import numpy as np
import yaml
import matplotlib
import sklearn


def main():
    root = Path(__file__).resolve().parents[1]

    splits_path = root / "data" / "processed" / "splits.json"
    if splits_path.exists():
        splits = json.loads(splits_path.read_text(encoding="utf-8"))
    else:
        splits = {}

    payload = {
        "python_version": sys.version,
        "platform": platform.platform(),
        "os_name": platform.system(),
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "yaml_version": getattr(yaml, "__version__", "unknown"),
        "matplotlib_version": matplotlib.__version__,
        "sklearn_version": sklearn.__version__,
        "seed": 1337,
        "run_ids": [
            "R001", "R002", "R003",
            "R101", "R102", "R103", "R104", "R105",
            "R201", "R202", "R203", "R204", "R205", "R206", "R207", "R208", "R209",
            "R210", "R211", "R212", "R213", "R214", "R215", "R216", "R217", "R218",
            "RS01", "RS02", "RS03"
        ],
        "split_ranges": splits,
    }

    out = root / "docs" / "repro_metadata.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Week11 metadata capture written to:", out)


if __name__ == "__main__":
    main()