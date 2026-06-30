# Quant Time Value of Money Dashboard

## 1. Project Summary

This project is an interactive Streamlit dashboard that explains the Time Value of Money using simple interest, compound interest, present value, discounting, and rate sensitivity.

The dashboard allows a user to enter a starting principal, interest rates, time horizon, compounding frequency, and a future target amount. It then calculates how money grows forward through time and how future money is discounted back to today.

This project is designed as a foundational quantitative finance dashboard because Time Value of Money is the base concept behind bonds, forwards, swaps, options, yield curves, DCF valuation, and portfolio growth.

---

## 2. Why I Built This

I built this project to convert a basic financial mathematics concept into an interactive quant dashboard.

The goal is to show that I can:

- explain financial mathematics clearly,
- convert formulas into Python code,
- build an interactive Streamlit dashboard,
- visualize financial behavior over time,
- calculate present value and future value,
- measure sensitivity to interest rate changes,
- communicate results in a business-friendly way.

---

## 3. Core Quant Concept

The main concept is:

> Money today and money in the future are not equal.

Money changes value through time because it can earn interest.

This idea is called:

\[
\text{Time Value of Money}
\]

It is used in:

- bond pricing,
- forward pricing,
- swap valuation,
- option pricing,
- pension valuation,
- actuarial reserves,
- discounted cash flow valuation,
- portfolio return analysis.

---

## 4. Required Basic Concepts

### Principal

Principal means starting money.

\[
P = \text{starting money}
\]

Example:

\[
P = 100,000
\]

### Interest Rate

Interest rate means the growth rate of money.

If interest rate is 5%, then:

\[
r = \frac{5}{100} = 0.05
\]

### Time

Time means number of years.

\[
t = \text{number of years}
\]

### Future Value

Future Value means how much money becomes in the future.

\[
FV = \text{future money}
\]

### Present Value

Present Value means how much money is needed today to reach a future amount.

\[
PV = \text{today's value of future money}
\]

### Compounding Frequency

Compounding frequency means how many times interest is added per year.

\[
m = \text{number of compounding periods per year}
\]

Examples:

- Annual: \(m=1\)
- Semi-Annual: \(m=2\)
- Quarterly: \(m=4\)
- Monthly: \(m=12\)
- Daily: \(m=252\)

---

## 5. Formula Explanation and Proof

## 5.1 Simple Interest

Simple interest means interest is calculated only on the original principal.

Interest each year is:

\[
P \times r
\]

For \(t\) years:

\[
\text{Total Interest} = P \times r \times t
\]

Future Value equals principal plus interest:

\[
FV = P + Prt
\]

Take \(P\) common:

\[
FV_{simple} = P(1+rt)
\]

### Simple Interest Formula

\[
FV_{simple} = P(1+rt)
\]

where:

- \(P\) = starting money,
- \(r\) = simple annual interest rate,
- \(t\) = number of years.

---

## 5.2 Compound Interest

Compound interest means interest earns more interest.

After one year:

\[
FV_1 = P(1+r)
\]

After two years:

\[
FV_2 = P(1+r)(1+r)
\]

\[
FV_2 = P(1+r)^2
\]

After three years:

\[
FV_3 = P(1+r)^3
\]

So after \(t\) years:

\[
FV_{compound} = P(1+r)^t
\]

If interest compounds \(m\) times per year:

\[
FV_{compound} = P\left(1+\frac{r}{m}\right)^{mt}
\]

where:

- \(P\) = principal,
- \(r\) = annual compound rate,
- \(m\) = compounding periods per year,
- \(t\) = number of years.

---

## 5.3 Continuous Compounding

In quant finance, continuous compounding is often used because it is mathematically clean.

The formula is:

\[
FV_{continuous} = Pe^{rt}
\]

where:

- \(e\) is Euler's number,
- \(r\) is the continuously compounded rate,
- \(t\) is time in years.

---

## 5.4 Present Value

Present value is future value backwards.

Start from compound future value:

\[
FV = PV(1+r)^t
\]

Divide both sides by:

\[
(1+r)^t
\]

Then:

\[
PV = \frac{FV}{(1+r)^t}
\]

With compounding frequency:

\[
PV = \frac{FV}{\left(1+\frac{r}{m}\right)^{mt}}
\]

With continuous compounding:

\[
PV = FVe^{-rt}
\]

---

## 6. Detailed Example

Dashboard inputs:

\[
P = 100,000
\]

\[
r_{simple} = 5\% = 0.05
\]

\[
r_{compound} = 4.5\% = 0.045
\]

\[
t = 30
\]

\[
FV_{target} = 500,000
\]

---

## 6.1 Simple Future Value

\[
FV_{simple} = P(1+rt)
\]

\[
FV_{simple} = 100,000(1 + 0.05 \times 30)
\]

\[
FV_{simple} = 100,000(1 + 1.5)
\]

\[
FV_{simple} = 100,000 \times 2.5
\]

\[
FV_{simple} = 250,000
\]

Simple interest earned:

\[
250,000 - 100,000 = 150,000
\]

---

## 6.2 Compound Future Value

\[
FV_{compound} = P(1+r)^t
\]

\[
FV_{compound} = 100,000(1.045)^{30}
\]

\[
FV_{compound} \approx 374,532
\]

Compound interest earned:

\[
374,532 - 100,000 = 274,532
\]

Compound advantage over simple interest:

\[
374,532 - 250,000 = 124,532
\]

So compound interest creates approximately:

\[
124,532
\]

more wealth than simple interest over 30 years.

---

## 6.3 Present Value Target

Target future amount:

\[
FV = 500,000
\]

Simple present value:

\[
PV_{simple} = \frac{500,000}{1 + 0.05 \times 30}
\]

\[
PV_{simple} = \frac{500,000}{2.5}
\]

\[
PV_{simple} = 200,000
\]

Compound present value:

\[
PV_{compound} = \frac{500,000}{1.045^{30}}
\]

\[
PV_{compound} \approx 133,500
\]

Cash saved by compound discounting:

\[
200,000 - 133,500 = 66,500
\]

This means that to reach 500,000 after 30 years, compound growth requires much less money today.

---

## 7. Dashboard Features

The dashboard includes:

- principal input,
- simple interest rate input,
- compound interest rate input,
- compounding frequency selector,
- time horizon slider,
- future value target input,
- simple future value calculation,
- compound future value calculation,
- present value calculation,
- compound advantage metric,
- break-even year calculation,
- rate sensitivity heatmap,
- CSV download.

---

## 8. Dashboard Structure

The app follows this structure:

1. Executive Summary
2. Inputs / Controls
3. Key Formulas
4. Main Visualization
5. Risk / Sensitivity Metrics
6. Interpretation
7. Limitations
8. Download CSV

---

## 9. Visualizations

The dashboard contains four main visualization tabs:

### Future Value Growth

Compares simple future value against compound future value over time.

### Interest Engine

Shows how compound growth is built from:

- original principal,
- past compounded interest,
- new interest added this year.

### Present Value

Shows how much money is needed today to reach a future target.

### Rate Sensitivity

Shows how future value changes when interest rates and time horizon change.

---

## 10. Screenshots

Add screenshots here after deploying the Streamlit app.

Example:

```markdown
![Dashboard Screenshot](assets/tvm_dashboard.png)
