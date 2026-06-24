select
    r.review_id,
    a.airline_id,
    p.airport_id,
    r.customer_name,
    r.country,
    r.review_body,
    r.lounge_name,
    r.type_of_lounge,
    r.date_visit_str,
    r.type_of_traveller,
    r.comfort,
    r.cleanliness,
    r.bar_beverages,
    r.catering,
    r.washrooms,
    r.wifi_connectivity,
    r.staff_service,
    r.is_recommended,
    r.is_verified
from {{ ref('stg_lounge_reviews') }} r
left join {{ ref('dim_airlines') }} a on r.airline_name = a.airline_name
left join {{ ref('dim_airports') }} p on r.airport_name = p.airport_name
