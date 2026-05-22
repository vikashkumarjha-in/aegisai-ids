# 🏗️ AegisAI System Architecture & Engineering Blueprint

AegisAI is engineered as a highly decoupled, modular Intrusion Detection System (IDS) and Security Operations Center (SOC) platform. The system processes high-throughput network telemetry by transitioning data through sequential structural layers—combining deterministic rule-based logic with statistical machine learning inference.

---

## 🛰️ Core Operational Pipeline

The system processes network metrics across five distinct pipeline stages, visualized below:

```text
  [ NETWORK INGESTION ] 
           │
           ▼
┌─────────────────────────┐
│ 1. Traffic Capture Layer│ ──► Simulates real-time packet & flow streaming
└──────────┬──────────────┘
           │ Raw Flow Parameters
           ▼
┌─────────────────────────┐
│ 2. Feature Extraction   │ ──► Preprocessing, LabelEncoding & Feature Scaling
└──────────┬──────────────┘
           │ Normalized Feature Matrix (41 Dimensions)
           ▼
┌─────────────────────────┐
│ 3. AI Detection Engine  │ ──► scikit-learn Pipeline (Logistic Regression)
└──────────┬──────────────┘
           │ Binary Classification (0: Benign / 1: Malicious)
           ▼
┌─────────────────────────┐
│ 4. Threat Classification│ ──► Severity Mapping & Contextual Risk Allocation
└──────────┬──────────────┘
           │ Multi-class Tagging (Low, Medium, High, Critical)
           ▼
┌─────────────────────────┐
│ 5. Alerting & Logging   │ ──► Threaded CSV Audit Trails & Live Web Telemetry
└─────────────────────────┘
           │
           ▼
  [ SOC COMMAND CENTER UI ]

```

---

## 🔍 Structural Layer Breakdowns

### 1. Traffic Ingestion & Capture Layer

* **Mechanism:** Implements a decoupled data generator engine (`utils/data_generator.py`) to simulate continuous network flow records.
* **Telemetry Generation:** Programmatically crafts realistic packet structures mimicking both normal web traffic patterns and hostile attack anomalies.

### 2. Feature Extraction & Preprocessing Pipeline

* **Input Handling:** Consumes multi-attribute flow data and maps it against the 41-feature schema required by the classification model.
* **Transformation Matrix:** Executes real-time `LabelEncoding` on categorical attributes (`protocol_type`, `service`, `flag`) and normalizes numerical values utilizing a version-locked `StandardScaler` to protect against feature variance bias.

### 3. AI Detection & Machine Learning Engine

* **Inference Hub:** Leverages an optimized `scikit-learn` classification pipeline.
* **Decision Matrix:** Runs high-precision, low-latency binary and multi-class predictions, evaluating incoming structural features to draw clean decision boundaries between legitimate actions and active network exploits.

### 4. Threat Classification & Alert Logic

* **Explainable Guardrails:** Passes model inference results through a rule-based validation matrix (`src/alert_logic.py`).
* **Risk Categorization:** Evaluates feature anomalies (e.g., critical `src_bytes` threshold breaches or high-frequency `count` variables) to dynamically tag events into precise risk profiles:
* `Benign` ──► **Low Severity**
* `Port Scan` / `Host Scan` ──► **Medium Severity**
* `Brute Force` / `Web Attack` ──► **High Severity**
* `DDoS` / `Botnet` / `Infiltration` ──► **Critical Severity**



### 5. Audit Logging & SIEM Telemetry Layer

* **Persistent Registry:** Commit predictions instantly to a persistent, atomic file structure (`logs/audit.csv`) to serve as a high-fidelity historical audit trail.
* **Frontend Synchronization:** Publishes structured event payloads seamlessly to the asynchronous FastAPI backend endpoints, driving real-time UI component updates across the Streamlit Security Operations Center interface.

```

```