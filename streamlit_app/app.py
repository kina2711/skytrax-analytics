import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Xóm Air - Aviation Reviews Analytics", layout="wide")

st.title("Xóm Air - Aviation Customer Experience Intelligence")
st.markdown("An analytical dashboard deriving insights from over 215,000 global passenger reviews.")

# Directory for parquet files
data_dir = os.path.join(os.path.dirname(__file__), 'data')

@st.cache_data
def load_data(filename):
    return pd.read_parquet(os.path.join(data_dir, filename))

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
        df1 = load_data('mart_q1_nps.parquet')
        fig1 = px.bar(df1, x='airline_name', y='recommendation_rate', 
                      title='Top 20 Airlines by Recommendation Rate (>100 reviews)',
                      labels={'recommendation_rate': 'Recommendation Rate (%)', 'airline_name': 'Airline Name'})
        st.plotly_chart(fig1, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

with tab2:
    st.header("2. Airline Pain Points Analysis")
    st.markdown("Percentage of 1-2 star ratings across different service categories.")
    try:
        df2 = load_data('mart_q2_painpoints.parquet')
        fig2 = px.bar(df2, x='service_type', y='bad_review_pct', color='service_type',
                      title='Proportion of 1-2 Star Ratings by Service Category (Industry Average)',
                      labels={'bad_review_pct': '1-2 Star Rating (%)', 'service_type': 'Service Category'})
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

with tab3:
    st.header("3. Seat Class & Customer Satisfaction")
    try:
        df3 = load_data('mart_q3_seat.parquet')
        st.dataframe(df3)
    except Exception as e:
        st.error(f"Data not found: {e}")

with tab4:
    st.header("4. Airport Bottlenecks")
    st.markdown("Identifying airports with the lowest queuing and cleanliness scores.")
    try:
        df4 = load_data('mart_q4_airport.parquet')
        fig4 = px.scatter(df4, x='avg_queuing', y='avg_cleanliness', size='total_reviews', color='airport_name',
                          title='Queuing vs. Cleanliness Analysis (Lower is Worse)',
                          labels={'avg_queuing': 'Queuing Score', 'avg_cleanliness': 'Cleanliness Score'})
        st.plotly_chart(fig4, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

with tab5:
    st.header("5. Additional Insights")
    
    st.subheader("5.1. Satisfaction Trends Over Time")
    try:
        df5 = load_data('mart_q5_temporal.parquet')
        if not df5.empty:
            st.line_chart(df5.set_index('flight_year')['overall_score'])
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.subheader("5.2. Aircraft with Lowest Seat Comfort")
    try:
        df6 = load_data('mart_q6_aircraft.parquet')
        fig6 = px.bar(df6, x='avg_seat_comfort', y='aircraft_type', orientation='h', title='Top 15 Aircraft Types by Lowest Seat Comfort')
        st.plotly_chart(fig6, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.subheader("5.3. Value for Money by Traveller Type")
    try:
        df7 = load_data('mart_q7_traveller.parquet')
        fig7 = px.bar(df7, x='traveller_type', y='avg_value', title='Average Value For Money by Traveller Type')
        st.plotly_chart(fig7, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")
    
    st.subheader("5.4. Verified vs. Unverified Reviews")
    try:
        df8 = load_data('mart_q8_verified.parquet')
        df8['is_verified_label'] = df8['is_verified'].map({1: 'Verified', 0: 'Not Verified'})
        st.dataframe(df8)
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.subheader("5.5. Premium Lounge Analysis")
    try:
        df9 = load_data('mart_q9_lounge.parquet')
        fig9 = px.scatter(df9, x='avg_comfort', y='avg_cleanliness', color='lounge_airline', size='total_reviews', title='Lounge Analysis: Comfort vs. Cleanliness')
        st.plotly_chart(fig9, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.subheader("5.6. Strictest Demographics")
    try:
        df10 = load_data('mart_q10_demographics.parquet')
        fig10 = px.bar(df10, x='country', y='avg_score', title='Top 10 Countries with Lowest Value for Money Scores (>500 reviews)')
        st.plotly_chart(fig10, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

with tab6:
    st.header("6. Deep Dive Analytics")
    st.markdown("---")
    
    st.subheader("6.1. Key Drivers of Recommendation")
    st.markdown("Analyzing which service factors have the strongest correlation with passenger recommendation rates.")
    try:
        df_ba1 = load_data('mart_ba_drivers.parquet')
        df_melted = df_ba1.melt(var_name='Service Category', value_name='Correlation Coefficient')
        fig_ba1 = px.bar(df_melted, x='Correlation Coefficient', y='Service Category', orientation='h', title='Impact of Service Categories on Recommendation Rates')
        st.plotly_chart(fig_ba1, use_container_width=True)
        st.markdown("**Observation:** Value for Money and Cabin Staff Service exhibit the highest correlation with customer recommendation. Airlines should prioritize crew training and service quality over secondary amenities like Wi-Fi.")
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.markdown("---")
    st.subheader("6.2. Pre vs. Post-COVID Impact")
    st.markdown("Evaluating service quality trends to identify potential cost-cutting measures post-pandemic.")
    try:
        df_ba2 = load_data('mart_ba_covid_trend.parquet')
        df_ba2 = df_ba2[df_ba2['flight_year'] <= 2024]
        fig_ba2 = px.line(df_ba2, x='flight_year', y=['avg_food', 'avg_staff', 'avg_seat'], 
                          labels={'value': 'Average Score (1-5)', 'flight_year': 'Year', 'variable': 'Service Category'},
                          title='Service Quality Trends (2018 - 2024)')
        st.plotly_chart(fig_ba2, use_container_width=True)
        st.markdown("**Observation:** Food & Beverages scores show a significant decline post-2020, likely indicating industry-wide cost-cutting measures in catering. In contrast, Seat Comfort remains relatively stable.")
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.markdown("---")
    st.subheader("6.3. Competitor Benchmarking")
    st.markdown("Comparing service touchpoints among Qatar Airways, Emirates, Singapore Airlines, and Cathay Pacific.")
    try:
        df_ba3 = load_data('mart_ba_competitors.parquet')
        import plotly.graph_objects as go
        categories = ['seat_comfort', 'cabin_staff_service', 'food_beverages', 'inflight_entertainment', 'wifi_connectivity', 'ground_service', 'value_for_money']
        fig_ba3 = go.Figure()
        for idx, row in df_ba3.iterrows():
            fig_ba3.add_trace(go.Scatterpolar(
                r=[row[c] for c in categories],
                theta=categories,
                fill='toself',
                name=row['airline_name']
            ))
        fig_ba3.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 5])), showlegend=True, title='Radar Chart: Competitor Benchmarking')
        st.plotly_chart(fig_ba3, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")
