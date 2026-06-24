with raw as (
    select * from read_csv_auto('e:\skytrax_review\dataset\seat_reviews\all_seats_review_raw.csv', header=true, all_varchar=true)
)
select
    md5(airline_name || date || customer_name || review_body) as review_id,
    airline_name,
    customer_name,
    country,
    review_body,
    "Seat Type" as seat_type,
    "Aircraft Type" as aircraft_type,
    "Seat Layout" as seat_layout,
    "Date Flown" as date_flown_str,
    "Type Of Traveller" as type_of_traveller,
    try_cast("Seat Legroom" as double) as seat_legroom,
    try_cast("Seat Recline" as double) as seat_recline,
    try_cast("Seat Width" as double) as seat_width,
    try_cast("Aisle Space" as double) as aisle_space,
    try_cast("Viewing Tv Screen" as double) as viewing_tv_screen,
    try_cast("Power Supply" as double) as power_supply,
    try_cast("Seat Storage" as double) as seat_storage,
    try_cast("Sleep Comfort" as double) as sleep_comfort,
    try_cast("Sitting Comfort" as double) as sitting_comfort,
    try_cast("Seat/bed Width" as double) as seat_bed_width,
    try_cast("Seat/bed Length" as double) as seat_bed_length,
    try_cast("Seat Privacy" as double) as seat_privacy,
    case when "Recommended" = 'yes' then 1 else 0 end as is_recommended,
    case when review_body like '%✅ Trip Verified%' or review_body like '%Verified Review%' then 1 else 0 end as is_verified
from raw
