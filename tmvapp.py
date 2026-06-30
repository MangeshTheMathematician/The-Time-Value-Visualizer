# Import Streamlit because this library creates the web dashboard.
import streamlit as st

# Import NumPy because this library helps with numerical arrays and mathematical calculations.
import numpy as np

# Import pandas because this library helps create tables and financial time-series data.
import pandas as pd

# Import Plotly Graph Objects because this library creates interactive financial charts.
import plotly.graph_objects as go

# Import Plotly subplots because we want multiple charts inside one figure.
from plotly.subplots import make_subplots


# Set the browser tab title and make the dashboard use the full screen width.
st.set_page_config(
    page_title="Quant TVM Dashboard",
    layout="wide"
)


# Add custom CSS to make the dashboard cleaner and more professional.
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
        }

        .small-note {
            color: #9ca3af;
            font-size: 0.90rem;
        }

        .formula-box {
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 18px;
            background-color: #111827;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Create the main dashboard title.
st.title("Quant Time Value of Money Dashboard")


# Create a short subtitle to explain the dashboard purpose.
st.caption(
    "Simple interest, compound interest, present value, discounting, and rate sensitivity in one clean quant-finance dashboard."
)


# Create the sidebar title for all user inputs.
st.sidebar.header("Inputs / Controls")


# Ask the user for starting money.
principal = st.sidebar.number_input(
    "Starting Money / Principal",
    min_value=1_000.0,
    max_value=100_000_000.0,
    value=100_000.0,
    step=1_000.0
)


# Ask the user for simple interest rate as a percentage.
simple_rate_percent = st.sidebar.number_input(
    "Simple Interest Rate (%)",
    min_value=0.0,
    max_value=50.0,
    value=5.0,
    step=0.1
)


# Ask the user for compound interest rate as a percentage.
compound_rate_percent = st.sidebar.number_input(
    "Compound Interest Rate (%)",
    min_value=0.0,
    max_value=50.0,
    value=4.5,
    step=0.1
)


# Ask the user for total time horizon in years.
time_horizon = st.sidebar.slider(
    "Time Horizon (Years)",
    min_value=1,
    max_value=50,
    value=30,
    step=1
)


# Ask the user for future target amount for present value analysis.
target_future_value = st.sidebar.number_input(
    "Target Future Amount",
    min_value=1_000.0,
    max_value=500_000_000.0,
    value=500_000.0,
    step=10_000.0
)


# Create compounding frequency choices.
frequency_choice = st.sidebar.selectbox(
    "Compounding Frequency",
    [
        "Annual",
        "Semi-Annual",
        "Quarterly",
        "Monthly",
        "Daily",
        "Continuous"
    ],
    index=0
)


# Convert the simple rate from percentage into decimal form.
simple_rate = simple_rate_percent / 100.0


# Convert the compound rate from percentage into decimal form.
compound_rate = compound_rate_percent / 100.0


# Create a dictionary that maps frequency names to number of compounding periods per year.
frequency_map = {
    "Annual": 1,
    "Semi-Annual": 2,
    "Quarterly": 4,
    "Monthly": 12,
    "Daily": 252,
    "Continuous": None
}


# Read the number of compounding periods from the selected frequency.
compound_frequency = frequency_map[frequency_choice]


# Create a helper function to format currency values.
def format_money(value):
    # Return N/A if the value is missing.
    if pd.isna(value):
        return "N/A"

    # Format the number as dollars with commas and zero decimals.
    return f"${value:,.0f}"


# Create a helper function to format percentages.
def format_percent(value):
    # Return N/A if the value is missing.
    if pd.isna(value):
        return "N/A"

    # Convert decimal into percentage text.
    return f"{value * 100:.2f}%"


# Create a helper function to calculate simple future value.
def simple_future_value(principal_amount, rate, years):
    # Apply the simple interest formula.
    return principal_amount * (1 + rate * years)


# Create a helper function to calculate compound future value.
def compound_future_value(principal_amount, rate, years, frequency):
    # Use continuous compounding if frequency is None.
    if frequency is None:
        return principal_amount * np.exp(rate * years)

    # Use periodic compounding if frequency is annual, monthly, daily, etc.
    return principal_amount * ((1 + rate / frequency) ** (frequency * years))


# Create a helper function to calculate simple present value.
def simple_present_value(future_value, rate, years):
    # Apply the simple discounting formula.
    return future_value / (1 + rate * years)


# Create a helper function to calculate compound present value.
def compound_present_value(future_value, rate, years, frequency):
    # Use continuous discounting if frequency is None.
    if frequency is None:
        return future_value * np.exp(-rate * years)

    # Use periodic compound discounting if frequency is annual, monthly, daily, etc.
    return future_value / ((1 + rate / frequency) ** (frequency * years))


# Create a helper function to calculate the effective annual compound rate.
def effective_annual_rate(rate, frequency):
    # Use continuous compounding formula if frequency is None.
    if frequency is None:
        return np.exp(rate) - 1

    # Use periodic compounding formula if frequency is finite.
    return (1 + rate / frequency) ** frequency - 1


# Create the year array from 0 to selected time horizon.
years = np.arange(0, time_horizon + 1)


# Create the main DataFrame that stores every calculation.
df = pd.DataFrame(
    {
        "Year": years
    }
)


# Calculate simple future value for every year.
df["Simple_FV"] = simple_future_value(
    principal,
    simple_rate,
    df["Year"]
)


# Calculate compound future value for every year.
df["Compound_FV"] = compound_future_value(
    principal,
    compound_rate,
    df["Year"],
    compound_frequency
)


# Calculate simple interest earned for every year.
df["Simple_Interest"] = df["Simple_FV"] - principal


# Calculate compound interest earned for every year.
df["Compound_Interest"] = df["Compound_FV"] - principal


# Calculate the dollar advantage of compound future value over simple future value.
df["Compound_Advantage"] = df["Compound_FV"] - df["Simple_FV"]


# Calculate the compound advantage as a percentage of original principal.
df["Compound_Advantage_Rate"] = df["Compound_Advantage"] / principal


# Calculate simple present value needed today to reach the target future value.
df["Simple_PV"] = simple_present_value(
    target_future_value,
    simple_rate,
    df["Year"]
)


# Calculate compound present value needed today to reach the target future value.
df["Compound_PV"] = compound_present_value(
    target_future_value,
    compound_rate,
    df["Year"],
    compound_frequency
)


# Calculate how much upfront cash compounding saves compared to simple interest.
df["PV_Cash_Saved"] = df["Simple_PV"] - df["Compound_PV"]


# Calculate the cash saved as a percentage of target future value.
df["PV_Cash_Saved_Rate"] = df["PV_Cash_Saved"] / target_future_value


# Calculate simple new interest earned each year.
df["Simple_New_Interest"] = np.where(
    df["Year"] == 0,
    0,
    principal * simple_rate
)


# Calculate compound new interest earned each year.
df["Compound_New_Interest"] = df["Compound_FV"].diff().fillna(0)


# Calculate previous compound interest already accumulated before current year.
df["Past_Compound_Interest"] = (df["Compound_FV"].shift(1).fillna(principal)) - principal


# Calculate the effective compound interest earned this year on original principal.
df["Effective_Compound_Rate_This_Year"] = df["Compound_New_Interest"] / principal


# Calculate discount factor under simple interest.
df["Simple_Discount_Factor"] = df["Simple_PV"] / target_future_value


# Calculate discount factor under compound interest.
df["Compound_Discount_Factor"] = df["Compound_PV"] / target_future_value


# Select the final row because it represents the selected full horizon.
final_row = df.iloc[-1]


# Calculate final simple future value.
final_simple_fv = final_row["Simple_FV"]


# Calculate final compound future value.
final_compound_fv = final_row["Compound_FV"]


# Calculate final compound advantage.
final_compound_advantage = final_row["Compound_Advantage"]


# Calculate final compound present value.
final_compound_pv = final_row["Compound_PV"]


# Calculate final present value cash saved.
final_pv_cash_saved = final_row["PV_Cash_Saved"]


# Calculate effective annual rate for compounding method.
compound_effective_annual_rate = effective_annual_rate(
    compound_rate,
    compound_frequency
)


# Find the first year where compound future value becomes greater than simple future value.
break_even_rows = df[df["Compound_FV"] > df["Simple_FV"]]


# Store break-even year if it exists.
break_even_year = int(break_even_rows["Year"].iloc[0]) if not break_even_rows.empty else None


# Calculate compound future value if the compound rate increases by 100 basis points.
compound_fv_plus_100bps = compound_future_value(
    principal,
    compound_rate + 0.01,
    time_horizon,
    compound_frequency
)


# Calculate future value sensitivity to a 100 bps rate increase.
fv_sensitivity_100bps = compound_fv_plus_100bps - final_compound_fv


# Calculate compound present value if the compound rate increases by 100 basis points.
compound_pv_plus_100bps = compound_present_value(
    target_future_value,
    compound_rate + 0.01,
    time_horizon,
    compound_frequency
)


# Calculate present value sensitivity to a 100 bps rate increase.
pv_sensitivity_100bps = compound_pv_plus_100bps - final_compound_pv


# Create the executive summary section.
st.header("1. Executive Summary")


# Create metric columns for headline results.
metric_1, metric_2, metric_3, metric_4, metric_5, metric_6 = st.columns(6)


# Show final simple future value.
metric_1.metric(
    "Simple FV",
    format_money(final_simple_fv)
)


# Show final compound future value.
metric_2.metric(
    "Compound FV",
    format_money(final_compound_fv)
)


# Show compound advantage in dollars.
metric_3.metric(
    "Compound Advantage",
    format_money(final_compound_advantage)
)


# Show compound present value required today.
metric_4.metric(
    "Compound PV Needed",
    format_money(final_compound_pv)
)


# Show upfront cash saved by compound discounting.
metric_5.metric(
    "PV Cash Saved",
    format_money(final_pv_cash_saved)
)


# Show break-even year.
metric_6.metric(
    "Break-even Year",
    "N/A" if break_even_year is None else f"Year {break_even_year}"
)


# Create a short explanation of the executive result.
if final_compound_fv > final_simple_fv:
    st.success(
        "Interpretation: compound growth beats simple growth over this horizon. "
        "This happens because interest begins earning interest."
    )
else:
    st.warning(
        "Interpretation: simple interest is still higher over this horizon. "
        "Compounding may need more time or a higher rate to win."
    )


# Show current selected assumptions in a compact table.
st.header("2. Inputs / Controls")


# Create a DataFrame of selected assumptions.
input_table = pd.DataFrame(
    {
        "Input": [
            "Principal",
            "Simple Rate",
            "Compound Rate",
            "Compounding Frequency",
            "Time Horizon",
            "Target Future Value"
        ],
        "Value": [
            format_money(principal),
            f"{simple_rate_percent:.2f}%",
            f"{compound_rate_percent:.2f}%",
            frequency_choice,
            f"{time_horizon} years",
            format_money(target_future_value)
        ]
    }
)


# Display the selected assumptions table.
st.dataframe(
    input_table,
    hide_index=True,
    use_container_width=True
)


# Show key formulas in an expandable section.
st.header("3. Key Formulas")


# Create an expander so the formulas are visible but not messy.
with st.expander("Open formula explanation", expanded=True):
    # Create two columns for formulas.
    formula_col_1, formula_col_2 = st.columns(2)

    # Put future value formulas on the left.
    with formula_col_1:
        # Label future value formulas.
        st.markdown("### Future Value")

        # Show simple future value formula.
        st.latex(r"FV_{simple} = P(1 + rt)")

        # Show compound future value formula.
        st.latex(r"FV_{compound} = P\left(1+\frac{r}{m}\right)^{mt}")

        # Show continuous compounding formula.
        st.latex(r"FV_{continuous} = Pe^{rt}")

    # Put present value formulas on the right.
    with formula_col_2:
        # Label present value formulas.
        st.markdown("### Present Value")

        # Show simple present value formula.
        st.latex(r"PV_{simple} = \frac{FV}{1 + rt}")

        # Show compound present value formula.
        st.latex(r"PV_{compound} = \frac{FV}{\left(1+\frac{r}{m}\right)^{mt}}")

        # Show continuous present value formula.
        st.latex(r"PV_{continuous} = FVe^{-rt}")


# Create main visualization section.
st.header("4. Main Visualization")


# Create tabs for the charts.
tab_growth, tab_interest, tab_pv, tab_sensitivity = st.tabs(
    [
        "Future Value Growth",
        "Interest Engine",
        "Present Value",
        "Rate Sensitivity"
    ]
)


# Create the future value chart tab.
with tab_growth:
    # Create a Plotly figure.
    fig_growth = go.Figure()

    # Add simple future value line.
    fig_growth.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df["Simple_FV"],
            mode="lines+markers",
            name="Simple Future Value"
        )
    )

    # Add compound future value line.
    fig_growth.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df["Compound_FV"],
            mode="lines+markers",
            name="Compound Future Value"
        )
    )

    # Add original principal reference line.
    fig_growth.add_trace(
        go.Scatter(
            x=df["Year"],
            y=[principal] * len(df),
            mode="lines",
            name="Original Principal",
            line=dict(dash="dash")
        )
    )

    # Improve the chart layout.
    fig_growth.update_layout(
        template="plotly_dark",
        height=500,
        title="Future Value: Simple vs Compound Growth",
        xaxis_title="Year",
        yaxis_title="Future Value",
        hovermode="x unified",
        legend_title="Series"
    )

    # Display the future value chart.
    st.plotly_chart(fig_growth, use_container_width=True)

    # Create a small sample table using five evenly spaced years.
    sample_years = np.linspace(0, time_horizon, 6, dtype=int)

    # Filter the full DataFrame for sample years.
    sample_growth = df[df["Year"].isin(sample_years)][
        [
            "Year",
            "Simple_FV",
            "Compound_FV",
            "Compound_Advantage",
            "Compound_Advantage_Rate"
        ]
    ]

    # Display the sample growth table.
    st.dataframe(
        sample_growth.style.format(
            {
                "Simple_FV": "${:,.0f}",
                "Compound_FV": "${:,.0f}",
                "Compound_Advantage": "${:,.0f}",
                "Compound_Advantage_Rate": "{:.2%}"
            }
        ),
        hide_index=True,
        use_container_width=True
    )


