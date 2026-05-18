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
- `python -m src.week04_compare`
- `python -m src.week04_plots`
- `pytest -q`
```

# Week 05 — ML Reconstruction Baseline + 3-Baseline Benchmark

## Goal
Implement baseline-3 using an unsupervised ML reconstruction model and produce the first 3-baseline benchmark table with time-aware evaluation.

## Implemented Components

### Configuration
Configuration file:

`configs/week05_ml.yaml`

Defines:
- run_id
- global seed
- channels used
- hidden layer structure
- max iterations
- solver
- validation threshold candidates
- target validation alarm rate
- representative channel for score plot

### ML Reconstruction Baseline
Implemented in:

`src/baseline_ml.py`

This module:
- converts telemetry into wide per-timestamp feature matrices
- fits an unsupervised reconstruction model on the training split only
- computes reconstruction error scores
- thresholds scores using training statistics
- selects threshold on validation only

### 3-Baseline Benchmark Runner
Implemented in:

`src/week05_benchmark.py`

This script:
- loads Week01 chronological splits
- trains baseline-3 only on training data
- tunes threshold on validation data
- freezes threshold before test
- evaluates baseline-3 on test using the same event harness as previous baselines
- combines baseline-1, baseline-2, and baseline-3 into one benchmark table
- logs training and inference runtime

### Plotting
Implemented in:

`src/week05_plots.py`

Generates:
- score distribution comparison (train vs test)

### Unit Tests
Implemented in:

`tests/test_week05.py`

Checks:
- benchmark table contains at least 3 rows
- required metric fields are present
- runtime log exists and contains positive values
- frozen threshold exists

## Generated Outputs

Running the Week 05 pipeline creates:

`data/runs/R001/`

- `ml_scores_train.csv`
- `ml_scores_test.csv`
- `week05_threshold_record.json`
- `ml_runtime_log.json`
- `benchmark_3baseline.csv`
- `# Week 05 — ML Reconstruction Baseline + 3-Baseline Benchmark

## Goal
Implement baseline-3 using an unsupervised ML reconstruction model and produce the first 3-baseline benchmark table with time-aware evaluation.

## Implemented Components

### Configuration
Configuration file:

`configs/week05_ml.yaml`

Defines:
- run_id
- global seed
- channels used
- hidden layer structure
- max iterations
- solver
- validation threshold candidates
- target validation alarm rate
- representative channel for score plot

### ML Reconstruction Baseline
Implemented in:

`src/baseline_ml.py`

This module:
- converts telemetry into wide per-timestamp feature matrices
- fits an unsupervised reconstruction model on the training split only
- computes reconstruction error scores
- thresholds scores using training statistics
- selects threshold on validation only

### 3-Baseline Benchmark Runner
Implemented in:

`src/week05_benchmark.py`

This script:
- loads Week01 chronological splits
- trains baseline-3 only on training data
- tunes threshold on validation data
- freezes threshold before test
- evaluates baseline-3 on test using the same event harness as previous baselines
- combines baseline-1, baseline-2, and baseline-3 into one benchmark table
- logs training and inference runtime

### Plotting
Implemented in:

`src/week05_plots.py`

Generates:
- score distribution comparison (train vs test)

### Unit Tests
Implemented in:

`tests/test_week05.py`

Checks:
- benchmark table contains at least 3 rows
- required metric fields are present
- runtime log exists and contains positive values
- frozen threshold exists

## Generated Outputs

Running the Week 05 pipeline creates:

`data/runs/R001/`

- `ml_scores_train.csv`
- `ml_scores_test.csv`
- `week05_threshold_record.json`
- `ml_runtime_log.json`
- `benchmark_3baseline.csv`
- `score_distribution_train_vs_test.png`

## 3-Baseline Benchmark Results

### Baseline-1
- Precision = 0.00000
- Recall = 0.000000
- EventF1 = 0.000000
- MDD = NaN
- FAB = 0
- Threshold = 3.0

### Baseline-2
- Precision = 0.00268
- Recall = 0.500000
- EventF1 = 0.005331
- MDD = 240.0
- FAB = 2233
- Threshold = 1.5

### Baseline-3
- Precision = 0.02331
- Recall = 0.833333
- EventF1 = 0.045351
- MDD = 402.0
- FAB = 419
- Threshold = 3.0

