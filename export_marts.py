import duckdb
import pandas as pd
import os

print("Exporting data marts to Parquet for Streamlit Cloud...")
db_path = 'skytrax_warehouse.duckdb'
con = duckdb.connect(db_path, read_only=True)

out_dir = 'streamlit_app/data'
os.makedirs(out_dir, exist_ok=True)

# Q1: NPS Proxy
df1 = con.execute("""
    select a.airline_name, count(r.review_id) as total_reviews, avg(r.is_recommended) * 100 as recommendation_rate
    from fact_airline_reviews r join dim_airlines a on r.airline_id = a.airline_id
    group by 1 having count(r.review_id) > 100 order by recommendation_rate desc limit 20
""").df()
df1.to_parquet(f'{out_dir}/mart_q1_nps.parquet')

# Q2: Pain Points
df2 = con.execute("""
    select 'Wifi & Connectivity' as service_type, sum(case when wifi_connectivity <= 2 then 1 else 0 end) * 100.0 / count(wifi_connectivity) as bad_review_pct from fact_airline_reviews
    union all select 'Food & Beverages' as service_type, sum(case when food_beverages <= 2 then 1 else 0 end) * 100.0 / count(food_beverages) as bad_review_pct from fact_airline_reviews
    union all select 'Inflight Entertainment' as service_type, sum(case when inflight_entertainment <= 2 then 1 else 0 end) * 100.0 / count(inflight_entertainment) as bad_review_pct from fact_airline_reviews
""").df()
df2.to_parquet(f'{out_dir}/mart_q2_painpoints.parquet')

# Q3: Seat Analytics
df3 = con.execute("""
    select seat_type, avg(seat_comfort) as avg_comfort, avg(cabin_staff_service) as avg_staff, avg(food_beverages) as avg_food, count(*) as sample_size
    from fact_airline_reviews where seat_type in ('Economy Class', 'Business Class', 'First Class', 'Premium Economy') group by 1 order by avg_comfort desc
""").df()
df3.to_parquet(f'{out_dir}/mart_q3_seat.parquet')

# Q4: Airport Bottlenecks
df4 = con.execute("""
    select a.airport_name, count(r.review_id) as total_reviews, avg(r.queuing_times) as avg_queuing, avg(r.terminal_cleanliness) as avg_cleanliness
    from fact_airport_reviews r join dim_airports a on r.airport_id = a.airport_id
    group by 1 having count(r.review_id) > 50 order by avg_queuing asc, avg_cleanliness asc limit 15
""").df()
df4.to_parquet(f'{out_dir}/mart_q4_airport.parquet')

# Q5: Temporal
df5 = con.execute("""
    select right(date_flown_str, 4) as flight_year, avg(seat_comfort + cabin_staff_service + value_for_money)/3.0 as overall_score, count(*) as total
    from fact_airline_reviews where try_cast(right(date_flown_str, 4) as int) between 2010 and 2024 group by 1 order by flight_year
""").df()
df5.to_parquet(f'{out_dir}/mart_q5_temporal.parquet')

# Q6: Aircraft worst seat comfort
df6 = con.execute("""
    select aircraft_type, avg(seat_comfort) as avg_seat_comfort, count(*) as total_reviews
    from fact_airline_reviews where aircraft_type is not null group by 1 having count(*) > 50 order by avg_seat_comfort asc limit 15
""").df()
df6.to_parquet(f'{out_dir}/mart_q6_aircraft.parquet')

# Q7: Traveller Type
df7 = con.execute("""
    select type_of_traveller as traveller_type, avg(value_for_money) as avg_value, avg(seat_comfort) as avg_comfort, count(*) as total_reviews
    from fact_airline_reviews where type_of_traveller is not null group by 1 order by avg_value desc
""").df()
df7.to_parquet(f'{out_dir}/mart_q7_traveller.parquet')

# Q8: Verified
df8 = con.execute("""
    select is_verified, avg(value_for_money) as avg_value, avg(seat_comfort) as avg_comfort, count(*) as reviews_count
    from fact_airline_reviews group by 1
""").df()
df8.to_parquet(f'{out_dir}/mart_q8_verified.parquet')

# Q9: Lounge Reviews
df9 = con.execute("""
    select a.airline_name as lounge_airline, avg(r.comfort) as avg_comfort, avg(r.cleanliness) as avg_cleanliness, count(*) as total_reviews
    from fact_lounge_reviews r join dim_airlines a on r.airline_id = a.airline_id
    group by 1 having count(*) > 30 order by avg_comfort desc limit 15
""").df()
df9.to_parquet(f'{out_dir}/mart_q9_lounge.parquet')

# Q10: Demographics
df10 = con.execute("""
    select country, avg(value_for_money) as avg_score, count(*) as total_reviews
    from fact_airline_reviews where country is not null group by 1 having count(*) > 500 order by avg_score asc limit 10
""").df()
df10.to_parquet(f'{out_dir}/mart_q10_demographics.parquet')

print("Done! Data exported to streamlit_app/data/")

print("Exporting BA Deep Dive Data Marts...")

# BA1: Key Drivers Analysis (Correlation with Recommended)
df_ba_drivers = con.execute("""
    select 
        corr(seat_comfort, is_recommended) as seat_comfort_corr,
        corr(cabin_staff_service, is_recommended) as cabin_staff_corr,
        corr(food_beverages, is_recommended) as food_beverages_corr,
        corr(inflight_entertainment, is_recommended) as inflight_ent_corr,
        corr(wifi_connectivity, is_recommended) as wifi_corr,
        corr(ground_service, is_recommended) as ground_service_corr,
        corr(value_for_money, is_recommended) as value_for_money_corr
    from fact_airline_reviews
""").df()
df_ba_drivers.to_parquet(f'{out_dir}/mart_ba_drivers.parquet')

# BA2: COVID Trend (Cost-cutting impact)
df_ba_covid = con.execute("""
    select 
        try_cast(right(date_flown_str, 4) as int) as flight_year,
        avg(food_beverages) as avg_food,
        avg(cabin_staff_service) as avg_staff,
        avg(seat_comfort) as avg_seat
    from fact_airline_reviews
    where try_cast(right(date_flown_str, 4) as int) between 2018 and 2024
    group by 1 order by flight_year
""").df()
df_ba_covid.to_parquet(f'{out_dir}/mart_ba_covid_trend.parquet')

# BA3: Competitor Benchmarking (Top Tier Airlines)
df_ba_comp = con.execute("""
    select 
        a.airline_name,
        avg(r.seat_comfort) as seat_comfort,
        avg(r.cabin_staff_service) as cabin_staff_service,
        avg(r.food_beverages) as food_beverages,
        avg(r.inflight_entertainment) as inflight_entertainment,
        avg(r.wifi_connectivity) as wifi_connectivity,
        avg(r.ground_service) as ground_service,
        avg(r.value_for_money) as value_for_money,
        count(*) as total_reviews
    from fact_airline_reviews r join dim_airlines a on r.airline_id = a.airline_id
    group by 1 having count(*) > 500
""").df()
df_ba_comp.to_parquet(f'{out_dir}/mart_ba_competitors.parquet')

print("BA Deep Dives generated successfully!")
