# EIRSAT-1 Thermal Telemetry — Week 01 Pipeline

## Project Summary
This repository contains the Week 01 (SSOT + time integrity + leakage-safe chronological splits) and Week 02 (fault injection harness) implementation for EIRSAT-1 thermal telemetry coursework.

Week 01 outputs:
- Canonical SSOT dataset (processed)
- Thermal channel inventory (sampling interval, missingness, monotonicity)
- Strict chronological train/val/test split generator (no shuffle) + leakage guards
- Split report + unit tests
- Initial event schema placeholder (schema_v0_1)

## ---

# Week 02 — Thermal Fault Injection Harness

## Goal
Implement a deterministic thermal fault injection system that produces injected telemetry and event labels without data leakage across dataset splits.

## Implemented Components

### Injection Configuration
Configuration file:

Defines:
- run_id
- global seed
- fault types enabled
- magnitude tiers
- duration tiers
- minimum event separation
- allowed telemetry channels

### Fault Operators Implemented

The injector supports the following fault types:

- Bias
- Drift
- Lag / slow response
- Stuck-at
- Dropout
- Noise increase (robustness testing)

Implemented in:

Defines:
- run_id
- global seed
- fault types enabled
- magnitude tiers
- duration tiers
- minimum event separation
- allowed telemetry channels

### Fault Operators Implemented

The injector supports the following fault types:

- Bias
- Drift
- Lag / slow response
- Stuck-at
- Dropout
- Noise increase (robustness testing)

Implemented in:
src/fault_ops.py

### Main Injection Engine

src/thermal_fault_injector.py


Features:
- deterministic event generation
- seed = global_seed + event_seed
- events restricted to chosen split
- no cross-split contamination

### Generated Outputs

Running the injector creates:
data/runs/R001/
telemetry_inj.csv
events.json
week02_summary.txt


### Reproduce Week02

Activate environment then run:

```powershell
python -m src.thermal_fault_injector
python -m src.week02_summary
pytest -q
```

---

# Week 03 — Baseline Detection + Evaluation

Goal: Implement a baseline anomaly detector and evaluate detection performance against injected thermal faults.

Components added:

- baseline_threshold.py  
  Z-score based anomaly detector using training statistics.

- eval_events.py  
  Converts point alarms into predicted events and computes detection metrics.

- week03_run_eval.py  
  Runs full evaluation pipeline and produces metrics.

- plot_alarms.py  
  Generates timeline visualization of telemetry and alarms.

Outputs generated:

data/runs/R001/

    metrics_table.csv
    alarm_timeline.png

Metrics computed:

- Precision
- Recall
- EventF1
- Mean Detection Delay (MDD)
- False Alarm Bursts (FAB)

Run Week03:

python -m src.week03_run_eval
python -m src.plot_alarms
pytest -q