# Create the interest engine tab.
with tab_interest:
    # Create a Plotly figure for stacked compound growth.
    fig_interest = go.Figure()

    # Add original principal as the base bar.
    fig_interest.add_trace(
        go.Bar(
            x=df["Year"],
            y=[principal] * len(df),
            name="Original Principal"
        )
    )

    # Add past compound interest as stacked bar.
    fig_interest.add_trace(
        go.Bar(
            x=df["Year"],
            y=df["Past_Compound_Interest"],
            name="Past Compounded Interest"
        )
    )

    # Add new compound interest this year as stacked bar.
    fig_interest.add_trace(
        go.Bar(
            x=df["Year"],
            y=df["Compound_New_Interest"],
            name="New Interest This Year"
        )
    )

    # Add simple future value line for comparison.
    fig_interest.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df["Simple_FV"],
            mode="lines",
            name="Simple FV Line"
        )
    )

    # Improve the interest engine chart.
    fig_interest.update_layout(
        template="plotly_dark",
        barmode="stack",
        height=500,
        title="Compound Interest Engine: Principal + Old Interest + New Interest",
        xaxis_title="Year",
        yaxis_title="Account Value",
        hovermode="x unified"
    )

    # Display the interest engine chart.
    st.plotly_chart(fig_interest, use_container_width=True)

    # Create a sample table for yearly interest.
    sample_interest = df[df["Year"].isin(sample_years)][
        [
            "Year",
            "Simple_New_Interest",
            "Compound_New_Interest",
            "Effective_Compound_Rate_This_Year"
        ]
    ]

    # Display the interest table.
    st.dataframe(
        sample_interest.style.format(
            {
                "Simple_New_Interest": "${:,.0f}",
                "Compound_New_Interest": "${:,.0f}",
                "Effective_Compound_Rate_This_Year": "{:.2%}"
            }
        ),
        hide_index=True,
        use_container_width=True
    )


