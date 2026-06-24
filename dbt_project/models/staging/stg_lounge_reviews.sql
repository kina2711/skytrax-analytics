with raw as (
    select * from read_csv_auto('e:\skytrax_review\dataset\lounges_reviews\all_lounge_review_raw.csv', header=true, all_varchar=true)
)
select
    md5(airline_name || date || customer_name || review_body) as review_id,
    airline_name,
    customer_name,
    country,
    review_body,
    "Lounge Name" as lounge_name,
    "Airport" as airport_name,
    "Type Of Lounge" as type_of_lounge,
    "Date Visit" as date_visit_str,
    "Type Of Traveller" as type_of_traveller,
    try_cast("Comfort" as double) as comfort,
    try_cast("Cleanliness" as double) as cleanliness,
    try_cast("Bar & Beverages" as double) as bar_beverages,
    try_cast("Catering" as double) as catering,
    try_cast("Washrooms" as double) as washrooms,
    try_cast("Wifi Connectivity" as double) as wifi_connectivity,
    try_cast("Staff Service" as double) as staff_service,
    case when "Recommended" = 'yes' then 1 else 0 end as is_recommended,
    case when review_body like '%✅ Trip Verified%' or review_body like '%Verified Review%' then 1 else 0 end as is_verified
from raw
