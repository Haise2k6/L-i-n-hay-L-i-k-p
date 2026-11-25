import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tính Lãi Đơn & Lãi Kép",
    page_icon="💰",
    layout="centered",
)

st.title("💰 Công cụ tính Lãi Đơn và Lãi Kép")

# Khu vực nhập dữ liệu
st.subheader("Thông số đầu vào")
col1, col2, col3 = st.columns(3)

with col1:
    C = st.number_input(
        "Số tiền gốc (VNĐ)",
        min_value=0,
        value=100_000_000,
        step=1_000_000,
        format="%d",
    )

with col2:
    i_percent = st.number_input(
        "Lãi suất / kỳ (%)",
        min_value=0.0,
        value=1.0,
        step=0.1,
        format="%.2f",
    )
    i = i_percent / 100

with col3:
    n = st.number_input(
        "Số kỳ hạn (n)",
        min_value=1,
        value=3,
        step=1,
    )

# Tính toán
An = C * (1 + i * n)
Bn = C * ((1 + i) ** n)
chenh_lech = Bn - An

# Hiển thị kết quả
st.divider()
st.subheader("Kết quả tính toán")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric(
        label="Tổng nhận theo lãi đơn (An)",
        value=f"{An:,.0f} đ",
        delta=f"Tiền lãi: {An - C:,.0f} đ",
    )

with res_col2:
    st.metric(
        label="Tổng nhận theo lãi kép (Bn)",
        value=f"{Bn:,.0f} đ",
        delta=f"Chênh lệch so với lãi đơn: +{chenh_lech:,.0f} đ",
    )

st.info(f"**Số tiền KH nhận được theo lãi đơn:** {An:,.0f} đồng")
st.success(f"**Số tiền KH nhận được theo lãi kép:** {Bn:,.0f} đồng")

# Bảng và biểu đồ so sánh theo từng kỳ
st.divider()
st.subheader("Biểu đồ so sánh theo từng kỳ")

ky_han = list(range(1, n + 1))
df = pd.DataFrame({
    "Kỳ": ky_han,
    "Lãi đơn (VNĐ)": [C * (1 + i * k) for k in ky_han],
    "Lãi kép (VNĐ)": [C * ((1 + i) ** k) for k in ky_han],
})

st.line_chart(df.set_index("Kỳ"))

with st.expander("Xem bảng chi tiết từng kỳ"):
    st.dataframe(
        df.style.format({
            "Lãi đơn (VNĐ)": "{:,.0f}",
            "Lãi kép (VNĐ)": "{:,.0f}",
        }),
        use_container_width=True,
        hide_index=True,
    )
