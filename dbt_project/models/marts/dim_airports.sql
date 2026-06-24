with airports as (
    select distinct airport_name from {{ ref('stg_airport_reviews') }}
    union
    select distinct airport_name from {{ ref('stg_lounge_reviews') }}
)
select
    row_number() over (order by airport_name) as airport_id,
    airport_name
from airports
where airport_name is not null
