import duckdb
import os

print("Building lightweight DuckDB for Streamlit Cloud...")

# Connect to the NEW lite DB
lite_db_path = 'skytrax_lite.duckdb'
if os.path.exists(lite_db_path):
    os.remove(lite_db_path)

con = duckdb.connect(lite_db_path)

# Attach the main warehouse
con.execute("ATTACH 'skytrax_warehouse.duckdb' AS warehouse (READ_ONLY)")

# Copy dimensions
print("Copying dimensions...")
con.execute("CREATE TABLE dim_airlines AS SELECT * FROM warehouse.dim_airlines")
con.execute("CREATE TABLE dim_airports AS SELECT * FROM warehouse.dim_airports")

# Copy facts but EXCLUDE the heavy text fields like review_body and review_header
print("Copying fact_airline_reviews (excluding raw text)...")
con.execute("""
CREATE TABLE fact_airline_reviews AS 
SELECT 
    airline_id, 
    date_flown_str,
    try_cast(right(date_flown_str, 4) as int) as flight_year,
    seat_comfort, 
    cabin_staff_service, 
    food_beverages, 
    inflight_entertainment, 
    wifi_connectivity, 
    ground_service, 
    value_for_money, 
    is_recommended, 
    country, 
    seat_type, 
    type_of_traveller, 
    is_verified,
    aircraft_type
FROM warehouse.fact_airline_reviews
""")

print("Copying fact_airport_reviews...")
con.execute("""
CREATE TABLE fact_airport_reviews AS 
SELECT airport_id, queuing_times, terminal_cleanliness 
FROM warehouse.fact_airport_reviews
""")

print("Copying fact_seat_reviews...")
con.execute("CREATE TABLE fact_seat_reviews AS SELECT * FROM warehouse.fact_seat_reviews")

print("Copying fact_lounge_reviews...")
con.execute("""
CREATE TABLE fact_lounge_reviews AS 
SELECT airline_id, comfort, cleanliness 
FROM warehouse.fact_lounge_reviews
""")

con.close()
print("skytrax_lite.duckdb built successfully! Ready for Streamlit Cloud.")
