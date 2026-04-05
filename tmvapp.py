import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="TVM Visualizer", layout="wide")

st.title("Simple vs. Compound Interest: The Time Value of Money")
st.markdown("""
Welcome! This app explains the math behind how money grows (or shrinks when looking backwards in time). 
We break down complex formulas into plain English so you can see exactly how your money behaves over time.
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

# Full DataFrame for plotting
df = pd.DataFrame({'Year': years})

# Future Value & Cumulative Interest
df['Simple_FV'] = P * (1 + r_simple * df['Year'])
df['Comp_FV'] = P * ((1 + r_comp) ** df['Year'])
df['Simple_Interest'] = df['Simple_FV'] - P
df['Comp_Interest'] = df['Comp_FV'] - P

# ------------------------------------------
# MARGINAL INTEREST & RATES (The "Per Term" Changes)
# ------------------------------------------
# Simple Interest Added This Year (Constant)
df['Simple_New_Interest'] = np.where(df['Year'] == 0, 0, P * r_simple)

# Compound Interest Added This Year (Growing)
df['Comp_New_Interest'] = df['Comp_FV'].diff().fillna(0)
df['Comp_Base_Before_This_Year'] = df['Comp_FV'].shift(1).fillna(P)

# The Benefit/Loss per term (Compound New Interest minus Simple New Interest)
df['Compound_Benefit_This_Year'] = df['Comp_New_Interest'] - df['Simple_New_Interest']

# Effective Interest Rate this year (based on original principal)
df['Effective_Comp_Rate'] = np.where(df['Year'] == 0, 0, (df['Comp_New_Interest'] / P) * 100)

# ------------------------------------------
# PRESENT VALUE DATA
# ------------------------------------------
df['Simple_PV'] = fv_target / (1 + r_simple * df['Year'])
df['Comp_PV'] = fv_target / ((1 + r_comp) ** df['Year'])

# Interest Gap (Free money from the market)
df['Simple_PV_Interest'] = fv_target - df['Simple_PV']
df['Comp_PV_Interest'] = fv_target - df['Comp_PV']

# Cash Saved Today by using Compound over Simple
df['PV_Cash_Saved'] = df['Simple_PV'] - df['Comp_PV']


# ==========================================
# SAMPLE DATA FOR TABLES (5 evenly spaced years)
# ==========================================
sample_indices = np.linspace(0, t_max, 5, dtype=int)
df_sample = df[df['Year'].isin(sample_indices)].copy()

# ==========================================
# GRAPH 1: CUMULATIVE INTEREST (PROFIT)
# ==========================================
st.header("1. The Profit (Cumulative Interest)")
st.info("**Layman Translation:** This shows *only* the extra money you made. The table shows the total profit gap between the two methods over time.")

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("### The Formulas")
    st.markdown("**Simple Interest:**")
    st.latex(r"I_{simple}(t) = P \cdot r \cdot t")
    st.markdown("**Compound Interest:**")
    st.latex(r"I_{comp}(t) = P \cdot [(1 + r)^t - 1]")
    
    st.markdown("### 5-Year Snapshot")
    table1 = df_sample[['Year', 'Simple_Interest', 'Comp_Interest']].copy()
    table1['Total Profit Difference'] = table1['Comp_Interest'] - table1['Simple_Interest']
    table1.columns = ['Year', 'Total Profit (Simple)', 'Total Profit (Compound)', 'Compound Benefit (Total)']
    
    st.dataframe(table1.style.format({
        'Total Profit (Simple)': '${:,.0f}',
        'Total Profit (Compound)': '${:,.0f}',
        'Compound Benefit (Total)': '${:,.0f}'
    }), hide_index=True, use_container_width=True)

with col2:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df['Year'], y=df['Simple_Interest'], mode='lines', name='Simple Interest', line=dict(color='#1f77b4', width=3)))
    fig1.add_trace(go.Scatter(x=df['Year'], y=df['Comp_Interest'], mode='lines', name='Compound Interest', line=dict(color='#ff7f0e', width=3)))
    fig1.update_layout(title="Cumulative Interest Over Time", xaxis_title="Years", yaxis_title="Total Interest Earned ($)", hovermode="x unified")
    st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ==========================================
# GRAPH 2: TOTAL AMOUNT & PER-TERM CHANGES
# ==========================================
st.header("2. How Interest Changes Per Term")
st.info(f"**Layman Translation:** Instead of looking at the total value, let's look at the **New Interest Added** each specific year. Notice how the 'Effective Rate' on your original ${P:,.0f} grows every year with compound interest, creating a larger financial benefit as time goes on.")

col3, col4 = st.columns([1, 2])
with col3:
    st.markdown("### Per-Term Snapshot")
    table2 = df_sample[['Year', 'Simple_New_Interest', 'Comp_New_Interest', 'Compound_Benefit_This_Year', 'Effective_Comp_Rate']].copy()
    table2.columns = ['Year', 'New Interest Added (Simple)', 'New Interest Added (Compound)', 'Compound Benefit vs Simple (This Year)', 'Effective Rate (Compound)']
    
    st.dataframe(table2.style.format({
        'New Interest Added (Simple)': '${:,.0f}',
        'New Interest Added (Compound)': '${:,.0f}',
        'Compound Benefit vs Simple (This Year)': '${:,.0f}',
        'Effective Rate (Compound)': '{:.2f}%'
    }), hide_index=True, use_container_width=True)

with col4:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df['Year'], y=df['Simple_FV'], mode='lines', name='Simple Total (Line)', line=dict(color='#1f77b4', dash='dash')))
    fig2.add_trace(go.Bar(x=df['Year'], y=[P]*len(df), name='Initial Principal', marker_color='#2ca02c'))
    past_interest = df['Comp_Base_Before_This_Year'] - P
    fig2.add_trace(go.Bar(x=df['Year'], y=past_interest, name='Past Compounded Interest', marker_color='#ffbb78'))
    fig2.add_trace(go.Bar(x=df['Year'], y=df['Comp_New_Interest'], name='New Interest Added This Year', marker_color='#d62728'))

    fig2.update_layout(barmode='stack', title="Proving Compound Growth Year-by-Year", xaxis_title="Years", yaxis_title="Total Account Value ($)", hovermode="x unified")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ==========================================
# GRAPH 3 & 4: PRESENT VALUE & INTEREST AFFECTED
# ==========================================
st.header("3. Present Value (Interest Affected & Cash Saved)")
st.info(f"**Layman Translation:** To reach **${fv_target:,.0f}**, compounding does the heavy lifting for you. Look at the 'Upfront Cash Saved' column. Because compounding generates a larger 'Interest Gap' (free money from the market), you don't have to put as much of your own money in today compared to simple interest.")

col5, col6 = st.columns([1, 2])
with col5:
    st.markdown("### Present Value Snapshot")
    table3 = df_sample[['Year', 'Simple_PV', 'Comp_PV', 'Comp_PV_Interest', 'PV_Cash_Saved']].copy()
    table3.columns = ['Year', 'Required Cash (Simple)', 'Required Cash (Compound)', 'Interest Gap (Compound)', 'Upfront Cash Saved (Benefit)']
    
    st.dataframe(table3.style.format({
        'Required Cash (Simple)': '${:,.0f}',
        'Required Cash (Compound)': '${:,.0f}',
        'Interest Gap (Compound)': '${:,.0f}',
        'Upfront Cash Saved (Benefit)': '${:,.0f}'
    }), hide_index=True, use_container_width=True)

with col6:
    fig3 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, 
                         subplot_titles=("How much cash you need TODAY (Present Value)", "How much free money the market pays (Interest Gap)"))
    
    # Graph 3: PV Curve
    fig3.add_trace(go.Scatter(x=df['Year'], y=df['Simple_PV'], mode='lines', name='PV (Simple)', line=dict(color='#1f77b4')), row=1, col=1)
    fig3.add_trace(go.Scatter(x=df['Year'], y=df['Comp_PV'], mode='lines', name='PV (Compound)', line=dict(color='#ff7f0e')), row=1, col=1)
    
    # Graph 4: Interest component in PV
    fig3.add_trace(go.Scatter(x=df['Year'], y=df['Simple_PV_Interest'], mode='lines', name='Interest Gap (Simple)', line=dict(color='#1f77b4', dash='dot')), row=2, col=1)
    fig3.add_trace(go.Scatter(x=df['Year'], y=df['Comp_PV_Interest'], mode='lines', name='Interest Gap (Compound)', line=dict(color='#ff7f0e', dash='dot')), row=2, col=1)

    fig3.update_layout(height=600, title=f"Working Backwards from a Target of ${fv_target:,.0f}", hovermode="x unified")
    fig3.update_yaxes(title_text="Required Starting Cash ($)", row=1, col=1)
    fig3.update_yaxes(title_text="Free Money (Interest $)", row=2, col=1)
    fig3.update_xaxes(title_text="Years to Grow", row=2, col=1)

    st.plotly_chart(fig3, use_container_width=True)