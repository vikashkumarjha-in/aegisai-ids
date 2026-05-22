# 📊 Dataset Selection & Feature Engineering

To guarantee rigorous benchmarking and robust evaluation metrics, AegisAI leverages the **NSL-KDD dataset**—the definitive, heavily cited standard in modern network intrusion detection system research. 

---

## 🎯 Why NSL-KDD?

Compared to legacy data frameworks, the NSL-KDD matrix provides critical architectural advantages that ensure high model generalization in production environments:

```text
  ┌─────────────────────────────────────────────────────────┐
  │                   NSL-KDD ADVANTAGES                    │
  ├───────────────────┬─────────────────────────────────────┤
  │ Research Standard │ Globally recognized baseline for    │
  │                   │ supervised anomaly detection tests. │
  ├───────────────────┼─────────────────────────────────────┤
  │ Class Stability   │Optimally sampled to eliminate severe│
  │                   │ class overrepresentation issues.    │
  ├───────────────────┼─────────────────────────────────────┤
  │ Dual Profile      │ Implements clean parallel paths for │
  │                   │ normal traffic and active attacks.  │
  ├───────────────────┼─────────────────────────────────────┤
  │ Core Versatility  │ Universally adaptable to both logic │
  │                   │ rules and statistical ML modeling.  │
  └───────────────────┴─────────────────────────────────────┘

```

---

## 🔍 Data Characteristics & Schema Vector

The ingested telemetry profiles encapsulate **41 discrete dimensional features** plus designated attack labels. The data vector maps connection characteristics across three main mathematical categories:

### 1. Nominal & Categorical Attributes

* **Protocol Type:** Transport layer mapping (`TCP`, `UDP`, `ICMP`).
* **Service:** Destination application network services (`HTTP`, `FTP`, `SMTP`, `SSH`, etc.).
* **Flag:** Network delta state indicators reflecting connection status (`SF`, `S0`, `REJ`, etc.).

### 2. Quantitative & Traffic Metric Ingestion

* **Source Bytes:** Volume of data transferred from source to destination hosts (`src_bytes`).
* **Destination Bytes:** Volume of data transferred from destination back to source hosts (`dst_bytes`).
* **Count Indicators:** High-frequency trackers tracking current connections over a specific time window.

### 3. Classification Space

* **Ground Truth Target Labels:** Maps individual flow records cleanly into dual binary spaces (`0: Benign` or `1: Malicious`) or multi-class security labels specifying discrete attack categories (DoS, Probe, R2L, U2R).

```

```