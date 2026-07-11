# Week 1 — Full Granular Guide (Every Team Member)
### Time-Series Preprocessing & Decomposition

This expands Week 1 from the master roadmap into every small step, from an empty laptop to committed code. Four tracks below — one per person. Everyone starts at the same "Day 0" setup, then splits.

---

## Day 0 — Everyone does this together (before any individual work starts)

**Step 0.1 — Confirm tools installed** (each person, on their own machine)
```bash
python3 --version      # need 3.9+
git --version
```
If missing: install Python from python.org, install Git from git-scm.com.

**Step 0.2 — One person creates the GitHub repo** (this is Person B's job, see Track B below — do it first, live on a call, so the other 3 aren't blocked)

**Step 0.3 — Everyone clones it**
```bash
git clone https://github.com/<org>/supply-chain-analytics.git
cd supply-chain-analytics
```

**Step 0.4 — Everyone creates their own virtual environment inside the repo folder**
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```
Explain to the team why: without this, everyone's global Python installs different package versions and code breaks mysteriously on other people's machines. This is the #1 cause of "it works on my computer" in group projects.

**Step 0.5 — Everyone installs the shared dependencies** (Person B will have committed `requirements.txt` first — see Track B step B.4)
```bash
pip install -r requirements.txt
```

**Step 0.6 — Everyone creates their own branch off `main`, named for their task**
```bash
git checkout -b week1-<yourtrack>-<yourname>
# e.g. git checkout -b week1-preprocessing-asha
```

Now the four tracks run in parallel.

---

## TRACK A — Lead: Preprocessing & Decomposition

### Phase 1: Look at the raw data before writing any code

**A1.1** — Open a Jupyter notebook:
```bash
jupyter notebook
```
Create `notebooks/01_preprocessing.ipynb`.

**A1.2** — Load each file individually and just look at it, one cell per file. Don't merge anything yet.
```python
import pandas as pd

orders = pd.read_csv('data/raw/Orders.csv')
orders.head()
```
Do this for `Orders.csv`, `OrderDetails.csv`, `Product.csv`. In separate cells, run:
```python
orders.info()          # check dtypes, nulls
orders.shape           # row/column count
orders['OrderDate'].sample(5)   # see raw date format before parsing
```
**Why this step matters:** you need to see the raw `OrderDate` string format (`2016/11/17`) before you tell pandas how to parse it — guessing wrong here silently corrupts every date downstream.

**A1.3** — Re-load with dates properly parsed:
```python
orders = pd.read_csv('data/raw/Orders.csv', parse_dates=['OrderDate'])
orders['OrderDate'].dtype   # should print datetime64[ns]
```

**A1.4** — Check for duplicates and obvious data problems in each file:
```python
orders.duplicated().sum()
orders['OrderID'].duplicated().sum()   # should be 0, OrderID is a primary key
order_details = pd.read_csv('data/raw/OrderDetails.csv')
order_details['OrderStatus'].value_counts()   # confirms Shipped/Canceled/Pending and their counts
```

### Phase 2: Merge into one working table

**A2.1** — Merge Orders + OrderDetails on `OrderID`:
```python
df = order_details.merge(orders, on='OrderID', how='left')
```
Immediately check nothing was lost or duplicated:
```python
print(len(order_details), len(orders), len(df))   # df should be 400, matching OrderDetails
df['OrderDate'].isna().sum()   # should be 0 — every order detail found its order date
```

**A2.2** — Merge in Product info to get category:
```python
products = pd.read_csv('data/raw/Product.csv')
df = df.merge(products, on='ProductID', how='left')
df['CategoryName'].isna().sum()   # should be 0
```

**A2.3** — Create the revenue field (useful for later EDA / anomaly context even if not core to demand):
```python
df['Revenue'] = df['OrderItemQuantity'] * df['PerUnitPrice']
```

**A2.4 — Commit checkpoint 1:**
```bash
git add notebooks/01_preprocessing.ipynb
git commit -m "feat: load and merge Orders, OrderDetails, Product into unified table"
git push origin week1-preprocessing-<yourname>
```
Do this now, don't wait until the whole notebook is done — small frequent commits are the point.

### Phase 3: Make the scope decision (Shipped only) — and write down why

**A3.1**
```python
df['OrderStatus'].value_counts()
```
**A3.2** — Filter:
```python
shipped = df[df['OrderStatus'] == 'Shipped'].copy()
print(f"{len(shipped)} of {len(df)} order lines are Shipped")
```
**A3.3** — Add a markdown cell in the notebook (not a code cell) explaining the decision in 2–3 sentences: *we forecast realized/shipped demand because Canceled and Pending orders were never fulfilled and would overstate true dispatch volume; we'll revisit Canceled/Pending separately as an anomaly-context signal in Week 2.* This sentence is what a grader/reviewer looks for — data decisions stated explicitly, not buried in code.

### Phase 4: Resample daily → monthly, per category

**A4.1** — Set the date as index and resample:
```python
monthly = (shipped
    .set_index('OrderDate')
    .groupby('CategoryName')
    .resample('MS')['OrderItemQuantity']
    .sum()
    .reset_index())
