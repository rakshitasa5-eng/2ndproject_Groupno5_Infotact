# 2ndproject
## Supply Chain Analytics - Demand Forecasting & Anomaly Detection
## Week 3 — Demand Forecasting Models
**Owner (Lead this week):** you
**Status:** 🟡 In progress
**Depends on:** `data/monthly_demand_clean.csv` and `data/monthly_demand_clean_long.csv` (produced in Week 1)
**Feeds into:** Week 4 Streamlit app (forecast chart + confidence interval slider)

---

## 1. What this week is, in one sentence

Take the cleaned monthly demand series from Week 1 and produce a forecast of the next 3 months of demand per product category, validated against real held-out data, with an honest error score — not just a chart that looks plausible.

## 2. Why this exists (tied back to the business objective)

The project's stated success metric is minimizing **MAPE** or **RMSE** — this week is where that number actually gets produced. Everything upstream (cleaning, decomposition) exists to make this forecast trustworthy; everything downstream (Streamlit, the confidence slider) exists to *show* it to a Supply Chain Manager who will use it to decide how much to order next quarter. If the forecast is wrong with false confidence, the business impact is the exact problem in the brief — bloated warehouses or stockouts. So this week isn't "run Prophet and get a chart" — it's "run Prophet, prove how wrong it might be, and say so honestly."

## 3. What I will actually produce this week

| Deliverable | File | Description |
|---|---|---|
| Forecasting notebook | `notebooks/03_forecasting.ipynb` | All exploration, model fitting, evaluation, plots |
| Reusable forecasting functions | `src/forecasting.py` | Clean functions Streamlit (Week 4) can import directly |
| Forecast output data | `data/forecast_output.csv` | Per-category forecast + confidence bounds, ready to plot |
| Model comparison table | in README + notebook | Baseline vs Prophet, MAPE/RMSE per category |

## 4. Method — what I will do and how

### Step 1: Chronological train/test split (per category)
Never a random split for time series — the model must never see the future during training.
```python
series = monthly_wide_interp['CPU'].dropna()
split_point = int(len(series) * 0.8)
train, test = series[:split_point], series[split_point:]
```
Given how few data points some categories have (RAM ≈ 8 months), an 80/20 split may leave test sets of only 1–2 points for the sparsest categories — I'll flag those as "insufficient data for reliable validation" rather than reporting a misleadingly precise MAPE on 1 data point.

### Step 2: Baseline model — simple moving average
Establishes the floor any "real" model has to beat. If Prophet can't beat a moving average, that's a real and reportable finding, not a failure to hide.
```python
def moving_average_forecast(train, test, window=3):
    history = list(train)
    preds = []
    for _ in range(len(test)):
        preds.append(np.mean(history[-window:]))
        history.append(preds[-1])
    return pd.Series(preds, index=test.index)
```

### Step 3: Primary model — Facebook Prophet
Chosen over ARIMA because it tolerates short/irregular monthly series better and produces confidence intervals natively — which Week 4's slider needs directly, without extra work.
```python
from prophet import Prophet

prophet_df = train.reset_index()
prophet_df.columns = ['ds', 'y']

model = Prophet(interval_width=0.90, yearly_seasonality=True)
model.fit(prophet_df)

future = model.make_future_dataframe(periods=len(test) + 3, freq='MS')
forecast = model.predict(future)
# forecast['yhat'], ['yhat_lower'], ['yhat_upper'] = the interval Week 4 will render
```

### Step 4: Evaluate honestly
```python
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error

test_forecast = forecast.set_index('ds').loc[test.index, 'yhat']
mape = mean_absolute_percentage_error(test, test_forecast)
rmse = mean_squared_error(test, test_forecast, squared=False)
ma_mape = mean_absolute_percentage_error(test, moving_average_forecast(train, test))
```
Both numbers get reported side by side for every category — not just the one that makes Prophet look best.

### Step 5: Repeat for all 5 categories, wrapped in one function
```python
def forecast_category(monthly_wide_interp, category, test_frac=0.2, periods=3):
    # returns: forecast_df, mape, rmse, ma_mape, data_sufficiency_flag
    ...
```
`data_sufficiency_flag` matters — it's how RAM gets marked "low confidence" in the app instead of silently shown with the same authority as CPU.

### Step 6 (stretch, only if time allows): ARIMA as a second comparison model
Only pursued if the Prophet-vs-baseline comparison is solid first. A three-way comparison is a bonus, not the requirement.

## 5. Output contract for Week 4 (Streamlit)

`data/forecast_output.csv` will have this exact schema, so the Streamlit dropdown just filters it — no re-fitting models inside the app:

| Column | Meaning |
|---|---|
| `ds` | date (month start) |
| `CategoryName` | one of the 5 categories |
| `yhat` | point forecast |
| `yhat_lower`, `yhat_upper` | 90% interval bounds (Week 4's slider will need multiple interval widths — see note below) |
| `is_forecast` | `True` for future months, `False` for historical fitted values |
| `data_sufficiency` | `"ok"` or `"low"` — drives the warning banner in the app |

**Open item to resolve with Week 4's owner:** the confidence-interval slider needs more than one interval width. Either (a) I refit Prophet at 3 fixed widths (80/90/95%) and store all three, or (b) Week 4 recomputes from Prophet's stored uncertainty samples. I'll decide this by mid-week and update this section — flagging now so it isn't a surprise handoff.

## 6. How to run this week's work

```bash
git checkout main
git pull
git checkout -b week3-forecasting-<yourname>

source venv/bin/activate
pip install -r requirements.txt      # confirms prophet, scikit-learn are present

jupyter notebook notebooks/03_forecasting.ipynb
```

## 7. Success criteria for this week (how I'll know it's actually done)

- [ ] Baseline moving-average forecast implemented and scored for all 5 categories
- [ ] Prophet forecast implemented and scored for all 5 categories
- [ ] MAPE and RMSE reported side by side (Prophet vs baseline) — including cases where Prophet loses
- [ ] Categories with insufficient test data explicitly flagged, not silently scored
- [ ] `data/forecast_output.csv` written in the agreed schema above
- [ ] `src/forecasting.py` has a single clean function Week 4 can import without touching notebook code
- [ ] Interval-width open item (Section 5) resolved and documented

## 8. How the rest of the team supports this, in parallel

| Person | Task this week |
|---|---|
| Support 1 | Re-runs the pipeline independently on 1–2 categories to catch leakage/off-by-one bugs before merge |
| Support 2 | Builds `get_category_data()` in the data-serving layer that Streamlit will call, using this section's output schema |
| Support 3 | Builds the confidence-interval slider UI against dummy forecast data, ready to wire in once Section 5's open item is resolved |

## 9. Commit plan

- Commit after Step 2 (baseline working): `feat: add moving average baseline forecast`
- Commit after Step 3–4 (Prophet + evaluation working, one category): `feat: add Prophet forecasting with MAPE/RMSE evaluation`
- Commit after Step 5 (all categories, function wrapped): `feat: generalize forecasting pipeline across all categories`
- Commit after Section 5 (output file finalized): `feat: export forecast_output.csv for streamlit consumption`
- Final commit: `docs: finalize week 3 README with results and model comparison table`

Open a PR into `main` at the end, tag a teammate for review before merging — don't merge your own forecasting PR without a second set of eyes on the MAPE/RMSE numbers specifically, since a silent leakage bug here is the easiest way to report a fake-good score.
