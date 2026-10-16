# Thesis Method Contract (current project baseline)

**Purpose:** This is the concise method contract coding agents must follow. Detailed rationales and citations remain in the thesis proposal, `docs/phase1_5_9_hyperparameter_architecture.md`, `docs/global_framework_audit.md`, and the global decision register.

## Research scope

Title: *Doğal Gaz İletim Sistemlerinde Zaman Serisi Verileri Kullanılarak Anomali Tespiti ve Kestirimci Bakım: Makine Öğrenmesi ile Derin Öğrenme Yaklaşımlarının Karşılaştırmalı Analizi*.

Goal: compare classical machine learning and deep-learning approaches for time-series anomaly detection and early warning in natural-gas-transmission-related behavior. RUL prediction is outside scope. The synthetic pipeline represents a BOTAŞ-like high-pressure segment only; it is not BOTAŞ data or a validated transient network simulator.

Research questions:
- RQ1: How do classical ML and deep learning methods differ in anomaly detection performance?
- RQ2: How do anomaly types affect model performance?
- RQ3: How early can gradual anomalies be detected before a predefined critical scenario point?
- RQ4: How can anomaly scores be converted to normal / early-warning / critical alarm classes?

Models: Isolation Forest, One-Class SVM, Local Outlier Factor, LSTM Autoencoder, GRU Autoencoder.

Data: SKAB; controlled synthetic data from the `fluids.compressible.Weymouth` library; SWaT only if available and its role is justified. The natural-gas synthetic data is quasi-steady, not a full transient simulator.

## Data split and leakage barriers

- Split unit: independent Weymouth simulation run; SKAB experiment/file/time-series unit.
- Weymouth normal runs: current baseline 30 train, 10 validation, 10 test. This is a practical design choice, not a literature-optimal ratio.
- Per anomaly condition: 10 validation and 10 test runs, no anomaly-containing training runs. Current registered conditions: fixed leak 2%, 5%, 10%; gradual leak 0→10% over 6 hours; sensor pressure bias ±0.5%; pressure sensor drift 0→±1% over 6 hours.
- Pipeline: assign split → fit scaler/preprocessing on normal training data only → transform validation/test → create causal windows within each split → train → calibrate thresholds on validation → freeze → test once.
- Do not split windows randomly. Never build a window across split/run boundaries. A W=16 window contains 16 time samples; training windows must be all-normal. For evaluation, label a window from its end timestamp.
- Anomaly injection occurs after the run is assigned to validation/test. Model features must exclude timestamp identifiers, run/experiment identifiers, labels, scenario names, severity/ramp settings, `Q_leak`, and any ground-truth-only field.

## Baseline window and features

- Sampling interval: 15 minutes. Current baseline W=16 (four hours), causal, stride 1.
- Classical models receive five statistics per selected sensor: mean, standard deviation, min, max, and linear slope.
- Deep models receive standardized multi-channel windows and reconstruct the same W×F shape.
- W=16 is the approved v1 design baseline (15-minute sampling means 4 hours of causal history). W=32 sensitivity is out of scope under the current approved framework.
- SKAB sensors and missing-data policy remain OPEN-DECISION-002 and 003 until EDA.
- Model-side flow representation remains OPEN-DECISION-016. Do not make an unapproved choice among Qin/Qout/derived imbalance or include leak ground truth in the model input.

## Simulator assumptions

- Use `fluids.compressible.Weymouth` with named arguments and explicit units/reference conditions. Do not reimplement the formula by hand.
- Parameter evidence must follow `docs/parameter_source_audit.md`; do not label the whole baseline bundle “literature-supported.” Current classifications: D=0.75 m, L=100 km, P1=9 MPa, SG=0.675, and Tavg=283.15 K are **partially unverified at exact-value/context level** in the current audit; P2≈5 MPa is a reference operating point, not a fixed output; Zavg=0.8065 is **derived/provisional**, not a universal literature constant; Ts=288.15 K and Ps=101325 Pa are ISO 13443 reference conditions; E=0.92 is a library correction factor, not measured operator efficiency.
- Zavg policy is selected as a fixed 0.8065 value for the v1 controlled synthetic baseline, with the simplification limitation documented. OPEN-DECISION-012 remains open only for actual Colab numerical validation and recording the outputs; selection of a config value alone is not validation. Earlier flow values are not final until that validation passes.
- A leak is a controlled simplified mass-balance disturbance at x=0.5L using two 50 km segments; it is not a full orifice/transient leak simulation.
- Normal demand variation ±5%, 15-minute sampling, 24-hour run composition, six-hour gradual ramp/hold segments, and demand-phase jitter are **design choices**, not universal physical constants. The approved run-to-run variability choice is recorded in `docs/decision_register.md` and `configs/simulation.yaml`.
- Measurement-noise candidates (pressure σ=5 kPa, flow σ=0.5% of nominal Q0, temperature σ=0.1 K) are **approved provisional explicit assumptions** for the pilot, not operator sensor specifications. OPEN-DECISION-014 remains open until the 2× sensitivity comparison and results record are complete.
- Synthetic-data limitation for the thesis: “Sentetik koşular aynı quasi-steady-state Weymouth üreticisi ve basit periyodik talep profiliyle üretildiğinden, sonuçlar bu kontrollü üretici altındaki yöntem karşılaştırmasını gösterir; gerçek doğal gaz iletim şebekelerine doğrudan genellenebilirlik iddiası taşımaz.” No extra experiment is added by this limitation statement.

