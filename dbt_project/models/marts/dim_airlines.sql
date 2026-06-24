with airlines as (
    select distinct airline_name from {{ ref('stg_airline_reviews') }}
    union
    select distinct airline_name from {{ ref('stg_lounge_reviews') }}
    union
    select distinct airline_name from {{ ref('stg_seat_reviews') }}
)
select
    row_number() over (order by airline_name) as airline_id,
    airline_name
from airlines
where airline_name is not null
