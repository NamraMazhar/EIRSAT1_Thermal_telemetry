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

# Week 04 — Baseline-2 Residual Detection + Comparative Evaluation

## Goal
Implement baseline-2 using orbit-cycle removal plus thresholding on the residual signal, then compare it against baseline-1 using event-based detection metrics.

## Implemented Components

### Configuration
Configuration file:

`configs/baseline2.yaml`

Defines:
- run_id
- global seed
- channels used
- orbit period samples
- phase bins
- validation threshold candidates
- frozen threshold

### Orbit-cycle Baseline Estimator

Fits a periodic baseline template using **training split only**.

Implemented in:  
`src/orbit_baseline.py`

Features:
- periodic template fit by phase
- train-only fitting
- forward application to validation/test
- residual computation:
  - residual = value − periodic_baseline

### Residual Detector

Applies thresholding on residual z-scores.

Implemented in:  
`src/baseline_residual.py`

Features:
- residual z-score computation
- threshold-based anomaly alarms
- uses training residual statistics only

### Comparative Evaluation Engine

Implemented in:  
`src/week04_compare.py`

Features:
- runs baseline-1 on test
- runs validation-only threshold sweep for baseline-2
- freezes selected threshold
- evaluates baseline-2 on test
- generates comparative metrics table
- stores threshold record and fit log

### Diagnostic Plotting

Implemented in:  
`src/week04_plots.py`

Generates:
- raw vs residual plot
- false alarm timeline

### Unit Tests

Implemented in:  
`tests/test_week04.py`

Checks:
- threshold record exists
- frozen threshold is not null
- comparative table has both methods
- required metric columns are present

## Generated Outputs

Running the Week 04 pipeline creates:

`data/runs/R001/`

- `comparative_metrics.csv`
- `threshold_record.json`
- `baseline2_fit_log.json`
- `baseline2_detected_test.csv`
- `raw_vs_residual_TEMP_CPU.png`
- `false_alarm_timeline.png`

## Comparative Results

### Baseline-1
- Precision = 0.00000
- Recall = 0.0
- EventF1 = 0.000000
- MDD = NaN
- FAB = 0

### Baseline-2
- Precision = 0.00268
- Recall = 0.5
- EventF1 = 0.005331
- MDD = 240.0
- FAB = 2233
- Frozen threshold = 1.5

## Reproduce Week04

Activate environment then run:

```powershell
python -m src.week04_compare
python -m src.week04_plots
pytest -q
