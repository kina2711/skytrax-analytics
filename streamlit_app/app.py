import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Xóm Air - Aviation Reviews Analytics", layout="wide")

st.title("✈️ Xóm Air - Aviation Customer Experience Intelligence")
st.markdown("Dashboard phân tích Insight từ hơn 215,000 lượt reviews của hành khách toàn cầu.")

# Đường dẫn tới thư mục data parquet
data_dir = os.path.join(os.path.dirname(__file__), 'data')

@st.cache_data
def load_data(filename):
    return pd.read_parquet(os.path.join(data_dir, filename))

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏆 1. NPS Proxy (Top Airlines)", 
    "🚨 2. Pain Points", 
    "💺 3. Seat Analytics", 
    "🏢 4. Airport Bottlenecks",
    "📈 5. More Insights",
    "🧠 6. Senior BA Deep Dives"
])

with tab1:
    st.header("1. Tỷ lệ giới thiệu (NPS Proxy)")
    st.markdown("Hãng bay nào đang sở hữu tỷ lệ khách hàng 'Sẽ giới thiệu' cao nhất?")
    try:
        df1 = load_data('mart_q1_nps.parquet')
        fig1 = px.bar(df1, x='airline_name', y='recommendation_rate', 
                      title='Top 20 Hãng bay có tỷ lệ Recommend cao nhất (>100 reviews)',
                      labels={'recommendation_rate': 'Tỷ lệ Recommend (%)', 'airline_name': 'Hãng bay'})
        st.plotly_chart(fig1, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

with tab2:
    st.header("2. Bóc tách điểm đau (Airline Pain points)")
    st.markdown("Tỷ lệ phần trăm đánh giá 1-2 sao cho từng dịch vụ.")
    try:
        df2 = load_data('mart_q2_painpoints.parquet')
        fig2 = px.bar(df2, x='service_type', y='bad_review_pct', color='service_type',
                      title='Tỷ lệ nhận 1-2 sao theo từng hạng mục dịch vụ (Toàn ngành)',
                      labels={'bad_review_pct': '% Đánh giá 1-2 sao', 'service_type': 'Dịch vụ'})
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

with tab3:
    st.header("3. Hạng ghế & Sự hài lòng")
    try:
        df3 = load_data('mart_q3_seat.parquet')
        st.dataframe(df3)
    except Exception as e:
        st.error(f"Data not found: {e}")

with tab4:
    st.header("4. Bắt bệnh cảng hàng không")
    st.markdown("Sân bay nào bị phàn nàn nhiều nhất về khâu xếp hàng và vệ sinh?")
    try:
        df4 = load_data('mart_q4_airport.parquet')
        fig4 = px.scatter(df4, x='avg_queuing', y='avg_cleanliness', size='total_reviews', color='airport_name',
                          title='Phân tích Xếp hàng vs Vệ sinh (Càng thấp càng tệ)',
                          labels={'avg_queuing': 'Điểm xếp hàng (Queuing)', 'avg_cleanliness': 'Điểm vệ sinh (Cleanliness)'})
        st.plotly_chart(fig4, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

with tab5:
    st.header("5-10. Các Insight khác")
    
    st.subheader("5. Xu hướng hài lòng theo thời gian")
    try:
        df5 = load_data('mart_q5_temporal.parquet')
        if not df5.empty:
            st.line_chart(df5.set_index('flight_year')['overall_score'])
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.subheader("6. Máy bay bị phàn nàn nhiều nhất về độ thoải mái")
    try:
        df6 = load_data('mart_q6_aircraft.parquet')
        fig6 = px.bar(df6, x='avg_seat_comfort', y='aircraft_type', orientation='h', title='Top 15 Máy bay có điểm Seat Comfort thấp nhất')
        st.plotly_chart(fig6, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.subheader("7. Loại hành khách nào dễ tính nhất?")
    try:
        df7 = load_data('mart_q7_traveller.parquet')
        fig7 = px.bar(df7, x='traveller_type', y='avg_value', title='Điểm trung bình Value For Money theo loại hành khách')
        st.plotly_chart(fig7, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")
    
    st.subheader("8. Verified vs Unverified Reviews")
    try:
        df8 = load_data('mart_q8_verified.parquet')
        df8['is_verified_label'] = df8['is_verified'].map({1: 'Verified', 0: 'Not Verified'})
        st.dataframe(df8)
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.subheader("9. Phòng chờ (Lounge) nào xịn nhất?")
    try:
        df9 = load_data('mart_q9_lounge.parquet')
        fig9 = px.scatter(df9, x='avg_comfort', y='avg_cleanliness', color='lounge_airline', size='total_reviews', title='Phân tích Phòng chờ: Độ thoải mái vs Vệ sinh')
        st.plotly_chart(fig9, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.subheader("10. Quốc gia khắt khe nhất")
    try:
        df10 = load_data('mart_q10_demographics.parquet')
        fig10 = px.bar(df10, x='country', y='avg_score', title='Top 10 Quốc gia chấm điểm Value for Money thấp nhất (>500 reviews)')
        st.plotly_chart(fig10, use_container_width=True)
    except Exception as e:
        st.error(f"Data not found: {e}")

with tab6:
    st.header("🧠 Phân tích chuyên sâu (Senior BA)")
    st.markdown("---")
    
    st.subheader("1. Động lực cốt lõi (Key Drivers of Recommendation)")
    st.markdown("Yếu tố nào quyết định đến sự hài lòng và sẵn sàng giới thiệu của khách hàng?")
    try:
        df_ba1 = load_data('mart_ba_drivers.parquet')
        df_melted = df_ba1.melt(var_name='Dịch vụ', value_name='Độ tương quan (Correlation)')
        fig_ba1 = px.bar(df_melted, x='Độ tương quan (Correlation)', y='Dịch vụ', orientation='h', title='Mức độ ảnh hưởng của các dịch vụ đến Tỷ lệ Recommend')
        st.plotly_chart(fig_ba1, use_container_width=True)
        st.info("💡 **Insight:** Value for Money và Cabin Staff Service là 2 yếu tố quyết định lớn nhất. Hãng hàng không nên tập trung tối ưu trải nghiệm phục vụ của nhân viên thay vì chỉ tập trung vào đồ ăn hay wifi.")
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.markdown("---")
    st.subheader("2. Tác động của Đại dịch (Pre vs Post-COVID)")
    st.markdown("Các hãng hàng không có đang cắt giảm chi phí dịch vụ sau đại dịch?")
    try:
        df_ba2 = load_data('mart_ba_covid_trend.parquet')
        df_ba2 = df_ba2[df_ba2['flight_year'] <= 2024]
        fig_ba2 = px.line(df_ba2, x='flight_year', y=['avg_food', 'avg_staff', 'avg_seat'], 
                          labels={'value': 'Điểm trung bình (1-5)', 'flight_year': 'Năm', 'variable': 'Dịch vụ'},
                          title='Xu hướng Chất lượng Dịch vụ (2018 - 2024)')
        st.plotly_chart(fig_ba2, use_container_width=True)
        st.info("💡 **Insight:** Điểm Food & Beverages giảm rõ rệt sau 2020, phản ánh làn sóng cắt giảm chi phí suất ăn của các hãng hàng không. Trong khi đó, Seat Comfort hầu như không thay đổi.")
    except Exception as e:
        st.error(f"Data not found: {e}")

    st.markdown("---")
    st.subheader("3. Benchmark Đối thủ: Trận chiến của các Ông lớn")
    st.markdown("So sánh điểm chạm dịch vụ giữa Qatar Airways, Emirates, Singapore Airlines và Cathay Pacific.")
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
