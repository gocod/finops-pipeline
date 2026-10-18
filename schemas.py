# schemas.py

BIGQUERY_SCHEMAS = {
    "raw_gcp_billing": [
        {"name": "billing_account_id", "type": "STRING"},
        {"name": "service_description", "type": "STRING"},
        {"name": "sku_description", "type": "STRING"},
        {"name": "usage_start_time", "type": "TIMESTAMP"},
        {"name": "project_id", "type": "STRING"},
        {"name": "cost_usd", "type": "FLOAT64"},
        {"name": "usage_amount", "type": "FLOAT64"},
    ],
    "raw_stripe": [
        {"name": "charge_id", "type": "STRING"},
        {"name": "customer_id", "type": "STRING"},
        {"name": "customer_email", "type": "STRING"},
        {"name": "amount_paid_usd", "type": "FLOAT64"},
        {"name": "subscription_tier", "type": "STRING"},
        {"name": "created_at", "type": "TIMESTAMP"},
    ],
    "raw_telemetry": [
        {"name": "request_id", "type": "STRING"},
        {"name": "customer_id", "type": "STRING"},
        {"name": "model_used", "type": "STRING"},
        {"name": "audio_seconds", "type": "FLOAT64"},
        {"name": "tokens_processed", "type": "INT64"},
        {"name": "timestamp", "type": "TIMESTAMP"},
    ]
}