monthly.head(10)
```

**A4.2** — Pivot to wide format (one column per category — much easier to plot and decompose):
```python
monthly_wide = monthly.pivot(index='OrderDate', columns='CategoryName', values='OrderItemQuantity')
monthly_wide.head()
```

**A4.3** — Look at it visually before doing anything else, to build intuition:
```python
import matplotlib.pyplot as plt
monthly_wide.plot(figsize=(12,6), marker='o')
plt.title('Monthly Shipped Quantity by Category (raw, before gap-filling)')
plt.show()
```
You should see visible gaps (missing months) in the line — that's expected and exactly what the next phase fixes.

**A4.4 — Commit checkpoint 2:**
```bash
git add notebooks/01_preprocessing.ipynb
git commit -m "feat: resample shipped orders to monthly totals per category"
git push
```

### Phase 5: Fill missing months (interpolation)

**A5.1** — Build the complete month range so gaps are explicit `NaN`s instead of just absent rows:
```python
full_range = pd.date_range(monthly_wide.index.min(), monthly_wide.index.max(), freq='MS')
monthly_wide = monthly_wide.reindex(full_range)
monthly_wide.index.name = 'OrderDate'
monthly_wide.isna().sum()   # count of missing months per category — expect this to be nontrivial
```

**A5.2** — Interpolate only *between* known points, never before the first sale or after the last:
```python
monthly_wide_interp = monthly_wide.interpolate(method='linear', limit_area='inside')
```

**A5.3** — Sanity check: plot before vs after for one category, side by side, to confirm interpolation looks reasonable and didn't create anything absurd (negative values, huge spikes):
```python
fig, axes = plt.subplots(1, 2, figsize=(14,5))
monthly_wide['CPU'].plot(ax=axes[0], title='CPU — before interpolation', marker='o')
monthly_wide_interp['CPU'].plot(ax=axes[1], title='CPU — after interpolation', marker='o')
plt.show()
```

**A5.4** — Check remaining NaNs (these are the leading/trailing gaps we deliberately did NOT fill):
```python
monthly_wide_interp.isna().sum()
```
Note in a markdown cell which categories start late or end early (e.g. RAM) — this will matter for the "low confidence" flag in the Streamlit app in Week 4.

**A5.5 — Commit checkpoint 3:**
```bash
git add notebooks/01_preprocessing.ipynb
git commit -m "feat: fill internal gaps via linear interpolation, preserve edge NaNs"
git push
```

### Phase 6: Decomposition

**A6.1** — Run decomposition on the category with the most complete data first (CPU or Storage), to prove the method works before trying sparser categories:
```python
from statsmodels.tsa.seasonal import seasonal_decompose

series = monthly_wide_interp['CPU'].dropna()
result = seasonal_decompose(series, model='additive', period=12)
fig = result.plot()
fig.set_size_inches(10, 8)
plt.show()
```

**A6.2** — Repeat for each of the other 4 categories in a loop, saving each plot:
```python
import os
os.makedirs('notebooks/figures', exist_ok=True)

for cat in monthly_wide_interp.columns:
    s = monthly_wide_interp[cat].dropna()
    if len(s) < 24:   # need at least 2 full yearly cycles for period=12 decomposition to mean anything
        print(f"{cat}: only {len(s)} months — skipping formal decomposition, note as low-data")
        continue
    result = seasonal_decompose(s, model='additive', period=12)
    fig = result.plot()
    fig.suptitle(cat)
    fig.savefig(f'notebooks/figures/decomposition_{cat}.png')
    plt.close(fig)
```
This will likely skip RAM (only 8 months) — that's correct behavior, not a bug. Write a markdown note explaining why.

**A6.3** — Write a short markdown summary per category: does it show a clear upward/downward trend? Any visible seasonal pattern (e.g. spikes around specific months)? Is the residual noisy? This is the actual "understand trend and seasonality" deliverable the brief asks for — the plots alone aren't enough, the written interpretation is what's graded.

### Phase 7: Save the clean output for the rest of the team to build on

**A7.1**
```python
monthly_wide_interp.to_csv('data/monthly_demand_clean.csv')
```

**A7.2** — Also save the long-format version (some downstream code, like Prophet in Week 3, wants one row per date+category rather than wide columns):
```python
monthly_long_clean = monthly_wide_interp.reset_index().melt(
    id_vars='OrderDate', var_name='CategoryName', value_name='Quantity')
