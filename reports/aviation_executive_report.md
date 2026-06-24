# BÁO CÁO QUẢN TRỊ: SKYTRAX ANALYTICS PLATFORM
**To:** C-Level Executives, Strategy Directors
**From:** Data Engineering & Analytics Team
**Date:** June 2026
**Subject:** Khai thác Insight Khách hàng Toàn cầu & Đề xuất Chiến lược

---

## I. TÓM TẮT THỰC THI (EXECUTIVE SUMMARY)
Báo cáo định lượng phân tích dựa trên tập dữ liệu 215,000 lượt đánh giá từ Skytrax. Phân tích tập trung vào các điểm nghẽn trong quy trình cung cấp dịch vụ, phân bổ chi phí hậu đại dịch, và đối chuẩn cạnh tranh (benchmarking).

**Kết luận cốt lõi:** Ngành hàng không ghi nhận sự sụt giảm chỉ số chất lượng dịch vụ ăn uống (Food & Beverages) hậu đại dịch. Yếu tố có trọng số cao nhất định đoạt tỷ lệ khách hàng giới thiệu (NPS Proxy) là Cabin Staff Service.

---

## II. PHÂN TÍCH CHUYÊN SÂU (KEY FINDINGS)

### 1. Động lực Cốt lõi của Lòng Trung Thành (Key Drivers of Recommendation)
- **Phát hiện:** Phân tích tương quan (Correlation Matrix) chỉ ra hai biến số **Value for Money** và **Cabin Staff Service** có hệ số tương quan tuyến tính cao nhất với tỷ lệ Recommendation (Correlation > 0.8). Biến số **Wifi & Connectivity** có hệ số tương quan thấp nhất.
- **Ý nghĩa:** Trải nghiệm dịch vụ nhân sự đóng vai trò quyết định. Nguồn lực đầu tư hạ tầng phần cứng (VD: Wifi) mang lại tỷ suất hoàn vốn (ROI) về mức độ hài lòng thấp hơn so với việc tối ưu hóa chất lượng nhân sự.

### 2. Tác động của Đại dịch (Pre vs Post-COVID Impact)
- **Phát hiện:** Chuỗi thời gian (Time-series analysis) 2018-2024 cho thấy sự sụt giảm có hệ thống ở chỉ số **Food & Beverages** bắt đầu từ 2021. 
- **Ý nghĩa:** Chỉ số phản ánh chiến lược tối ưu hóa chi phí (Cost-cutting) biên lợi nhuận của toàn ngành. Ngược lại, chỉ số Seat Comfort duy trì sự ổn định, phù hợp với đặc thù khấu hao tài sản dài hạn.

### 3. Đối chuẩn Cạnh tranh (Competitor Benchmarking)
Kết quả từ Radar Chart Benchmark cho nhóm hãng hàng không Tier-1 (Qatar Airways, Emirates, Singapore Airlines):
- **Qatar Airways & Singapore Airlines:** Duy trì chỉ số đồng đều, dẫn đầu phân khúc về Cabin Staff Service.
- **Emirates:** Có lợi thế cạnh tranh cốt lõi ở hạng mục Inflight Entertainment, tuy nhiên ghi nhận điểm số Value for Money thấp hơn mức trung bình của nhóm.

---

## III. ĐỀ XUẤT CHIẾN LƯỢC (STRATEGIC RECOMMENDATIONS)

Dựa trên dữ liệu, chúng tôi đề xuất các hướng can thiệp phân bổ nguồn lực:

> [!TIP]
> **1. Tái cấu trúc ngân sách vận hành (OPEX)**
> Ưu tiên phân bổ chi phí cho đào tạo nghiệp vụ và KPI nhân sự thay vì hạ tầng phụ trợ.

> [!WARNING]
> **2. Rủi ro từ tối ưu hóa chi phí suất ăn**
> Ngưỡng chịu đựng (Tolerance Limit) của khách hàng với Food & Beverages đã chạm mức cảnh báo. Cần xem xét lại các hợp đồng cung ứng dịch vụ Catering.

> [!NOTE]
> **3. Điều chỉnh chiến lược định vị**
> Đối với các hãng có điểm số Value for Money thấp, cần tập trung khuếch đại truyền thông vào các giá trị tiện ích cộng thêm (như Inflight Entertainment) nhằm định hình lại kỳ vọng của hành khách.

---
*Báo cáo được trích xuất từ hệ thống Data Warehouse (DuckDB). Chi tiết vui lòng truy cập Streamlit Dashboard.*
