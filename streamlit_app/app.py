import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Xóm Air - Aviation Reviews Analytics", layout="wide")

st.title("Xóm Air - Aviation Customer Experience Intelligence")
st.markdown("An analytical dashboard deriving insights from over 215,000 global passenger reviews.")

# Connect to the lightweight DuckDB database
db_path = os.path.join(os.path.dirname(__file__), '..', 'skytrax_lite.duckdb')
con = duckdb.connect(db_path, read_only=True)

# Fetch Slicer Data
@st.cache_data
def get_slicers():
    try:
        years = con.execute("SELECT DISTINCT flight_year FROM fact_airline_reviews WHERE flight_year IS NOT NULL ORDER BY 1").df()['flight_year'].tolist()
        years = [int(y) for y in years]
    except:
        years = []
        
    try:
        airlines = con.execute("SELECT DISTINCT airline_name FROM dim_airlines ORDER BY 1").df()['airline_name'].tolist()
    except:
        airlines = []
        
    try:
        countries = con.execute("SELECT DISTINCT country FROM fact_airline_reviews WHERE country IS NOT NULL ORDER BY 1").df()['country'].tolist()
    except:
        countries = []
        
    return years, airlines, countries

years, airlines, countries = get_slicers()

# Sidebar Filters
st.sidebar.header("Global Filters & Slicers")

selected_years = st.sidebar.multiselect("Select Flight Year(s)", options=years, default=years)
selected_airlines = st.sidebar.multiselect("Select Airline(s)", options=airlines, default=[], help="Leave empty to select all airlines")
selected_countries = st.sidebar.multiselect("Select Passenger Country", options=countries, default=[], help="Leave empty to select all countries")

min_reviews_filter = st.sidebar.slider("Minimum Total Reviews Threshold", min_value=10, max_value=1000, value=50, step=10, help="Filter out entities with too few reviews")

# Build WHERE clauses for airline facts
where_clauses = ["1=1"]
if selected_years:
    years_str = ','.join(str(y) for y in selected_years)
    where_clauses.append(f"r.flight_year IN ({years_str})")
if selected_airlines:
    airlines_str = ','.join([f"'{a.replace(chr(39), chr(39)+chr(39))}'" for a in selected_airlines])
    where_clauses.append(f"a.airline_name IN ({airlines_str})")
if selected_countries:
    countries_str = ','.join([f"'{c.replace(chr(39), chr(39)+chr(39))}'" for c in selected_countries])
    where_clauses.append(f"r.country IN ({countries_str})")
    
fact_filter = " AND ".join(where_clauses)

# For tables without dim_airlines joined (just using r.)
where_clauses_no_join = ["1=1"]
if selected_years:
    where_clauses_no_join.append(f"flight_year IN ({years_str})")
if selected_countries:
    where_clauses_no_join.append(f"country IN ({countries_str})")
if selected_airlines:
    where_clauses_no_join.append(f"airline_id IN (SELECT airline_id FROM dim_airlines WHERE airline_name IN ({airlines_str}))")

fact_filter_no_join = " AND ".join(where_clauses_no_join)

def run_query(query):
    return con.execute(query).df()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "1. NPS Proxy (Top Airlines)", 
    "2. Pain Points", 
    "3. Seat Analytics", 
    "4. Airport Bottlenecks",
    "5. Additional Insights",
    "6. Deep Dive Analytics"
])

with tab1:
    st.header("1. Recommendation Rate (NPS Proxy)")
    st.markdown("Identifying the airlines with the highest customer recommendation rates.")
    try:
        q1 = f"""
            select a.airline_name, count(r.is_recommended) as total_reviews, avg(r.is_recommended) * 100 as recommendation_rate
            from fact_airline_reviews r join dim_airlines a on r.airline_id = a.airline_id
            where {fact_filter}
            group by 1 having count(r.is_recommended) >= {min_reviews_filter} order by recommendation_rate desc limit 20
        """
        df1 = run_query(q1)
        if not df1.empty:
            fig1 = px.bar(df1, x='airline_name', y='recommendation_rate', 
                          title='Top Airlines by Recommendation Rate',
                          labels={'recommendation_rate': 'Recommendation Rate (%)', 'airline_name': 'Airline Name'},
                          hover_data=['total_reviews'])
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.warning("No data matches the selected filters.")
    except Exception as e:
        st.error(f"Error: {e}")

