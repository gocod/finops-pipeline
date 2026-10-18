select
    request_id,
    customer_id,
    model_used,
    audio_seconds,
    tokens_processed,
    cast(timestamp as timestamp) as requested_at
from {{ source('raw_telemetry', 'api_requests') }}