import json
from pathlib import Path


def test_events_count_matches():
    root = Path(__file__).resolve().parents[1]
    events_path = root / "data" / "runs" / "R001" / "events.json"

    payload = json.loads(events_path.read_text(encoding="utf-8"))
    assert payload["events_generated"] == len(payload["events"])


def test_all_events_have_required_fields():
    root = Path(__file__).resolve().parents[1]
    events_path = root / "data" / "runs" / "R001" / "events.json"

    payload = json.loads(events_path.read_text(encoding="utf-8"))
    required = {
        "event_id", "channel", "start_time", "end_time",
        "event_type", "magnitude", "duration_samples", "split"
    }

    for ev in payload["events"]:
        assert required.issubset(ev.keys())