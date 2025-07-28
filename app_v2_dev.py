import streamlit as st
import plotly.graph_objects as go

st.title("🏡 Mortgage Calculator")


# Default values
if "home_price" not in st.session_state:
    st.session_state.home_price = 500000
if "down_payment_usd" not in st.session_state:
    st.session_state.down_payment_usd = 100000
if "down_payment_percent" not in st.session_state:
    st.session_state.down_payment_percent = st.session_state.down_payment_usd / st.session_state.home_price * 100

# Input Home Price 

home_price = st.number_input("Home Price (USD)", value=st.session_state.home_price, step=1000, key="home_price_input")



# Columns for down payment in USD and percent
col1, col2 = st.columns(2)

# Input Loan Amount
with col1:
    down_payment_usd = st.number_input("Down Payment (USD)", value=st.session_state.down_payment_usd, step=1000, key="down_payment_usd_input")
with col2:
    down_payment_percent = st.number_input("Percentage (%)", value=st.session_state.down_payment_percent, step=0.25, key="down_payment_percent_input")



# Sync Logic

if st.session_state.home_price_input != st.session_state.home_price:
    # User changed home price → update percent
    st.session_state.home_price = st.session_state.home_price_input
    st.session_state.down_payment_percent = round(st.session_state.down_payment_usd / st.session_state.home_price * 100, 2)
    st.rerun()


if st.session_state.down_payment_usd_input != st.session_state.down_payment_usd:
    #User changed USD -> Update USD and %
    st.session_state.home_price = st.session_state.home_price_input
    st.session_state.down_payment_usd = st.session_state.down_payment_usd_input
    st.session_state.down_payment_percent = round(st.session_state.down_payment_usd / home_price * 100, 2)
    st.rerun()

elif st.session_state.down_payment_percent_input != st.session_state.down_payment_percent:
    #User changed % -> Update % and USD
    st.session_state.home_price = st.session_state.home_price_input
    st.session_state.down_payment_percent = st.session_state.down_payment_percent_input
    st.session_state.down_payment_usd = round(st.session_state.down_payment_percent / 100 * home_price)
    st.rerun() 

st.session_state.home_price = st.session_state.home_price_input

#Small Output

loan_amount = st.session_state.home_price - st.session_state.down_payment_usd
st.write(f"📌 You will put down **${st.session_state.down_payment_usd:,.0f}** ({st.session_state.down_payment_percent:.2f}%)")
st.write(f"📌 Loan Amount: **${loan_amount:,.2f}**")


# Others

interest_rate = st.number_input("Annual interest rate (%)", value=4.0, step=0.1)
loan_years = st.number_input("Loan term (years)", value=30, step=1)
tax_rate = st.number_input("Annual property tax rate (%)", value=2.0, step=0.1)
hoa_fee = st.number_input("Monthly HOA fee (USD)", value=50.0, step=10.0)


#Output

if st.button("Calculate Monthly Payment"):
    monthly_rate = interest_rate / 100 / 12
    num_payments = loan_years * 12

    if interest_rate == 0:
        mortgage_payment = loan_amount / num_payments
    else:
        mortgage_payment = loan_amount * monthly_rate * (1 + monthly_rate) ** num_payments / ((1 + monthly_rate) ** num_payments - 1)

    # Tax Calculation
    annual_tax = st.session_state.home_price * tax_rate / 100
    monthly_tax = annual_tax / 12

    # Total Money 
    total_monthly = mortgage_payment + monthly_tax + hoa_fee


    # Show results
    st.markdown(f"💰 **Monthly Principle and Interest:** ${mortgage_payment:,.2f}")
    st.markdown(f"🏠 **Monthly property tax:** ${monthly_tax:,.2f}")
    st.markdown(f"🏘️ **Monthly HOA fee:** ${hoa_fee:,.2f}")
    st.success(f"📌 **Total monthly payment:** ${total_monthly:,.2f}")

    # Pie chart
    labels = ['Mortgage', 'Property Tax', 'HOA Fee']
    values = [mortgage_payment, monthly_tax, hoa_fee]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    fig.update_layout(title_text="Monthly Payment Breakdown")

    st.plotly_chart(fig)