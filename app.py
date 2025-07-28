
import streamlit as st
import plotly.graph_objects as go

st.title("🏡 Mortgage Calculator")

# Default values
if "home_price" not in st.session_state:
    st.session_state.home_price = 500000.0
if "down_payment_usd" not in st.session_state:
    st.session_state.down_payment_usd = 100000.0
if "down_payment_percent" not in st.session_state:
    st.session_state.down_payment_percent = st.session_state.down_payment_usd / st.session_state.home_price * 100

if "insurance_usd" not in st.session_state:
    st.session_state.insurance_usd = 5000.0
if "insurance_percent" not in st.session_state:
    st.session_state.insurance_percent = st.session_state.insurance_usd / st.session_state.home_price * 100

# Input Home Price 
home_price = st.number_input("Home Price (USD)", value=float(st.session_state.home_price), step=1000.0, key="home_price_input")

# Down payment columns
col1, col2 = st.columns(2)
with col1:
    down_payment_usd = st.number_input("Down Payment (USD)", value=float(st.session_state.down_payment_usd), step=1000.0, key="down_payment_usd_input")
with col2:
    down_payment_percent = st.number_input("Percentage (%)", value=float(st.session_state.down_payment_percent), step=0.25, key="down_payment_percent_input")


# Sync Logic
if st.session_state.home_price_input != st.session_state.home_price:
    st.session_state.home_price = st.session_state.home_price_input
    st.session_state.down_payment_percent = round(st.session_state.down_payment_usd / st.session_state.home_price * 100, 2)
    st.session_state.insurance_percent = round(st.session_state.insurance_usd / st.session_state.home_price * 100, 2)
    st.rerun()

# Down payment sync
if st.session_state.down_payment_usd_input != st.session_state.down_payment_usd:
    st.session_state.down_payment_usd = st.session_state.down_payment_usd_input
    st.session_state.down_payment_percent = round(st.session_state.down_payment_usd / home_price * 100, 2)
    st.rerun()
elif st.session_state.down_payment_percent_input != st.session_state.down_payment_percent:
    st.session_state.down_payment_percent = st.session_state.down_payment_percent_input
    st.session_state.down_payment_usd = round(st.session_state.down_payment_percent / 100 * home_price)
    st.rerun()

# Small Output
loan_amount = st.session_state.home_price - st.session_state.down_payment_usd
st.write(f"<span style='font-size: 0.8em;'>📌 You will put down **${st.session_state.down_payment_usd:,.0f}** ({st.session_state.down_payment_percent:.2f}%)</span>", unsafe_allow_html=True)
st.write(f"<span style='font-size: 0.8em;'>📌 Loan Amount: **${loan_amount:,.2f}**</span>", unsafe_allow_html=True)

#PMI Warning: 
show_pmi_option = False 
if st.session_state.down_payment_percent < 20: 
    st.markdown("**⚠️ Down payment is less than 20%. PMI may apply.**")
    show_pmi_option = True

#PMI Input
pmi_monthly = 0
if show_pmi_option:
    enable_pmi = st.checkbox("Include PMI?")
    if enable_pmi:
        pmi_rate = st.number_input("PMI annual rate (%)", value=0.5, step=0.1)
        pmi_monthly = loan_amount * pmi_rate / 100 / 12
        pmi_yearly = pmi_monthly * 12
        st.markdown(f"<span style='font-size: 0.7em;'>🔐 Yearly PMI: **${pmi_yearly:,.2f}**</span>", unsafe_allow_html=True)


# Others
interest_rate = st.number_input("Annual interest rate (%)", value=4.0, step=0.1)
loan_years = st.number_input("Loan term (years)", value=30, step=1)
tax_rate = st.number_input("Annual property tax rate (%)", value=2.0, step=0.1)

# Insurance columns
col3, col4 = st.columns(2)
with col3:
    insurance_usd_input = st.number_input("Insurance (USD/year)", value=float(st.session_state.insurance_usd), step=100.0, key="insurance_usd_input")
with col4:
    insurance_percent_input = st.number_input("Insurance (%)", value=float(st.session_state.insurance_percent), step=0.1, key="insurance_percent_input")

# Insurance sync
if st.session_state.insurance_usd_input != st.session_state.insurance_usd:
    st.session_state.insurance_usd = st.session_state.insurance_usd_input
    st.session_state.insurance_percent = round(st.session_state.insurance_usd / st.session_state.home_price * 100, 2)
    st.rerun()
elif st.session_state.insurance_percent_input != st.session_state.insurance_percent:
    st.session_state.insurance_percent = st.session_state.insurance_percent_input
    st.session_state.insurance_usd = round(st.session_state.insurance_percent / 100 * st.session_state.home_price)
    st.rerun()

hoa_fee = st.number_input("Monthly HOA fee (USD)", value=50.0, step=10.0)
hoa_fee_yearly = hoa_fee * 12
st.markdown(f"<span style='font-size: 0.7em;'>🌸 Annual HOA: **${hoa_fee_yearly:,.2f}**</span>", unsafe_allow_html=True)


# Output
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

    # Monthly Insurance
    monthly_insurance = st.session_state.insurance_usd / 12

    # Total Monthly Payment
    total_monthly = mortgage_payment + monthly_tax + monthly_insurance + hoa_fee + pmi_monthly


    # Show results
    st.markdown(f"💰 **Monthly Principle and Interest:** ${mortgage_payment:,.2f}")
    st.markdown(f"🏠 **Monthly property tax:** ${monthly_tax:,.2f}")
    st.markdown(f"🛡️ **Monthly Insurance:** ${monthly_insurance:,.2f}")
    st.markdown(f"🌸 **Monthly HOA fee:** ${hoa_fee:,.2f}")
    if pmi_monthly > 0:
        st.markdown(f"🔐 **Monthly PMI:** ${pmi_monthly:,.2f}")
    st.success(f"📌 **Total monthly payment:** ${total_monthly:,.2f}")

    # Pie chart
    # labels = ['Mortgage', 'Property Tax','Insurance', 'HOA Fee', 'PMI']
    # values = [mortgage_payment, monthly_tax, monthly_insurance, hoa_fee, pmi_monthly]

    labels = []
    values = []

    if mortgage_payment > 0:
        labels.append("Mortgage")
        values.append(mortgage_payment)

    if monthly_tax > 0:
        labels.append("Property Tax")
        values.append(monthly_tax)

    if monthly_insurance > 0:
        labels.append("Insurance")
        values.append(monthly_insurance)

    if hoa_fee > 0:
        labels.append("HOA Fee")
        values.append(hoa_fee)

    if pmi_monthly > 0:
        labels.append("PMI")
        values.append(pmi_monthly)

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    fig.update_layout(title_text="Monthly Payment Breakdown")

    st.plotly_chart(fig)