# Create the present value tab.
with tab_pv:
    # Create a two-row subplot for present value and cash saved.
    fig_pv = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.12,
        subplot_titles=(
            "Cash Needed Today to Reach Future Target",
            "Upfront Cash Saved by Compound Discounting"
        )
    )

    # Add simple present value line.
    fig_pv.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df["Simple_PV"],
            mode="lines+markers",
            name="Simple PV"
        ),
        row=1,
        col=1
    )

    # Add compound present value line.
    fig_pv.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df["Compound_PV"],
            mode="lines+markers",
            name="Compound PV"
        ),
        row=1,
        col=1
    )

    # Add PV cash saved line.
    fig_pv.add_trace(
        go.Scatter(
            x=df["Year"],
            y=df["PV_Cash_Saved"],
            mode="lines",
            name="PV Cash Saved"
        ),
        row=2,
        col=1
    )

    # Improve the present value subplot layout.
    fig_pv.update_layout(
        template="plotly_dark",
        height=650,
        title=f"Present Value Analysis for Target {format_money(target_future_value)}",
        hovermode="x unified"
    )

    # Add y-axis label for first chart.
    fig_pv.update_yaxes(
        title_text="Required Cash Today",
        row=1,
        col=1
    )

    # Add y-axis label for second chart.
    fig_pv.update_yaxes(
        title_text="Cash Saved",
        row=2,
        col=1
    )

    # Add x-axis label.
    fig_pv.update_xaxes(
        title_text="Years",
        row=2,
        col=1
    )

    # Display the PV chart.
    st.plotly_chart(fig_pv, use_container_width=True)

    # Create sample PV table.
    sample_pv = df[df["Year"].isin(sample_years)][
        [
            "Year",
            "Simple_PV",
            "Compound_PV",
            "PV_Cash_Saved",
            "PV_Cash_Saved_Rate"
        ]
    ]

    # Display sample PV table.
    st.dataframe(
        sample_pv.style.format(
            {
                "Simple_PV": "${:,.0f}",
                "Compound_PV": "${:,.0f}",
                "PV_Cash_Saved": "${:,.0f}",
                "PV_Cash_Saved_Rate": "{:.2%}"
            }
        ),
        hide_index=True,
        use_container_width=True
    )


