select
    billing_account_id,
    service_description,
    sku_description,
    project_id,
    cost_usd,
    usage_amount,
    cast(usage_start_time as timestamp) as usage_start_time
from {{ source('raw_gcp_billing', 'gcp_billing_export') }}