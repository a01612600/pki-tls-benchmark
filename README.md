# Classical PKI in TLS — Certificate Verification Cost Analysis

Research project focused on empirically evaluating the computational cost of digital certificate verification in TLS 1.3, comparing different classical cryptographic algorithms and X.509 certificate chain depths.

---

# Objective

Analyze how TLS handshake latency changes as:

- cryptographic algorithm size and type increase,
- certificate chain depth increases,
- total exchanged certificate size increases.

The project compares RSA and ECDSA under controlled experimental conditions and repeated measurements.

---

# Experimental Setup

## Evaluated Algorithms

- RSA-2048
- RSA-4096
- ECDSA P-256 (`ec256`)
- ECDSA P-384 (`ec384`)

## Certificate Chain Depth

X.509 chains with the following depths were evaluated:

- 1 certificate
- 2 certificates
- 3 certificates
- 4 certificates

## Total Experimental Conditions

- 16 experimental combinations  
  `(4 algorithms × 4 depths)`

## Measurements

- ~650 handshakes per condition
- 10,400 total observations

## TLS Configuration

- TLS 1.3
- Session resumption disabled (`-no_ticket`)
- Local TLS server using OpenSSL

---

# Results

During Weeks 3–6, the complete dataset collection, validation, and statistical analysis pipeline was finalized.

The project successfully:

- generated certificate chains automatically,
- executed repeated TLS handshakes,
- measured handshake latency,
- recorded certificate sizes,
- automated experimental runs,
- generated statistical visualizations,
- performed normality testing,
- executed Mann–Whitney U tests,
- fitted linear regression models,
- validated dataset consistency.

---

# Data Quality

## Validation Checks

- Missing values: `0`
- Duplicate rows: `0`
- All conditions completed successfully
- Balanced observation distribution

## Coefficient of Variation (CV)

Most experimental conditions presented:

- `CV < 20%`

Some RSA-4096 configurations exhibited higher variability, documented using:

- boxplots,
- outlier analysis,
- scatter plots,
- error bars,
- statistical summary tables.

---

# Statistical Analysis

The following analyses were performed:

- Shapiro–Wilk normality test
- Mann–Whitney U test
- descriptive statistics,
- linear regression,
- certificate size analysis,
- latency vs depth visualization,
- latency vs certificate size visualization.

---

# Dataset Integrity

The final dataset was verified using SHA-256 hashing.

```text
5286440e0078ac054802b4fb3cb204941086f8501a2d9c4333f9fd8bd3575604
```

---

# Experimental Environment

The project was executed on macOS using:

- Python 3.14.4
- OpenSSL 3.6.2
- local `.venv` virtual environment

To avoid system dependency conflicts, the project used:

- Homebrew
- isolated Python virtual environments

Complete environment information is available in:

```text
analysis/system_info.txt
```

Including:

- CPU
- RAM
- operating system
- OpenSSL version
- Python version

---

# Final Dataset

Location:

```text
data/final_dataset.csv
```

## Dataset Structure

```text
replica_id
algo
depth
run_id
handshake_ms
timestamp
cert_bytes
session_resumption
```

---

# Reproducibility

## Clone Repository

```bash
git clone https://github.com/a01612600/pki-tls-benchmark.git
cd pki-tls-benchmark
```

## Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Dataset Collection

```bash
python scripts/collect_week5.py
```

## Run Statistical Analysis

```bash
python analysis/week6_summary.py
python analysis/week6_normality.py
python analysis/week6_mannwhitney.py
python analysis/week6_regression.py
python analysis/week6_scatter.py
```

---

# License

MIT License