## Runtime Logging
- Train time = 4.791953900001317 sec
- Infer time = 0.001968799999303883 sec

## Reproducibility
Deterministic settings:
- fixed seed = 1337
- no random shuffle across splits
- train-only fitting
- validation-only threshold tuning
- frozen threshold on test

Saved score file hashes were checked across reruns to verify deterministic outputs.

## Reproduce Week05

Run:

```powershell
python -m src.week05_benchmark
python -m src.week05_plots
pytest -q
```

# Week 06 — Multi-Run Robust Results Pack + Injection Protocol v0.2

## Goal
Refine injection realism and protocol v0.2, then produce the first robust results pack across multiple injection settings.

## Implemented Components

### Injection Protocol v0.2
Three frozen configuration files were created:

- `configs/injection_v2_R001.yaml`
- `configs/injection_v2_R002.yaml`
- `configs/injection_v2_R003.yaml`

These define:
- run_id
- global seed
- split to inject
- fault magnitudes and durations
- controlled drift slope scaling
- optional mixed-fault setting
- dropout handling policy
- allowed channels

### Injector v2
Implemented in:

`src/thermal_fault_injector_v2.py`

Features:
- deterministic event generation
- controlled drift refinement
- optional mixed faults
- dropout handling policy
- reproducible telemetry and events generation
- schema version `schema_v0_2`

### Multi-Run Evaluation
Implemented in:

`src/week06_run_all.py`

This script:
- loads R001, R002, R003
- evaluates all three baselines for each run
- produces a consolidated results table with 9 rows total

### Trade-off Plot
Implemented in:

`src/week06_plot_tradeoff.py`

This script generates:
- `FAB vs EventF1` plot
- labeled run_id points
- method-wise comparison

### Unit Tests
Implemented in:

`tests/test_week06.py`

Checks:
- consolidated results file exists
- 9+ rows present
- 3 run_ids present
- trade-off plot exists

## Generated Outputs

Outputs created:

`data/runs/R001/`
- `telemetry_inj.csv`
- `events.json`

`data/runs/R002/`
- `telemetry_inj.csv`
- `events.json`

`data/runs/R003/`
- `telemetry_inj.csv`
- `events.json`

Global Week06 outputs:
- `data/runs/week06_consolidated_results.csv`
- `data/runs/week06_tradeoff_plot.png`

## Consolidated Results

### R001
- baseline-1: Precision = 0.000000, Recall = 0.000000, EventF1 = 0.000000, MDD = NaN, FAB = 0
- baseline-2: Precision = 0.002658, Recall = 0.500000, EventF1 = 0.005289, MDD = 250.0, FAB = 2251
- baseline-3: Precision = 0.018595, Recall = 0.750000, EventF1 = 0.036290, MDD = 560.0, FAB = 475

### R002
- baseline-1: Precision = 0.500000, Recall = 0.083333, EventF1 = 0.142857, MDD = 2940.0, FAB = 1
- baseline-2: Precision = 0.002676, Recall = 0.500000, EventF1 = 0.005324, MDD = 300.0, FAB = 2236
- baseline-3: Precision = 0.020305, Recall = 1.000000, EventF1 = 0.039801, MDD = 635.0, FAB = 579

### R003
- baseline-1: Precision = 0.000000, Recall = 0.000000, EventF1 = 0.000000, MDD = NaN, FAB = 0
- baseline-2: Precision = 0.002692, Recall = 0.500000, EventF1 = 0.005355, MDD = 50.0, FAB = 2223
- baseline-3: Precision = 0.014981, Recall = 1.000000, EventF1 = 0.029520, MDD = 260.0, FAB = 789

## Reproducibility
A selected run (`R002`) was regenerated and the hashes of:
- `telemetry_inj.csv`
- `events.json`

matched exactly across reruns, confirming deterministic multi-run generation.

## Reproduce Week06

Run:

```powershell
python -m src.thermal_fault_injector_v2 configs/injection_v2_R001.yaml
python -m src.thermal_fault_injector_v2 configs/injection_v2_R002.yaml
python -m src.thermal_fault_injector_v2 configs/injection_v2_R003.yaml
python -m src.week06_run_all
python -m src.week06_plot_tradeoff
pytest -q
```