monthly_long_clean.to_csv('data/monthly_demand_clean_long.csv', index=False)
```

**A7.3 — Final commit for the week, plus open the PR:**
```bash
git add data/monthly_demand_clean.csv data/monthly_demand_clean_long.csv notebooks/
git commit -m "feat: finalize clean monthly demand dataset and decomposition writeup"
git push origin week1-preprocessing-<yourname>
```
Then open a Pull Request on GitHub into `main`, tag one teammate (rotate who reviews each week) to review before merging. **Do not merge your own PR without a review** — this is the collaboration signal that matters most in a 4-person project.

---

## TRACK B — Support: Repo & Environment Setup

*Do this first, live, before anyone else starts — everyone else is blocked until this exists.*

**B.1** — Create the GitHub repository (via github.com → New Repository), initialize with a README, add a `.gitignore` for Python.

**B.2** — Clone it locally, then build the folder skeleton:
```bash
mkdir -p data/raw notebooks src app
touch data/raw/.gitkeep notebooks/.gitkeep src/__init__.py app/.gitkeep
```

**B.3** — Copy the 7 CSVs into `data/raw/`. Decide as a team: commit the CSVs directly (simplest for a small dataset like this, ~400 rows/file) or `.gitignore` them and document where to download them. For a dataset this small, just commit them — add a note to `.gitignore` only if the files were large.

**B.4** — Write `requirements.txt`:
```
pandas
numpy
matplotlib
seaborn
statsmodels
scikit-learn
prophet
streamlit
plotly
```
Test it installs clean in a fresh venv before committing:
```bash
python3 -m venv test_venv
source test_venv/bin/activate
pip install -r requirements.txt
deactivate && rm -rf test_venv
```

**B.5** — Write `.gitignore`:
```
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.DS_Store
```

**B.6** — Set up branch protection on `main` (GitHub → Settings → Branches): require at least 1 PR review before merge. This is what enforces the "everyone reviews, nobody merges their own work" rule from Track A.

**B.7** — Invite all teammates as collaborators, confirm everyone can clone and push.

**B.8 — Commit:**
```bash
git add .
git commit -m "chore: initialize repo structure, dependencies, and raw data"
git push origin main
```

**B.9 (once A's Phase 2–3 decisions exist)** — Start drafting the top-level `README.md` skeleton (sections: Problem Statement, Data Sources & Caveats, Setup Instructions, Team, Roadmap) — leave placeholders for results that will fill in over the coming weeks. Commit: `docs: add README skeleton`.

---

## TRACK C — Support: Independent EDA Notebook

*Goal: surface patterns the Lead's pipeline-focused work won't have time to find, and validate the Lead's merge independently.*

**C.1** — Create `notebooks/00_eda.ipynb` on your own branch (`week1-eda-<yourname>`).

**C.2** — Load all 7 raw files independently (don't copy the Lead's merge code — the point is an independent check):
```python
import pandas as pd
customer = pd.read_csv('data/raw/Customer.csv')
employee = pd.read_csv('data/raw/Employee.csv')
region = pd.read_csv('data/raw/Region.csv')
warehouse = pd.read_csv('data/raw/Warehouse.csv')
```

**C.3** — Profile each table: nulls, dtypes, duplicate keys, cardinality:
```python
for name, table in [('Customer', customer), ('Employee', employee),
                     ('Region', region), ('Warehouse', warehouse)]:
    print(f"--- {name} ---")
    print(table.info())
    print(table.isna().sum())
    print()
```

**C.4** — Category-level exploration: order counts and revenue split by `CategoryName`:
```python
orders = pd.read_csv('data/raw/Orders.csv', parse_dates=['OrderDate'])
order_details = pd.read_csv('data/raw/OrderDetails.csv')
products = pd.read_csv('data/raw/Product.csv')
df = order_details.merge(orders, on='OrderID').merge(products, on='ProductID')

