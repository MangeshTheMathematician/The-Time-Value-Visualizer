import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Interest Visualizer", layout="wide")

st.title("Simple vs. Compound Interest: The Magic of Time")
st.markdown("""
Welcome! This app explains the math behind how money grows (or shrinks when looking backwards in time). 
We will break down all the complex formulas into plain English so you can see exactly how your money behaves over time.
""")

# ==========================================
# SIDEBAR: USER INPUTS
# ==========================================
st.sidebar.header("Input Your Numbers")

P = st.sidebar.number_input("Starting Money (Principal)", value=100000, step=1000)
r_simple_input = st.sidebar.number_input("Simple Interest Rate (%)", value=5.0, step=0.1)
r_comp_input = st.sidebar.number_input("Compound Interest Rate (%)", value=4.5, step=0.1)
t_max = st.sidebar.slider("Time Horizon (Years)", min_value=5, max_value=50, value=30, step=5)

st.sidebar.markdown("---")
st.sidebar.header("Present Value Goal")
fv_target = st.sidebar.number_input("Target Future Amount", value=500000, step=10000)

# Convert percentage to decimals for math
r_simple = r_simple_input / 100
r_comp = r_comp_input / 100

# ==========================================
# DATA CALCULATION
# ==========================================
years = np.arange(0, t_max + 1)

# Future Value & Cumulative Interest Data
df = pd.DataFrame({'Year': years})
df['Simple_FV'] = P * (1 + r_simple * df['Year'])
df['Comp_FV'] = P * ((1 + r_comp) ** df['Year'])
df['Simple_Interest'] = df['Simple_FV'] - P
df['Comp_Interest'] = df['Comp_FV'] - P

# Year-by-Year Compound Breakdown (For Graph 2)
# To prove how interest applies on new value:
df['Comp_New_Interest_This_Year'] = df['Comp_FV'].diff().fillna(0)
df['Comp_Base_Before_This_Year'] = df['Comp_FV'].shift(1).fillna(P)

# Present Value Data
df['Simple_PV'] = fv_target / (1 + r_simple * df['Year'])
df['Comp_PV'] = fv_target / ((1 + r_comp) ** df['Year'])
df['Simple_PV_Interest'] = fv_target - df['Simple_PV']
df['Comp_PV_Interest'] = fv_target - df['Comp_PV']


# ==========================================
# GRAPH 1: CUMULATIVE INTEREST (PROFIT)
# ==========================================
st.header("1. The Profit (Cumulative Interest)")
st.info("**Layman Translation:** This shows *only* the extra money you made, not your starting money. Simple interest is a straight ladder—you get the exact same cash bonus every year. Compound interest is a snowball rolling down a hill—it grows a little at first, but gets massive as it picks up speed.")

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("### The Formulas")
    st.markdown("**Simple Interest:**")
    st.latex(r"I_{simple}(t) = P \cdot r \cdot t")
    st.markdown("**Compound Interest:**")
    st.latex(r"I_{comp}(t) = P \cdot [(1 + r)^t - 1]")

with col2:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df['Year'], y=df['Simple_Interest'], mode='lines', name='Simple Interest', line=dict(color='#1f77b4', width=3)))
    fig1.add_trace(go.Scatter(x=df['Year'], y=df['Comp_Interest'], mode='lines', name='Compound Interest', line=dict(color='#ff7f0e', width=3)))
    fig1.update_layout(title="Cumulative Interest Over Time", xaxis_title="Years", yaxis_title="Total Interest Earned ($)", hovermode="x unified")
    st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ==========================================
# GRAPH 2: TOTAL AMOUNT & PROOF OF COMPOUNDING
# ==========================================
st.header("2. Total Amount (Future Value) & The 'Interest on Interest' Proof")
st.info("**Layman Translation:** This shows your starting money PLUS the profit. Look at the bar chart below: see how the new orange chunk (this year's interest) gets bigger every single year? That's because it's calculated on a larger base amount, not just your initial seed. That is the magic of compounding.")