# Week 07 — Ablation Set A: Fault-Type Sweep + Failure Analysis

## Goal
Run Ablation Set A by fixing severity and varying only fault type, then evaluate how each method performs across bias, drift, lag, stuck_at, and dropout faults.

## Implemented Components

### Frozen Fault-Type Configs
The following ablation configs were created:

- `configs/ablation_A_bias.yaml`
- `configs/ablation_A_drift.yaml`
- `configs/ablation_A_lag.yaml`
- `configs/ablation_A_stuck_at.yaml`
- `configs/ablation_A_dropout.yaml`

Run mapping:
- `R101` → bias
- `R102` → drift
- `R103` → lag
- `R104` → stuck_at
- `R105` → dropout

All runs use:
- fixed seed = 1337
- fixed split = test
- fixed medium magnitude and medium duration
- same event count and same channel set
- only fault type changes

### Ablation Run Generation
Implemented in:

`src/week07_generate_ablation_A.py`

This script generates all five fault-type-specific injected runs using the Week06 injector v2.

### Multi-Method Evaluation
Implemented in:

`src/week07_run_methods.py`

This script evaluates all three methods across all five runs:
- baseline-1: raw threshold
- baseline-2: residual threshold
- baseline-3: ML reconstruction

Outputs:
- Precision
- Recall
- EventF1
- MDD
- FAB
- Threshold

### Summary Plots
Implemented in:

`src/week07_summary_plots.py`

Generates:
- `week07_faulttype_eventf1.png`
- `week07_faulttype_mdd.png`
- `week07_faulttype_fab.png`

### Failure Analysis
Implemented in:

`src/week07_failure_analysis.py`

Creates:
- `week07_failure_cases.csv`

This file stores representative FN/FP cases for later annotation and paper figures.

### Results Index
Implemented in:

`src/week07_results_index.py`

Creates:
- `week07_results_index.csv`

This maps:
- run_id
- config file
- telemetry output
- event file

### Unit Tests
Implemented in:

`tests/test_week07.py`

Checks:
- ablation results file exists
- 5 fault types are present
- failure cases file exists
- results index exists

## Generated Outputs

Run folders:
- `data/runs/R101/`
- `data/runs/R102/`
- `data/runs/R103/`
- `data/runs/R104/`
- `data/runs/R105/`

Global Week07 outputs:
- `data/runs/week07_ablation_results.csv`
- `data/runs/week07_faulttype_eventf1.png`
- `data/runs/week07_faulttype_mdd.png`
- `data/runs/week07_faulttype_fab.png`
- `data/runs/week07_failure_cases.csv`
- `data/runs/week07_results_index.csv`

## Reproduce Week07

Run:

```powershell
python -m src.week07_generate_ablation_A
python -m src.week07_run_methods
python -m src.week07_summary_plots
python -m src.week07_failure_analysis
python -m src.week07_results_index
pytest -q
````

# Week 08 — Ablation Set B: Magnitude + Duration Sensitivity Sweep

## Goal
Run Ablation Set B by sweeping fault magnitude and duration for two fault types, then produce sensitivity curves for EventF1, MDD, and FAB.

## Implemented Components

### Grid Config Generation
Implemented in:

`src/week08_generate_configs.py`

This script creates 18 frozen configs covering:

- fault types: `bias`, `drift`
- magnitudes: `small`, `medium`, `large`
- durations: `short`, `medium`, `long`

Run IDs:
- `R201`–`R209` → bias sweep
- `R210`–`R218` → drift sweep

It also creates:

- `data/runs/week08_config_index.csv`

### Grid Run Generation
Implemented in:

`src/week08_generate_grid.py`

This script generates all 18 injected runs using the Week06 injector v2.

### Full Grid Evaluation
Implemented in:

`src/week08_run_grid_methods.py`

This script evaluates all three methods for every config:

- baseline-1: raw threshold
- baseline-2: residual threshold
- baseline-3: ML reconstruction

For each run it stores:
- Precision
- Recall
- EventF1
- MDD
- FAB
- Threshold

Outputs:
- `data/runs/week08_grid_results.csv`
- `data/runs/week08_threshold_tuning.csv`

### Sensitivity Plots
Implemented in:

`src/week08_make_plots.py`

Generated plots:
- `week08_eventf1_vs_magnitude.png`
- `week08_mdd_vs_duration.png`
- `week08_fab_vs_threshold.png`

### Unit Tests
Implemented in:

`tests/test_week08.py`

Checks:
- results table exists
- threshold tuning file exists
- all 3 plots exist
- grid coverage includes at least 18 run IDs

## Generated Outputs

Global Week08 outputs:
- `data/runs/week08_config_index.csv`
- `data/runs/week08_grid_results.csv`
- `data/runs/week08_threshold_tuning.csv`
- `data/runs/week08_eventf1_vs_magnitude.png`
- `data/runs/week08_mdd_vs_duration.png`
- `data/runs/week08_fab_vs_threshold.png`

Run folders created:
- `data/runs/R201/` to `data/runs/R218/`

## Experimental Grid
Week08 evaluates:

- 2 fault types
- 3 magnitudes
- 3 durations

Total configurations:

- `2 × 3 × 3 = 18`

With 3 methods per configuration, the benchmark table contains:

- `18 × 3 = 54` evaluated entries

## Observed Pattern
Initial Week08 outputs continue the same broad trend seen earlier:

- baseline-1 remains too conservative
- baseline-2 improves recall but produces very high FAB
- baseline-3 remains the strongest overall method

This week adds sensitivity evidence showing how method performance changes as fault severity changes.

## Reproduce Week08

Run:

```powershell
python -m src.week08_generate_configs
python -m src.week08_generate_grid
python -m src.week08_run_grid_methods
python -m src.week08_make_plots
pytest -q
````
# Week 09 — Refined Proposed Method + Robustness Stress Tests

