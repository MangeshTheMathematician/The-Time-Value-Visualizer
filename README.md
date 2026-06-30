Quant Time Value of Money (TVM) Dashboard

1. Executive Summary

This project is an interactive quantitative finance dashboard built with Streamlit that models the Time Value of Money (TVM). It simulates simple interest, compound interest, continuous compounding, present value discounting, and rate sensitivity over customizable time horizons.

Money today and money in the future are not equal. This dashboard serves as a foundational financial engineering tool to visualize how capital scales through time and how future cash flows are discounted back to present value—the core mechanical concept behind bond pricing, swap valuation, option pricing, and discounted cash flow (DCF) models.

2. Technical Stack

Frontend / App Framework: Streamlit

Numerical Computing: NumPy

Data Manipulation: Pandas

Data Visualization: Plotly Graph Objects & Subplots

3. How to Run Locally

To run this dashboard on your local machine, follow these steps:

Clone the repository:

git clone [https://github.com/MangeshTheMathematician/The-Time-Value-Visualizer.git](https://github.com/MangeshTheMathematician/The-Time-Value-Visualizer.git)


Navigate to the folder:

cd The-Time-Value-Visualizer


Install the required dependencies:

pip install -r requirements.txt


Run the Streamlit app:

streamlit run tmvapp.py


(Note: You can view the live deployment of this dashboard here: https://hessian-ai-timevaluemoney.streamlit.app/)

4. Dashboard Features

Interactive Controls: Dynamic sliders and inputs for Principal, Simple/Compound Rates, Time Horizon, Target Future Value, and Compounding Frequencies (Annual to Continuous).

Growth Engine Visualization: Stacked bar charts separating original principal, past compounded interest, and new interest generated per period.

Present Value Analysis: Visual comparisons of the upfront capital required today to reach a target future value using simple vs. compound discounting.

Rate Sensitivity Heatmap: A 2D matrix visualizing how future value fluctuates across an array of interest rate shocks and time horizons.

5. Mathematical Engine & Proofs

At the core of this dashboard are standard quantitative finance formulas, executed via vectorized NumPy arrays for rapid simulation.

Future Value (FV)

Future value calculates how much a present cash flow will grow over $t$ years.

Simple Interest: Interest is calculated exclusively on the original principal ($P$).


$$FV_{simple} = P(1 + rt)$$

Compound Interest: Interest earns interest. For compounding $m$ times per year:


$$FV_{compound} = P\left(1+\frac{r}{m}\right)^{mt}$$

Continuous Compounding: The theoretical limit used in quantitative pricing models:


$$FV_{continuous} = Pe^{rt}$$

Present Value (PV)

Present value discounts a future target amount back to today's dollars.

Compound Present Value:


$$PV = \frac{FV}{\left(1+\frac{r}{m}\right)^{mt}}$$

Continuous Present Value:


$$PV = FVe^{-rt}$$

6. Case Study: The Power of Compounding

The dashboard proves mathematically that a lower compound rate can outperform a higher simple rate over long horizons.

Assuming the following inputs:

$P = \$100,000$

$r_{simple} = 5.0\%$

$r_{compound} = 4.5\%$ (Annual compounding)

$t = 30$ years

Future Value Comparison:

Simple Growth: $\$100,000(1 + 0.05 \times 30) = \$250,000$

Compound Growth: $\$100,000(1.045)^{30} \approx \$374,532$

Even though the compound rate (4.5%) is lower than the simple rate (5%), compounding generates an excess wealth of $124,532 over 30 years due to the geometric scaling of interest earning interest.

Present Value Target (Goal: $500,000 in 30 years):

Capital needed today (Simple): $\frac{\$500,000}{1 + (0.05 \times 30)} = \$200,000$

Capital needed today (Compound): $\frac{\$500,000}{1.045^{30}} \approx \$133,500$

Compound discounting saves the investor $66,500 in upfront capital requirements.

7. Limitations & Assumptions

Deterministic Environment: This model assumes constant interest rates across the entire time horizon. It does not model stochastic rate volatility.

Frictionless Market: The calculations do not account for inflation, capital gains tax, liquidity constraints, or default risk.

Educational Scope: Simple interest is modeled for educational benchmarking, though institutional finance relies almost exclusively on periodic or continuous compounding.
