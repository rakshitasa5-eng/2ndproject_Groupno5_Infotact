# 2ndproject
## Supply Chain Analytics - Demand Forecasting & Anomaly Detection
Week: 2
Phase: Data Validation & Business Analysis
Tools Used: Python, Pandas, NumPy, Matplotlib, Jupyter Notebook, Git, GitHub

## 📖 Project Overview

This project builds a Supply Chain Analytics pipeline that predicts future product demand and
detects unusual supply chain behavior using historical order data.

Week 1 produced a clean, structured monthly demand dataset. Week 2 builds directly on that
foundation: it validates the cleaned data, applies statistical anomaly detection, and translates
the results into business-relevant findings that support inventory and demand-planning decisions.

## 🎯 Week 2 Objective

The main objective of Week 2 was to validate the monthly demand dataset produced in Week 1,
identify unusual demand behavior, and interpret those anomalies from a business perspective.

The work completed includes:

- Validating the monthly demand dataset and category counts
- Checking for duplicate records, negative quantities, and residual missing values
- Detecting statistical anomalies in monthly demand (IQR-based)
- Investigating possible business reasons behind flagged anomalies
- Summarizing anomalies by product category
- Visualizing normal demand versus anomaly points
- Cross-validating results against the Team Lead's anomaly detection model
- Documenting findings and business interpretation notes

## 📂 Datasets Used

| Dataset | Purpose |
|---|---|
| `monthly_demand_clean.csv` | Week 1 output — monthly demand per category (wide format) |
| `monthly_demand_clean_long.csv` | Long-format version of the above, created in Week 2 for validation and plotting |
| `merged_supply_chain.csv` | Week 1 merged order-level dataset, used for business-reason investigation |

## 📊 Business Problem

Supply chain organizations often struggle to maintain optimal inventory levels. Unusual spikes or
drops in demand — caused by stockouts, promotions, or seasonal effects — are easy to miss in raw
data but can seriously distort forecasting if left unexplained. Week 2 addresses this by:

- Confirming the Week 1 dataset is reliable enough to build models on
- Systematically identifying which months/categories behaved abnormally
- Attaching plausible business explanations to those anomalies, rather than treating them as noise

## ⚙️ Week 2 Workflow

### Step 1 – Dataset Validation
Loaded `monthly_demand_clean.csv`, converted it to long format, and verified that every product
category (CPU, Mother Board, RAM, Storage, Video Card) has the same number of monthly records,
confirming Week 1's timeline construction was applied consistently across categories.

### Step 2 – Data Quality Checks
Checked the long-format dataset for:
- Duplicate (date, category) records — none expected or found
- Negative demand values — not physically valid, checked and confirmed absent
- Remaining missing values — confirmed these are limited to leading/trailing gaps by design
  (per Week 1's interpolation approach), not gaps in the middle of a series

### Step 3 – Anomaly Detection (Statistical)
Applied an IQR (Interquartile Range) method per category to flag months with unusually high or low
demand relative to that category's typical range.

### Step 4 – Business Interpretation of Anomalies
For each flagged anomaly, reviewed surrounding months and order-level data
(`merged_supply_chain.csv`) to form a hypothesis for the likely cause:
- Sudden drop near zero → possible stockout
- Spike around known seasonal periods (e.g. Nov/Dec) → possible seasonal demand
- Isolated spike with no seasonal pattern → possible promotion/discount event
- Isolated single-month dip with normal months either side → possible data/reporting issue

### Step 5 – Anomaly Summary by Category
Built a summary table showing, per category: number of anomalies, average/min/max anomaly value,
and anomaly rate (% of months flagged).

### Step 6 – Visualization
Created one chart per category plotting normal monthly demand as a line, with anomaly months
overlaid as distinct points, for quick visual comparison.

### Step 7 – Cross-Validation with Team Lead's Model
Compared the independent IQR-based anomaly flags against the Team Lead's anomaly detection model
output (Z-Score / IQR / Isolation Forest) to check for agreement, investigate discrepancies, and
confirm the model's output was reasonable (correct row counts, plausible flagged dates, no
categories with implausibly 0% or 100% anomaly rates).

### Step 8 – Documentation
Recorded data quality findings, anomaly summary, business interpretation, model validation
outcome, and recommendations in the notebook and this documentation file.

## 📁 Files Generated

- `monthly_demand_clean_long.csv` — long-format demand dataset (date, category, demand)
- `anomaly_summary_by_category.csv` — anomaly counts and stats per category
- `anomaly_charts.png` — normal vs. anomaly demand charts, one panel per category
- `03_Data_Validation.ipynb` — full notebook with code, charts, and interpretation notes

## 📈 Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook
- Git
- GitHub

## ✅ Week 2 Deliverables

Completed:

- Validated monthly demand dataset and category counts
- Checked for duplicates, negative values, and missing values
- Flagged statistical anomalies per category
- Investigated and documented possible business reasons for anomalies
- Built anomaly summary table by category
- Created anomaly visualization charts
- Cross-validated results against Team Lead's anomaly detection model
- Documented business findings and validation report
- Submitted notebook and reviewed Team Lead's pull request

## 📌 Business Outcome

At the end of Week 2, the Week 1 dataset has been validated as reliable, and demand anomalies have
been identified, quantified by category, and explained with plausible business reasoning
(stockouts, seasonality, promotions). This gives the team confidence in the underlying data and
a documented record of unusual demand events before moving into forecasting.

## 🚀 Next Phase (Week 3)

The validated dataset and anomaly findings from Week 2 will feed into demand forecasting model
development (e.g. ARIMA, Prophet, or machine learning-based forecasting) to predict future product
demand by category.