col3, col4 = st.columns([1, 2])
with col3:
    st.markdown("### The Formulas")
    st.markdown("**Simple Future Value:**")
    st.latex(r"FV_{simple} = P(1 + r \cdot t)")
    st.markdown("**Compound Future Value:**")
    st.latex(r"FV_{comp} = P(1 + r)^t")

with col4:
    # We use a stacked bar/line combo to PROVE the compounding effect year by year
    fig2 = go.Figure()
    
    # Adding line for Simple FV
    fig2.add_trace(go.Scatter(x=df['Year'], y=df['Simple_FV'], mode='lines', name='Simple Total (Line)', line=dict(color='#1f77b4', dash='dash')))
    
    # Adding stacked bars to prove compound growth mechanics
    fig2.add_trace(go.Bar(x=df['Year'], y=[P]*len(df), name='Initial Principal', marker_color='#2ca02c'))
    
    # The interest accumulated in past years
    past_interest = df['Comp_Base_Before_This_Year'] - P
    fig2.add_trace(go.Bar(x=df['Year'], y=past_interest, name='Past Compounded Interest', marker_color='#ffbb78'))
    
    # The new interest earned THIS year
    fig2.add_trace(go.Bar(x=df['Year'], y=df['Comp_New_Interest_This_Year'], name='New Interest Added This Year', marker_color='#d62728'))

    fig2.update_layout(barmode='stack', title="Proving Compound Growth Year-by-Year", xaxis_title="Years", yaxis_title="Total Account Value ($)", hovermode="x unified")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ==========================================
# GRAPH 3 & 4: PRESENT VALUE
# ==========================================
st.header("3 & 4. Present Value (Time-Traveling Your Money)")
st.info(f"**Layman Translation:** Imagine you need exactly **${fv_target:,.0f}** in the future to buy a house. *Present Value* asks: 'How much cash do I need to lock away TODAY to reach that goal?' The longer you have to wait, the less money you need to put in today because time does the heavy lifting for you.")

col5, col6 = st.columns([1, 2])
with col5:
    st.markdown("### The Formulas")
    st.markdown("**Simple Present Value:**")
    st.latex(r"PV_{simple} = \frac{FV}{1 + r \cdot t}")
    st.markdown("**Compound Present Value:**")
    st.latex(r"PV_{comp} = \frac{FV}{(1 + r)^t}")

with col6:
    # Subplots to show the two PV graphs requested
    fig3 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, 
                         subplot_titles=("How much you need TODAY (Present Value)", "How much the market pays for you (Interest)"))
    
    # Graph 3: PV Curve
    fig3.add_trace(go.Scatter(x=df['Year'], y=df['Simple_PV'], mode='lines', name='PV (Simple)', line=dict(color='#1f77b4')), row=1, col=1)
    fig3.add_trace(go.Scatter(x=df['Year'], y=df['Comp_PV'], mode='lines', name='PV (Compound)', line=dict(color='#ff7f0e')), row=1, col=1)
    
    # Graph 4: Interest component in PV
    fig3.add_trace(go.Scatter(x=df['Year'], y=df['Simple_PV_Interest'], mode='lines', name='Interest Earned (Simple)', line=dict(color='#1f77b4', dash='dot')), row=2, col=1)
    fig3.add_trace(go.Scatter(x=df['Year'], y=df['Comp_PV_Interest'], mode='lines', name='Interest Earned (Compound)', line=dict(color='#ff7f0e', dash='dot')), row=2, col=1)

    fig3.update_layout(height=600, title=f"Working Backwards from a Target of ${fv_target:,.0f}", hovermode="x unified")
    fig3.update_yaxes(title_text="Required Starting Cash ($)", row=1, col=1)
    fig3.update_yaxes(title_text="Free Money (Interest $)", row=2, col=1)
    fig3.update_xaxes(title_text="Years to Grow", row=2, col=1)

    st.plotly_chart(fig3, use_container_width=True)