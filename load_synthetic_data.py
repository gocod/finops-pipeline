import datetime
import random
import uuid
from google.cloud import bigquery
import numpy as np
import pandas as pd
from faker import Faker

# --- CONFIGURATION (Scaled for Looker Studio Dashboards) ---
PROJECT_ID = "fde-finops-analytics-prod"
LOCATION = "US"
NUM_CUSTOMERS = 150       # Increased from 10 to 150 customers
NUM_DAYS = 90             # Expanded from 7 days to 90 days of history
NUM_TELEMETRY_RECORDS = 15000  # Scaled up telemetry volume

fake = Faker()
client = bigquery.Client(project=PROJECT_ID)

# Shared master list of customers so Stripe & Telemetry reference the exact same IDs
def get_or_create_customers():
    customers = []
    tiers = ["Growth", "Enterprise", "Starter"]
    tier_weights = [0.35, 0.15, 0.50]
    
    for i in range(1, NUM_CUSTOMERS + 1):
        cust_id = f"cust_{100 + i}"
        tier = random.choices(tiers, weights=tier_weights)[0]
        customers.append({
            "id": cust_id, 
            "tier": tier, 
            "email": fake.company_email()
        })
    return customers

SHARED_CUSTOMERS = get_or_create_customers()


def generate_and_load_stripe():
    print("Generating Stripe revenue data...")
    records = []
    end_date = datetime.datetime.now(datetime.timezone.utc)
    
    for c in SHARED_CUSTOMERS:
        # Generate monthly billing cycles over the 90-day window
        for month_offset in range(3):
            created_at = end_date - datetime.timedelta(
                days=min(NUM_DAYS, (2 - month_offset) * 30 + random.uniform(0, 5))
            )
            if c["tier"] == "Enterprise":
                amount = 500.0
            elif c["tier"] == "Growth":
                amount = 150.0
            else:
                amount = 49.0
                
            records.append({
                "charge_id": f"ch_{uuid.uuid4().hex[:12]}",
                "customer_id": c["id"],
                "customer_email": c["email"],
                "amount_paid_usd": amount,
                "subscription_tier": c["tier"],
                "created_at": created_at.isoformat(),
            })

    df = pd.DataFrame(records)
    df["created_at"] = pd.to_datetime(df["created_at"])

    table_id = f"{PROJECT_ID}.raw_stripe.stripe_charges"
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True,
    )
    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config, location=LOCATION
    )
    job.result()
    print(f"✅ Loaded {len(df)} rows into {table_id}")


def generate_and_load_telemetry():
    print("Generating API telemetry log data...")
    customer_ids = [c["id"] for c in SHARED_CUSTOMERS]
    models = ["universal-3.5-pro", "universal-realtime", "universal-4.0-ultra"]

    records = []
    end_date = datetime.datetime.now(datetime.timezone.utc)
    for _ in range(NUM_TELEMETRY_RECORDS):
        timestamp = end_date - datetime.timedelta(
            days=random.uniform(0, NUM_DAYS)
        )
        audio_sec = round(random.uniform(5.0, 240.0), 2)
        records.append({
            "request_id": str(uuid.uuid4()),
            "customer_id": random.choice(customer_ids),
            "model_used": random.choice(models),
            "audio_seconds": audio_sec,
            "tokens_processed": int(audio_sec * random.uniform(12, 22)),
            "timestamp": timestamp.isoformat(),
        })

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    table_id = f"{PROJECT_ID}.raw_telemetry.api_requests"
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE", autodetect=True
    )
    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config, location=LOCATION
    )
    job.result()
    print(f"✅ Loaded {len(df)} rows into {table_id}")


def generate_and_load_gcp_billing():
    print("Generating GCP infrastructure billing data...")
    skus = [
        {"desc": "TPU v5e Node Hour", "hourly_rate": 1.20},
        {"desc": "NVIDIA L4 GPU Hour", "hourly_rate": 0.70},
        {"desc": "Compute Engine N2 Standard", "hourly_rate": 0.15},
    ]

    records = []
    end_date = datetime.datetime.now(datetime.timezone.utc)

    # Generate hourly cost records per SKU over NUM_DAYS (90 days * 24 hours)
    for hour_offset in range(NUM_DAYS * 24):
        usage_time = end_date - datetime.timedelta(hours=hour_offset)
        for sku in skus:
            usage_amount = round(random.uniform(6.0, 24.0), 2)
            cost = round(usage_amount * sku["hourly_rate"], 4)
            records.append({
                "billing_account_id": "01A2B3-4C5D6E-7F8901",
                "service_description": "Compute Engine / Vertex AI",
                "sku_description": sku["desc"],
                "usage_start_time": usage_time.isoformat(),
                "project_id": "fde-app-workloads-prod",
                "cost_usd": cost,
                "usage_amount": usage_amount,
            })

    df = pd.DataFrame(records)
    df["usage_start_time"] = pd.to_datetime(df["usage_start_time"])

    table_id = f"{PROJECT_ID}.raw_gcp_billing.gcp_billing_export"
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE", autodetect=True
    )
    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config, location=LOCATION
    )
    job.result()
    print(f"✅ Loaded {len(df)} rows into {table_id}")


if __name__ == "__main__":
    print(f"🚀 Starting Scaled FinOps Data Generator for Project: {PROJECT_ID}\n")
    generate_and_load_stripe()
    generate_and_load_telemetry()
    generate_and_load_gcp_billing()
    print("\n🎉 All 90-day raw tables populated successfully in BigQuery!")