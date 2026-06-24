with raw as (
    select * from read_csv_auto('e:\skytrax_review\dataset\airport_reviews\all_airport_review_raw.csv', header=true, all_varchar=true)
)
select
    md5(airport_name || date || customer_name || review_body) as review_id,
    airport_name,
    customer_name,
    country,
    review_body,
    "Experience At Airport" as experience_at_airport,
    "Date Visit" as date_visit_str,
    "Type Of Traveller" as type_of_traveller,
    try_cast("Queuing Times" as double) as queuing_times,
    try_cast("Terminal Cleanliness" as double) as terminal_cleanliness,
    try_cast("Terminal Seating" as double) as terminal_seating,
    try_cast("Terminal Signs" as double) as terminal_signs,
    try_cast("Food Beverages" as double) as food_beverages,
    try_cast("Airport Shopping" as double) as airport_shopping,
    try_cast("Airport Staff" as double) as airport_staff,
    try_cast("Wifi Connectivity" as double) as wifi_connectivity,
    case when "Recommended" = 'yes' then 1 else 0 end as is_recommended,
    case when review_body like '%✅ Trip Verified%' or review_body like '%Verified Review%' then 1 else 0 end as is_verified
from raw
