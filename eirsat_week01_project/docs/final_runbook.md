\# Final Runbook



\## Final declared config set

\- `FINAL/configs/final\_injection\_config.yaml`

\- `FINAL/configs/final\_eval\_config.yaml`

\- `FINAL/configs/final\_proposed\_config.yaml`



\## Final headline artifacts

\- `FINAL/artifacts/final\_telemetry\_inj.csv`

\- `FINAL/artifacts/final\_events.json`

\- `FINAL/artifacts/final\_main\_results\_table.csv`

\- `FINAL/artifacts/final\_tradeoff\_plot.png`

\- `FINAL/artifacts/final\_faulttype\_plot.png`

\- `FINAL/artifacts/final\_sensitivity\_plot.png`

\- `FINAL/artifacts/final\_hashes.csv`



\## Release candidate commands

1\. Activate environment:

&#x20;  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

2\. Activate venv:

&#x20;  `.\\.venv\\Scripts\\Activate.ps1`

3\. Freeze final set:

&#x20;  `python -m src.week12\_freeze\_final\_set`

4\. Export final artifacts:

&#x20;  `python -m src.week12\_make\_final\_artifacts`

5\. Generate final hashes:

&#x20;  `python -m src.week12\_hash\_check`

6\. Run release candidate:

&#x20;  `python -m src.week12\_release\_candidate`

7\. Run final QA:

&#x20;  `python -m src.week12\_final\_qa`

8\. Run tests:

&#x20;  `pytest -q`