with tab2:
    st.header("2. Airline Pain Points Analysis")
    st.markdown("Percentage of 1-2 star ratings across different service categories.")
    try:
        q2 = f"""
            select 'Wifi & Connectivity' as service_type, sum(case when wifi_connectivity <= 2 then 1 else 0 end) * 100.0 / count(wifi_connectivity) as bad_review_pct from fact_airline_reviews where {fact_filter_no_join}
            union all select 'Food & Beverages' as service_type, sum(case when food_beverages <= 2 then 1 else 0 end) * 100.0 / count(food_beverages) as bad_review_pct from fact_airline_reviews where {fact_filter_no_join}
            union all select 'Inflight Entertainment' as service_type, sum(case when inflight_entertainment <= 2 then 1 else 0 end) * 100.0 / count(inflight_entertainment) as bad_review_pct from fact_airline_reviews where {fact_filter_no_join}
        """
        df2 = run_query(q2)
        if not df2.empty and not df2['bad_review_pct'].isnull().all():
            fig2 = px.bar(df2, x='service_type', y='bad_review_pct', color='service_type',
                          title='Proportion of 1-2 Star Ratings by Service Category',
                          labels={'bad_review_pct': '1-2 Star Rating (%)', 'service_type': 'Service Category'})
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No data matches the selected filters.")
    except Exception as e:
        st.error(f"Error: {e}")

with tab3:
    st.header("3. Seat Class & Customer Satisfaction")
    try:
        q3 = f"""
            select seat_type, avg(seat_comfort) as avg_comfort, avg(cabin_staff_service) as avg_staff, avg(food_beverages) as avg_food, count(*) as sample_size
            from fact_airline_reviews where seat_type in ('Economy Class', 'Business Class', 'First Class', 'Premium Economy') 
            and {fact_filter_no_join}
            group by 1 order by avg_comfort desc
        """
        df3 = run_query(q3)
        st.dataframe(df3)
    except Exception as e:
        st.error(f"Error: {e}")

