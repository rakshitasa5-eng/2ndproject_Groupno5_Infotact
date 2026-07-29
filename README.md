# 2ndproject
## Supply Chain Analytics - Demand Forecasting & Anomaly Detection
## 🚀 Week 4 – Interactive Dashboard (Streamlit)

An interactive Streamlit dashboard was built on top of the Week 1–3 analysis, allowing
category-level exploration of demand trends, anomalies, model performance, and future
forecasts, without needing to open Jupyter.

### Features
- **Category dropdown** (sidebar) — switch between CPU, Mother Board, RAM, Storage, Video Card
- **Historical Trends tab** — monthly demand with a 3-month rolling trend line
- **Anomaly Detection tab** — Z-Score / IQR / Isolation Forest flagged points overlaid on the trend
- **Model Comparison tab** — RMSE comparison across Moving Average / SARIMA / Prophet, with the best model per category highlighted
- **Future Forecast tab** — forecast with an **adjustable confidence-interval slider (50–99%)**

### Files
| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application |
| `requirements.txt` | Python dependencies for deployment |
| `06_Streamlit_Deployment.ipynb` | Notebook documenting/testing the app before deployment |
| `monthly_demand_clean.csv` | Historical demand (Week 1) |
| `final_anomaly_dataset.csv` | Anomaly flags (Week 2) |
| `future_demand_forecast.csv`, `model_comparison_results.csv`, `best_model_per_category.csv` | Forecasting outputs (Week 3) |

### Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open the printed local URL in your browser. You'll see output like:
```
Local URL: http://localhost:8501
Network URL: http://10.4.7.68:8501
```
- **Local URL** — use this on the same machine running the app
- **Network URL** — use this to access the dashboard from another device on the same network (e.g. phone, another computer)

### Deploy publicly (Streamlit Community Cloud, free)
1. Push this repo to GitHub (must include `app.py`, `requirements.txt`, and the CSV files above)
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → sign in with GitHub
3. **New app** → select this repo/branch → main file path: `app.py` → **Deploy**
4. Share the generated public URL

### Known data limitations (handled explicitly in the app, not hidden)
- **MAPE is not used for model selection** — several test-period months have zero actual
  demand, making MAPE mathematically unstable (division by zero, values ~1e19). RMSE is
  used instead, matching `best_model_per_category.csv`.
- **The confidence-interval slider is an approximation.** The source data only contains a
  fixed 95% interval; the app rescales it to other confidence levels using the implied
  standard error and a normal-distribution z-score, rather than re-fitting the model live.
- **Mother Board and RAM forecasts show unusually wide/negative confidence bounds**,
  indicating the underlying model did not converge well for these categories. The app
  clips negative bounds at 0 for display and shows an explicit warning rather than
  silently displaying misleading numbers.
