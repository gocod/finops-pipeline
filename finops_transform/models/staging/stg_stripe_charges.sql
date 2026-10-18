select
    charge_id,
    customer_id,
    customer_email,
    amount_paid_usd,
    subscription_tier,
    cast(created_at as timestamp) as charged_at
from {{ source('raw_stripe', 'stripe_charges') }}