# Create the sensitivity tab.
with tab_sensitivity:
    # Create an array of rate shocks around the selected compound rate.
    rate_grid = np.linspace(
        max(0, compound_rate - 0.03),
        compound_rate + 0.03,
        13
    )

    # Create an array of time values from 1 year to horizon.
    time_grid = np.arange(1, time_horizon + 1)

    # Create an empty list to store heatmap rows.
    heatmap_values = []

    # Loop through every rate in the rate grid.
    for grid_rate in rate_grid:
        # Calculate compound future value across every time point for this rate.
        row_values = compound_future_value(
            principal,
            grid_rate,
            time_grid,
            compound_frequency
        )

        # Add the row values to the heatmap list.
        heatmap_values.append(row_values)

    # Convert heatmap values into a NumPy array.
    heatmap_values = np.array(heatmap_values)

    # Create heatmap figure.
    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=heatmap_values,
            x=time_grid,
            y=[f"{rate * 100:.2f}%" for rate in rate_grid],
            colorbar=dict(title="Future Value")
        )
    )

    # Improve heatmap layout.
    fig_heatmap.update_layout(
        template="plotly_dark",
        height=550,
        title="Rate Sensitivity Heatmap: Future Value by Rate and Time",
        xaxis_title="Years",
        yaxis_title="Compound Rate"
    )

    # Display heatmap.
    st.plotly_chart(fig_heatmap, use_container_width=True)


