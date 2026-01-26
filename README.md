# AegisAI
AI-Powered Intrusion Detection System

AegisAI is a real-world AI-based Intrusion Detection System
designed to detect, analyze, and respond to cyber threats.

## Problem Statement
Traditional IDS rely on predefined rules and signatures, making them
ineffective against unknown or evolving cyber attacks. AegisAI addresses
this gap using AI-based behavioral analysis.

## IDS Design Approach
AegisAI is designed as a Hybrid IDS to leverage the strengths of both
signature-based detection and AI-based anomaly detection.

## Dataset
AegisAI initially uses the NSL-KDD dataset to train and evaluate AI-based
intrusion detection models before moving to real-time traffic analysis.

## Development Setup
Initial development focuses on dataset loading and preprocessing using Python
before implementing AI-based intrusion detection models.

## Data Preprocessing
The project implements initial data cleaning and preprocessing steps including
missing value inspection, duplicate removal, and label encoding to prepare
datasets for AI-based intrusion detection.

## Feature Engineering
The project performs feature-label separation and normalization to prepare
datasets for machine learning-based intrusion detection models.

## Model Training
A baseline machine learning model is trained using labeled intrusion data
to classify normal and malicious network behavior.

## Model Evaluation
The trained machine learning model is evaluated using standard
classification metrics including accuracy, precision, recall,
F1-score, and confusion matrix analysis to assess detection performance.

## Alert Generation
AegisAI converts model predictions into security alerts,
distinguishing normal traffic from potential intrusions.

## Model Training & Evaluation
A baseline machine learning model using Logistic Regression has been implemented.
The model is trained on preprocessed intrusion data and saved for reuse.
Evaluation metrics such as accuracy and classification report validate
correct pipeline execution.

> Status: Training and evaluation pipeline completed successfully.

## Model Persistence
The trained intrusion detection model is saved using joblib and reused
during evaluation without retraining, enabling deployment readiness.

## Feature Scaling & Training Stability

Feature engineering was enhanced by replacing manual normalization
with industry-standard feature scaling using `StandardScaler`. The training
pipeline was updated to ensure all numerical features are scaled before model
training, improving stability and convergence of the Logistic Regression model.

Key improvements:
- Standardized feature scaling
- Cleaner feature-label separation
- Improved model training reliability

## Robust Training with Small Dataset

Implemented a safe training fallback mechanism.
If train-test splitting results in a single-class training set,
the model automatically trains on the full dataset.
This ensures pipeline stability during early-stage development
with limited data.

## Stable Training with Balanced Dataset

To prevent training failures caused by single-class splits,
the dataset was updated to ensure a minimum of two samples
per class. The training pipeline now strictly validates data
before training and follows a clean, production-style workflow.

## IDS-Oriented Feature Engineering

We introduced intrusion-detection-inspired feature logic.
Instead of using raw values directly, behavioral indicators such as
packet ratio and activity thresholds were created.

This improves interpretability and moves the system closer to a
real-world IDS design while remaining compatible with small datasets.

## Rule-based IDS and ML Comparison

A simple rule-based detector was implemented to provide explainable,
behavior-based intrusion decisions (e.g. packet ratio thresholds,
high-activity flags). A comparison script (`compare.py`) measures
performance (accuracy, precision/recall) and agreement between the
trained ML model and the rule-based detector. This helps validate
the ML model against human-understandable rules.

## sModel Validation & Confusion Matrix

A validation script (`src/validate.py`) runs the trained model on the
processed dataset, prints accuracy and classification metrics, and saves
a confusion matrix image (`models/confusion_matrix.png`). This provides
a quick visual check of prediction results and is useful for demos.

## Class Imbalance Handling

Added automatic class-imbalance handling to the training pipeline. The script:
- detects class distribution,
- for small, imbalanced datasets (<=200 rows) performs safe random oversampling of the minority class,
- for larger datasets uses `class_weight='balanced'` in the classifier,
- trains a pipeline (scaler + classifier) and saves it for later evaluation.

This keeps the training stable and reduces bias towards majority classes during early development.

## Versioning & Experiment Registry

Each trained model is saved as a versioned artifact (ids_model_vN.pkl). The latest
model is available as ids_model.pkl for evaluation and deployment. Training metadata
(train accuracy, timestamp, notes) is appended to `models/experiments.csv` to track
experiments and enable reproducibility.

## Hyperparameter Tuning & Safe Fallback

Introduces an automated tuning script (`src/hyperparameter_tuning.py`) that:
- attempts GridSearchCV for Logistic Regression when class counts and sample size permit,
- otherwise falls back to training a default pipeline (safe for tiny datasets),
- saves tuned or fallback models as versioned artifacts and records training/tuning metrics in `models/experiments.csv`.

## Usage

This project includes a simple Command-Line Interface (CLI) for training and evaluating models.
To use the CLI, open the project root and run:
Train a model:

# AegisAI IDS API (FastAPI)

## Day 22 Overview
On Day 22, we implemented the **Intrusion Detection System (IDS) REST API** using **FastAPI**. The API loads the trained pipeline (`ids_model_v4.pkl`) and provides a `/predict` endpoint to detect network attacks based on engineered features.

### Features:
- Loads trained pipeline (scaler + model) for inference.
- POST `/predict` endpoint accepts JSON with:
  ```json
  {
    "packet_ratio": 0.75,
    "high_activity": 1
  }
