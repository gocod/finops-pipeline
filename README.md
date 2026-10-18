# Cloud FinOps & Unit Economics Intelligence Pipeline

An end-to-end cloud financial analytics pipeline built on **Google Cloud Platform (GCP)**, **BigQuery**, **dbt**, and **Looker Studio**. 

This project bridges the gap between infrastructure spend and subscription revenue by modeling raw telemetry logs, GCP billing data, and Stripe charges into precise, customer-level unit economic margins.

---

## 🏗️ Architecture & Data Flow
[ Synthetic Telemetry ] ──┐
[ GCP Billing Data    ] ──┼─► [ Python Data Loader ] ─► [ BigQuery Raw ] ─► [ dbt Data Pipeline ] ─► [ Looker Studio Dashboard ]
[ Stripe Transactions ] ──┘

1. **Ingestion Layer (`load_synthetic_data.py`)**: Python ingestion pipeline generating 90 days of synthetic customer API usage, raw infrastructure compute costs, and flat-rate Stripe subscription billing into BigQuery raw tables.
2. **Transformation Layer (`finops_transform/`)**: 3-layer modular dbt architecture:
   * **Staging (`stg_`)**: Standardizes schema types, renames raw fields, and casts timestamps to consistent date grains (`usage_month`).
   * **Intermediate (`int_`)**: Aggregates hourly API audio processing seconds and infrastructure compute costs per customer.
   * **Marts (`fct_`)**: Joins customer revenue against GCP compute costs to calculate `cost_per_audio_second_usd` and `net_margin_usd`.
3. **Serving Layer**: Live Looker Studio dashboard providing real-time unit economics visibility across customer subscription tiers (`Starter`, `Growth`, `Enterprise`).

---

## 💡 FinOps & Business Impact

* **Unit Margin Visibility**: Calculates exact cost-per-unit metrics (`$ / audio second`) by linking application usage directly to cloud infrastructure billings.
* **Margin Drain Identification**: Pinpoints high-usage accounts operating at a negative net margin due to flat-rate subscription tier ceilings.
* **Pricing & Capacity Planning**: Equips Finance & Engineering leadership with data-driven insights to optimize pricing models and tier usage caps.

---

## ⚙️ Data Pipeline Models (dbt)

| Model Name | Layer | Description |
| :--- | :--- | :--- |
| `stg_api_requests` | Staging | Cleans and casts API request logs and audio usage metrics |
| `stg_gcp_billing` | Staging | Normalizes GCP billing export line items and compute costs |
| `stg_stripe_charges` | Staging | Extracts subscription tier metadata and revenue transactions |
| `int_hourly_usage_costs` | Intermediate | Maps customer API volume to hourly cloud infrastructure charges |
| `fct_customer_unit_margins` | Marts | Final unit economics model computing revenue, infra costs, and net margin |

---

## 🧪 Data Governance & Testing

Data quality is enforced using dbt schema assertions:
* **Uniqueness & Non-Null**: Verified across surrogate keys and customer IDs (`not_null`, `unique`).
* **Relational Integrity**: Foreign key relationships validated between staging usage records and billing entities.

To execute tests locally:
```powershell
dbt test

🛠️ Project Setup & Local Execution
Prerequisites
Python 3.10+

Google Cloud Platform (GCP) Account & BigQuery Dataset

dbt-bigquery (v1.5+)

Steps
Clone the repository:
git clone https://github.com/gocod/finops-pipeline.git
cd finops-pipeline

Activate Virtual Environment & Install Dependencies:
python -m venv .venv
.venv\Scripts\Activate
pip install dbt-bigquery google-cloud-bigquery

Ingest Synthetic Raw Data:
python load_synthetic_data.py

Run dbt Models & Quality Tests:
cd finops_transform
dbt run --full-refresh
dbt test

📊 Dashboard Preview
📜 License
Distributed under the MIT License.
