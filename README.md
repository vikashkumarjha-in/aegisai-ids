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
