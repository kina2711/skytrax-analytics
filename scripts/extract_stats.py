import duckdb
import pandas as pd
import json

con = duckdb.connect('data/warehouse/skytrax_warehouse.duckdb', read_only=True)

# 1. Loyalty Drivers (Correlations)
df_fact = con.execute("SELECT * FROM fact_airline_reviews").df()
df_fact['recommended'] = df_fact['is_recommended'].astype(int)
corrs = df_fact[['cabin_staff_service', 'food_beverages', 'inflight_entertainment', 'ground_service', 'wifi_connectivity', 'value_for_money', 'recommended']].corr()['recommended']
corr_staff = round(corrs['cabin_staff_service'], 2)
corr_vfm = round(corrs['value_for_money'], 2)
corr_wifi = round(corrs['wifi_connectivity'], 2)

# 2. Post-COVID Food Degradation
df_food = con.execute("""
    SELECT 
        CAST(RIGHT(date_flown_str, 4) AS INTEGER) as year,
        AVG(food_beverages) as avg_food,
        AVG(seat_comfort) as avg_seat
    FROM fact_airline_reviews
    WHERE date_flown_str IS NOT NULL AND date_flown_str != ''
    AND LENGTH(date_flown_str) > 3
    GROUP BY 1
    ORDER BY 1
""").df()

food_2019 = df_food[df_food['year'] == 2019]['avg_food'].values
food_2019 = round(food_2019[0], 2) if len(food_2019) > 0 else 0

food_2023 = df_food[df_food['year'] == 2023]['avg_food'].values
food_2023 = round(food_2023[0], 2) if len(food_2023) > 0 else 0

seat_2019 = df_food[df_food['year'] == 2019]['avg_seat'].values
seat_2019 = round(seat_2019[0], 2) if len(seat_2019) > 0 else 0

seat_2023 = df_food[df_food['year'] == 2023]['avg_seat'].values
seat_2023 = round(seat_2023[0], 2) if len(seat_2023) > 0 else 0

# 3. Competitor Benchmarking
df_tier1 = con.execute("""
    SELECT 
        a.airline_name,
        AVG(f.cabin_staff_service) as avg_staff,
        AVG(f.inflight_entertainment) as avg_ent,
        AVG(f.value_for_money) as avg_vfm
    FROM fact_airline_reviews f
    JOIN dim_airlines a ON f.airline_id = a.airline_id
    WHERE a.airline_name IN ('Qatar Airways', 'Emirates', 'Singapore Airlines')
    GROUP BY 1
""").df()

tier1_stats = {}
for _, row in df_tier1.iterrows():
    tier1_stats[row['airline_name']] = {
        'staff': round(row['avg_staff'], 2),
        'ent': round(row['avg_ent'], 2),
        'vfm': round(row['avg_vfm'], 2)
    }

output = {
    'correlations': {
        'staff': corr_staff,
        'vfm': corr_vfm,
        'wifi': corr_wifi
    },
    'trends': {
        'food_2019': food_2019,
        'food_2023': food_2023,
        'seat_2019': seat_2019,
        'seat_2023': seat_2023
    },
    'tier1': tier1_stats
}

with open('stats.json', 'w') as f:
    json.dump(output, f, indent=2)
