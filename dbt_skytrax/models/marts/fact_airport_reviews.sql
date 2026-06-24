select
    r.review_id,
    a.airport_id,
    r.customer_name,
    r.country,
    r.review_body,
    r.experience_at_airport,
    r.date_visit_str,
    r.type_of_traveller,
    r.queuing_times,
    r.terminal_cleanliness,
    r.terminal_seating,
    r.terminal_signs,
    r.food_beverages,
    r.airport_shopping,
    r.airport_staff,
    r.wifi_connectivity,
    r.is_recommended,
    r.is_verified
from {{ ref('stg_airport_reviews') }} r
left join {{ ref('dim_airports') }} a on r.airport_name = a.airport_name
