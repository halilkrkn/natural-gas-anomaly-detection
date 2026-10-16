# Software Architecture — small, modular, thesis-first

## Architecture objective

Keep scientific logic reusable and testable outside notebooks while avoiding unnecessary framework layers. Use ordinary Python modules/functions and a small common model interface. Apply SOLID only when it improves a concrete responsibility or testability.

## Proposed package boundaries

```text
src/natural_gas_anomaly_detection/
├── data/             # read/validate SKAB and generated run tables; manifest/split helpers
├── preprocessing/    # train-only scaler fitting and transform application
├── simulation/       # fluids Weymouth adapter, demand profile, segment/run generation
├── anomaly/          # post-split fault injection and physical timeline labels
├── features/         # causal windowing and classical window-statistics features
├── models/
│   ├── classical/    # Isolation Forest, One-Class SVM, LOF adapters
│   └── deep_learning/# LSTM-AE, GRU-AE and shared training/scoring helpers
├── evaluation/       # score direction, validation threshold selection, metrics, lead time
└── visualization/   # plotting functions only
```

Notebooks orchestrate EDA and experiments (`notebooks/`), call reusable code, and display results. Do not duplicate production algorithms between notebooks and `src/`.

## Important seams/interfaces

- **Data/run manifest:** records stable `run_id`, split, scenario metadata, time index and ground truth. Identifiers/metadata are never passed directly as features.
- **Preprocessor:** `fit` only on normal training values/features; `transform` applies immutable fitted state.
- **Window builder:** accepts a single already-assigned split/run and creates causal W-length windows without crossing boundaries; records each window-end index.
- **Feature transformer:** classical models receive a 2-D feature matrix from five named statistics per sensor. Deep models receive a 3-D `(batch, W, F)` tensor.
- **Model adapter:** fit on normal training data; return a 1-D anomaly score for each unseen window, always high = anomalous.
- **Threshold calibrator:** pure functions that accept validation scores and labels, return thresholds plus calibration metadata. It must not accept test data.
- **Evaluator:** consumes frozen scores/thresholds/ground truth and produces window-level and run-level metrics; it must not tune a model.
- **Weymouth adapter:** wraps the external `fluids` function with explicit SI/reference parameters and input/output validation. It does not reimplement gas-flow equations.

Do not create a generic plug-in architecture, deep inheritance, a repository-wide `BasePipeline` or one class for every noun. Introduce interfaces only where two or more components genuinely need substitutability (e.g. scoring adapters).

## Suggested implementation sequence

1. Project/config validation and common data structures.
2. Data inventory, SKAB EDA, split manifests, missing-data policy.
3. Windowing and train-only preprocessing with leakage tests.
4. Weymouth adapter plus round-trip/physical tests; only then produce trusted simulations.
5. Scenario generation and post-split anomaly injection with ground-truth timelines.
6. Classical feature extraction and common score interface.
7. IF, OCSVM, LOF adapters.
8. LSTM-AE and GRU-AE with shared training/scoring behavior.
9. Validation-only threshold calibration and evaluation metrics.
10. Reproducible pilot, controlled sensitivity checks, final experiment manifest.

## Test layers

- Unit: input validation, split boundaries, all-normal training windows, statistics, score sign, threshold tie-breaking, metric edge cases, segment mass balance.
- Integration: `fluids` nominal pressure/flow round-trip, complete synthetic run generation, anomaly injection labels, each model's score shape.
- Smoke: small sample / one seed / a few epochs only; no full benchmark by default.
- Experiment audit: verify config snapshots, run IDs, seeds, no test-time tuning, expected output files.

## Configuration and outputs

Scientific choices live in `configs/` and their rationale/status in `docs/decision_register.md`. Keep data locations in a non-secret local override or environment variables where possible; never hard-code a user-specific Drive path in reusable modules. Keep generated datasets, checkpoints, raw score arrays and heavy logs outside Git.