## Score and evaluation contract

- Every model adapter exposes an anomaly score with **higher = more anomalous**.
- IF/OCSVM/LOF scoring APIs and sign transforms must be unit-tested. LOF uses `novelty=True` for unseen validation/test windows.
- Autoencoder window score is mean squared reconstruction error averaged across all W samples and F input channels. Also save per-channel MSE for diagnostics; it is not itself the window alarm score.
- Thresholds are numeric and model-specific. Same selection algorithm across models; validation-only calibration.
- Binary threshold: maximize validation F1; ties break by higher validation Recall, then lower FPR on normal validation samples.
- Three-class threshold pair T1/T2: jointly optimize validation Macro-F1 over normal / early-warning / critical labels; apply the registered tie-breaking policy from `configs/experiments.yaml`. Do not apply this three-class calibration to fixed anomaly scenarios.
- Alarm map: score < T1 = normal; T1 ≤ score < T2 = early warning; score ≥ T2 = critical.
- For gradual synthetic scenarios, lead time is t_critical (predefined scenario point such as 10% leak or full specified drift) minus first detection time; this is not the learned T2 threshold. For SKAB report detection delay after labeled anomaly onset.
- Primary event detection is the first T1 crossing after scenario onset; no consecutive-crossing persistence filter in the primary protocol. Report point-level FPR and the proportion of normal runs with at least one alarm. A single crossing can inflate false alarms; this risk is explicit and the primary rule remains unchanged unless formally revised.
- Overlapping windows are highly correlated. Window-level metrics describe point/window behavior, but the number of windows is not the number of independent experiments; summarize variability at independent run level as well.
- Three-class normal/early-warning/critical calibration is evaluated only on controlled gradual Weymouth scenarios with scenario-stage labels. SKAB is evaluated with binary anomaly labels and detection delay because its labels do not provide the same controlled physical severity scale. This scope distinction should be confirmed with the thesis advisor.
- Three-class T1/T2 selection uses labeled validation scenarios to maximize Macro-F1. Therefore training is unsupervised/normal-only, but threshold calibration is validation-supervised (or semi-supervised in the broad evaluation sense); this must be stated transparently. Test data never selects thresholds.

## Candidate model configuration

Read `configs/models.yaml` and `docs/phase1_5_9_hyperparameter_architecture.md`. Current provisional AE candidates are hidden size 32, batch size 128, max 100 epochs, and early-stopping patience 10; these are transferred candidates, not gas-pipeline optima. OCSVM `nu=0.1` remains a cross-domain pilot candidate, not direct natural-gas evidence. IF/LOF values are mainly library-default baselines. Development seed 42 is not the final repeated-run decision. Do not describe these as optimized values before pilot validation.

## Reproducibility outputs

Each run must preserve config snapshot, Git commit, split/run manifest, seeds, package versions, model checkpoint outside Git, validation thresholds, raw score and prediction arrays, run-level and aggregate metrics, and logs. Report mean ± SD across appropriate independent simulation runs/repetitions; overlapping windows are not independent replications.

## Global open decisions

See `docs/decision_register.md` for authoritative current status, why open, exact closure condition, and pre-closure work.

**Approved OPEN-DECISION-006 subpolicy:** at hour 18, gradual leak injection ends (`Q_leak=0`) and sensor drift injection is removed with offset reset to zero; the quasi-steady v1 model assumes instantaneous return, not transient recovery. No recovery class is added. Windows are excluded from three-class validation calibration and class metrics until 16 consecutive post-reset samples are available (nominally around a 22:00 window end at 15-minute sampling). The exact window-end boundary remains an implementation check; see `configs/experiments.yaml`. At minimum, do not silently close OPEN-DECISION-002, 003, 007, 008, 009, 011, 012, 014, 016, or OPEN-DECISION-006's remaining window-end/implementation check. OPEN-DECISION-021 policy is closed but run-manifest implementation must be checked. OPEN-DECISION-020 is superseded, not active.
