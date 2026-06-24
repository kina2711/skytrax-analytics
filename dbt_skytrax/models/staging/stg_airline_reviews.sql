with raw as (
    select * from read_csv_auto('e:\skytrax_review\dataset\airlines_reviews\all_airlines_review_raw.csv', header=true, all_varchar=true)
)
select
    md5(airline_name || date || customer_name || review_body) as review_id,
    airline_name,
    customer_name,
    country,
    review_body,
    "Type Of Traveller" as type_of_traveller,
    "Seat Type" as seat_type,
    "Route" as route,
    "Date Flown" as date_flown_str,
    case when "Recommended" = 'yes' then 1 else 0 end as is_recommended,
    try_cast("Seat Comfort" as int) as seat_comfort,
    try_cast("Cabin Staff Service" as int) as cabin_staff_service,
    try_cast("Food & Beverages" as int) as food_beverages,
    try_cast("Inflight Entertainment" as int) as inflight_entertainment,
    try_cast("Wifi & Connectivity" as int) as wifi_connectivity,
    try_cast("Ground Service" as int) as ground_service,
    try_cast("Value For Money" as int) as value_for_money,
    case when review_body like '%✅ Trip Verified%' or review_body like '%Verified Review%' then 1 else 0 end as is_verified
from raw
