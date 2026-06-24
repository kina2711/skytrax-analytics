select
    r.review_id,
    a.airline_id,
    r.customer_name,
    r.country,
    r.review_body,
    r.type_of_traveller,
    r.seat_type,
    r.route,
    r.date_flown_str,
    r.is_recommended,
    r.seat_comfort,
    r.cabin_staff_service,
    r.food_beverages,
    r.inflight_entertainment,
    r.wifi_connectivity,
    r.ground_service,
    r.value_for_money,
    r.is_verified
from {{ ref('stg_airline_reviews') }} r
left join {{ ref('dim_airlines') }} a on r.airline_name = a.airline_name
