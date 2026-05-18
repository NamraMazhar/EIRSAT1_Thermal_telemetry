\# RUNBOOK



\## Environment setup

1\. Open PowerShell

2\. Go to project root:

&#x20;  `cd D:\\EIRSAT1\_Thermal\_telemetry\\eirsat\_week01\_project`

3\. Activate venv:

&#x20;  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

4\. Activate Python environment:

&#x20;  `.\\.venv\\Scripts\\Activate.ps1`



\## Core data pipeline

5\. Ingest dataset:

&#x20;  `python -m src.ingest`

6\. Build inventory:

&#x20;  `python -m src.inventory`

7\. Create splits:

&#x20;  `python -m src.make\_splits`

8\. Generate split report:

&#x20;  `python -m src.split\_report`



\## Injection pipeline

9\. Generate Week06 multi-run configs:

&#x20;  use frozen config files in `configs/`

10\. Generate Week06 runs:

&#x20;   `python -m src.thermal\_fault\_injector\_v2 configs/injection\_v2\_R001.yaml`

&#x20;   `python -m src.thermal\_fault\_injector\_v2 configs/injection\_v2\_R002.yaml`

&#x20;   `python -m src.thermal\_fault\_injector\_v2 configs/injection\_v2\_R003.yaml`



\## Ablation / stress pipelines

11\. Week07 ablation:

&#x20;   `python -m src.week07\_generate\_ablation\_A`

&#x20;   `python -m src.week07\_run\_methods`

12\. Week08 grid:

&#x20;   `python -m src.week08\_generate\_configs`

&#x20;   `python -m src.week08\_generate\_grid`

&#x20;   `python -m src.week08\_run\_grid\_methods`

13\. Week09 robustness:

&#x20;   `python -m src.week09\_generate\_stress\_runs`

&#x20;   `python -m src.week09\_run\_comparison`

&#x20;   `python -m src.week09\_tradeoff\_plots`

&#x20;   `python -m src.week09\_main\_table`



\## Paper artifacts

14\. Generate paper figures:

&#x20;   `python -m src.week10\_make\_figures`

15\. Generate paper tables:

&#x20;   `python -m src.week10\_make\_tables`



\## Validation

16\. Run tests:

&#x20;   `pytest -q`

