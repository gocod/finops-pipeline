with customer_costs as (
    select
        date_trunc(extract(date from usage_hour), month) as usage_month,
        customer_id,
        sum(total_audio_seconds) as total_audio_seconds,
        sum(total_gcp_cost_usd) as total_infrastructure_cost_usd
    from {{ ref('int_hourly_usage_costs') }}
    where customer_id is not null
    group by 1, 2
),

customer_revenue as (
    select
        date_trunc(extract(date from charged_at), month) as usage_month,
        customer_id,
        max(customer_email) as customer_email,
        max(subscription_tier) as subscription_tier,
        sum(amount_paid_usd) as total_revenue_usd
    from {{ ref('stg_stripe_charges') }}
    where customer_id is not null
    group by 1, 2
)

select
    coalesce(r.usage_month, c.usage_month) as usage_month,
    coalesce(r.customer_id, c.customer_id) as customer_id,
    r.customer_email,
    r.subscription_tier,
    coalesce(r.total_revenue_usd, 0) as total_revenue_usd,
    coalesce(c.total_infrastructure_cost_usd, 0) as total_infrastructure_cost_usd,
    coalesce(c.total_audio_seconds, 0) as total_audio_seconds,
    safe_divide(c.total_infrastructure_cost_usd, c.total_audio_seconds) as cost_per_audio_second_usd,
    coalesce(r.total_revenue_usd, 0) - coalesce(c.total_infrastructure_cost_usd, 0) as net_margin_usd
from customer_revenue r
left join customer_costs c
    on r.customer_id = c.customer_id
   and r.usage_month = c.usage_month