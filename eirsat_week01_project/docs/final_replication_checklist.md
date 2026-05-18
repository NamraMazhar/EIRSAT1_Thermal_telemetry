\# Final Replication Checklist



\## Step 1 — environment

\- \[ ] Open PowerShell in project root

\- \[ ] Activate `.venv`



\## Step 2 — final set

\- \[ ] Run `python -m src.week12\_freeze\_final\_set`

\- \[ ] Check `FINAL/configs/` contains exactly 3 final config files



\## Step 3 — artifacts

\- \[ ] Run `python -m src.week12\_make\_final\_artifacts`

\- \[ ] Check `FINAL/artifacts/` contains final telemetry, events, results table, and key plots



\## Step 4 — hashes

\- \[ ] Run `python -m src.week12\_hash\_check`

\- \[ ] Check `FINAL/artifacts/final\_hashes.csv` exists



\## Step 5 — release candidate

\- \[ ] Run `python -m src.week12\_release\_candidate`

\- \[ ] Check `docs/final\_release\_candidate\_log.txt` contains `STATUS=SUCCESS`



\## Step 6 — QA

\- \[ ] Run `python -m src.week12\_final\_qa`

\- \[ ] Check `docs/final\_qa\_summary.txt` contains `STATUS=PASS`



\## Step 7 — tests

\- \[ ] Run `pytest -q`

\- \[ ] Confirm all tests pass

