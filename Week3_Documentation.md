# Supply Chain Analytics — Demand Forecasting & Anomaly Detection
## Week 3 Documentation: Demand Forecasting Models

*Group 5 | Infotact Internship Project*
*Tools Used: Python, Pandas, NumPy, statsmodels (SARIMA), Prophet, scikit-learn, Matplotlib, Jupyter Notebook*

## 1. Overview

Week 3 builds on the validated, anomaly-flagged monthly demand dataset produced in Weeks 1 and 2.
The objective this week was to move from data preparation into predictive analytics: establishing
a naive baseline forecast, building statistical and machine-learning forecasting models, and
evaluating their accuracy on unseen historical data before generating a genuine future forecast.

The dataset used is monthly (not daily) demand per product category, spanning June 2013 to
November 2017, across five categories: CPU, Mother Board, RAM, Storage, and Video Card. Because
the underlying data is monthly rather than daily, the project's "next 90 days" forecasting
requirement was interpreted as a 3-month-ahead forecast, which is the equivalent horizon at
monthly granularity.

## 2. Objective

- Establish a naive baseline forecast (moving average) as a benchmark for all other models.
- Implement a statistical forecasting model (SARIMA) capturing trend and 12-month seasonality.
- Implement Facebook Prophet as a second, comparative forecasting approach with built-in
  confidence intervals.
- Split data chronologically into train/test sets to validate accuracy against unseen months.
- Evaluate all models using MAPE (Mean Absolute Percentage Error) and RMSE (Root Mean Square
  Error).
- Select the best-performing model per category and generate a genuine future forecast.
- Connect forecasting results back to Week 2's anomaly findings for business interpretation.

## 3. Datasets Used

| Dataset | Purpose |
|---|---|
| `final_detected_anomalies.csv` | Monthly demand per category with Z-Score / IQR / Isolation Forest anomaly flags (Week 2 output); primary input for forecasting |
| `final_anomaly_dataset.csv` | Per-category anomaly counts, used to relate forecast accuracy to historical volatility |
| `monthly_demand_clean_long.csv` | Long-format monthly demand series, alternate source for the same data |

## 4. Methodology / Workflow

### 4.1 Data Preparation
Loaded the Week 2 output and converted each category's series into a continuous monthly-frequency
time series to satisfy the requirements of ARIMA and Prophet, which require an unbroken date index.

### 4.2 Train / Test Split
Data was split chronologically — never shuffled — holding out the most recent 6 months as a test
set and training on all months prior. This simulates genuinely forecasting unseen future demand
rather than interpolating within known data.

### 4.3 Baseline Model — Simple Moving Average
A rolling 3-month moving average was used as the baseline forecast. Every subsequent model's
accuracy is measured against this benchmark; a model that cannot outperform the moving average is
not considered an improvement worth deploying.

### 4.4 SARIMA (Seasonal ARIMA)
A Seasonal ARIMA model was fit per category, with a 12-month seasonal period to capture yearly
demand cycles. Model order and seasonal order were selected via a grid search minimizing AIC
(Akaike Information Criterion), rather than chosen manually, to ensure an objective, reproducible
model selection process.

### 4.5 Prophet
Facebook Prophet was fit per category as a second forecasting approach, configured with yearly
seasonality enabled (daily/weekly seasonality disabled, since the data is monthly). Prophet
additionally provides 80% confidence intervals for each forecasted point, which are carried
forward into the Week 4 Streamlit dashboard's adjustable confidence interval feature.

### 4.6 Model Evaluation
Each model's forecast on the held-out test months was scored using:
- **MAPE** (Mean Absolute Percentage Error) — average percentage deviation from actual demand
- **RMSE** (Root Mean Square Error) — average magnitude of forecast error in the same units as
  demand

Note: several categories contain zero-demand months, which makes MAPE mathematically unstable
(division by zero). This is a genuine limitation of the metric on this dataset and is reported
transparently rather than concealed; RMSE is treated as the more reliable metric where this occurs.

### 4.7 Model Selection & Future Forecast
The best-performing model per category (lowest RMSE on the test set) was refit on the full
historical dataset and used to generate a 3-month-ahead forecast with 80% confidence intervals,
saved in a format directly usable by the Week 4 Streamlit application.

### 4.8 Linking Forecasting to Anomaly Detection
Forecast accuracy per category was compared against that category's historical anomaly count (from
Week 2). Categories with a higher number of confirmed anomalies were examined for a corresponding
increase in forecast error, to identify which product categories require wider manual
safety-stock buffers due to inherent unpredictability.

## 5. Files Generated

| File | Description |
|---|---|
| `03_Demand_Forecasting.ipynb` | Full notebook: baseline, SARIMA, Prophet, evaluation, and future forecast, across all 5 categories |
| `model_comparison_results.csv` | MAPE and RMSE for every model, for every category |
| `best_model_per_category.csv` | The winning model (lowest RMSE) selected per category |
| `future_demand_forecast.csv` | 3-month-ahead forecast with upper/lower confidence intervals per category (feeds Week 4) |

## 6. Technologies Used

- Python
- Pandas / NumPy
- statsmodels (SARIMAX)
- Prophet
- scikit-learn (evaluation metrics)
- Matplotlib
- Jupyter Notebook

## 7. Deliverables — Week 3

| Deliverable | Status |
|---|---|
| Chronological train/test split implemented | Completed |
| Baseline moving average model | Completed |
| SARIMA model with AIC-based order selection | Completed |
| Prophet model with confidence intervals | Completed |
| MAPE / RMSE evaluation for all models, all categories | Completed |
| Best model selected per category | Completed |
| 3-month-ahead future forecast generated and saved | Completed |
| Forecast accuracy linked to Week 2 anomaly findings | Completed |
| Findings documented (method, results, limitations) | Completed |

## 8. Business Outcome

By the end of Week 3, each product category has a validated, benchmarked demand forecast for the
next 3 months, along with an honest accounting of which categories are reliably predictable versus
which carry higher uncertainty due to historical volatility and anomalies. This gives the Supply
Chain Manager persona a data-driven basis for procurement scheduling, and gives the Operations
Analyst a documented baseline against which to judge future demand deviations.

## 9. Next Phase (Week 4)

The saved future forecast (`future_demand_forecast.csv`), along with the Week 2 anomaly outputs,
will be surfaced in an interactive Streamlit application: a dropdown to select product category, a
chart of the next 3 months of forecasted demand with adjustable confidence intervals, and
historical anomalies overlaid on the same chart.
