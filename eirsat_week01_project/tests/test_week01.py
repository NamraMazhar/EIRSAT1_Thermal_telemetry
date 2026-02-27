import json
from pathlib import Path
import pandas as pd
from src.config import NO_SHUFFLE, PROCESSED_FILE, SPLITS_FILE


def test_no_shuffle_guard():
    assert NO_SHUFFLE is True


def test_split_non_overlap():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_parquet(root / PROCESSED_FILE)

    splits = json.loads((root / SPLITS_FILE).read_text(encoding="utf-8"))

    t1 = pd.to_datetime(splits["train"]["end"])
    t2 = pd.to_datetime(splits["val"]["end"])

    train = df[df["timestamp"] < t1]
    val = df[(df["timestamp"] >= t1) & (df["timestamp"] < t2)]
    test = df[df["timestamp"] >= t2]

    assert train["timestamp"].max() < val["timestamp"].min()
    assert val["timestamp"].max() < test["timestamp"].min()