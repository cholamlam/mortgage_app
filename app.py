import streamlit as st
import plotly.graph_objects as go


st.title("🏡 Mortgage Calculator")

# Nhập thông tin cơ bản
loan_amount = st.number_input("Loan amount (USD)", value=300000, step=1000)
interest_rate = st.number_input("Annual interest rate (%)", value=4.0, step=0.1)
loan_years = st.number_input("Loan term (years)", value=30, step=1)

# Nhập thêm phần thuế
tax_rate = st.number_input("Annual property tax rate (%)", value=2.0, step=0.1)
hoa_fee = st.number_input("Monthly HOA fee (USD)", value=100.0, step=10.0)

if st.button("Calculate Monthly Payment"):
    monthly_rate = interest_rate / 100 / 12
    num_payments = loan_years * 12

    if interest_rate == 0:
        mortgage_payment = loan_amount / num_payments
    else:
        mortgage_payment = loan_amount * monthly_rate * (1 + monthly_rate) ** num_payments / ((1 + monthly_rate) ** num_payments - 1)

    # Tính tiền thuế mỗi tháng
    annual_tax = loan_amount * tax_rate / 100
    monthly_tax = annual_tax / 12

    # Tổng cộng
    total_monthly = mortgage_payment + monthly_tax + hoa_fee


    # Show results
    st.markdown(f"💰 **Monthly mortgage payment:** ${mortgage_payment:,.2f}")
    st.markdown(f"🏠 **Monthly property tax:** ${monthly_tax:,.2f}")
    st.markdown(f"🏘️ **Monthly HOA fee:** ${hoa_fee:,.2f}")
    st.success(f"📌 **Total monthly payment:** ${total_monthly:,.2f}")

    # Pie chart
    labels = ['Mortgage', 'Property Tax', 'HOA Fee']
    values = [mortgage_payment, monthly_tax, hoa_fee]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    fig.update_layout(title_text="Monthly Payment Breakdown")

    st.plotly_chart(fig)