## Goal
Refine the proposed residual-learning method and compare it against the three baselines under robustness stress tests for timing/orbit-phase, missingness, and noise.

## Implemented Components

### Proposed Method (Refined v2)
Implemented in:

`src/proposed_method.py`

This method:
- fits a periodic baseline on training data only
- estimates expected residual behavior
- computes residual-based anomaly scores
- uses stronger thresholding
- applies additional smoothing and minimum-event filtering

### Stress Run Generation
Implemented in:

`src/week09_generate_stress_runs.py`

Generated stress runs:
- `RS01` → timing / orbit-phase shift
- `RS02` → missingness stress
- `RS03` → noise stress

### 4-Method Comparison
Implemented in:

`src/week09_run_comparison.py`

Methods included:
- baseline-1: raw threshold
- baseline-2: residual threshold
- baseline-3: ML reconstruction
- proposed: residual learning refined v2

Output:
- `data/runs/week09_stress_results.csv`

### Trade-off Plots
Implemented in:

`src/week09_tradeoff_plots.py`

Generated:
- `week09_eventf1_vs_fab.png`
- `week09_mdd_vs_fab.png`

### Main Results Table
Implemented in:

`src/week09_main_table.py`

Generated:
- `week09_main_results_table.csv`
- `week09_stress_matrix.csv`

### Unit Tests
Implemented in:

`tests/test_week09.py`

Checks:
- stress results exist
- main table exists
- at least 4 methods are present
- at least 3 stress dimensions are present
- trade-off plots exist

## Generated Outputs

Global Week09 outputs:
- `data/runs/week09_stress_results.csv`
- `data/runs/week09_main_results_table.csv`
- `data/runs/week09_stress_matrix.csv`
- `data/runs/week09_eventf1_vs_fab.png`
- `data/runs/week09_mdd_vs_fab.png`

Stress run folders:
- `data/runs/RS01/`
- `data/runs/RS02/`
- `data/runs/RS03/`

## Key Observations
- baseline-3 remains the strongest balanced baseline overall
- the refined proposed method is substantially better than the earlier Week09 prototype
- under timing/orbit-phase stress (`RS01`), the refined proposed method achieved the highest EventF1
- under missingness (`RS02`), the refined proposed method became nearly tied with baseline-3
- under noise (`RS03`), the refined proposed method remained slightly below baseline-3 but was much improved relative to the earlier prototype
- early-alarm behavior is visible in some negative MDD cases and should be interpreted carefully

## Reproduce Week09

Run:

```powershell
python -m src.week09_generate_stress_runs
python -m src.week09_run_comparison
python -m src.week09_tradeoff_plots
python -m src.week09_main_table
pytest -q
```