with tab4:
    st.header("4. Airport Bottlenecks")
    st.markdown("Identifying airports with the lowest queuing and cleanliness scores. (Note: Airport reviews do not have flight_year/airline dimensions)")
    try:
        q4 = f"""
            select a.airport_name, count(r.airport_id) as total_reviews, avg(r.queuing_times) as avg_queuing, avg(r.terminal_cleanliness) as avg_cleanliness
            from fact_airport_reviews r join dim_airports a on r.airport_id = a.airport_id
            group by 1 having count(r.airport_id) >= {min_reviews_filter} order by avg_queuing asc, avg_cleanliness asc limit 15
        """
        df4 = run_query(q4)
        if not df4.empty:
            fig4 = px.scatter(df4, x='avg_queuing', y='avg_cleanliness', size='total_reviews', color='airport_name',
                              title='Queuing vs. Cleanliness Analysis (Lower is Worse)',
                              labels={'avg_queuing': 'Queuing Score', 'avg_cleanliness': 'Cleanliness Score'},
                              hover_data=['total_reviews'])
            st.plotly_chart(fig4, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

with tab5:
    st.header("5. Additional Insights")
    
    st.subheader("5.1. Satisfaction Trends Over Time")
    try:
        q5 = f"""
            select flight_year, avg(seat_comfort + cabin_staff_service + value_for_money)/3.0 as overall_score, count(*) as total
            from fact_airline_reviews where flight_year between 2010 and 2024 and {fact_filter_no_join}
            group by 1 order by flight_year
        """
        df5 = run_query(q5)
        if not df5.empty:
            st.line_chart(df5.set_index('flight_year')['overall_score'])
    except Exception as e:
        st.error(f"Error: {e}")

    st.subheader("5.2. Aircraft with Lowest Seat Comfort")
    try:
        q6 = f"""
            select aircraft_type, avg(seat_comfort) as avg_seat_comfort, count(*) as total_reviews
            from fact_airline_reviews where aircraft_type is not null and {fact_filter_no_join}
            group by 1 having count(*) >= {min_reviews_filter} order by avg_seat_comfort asc limit 15
        """
        df6 = run_query(q6)
        if not df6.empty:
            fig6 = px.bar(df6, x='avg_seat_comfort', y='aircraft_type', orientation='h', title='Top 15 Aircraft Types by Lowest Seat Comfort', hover_data=['total_reviews'])
            st.plotly_chart(fig6, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

    st.subheader("5.3. Value for Money by Traveller Type")
    try:
        q7 = f"""
            select type_of_traveller as traveller_type, avg(value_for_money) as avg_value, avg(seat_comfort) as avg_comfort, count(*) as total_reviews
            from fact_airline_reviews where type_of_traveller is not null and {fact_filter_no_join}
            group by 1 order by avg_value desc
        """
        df7 = run_query(q7)
        if not df7.empty:
            fig7 = px.bar(df7, x='traveller_type', y='avg_value', title='Average Value For Money by Traveller Type', hover_data=['total_reviews'])
            st.plotly_chart(fig7, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

with tab6:
    st.header("6. Deep Dive Analytics")
    st.markdown("---")
    
    st.subheader("6.1. Key Drivers of Recommendation")
    st.markdown("Analyzing which service factors have the strongest correlation with passenger recommendation rates.")
    try:
        q_ba1 = f"""
            select 
                corr(seat_comfort, is_recommended) as "Seat Comfort",
                corr(cabin_staff_service, is_recommended) as "Cabin Staff",
                corr(food_beverages, is_recommended) as "Food & Beverages",
                corr(inflight_entertainment, is_recommended) as "Entertainment",
                corr(wifi_connectivity, is_recommended) as "Wifi",
                corr(ground_service, is_recommended) as "Ground Service",
                corr(value_for_money, is_recommended) as "Value for Money"
            from fact_airline_reviews where {fact_filter_no_join}
        """
        df_ba1 = run_query(q_ba1)
        if not df_ba1.empty and not df_ba1.isnull().all().all():
            df_melted = df_ba1.melt(var_name='Service Category', value_name='Correlation Coefficient')
            fig_ba1 = px.bar(df_melted, x='Correlation Coefficient', y='Service Category', orientation='h', title='Impact of Service Categories on Recommendation Rates')
            st.plotly_chart(fig_ba1, use_container_width=True)
            st.markdown("**Observation:** Value for Money and Cabin Staff Service generally exhibit the highest correlation with customer recommendation.")
        else:
            st.warning("Not enough variance in the filtered data to calculate correlations.")
    except Exception as e:
        st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("6.2. Pre vs. Post-COVID Impact")
    st.markdown("Evaluating service quality trends to identify potential cost-cutting measures post-pandemic.")
    try:
        q_ba2 = f"""
            select 
                flight_year,
                avg(food_beverages) as avg_food,
                avg(cabin_staff_service) as avg_staff,
                avg(seat_comfort) as avg_seat
            from fact_airline_reviews
            where flight_year between 2018 and 2024 and {fact_filter_no_join}
            group by 1 order by flight_year
        """
        df_ba2 = run_query(q_ba2)
        if not df_ba2.empty:
            fig_ba2 = px.line(df_ba2, x='flight_year', y=['avg_food', 'avg_staff', 'avg_seat'], 
                              labels={'value': 'Average Score (1-5)', 'flight_year': 'Year', 'variable': 'Service Category'},
                              title='Service Quality Trends (2018 - 2024)',
                              markers=True)
            st.plotly_chart(fig_ba2, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

    st.markdown("---")
    st.subheader("6.3. Competitor Benchmarking")
    st.markdown("Comparing service touchpoints among selected airlines.")
    try:
        q_ba3 = f"""
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
            where {fact_filter}
            group by 1 having count(*) >= {min_reviews_filter}
        """
        df_ba3 = run_query(q_ba3)
        if not df_ba3.empty:
            all_airlines = sorted(df_ba3['airline_name'].tolist())
            default_airlines = [a for a in ['Qatar Airways', 'Emirates', 'Singapore Airlines', 'Cathay Pacific Airways'] if a in all_airlines]
            
            # Since the global filter already filtered airlines, this sub-selector is for the radar chart specifically
            selected_radar_airlines = st.multiselect("Select Airlines to Compare on Radar Chart", options=all_airlines, default=default_airlines)
            
            if selected_radar_airlines:
                df_ba3_filtered = df_ba3[df_ba3['airline_name'].isin(selected_radar_airlines)]
                import plotly.graph_objects as go
                categories = ['seat_comfort', 'cabin_staff_service', 'food_beverages', 'inflight_entertainment', 'wifi_connectivity', 'ground_service', 'value_for_money']
                fig_ba3 = go.Figure()
                for idx, row in df_ba3_filtered.iterrows():
                    fig_ba3.add_trace(go.Scatterpolar(
                        r=[row[c] for c in categories],
                        theta=categories,
                        fill='toself',
                        name=f"{row['airline_name']} ({row['total_reviews']} reviews)"
                    ))
                fig_ba3.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 5])), showlegend=True, title='Radar Chart: Competitor Benchmarking')
                st.plotly_chart(fig_ba3, use_container_width=True)
            else:
                st.warning("Please select at least one airline to benchmark.")
        else:
            st.warning("No airlines met the minimum reviews threshold with the current filters.")
    except Exception as e:
        st.error(f"Error: {e}")