df.groupby('CategoryName')['OrderItemQuantity'].agg(['count','sum','mean'])
```

**C.5** — Join through Warehouse → Region to see if geography matters at all (this feeds Week 2's "was it a regional stockout?" context question):
```python
employee_wh = employee.merge(warehouse, on='WarehouseID').merge(region, on='RegionID')
employee_wh[['EmployeeName','WarehouseName','RegionName','State']].head()
```
Note: your data doesn't directly link an *order* to a warehouse/region (only employees are linked to warehouses) — write this down as a limitation. Don't force a join that doesn't exist in the schema.

**C.6** — Customer behavior check: do a few large-credit-limit customers dominate order volume (relevant later for "was this anomaly just one big customer")?
```python
cust_orders = orders.merge(customer, on='CustomerID')
cust_orders.groupby('CustomerName').size().sort_values(ascending=False).head(10)
```

**C.7** — Plot order volume over time at the raw/unaggregated level, to visually confirm the sparsity finding before the Lead commits to monthly aggregation — this is your independent validation of that key Week 1 decision:
```python
import matplotlib.pyplot as plt
orders.set_index('OrderDate').resample('MS').size().plot(marker='o', figsize=(12,5))
plt.title('Total Orders per Month (all categories)')
plt.show()
```

**C.8** — Write a short markdown findings summary at the top of the notebook (3–5 bullets): sparsity confirmed/not, any single-customer dominance, any data quality issues found, anything Track A should know before finalizing their pipeline.

**C.9 — Commit:**
```bash
git add notebooks/00_eda.ipynb
git commit -m "docs: add independent EDA notebook — data quality, category, customer, geography checks"
git push origin week1-eda-<yourname>
```
Open a PR, and specifically flag anything from C.8 that might change Track A's approach — this is meant to happen *during* the week, not after, so raise it in your team sync rather than waiting for the PR review.

---

## TRACK D — Support: Streamlit App Skeleton (with dummy data)

*Goal: the app shell exists now, so Week 4 is "swap in real data," not "build the app from scratch under deadline pressure."*

**D.1** — Create `app/streamlit_app.py` on your own branch (`week1-streamlit-skeleton-<yourname>`).

**D.2** — Confirm Streamlit runs at all:
```python
import streamlit as st
st.title("Hello Supply Chain")
```
```bash
streamlit run app/streamlit_app.py
```
Confirm it opens in the browser before building anything else.

**D.3** — Build the sidebar controls with placeholder options (these exact widgets are named in the brief — dropdown for category, slider for confidence interval):
```python
categories = ["CPU", "Video Card", "Storage", "Mother Board", "RAM"]  # from Track A/C's real category list
category = st.sidebar.selectbox("Product Category", categories)
confidence = st.sidebar.slider("Forecast confidence interval", 0.70, 0.95, 0.90, step=0.05)
horizon = st.sidebar.slider("Forecast horizon (months)", 1, 6, 3)
```

**D.4** — Generate dummy time-series data so the chart area has something to render:
```python
import pandas as pd
import numpy as np

dummy_dates = pd.date_range('2023-01-01', periods=24, freq='MS')
dummy_values = np.random.randint(50, 200, size=24)
dummy_series = pd.Series(dummy_values, index=dummy_dates)

st.subheader(f"{category} — Demand (placeholder data)")
st.line_chart(dummy_series)
```

**D.5** — Add a placeholder anomaly table area (Track A/B's anomaly work will feed this in Week 2):
```python
st.subheader("Flagged Anomalies (placeholder)")
dummy_anomalies = pd.DataFrame({
    'Date': dummy_dates[[3, 11, 18]],
    'Value': dummy_values[[3, 11, 18]],
    'Note': ['placeholder anomaly'] * 3
})
st.dataframe(dummy_anomalies)
```

**D.6** — Take a screenshot of the running app, add it to a `docs/screenshots/` folder — useful for the final README and for showing progress in the weekly team sync.

**D.7 — Commit:**
```bash
git add app/streamlit_app.py docs/screenshots/
git commit -m "feat: scaffold streamlit app with sidebar controls and placeholder chart using dummy data"
git push origin week1-streamlit-skeleton-<yourname>
```
Open a PR. Note in the PR description exactly which function signature you expect from Track A/B's data pipeline (e.g. `get_category_data(category) -> {history, forecast, anomalies}`) — this becomes the informal contract that makes Week 3–4 integration painless instead of a last-minute mess.

---

## End-of-week sync (all 4 people, ~30 min call)

Go through in order:
1. **Track B** confirms repo/env is stable — everyone can `pip install -r requirements.txt` clean.
2. **Track A** presents `monthly_demand_clean.csv` and the decomposition findings — trend/seasonality per category, and which categories are low-data (flag RAM).
3. **Track C** presents EDA findings — specifically raises anything that should change Track A's approach (do this *before* Track A's PR merges, not after).
4. **Track D** demos the running Streamlit skeleton and states the data-contract it expects for Week 3.
5. All 4 PRs get reviewed (rotate reviewer assignments) and merged to `main`.
6. Assign Week 2 Lead (Anomaly Detection) and confirm everyone's Week 2 support role from the master roadmap.

By the end of Day 0 through this sync, every person should have **3+ commits** on their branch and one merged PR — a healthy, visible contribution from all four people, not just the nominal "Week 1 Lead."
