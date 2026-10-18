with api_hourly as (
    select
        timestamp_trunc(requested_at, hour) as usage_hour,
        customer_id,
        count(request_id) as total_requests,
        sum(audio_seconds) as total_audio_seconds,
        sum(tokens_processed) as total_tokens
    from {{ ref('stg_api_requests') }}
    group by 1, 2
),

gcp_hourly as (
    select
        timestamp_trunc(usage_start_time, hour) as usage_hour,
        sum(cost_usd) as total_gcp_cost_usd
    from {{ ref('stg_gcp_billing') }}
    group by 1
)

select
    coalesce(a.usage_hour, g.usage_hour) as usage_hour,
    a.customer_id,
    a.total_requests,
    a.total_audio_seconds,
    a.total_tokens,
    coalesce(g.total_gcp_cost_usd, 0) as total_gcp_cost_usd
from api_hourly a
full outer join gcp_hourly g
    on a.usage_hour = g.usage_hour