# Create risk and sensitivity metrics section.
st.header("5. Risk / Sensitivity Metrics")


# Explain why this is called sensitivity instead of trading risk.
st.caption(
    "This TVM dashboard has no market randomness, so risk means rate sensitivity: how much value changes when interest rates move."
)


# Create columns for sensitivity metrics.
risk_col_1, risk_col_2, risk_col_3, risk_col_4 = st.columns(4)


# Show effective annual compound rate.
risk_col_1.metric(
    "Effective Annual Compound Rate",
    format_percent(compound_effective_annual_rate)
)


# Show FV sensitivity to +100 bps.
risk_col_2.metric(
    "FV Sensitivity to +100 bps",
    format_money(fv_sensitivity_100bps)
)


# Show PV sensitivity to +100 bps.
risk_col_3.metric(
    "PV Sensitivity to +100 bps",
    format_money(pv_sensitivity_100bps)
)


# Show final compound advantage rate.
risk_col_4.metric(
    "Compound Advantage Rate",
    format_percent(final_compound_advantage / principal)
)


# Create interpretation section.
st.header("6. Interpretation")


# Interpret compounding effect.
if final_compound_advantage > 0:
    st.success(
        f"At year {time_horizon}, compounding creates {format_money(final_compound_advantage)} more wealth than simple interest."
    )
else:
    st.warning(
        f"At year {time_horizon}, compounding does not beat simple interest under current assumptions."
    )


# Interpret present value effect.
if final_pv_cash_saved > 0:
    st.success(
        f"To reach {format_money(target_future_value)}, compound discounting requires {format_money(final_compound_pv)} today, "
        f"saving {format_money(final_pv_cash_saved)} compared with simple discounting."
    )
else:
    st.warning(
        "Under current assumptions, compound discounting does not reduce required cash versus simple discounting."
    )


# Interpret break-even year.
if break_even_year is not None:
    st.info(
        f"The compound future value first beats the simple future value in year {break_even_year}."
    )
else:
    st.info(
        "Compound future value does not beat simple future value inside the selected time horizon."
    )


# Create limitations section.
st.header("7. Limitations")


# Put limitations inside an expander to keep dashboard clean.
with st.expander("Read limitations"):
    # Write limitation notes.
    st.markdown(
        """
        - This is a deterministic educational model, not a market prediction model.
        - Tax, inflation, liquidity, default risk, and reinvestment risk are not included.
        - Interest rates are assumed constant through time.
        - Simple interest is shown for learning, but most institutional finance uses compound or continuously compounded discounting.
        - Present value calculations depend heavily on the selected discount rate.
        """
    )


# Create download section.
st.header("8. Download CSV")


# Create a CSV version of the full DataFrame.
csv_data = df.to_csv(index=False).encode("utf-8")


# Add download button.
st.download_button(
    label="Download Full TVM Calculation Table",
    data=csv_data,
    file_name="time_value_of_money_dashboard.csv",
    mime="text/csv"
)
