import duckdb
import os

print("Starting DuckDB warehouse initialization...")
db_path = 'skytrax_warehouse.duckdb'
if os.path.exists(db_path):
    os.remove(db_path)

con = duckdb.connect(db_path)

# 1. Staging
print("1. Creating Staging views...")
con.execute("""
create view stg_airline_reviews as
with raw as (select * from read_csv_auto('e:\skytrax_review\dataset\\airlines_reviews\\all_airlines_review_raw.csv', header=true, all_varchar=true))
select
    md5(airline_name || date || customer_name || review_body) as review_id,
    airline_name, customer_name, country, review_body, "Type Of Traveller" as type_of_traveller, "Seat Type" as seat_type, "Route" as route, "Date Flown" as date_flown_str,
    case when "Recommended" = 'yes' then 1 else 0 end as is_recommended,
    try_cast("Seat Comfort" as int) as seat_comfort, try_cast("Cabin Staff Service" as int) as cabin_staff_service, try_cast("Food & Beverages" as int) as food_beverages,
    try_cast("Inflight Entertainment" as int) as inflight_entertainment, try_cast("Wifi & Connectivity" as int) as wifi_connectivity, try_cast("Ground Service" as int) as ground_service,
    try_cast("Value For Money" as int) as value_for_money,
    case when review_body like '%✅ Trip Verified%' or review_body like '%Verified Review%' then 1 else 0 end as is_verified
from raw;
""")

con.execute("""
create view stg_airport_reviews as
with raw as (select * from read_csv_auto('e:\skytrax_review\dataset\\airport_reviews\\all_airport_review_raw.csv', header=true, all_varchar=true))
select
    md5(airport_name || date || customer_name || review_body) as review_id,
    airport_name, customer_name, country, review_body, "Experience At Airport" as experience_at_airport, "Date Visit" as date_visit_str, "Type Of Traveller" as type_of_traveller,
    try_cast("Queuing Times" as double) as queuing_times, try_cast("Terminal Cleanliness" as double) as terminal_cleanliness, try_cast("Terminal Seating" as double) as terminal_seating,
    try_cast("Terminal Signs" as double) as terminal_signs, try_cast("Food Beverages" as double) as food_beverages, try_cast("Airport Shopping" as double) as airport_shopping,
    try_cast("Airport Staff" as double) as airport_staff, try_cast("Wifi Connectivity" as double) as wifi_connectivity,
    case when "Recommended" = 'yes' then 1 else 0 end as is_recommended,
    case when review_body like '%✅ Trip Verified%' or review_body like '%Verified Review%' then 1 else 0 end as is_verified
from raw;
""")

con.execute("""
create view stg_lounge_reviews as
with raw as (select * from read_csv_auto('e:\skytrax_review\dataset\\lounges_reviews\\all_lounge_review_raw.csv', header=true, all_varchar=true))
select
    md5(airline_name || date || customer_name || review_body) as review_id,
    airline_name, customer_name, country, review_body, "Lounge Name" as lounge_name, "Airport" as airport_name, "Type Of Lounge" as type_of_lounge, "Date Visit" as date_visit_str, "Type Of Traveller" as type_of_traveller,
    try_cast("Comfort" as double) as comfort, try_cast("Cleanliness" as double) as cleanliness, try_cast("Bar & Beverages" as double) as bar_beverages, try_cast("Catering" as double) as catering,
    try_cast("Washrooms" as double) as washrooms, try_cast("Wifi Connectivity" as double) as wifi_connectivity, try_cast("Staff Service" as double) as staff_service,
    case when "Recommended" = 'yes' then 1 else 0 end as is_recommended,
    case when review_body like '%✅ Trip Verified%' or review_body like '%Verified Review%' then 1 else 0 end as is_verified
from raw;
""")

con.execute("""
create view stg_seat_reviews as
with raw as (select * from read_csv_auto('e:\skytrax_review\dataset\\seat_reviews\\all_seats_review_raw.csv', header=true, all_varchar=true))
select
    md5(airline_name || date || customer_name || review_body) as review_id,
    airline_name, customer_name, country, review_body, "Seat Type" as seat_type, "Aircraft Type" as aircraft_type, "Seat Layout" as seat_layout, "Date Flown" as date_flown_str, "Type Of Traveller" as type_of_traveller,
    try_cast("Seat Legroom" as double) as seat_legroom, try_cast("Seat Recline" as double) as seat_recline, try_cast("Seat Width" as double) as seat_width, try_cast("Aisle Space" as double) as aisle_space,
    try_cast("Viewing Tv Screen" as double) as viewing_tv_screen, try_cast("Power Supply" as double) as power_supply, try_cast("Seat Storage" as double) as seat_storage,
    try_cast("Sleep Comfort" as double) as sleep_comfort, try_cast("Sitting Comfort" as double) as sitting_comfort, try_cast("Seat/bed Width" as double) as seat_bed_width,
    try_cast("Seat/bed Length" as double) as seat_bed_length, try_cast("Seat Privacy" as double) as seat_privacy,
    case when "Recommended" = 'yes' then 1 else 0 end as is_recommended,
    case when review_body like '%✅ Trip Verified%' or review_body like '%Verified Review%' then 1 else 0 end as is_verified
from raw;
""")

# 2. Marts
print("2. Creating Dimension tables...")
con.execute("""
create table dim_airlines as
with airlines as (
    select distinct airline_name from stg_airline_reviews union select distinct airline_name from stg_lounge_reviews union select distinct airline_name from stg_seat_reviews
)
select row_number() over (order by airline_name) as airline_id, airline_name from airlines where airline_name is not null;
""")

con.execute("""
create table dim_airports as
with airports as (
    select distinct airport_name from stg_airport_reviews union select distinct airport_name from stg_lounge_reviews
)
select row_number() over (order by airport_name) as airport_id, airport_name from airports where airport_name is not null;
""")

print("3. Creating Fact tables...")
con.execute("""
create table fact_airline_reviews as
select r.*, a.airline_id from stg_airline_reviews r left join dim_airlines a on r.airline_name = a.airline_name;
""")

con.execute("""
create table fact_airport_reviews as
select r.*, a.airport_id from stg_airport_reviews r left join dim_airports a on r.airport_name = a.airport_name;
""")

con.execute("""
create table fact_lounge_reviews as
select r.*, a.airline_id, p.airport_id from stg_lounge_reviews r left join dim_airlines a on r.airline_name = a.airline_name left join dim_airports p on r.airport_name = p.airport_name;
""")

con.execute("""
create table fact_seat_reviews as
select r.*, a.airline_id from stg_seat_reviews r left join dim_airlines a on r.airline_name = a.airline_name;
""")

print("Pipeline finished! skytrax_warehouse.duckdb is ready for Streamlit.")
