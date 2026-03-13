import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

root = Path(__file__).resolve().parents[1]

df = pd.read_csv(root / "data/runs/R001/telemetry_inj.csv")

ch = df[df["channel"] == "TEMP_CPU"].iloc[:2000]

plt.plot(ch["timestamp"], ch["value"])
plt.xticks(rotation=45)
plt.title("Alarm timeline example")
plt.tight_layout()

plt.savefig(root / "data/runs/R001/alarm_timeline.png")