"""
Supply Chain Demand Analytics — Streamlit Dashboard
Week 4: Interactive deployment of Week 1-3 analysis
(Historical trends, anomaly detection, model comparison, future forecasting)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import streamlit as st

# -----------------------------------------------------------------------
# Page config — must be the first Streamlit command
# -----------------------------------------------------------------------
st.set_page_config(
    page_title="Supply Chain Demand Analytics",
    page_icon="📦",
    layout="wide",
)

# -----------------------------------------------------------------------
# Data loading (cached so files aren't re-read on every interaction)
# -----------------------------------------------------------------------
@st.cache_data
def load_historical():
    df = pd.read_csv("monthly_demand_clean.csv", index_col=0, parse_dates=True)
    return df

@st.cache_data
def load_anomalies():
    df = pd.read_csv("final_anomaly_dataset.csv", parse_dates=["OrderDate"])
    return df

@st.cache_data
def load_future_forecast():
    df = pd.read_csv("future_demand_forecast.csv", parse_dates=["OrderDate"])
    return df

@st.cache_data
def load_model_comparison():
    return pd.read_csv("model_comparison_results.csv")

@st.cache_data
def load_best_model():
    return pd.read_csv("best_model_per_category.csv")


historical_df = load_historical()
anomalies_df = load_anomalies()
future_df = load_future_forecast()
model_comparison_df = load_model_comparison()
best_model_df = load_best_model()

CATEGORIES = historical_df.columns.tolist()

# -----------------------------------------------------------------------
# Sidebar — global controls (dropdown for product selection)
# -----------------------------------------------------------------------
st.sidebar.title("📦 Controls")

selected_category = st.sidebar.selectbox(
    "Select a product category",
    CATEGORIES,
    help="Applies to every tab in the dashboard.",
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Data source: Week 1-3 pipeline outputs "
    "(monthly_demand_clean.csv, final_anomaly_dataset.csv, "
    "future_demand_forecast.csv, model_comparison_results.csv)."
)

st.title("📈 Supply Chain Demand Analytics Dashboard")
st.caption(f"Currently viewing: **{selected_category}**")

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Historical Trends", "🚨 Anomaly Detection", "🏆 Model Comparison", "🔮 Future Forecast"]
)

# =========================================================================
# TAB 1 — Historical Trends
# =========================================================================
with tab1:
    st.subheader(f"{selected_category} — Historical Monthly Demand")

    series = historical_df[selected_category]

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(series.index, series.values, color="lightgray", linewidth=1, label="Actual")
    ax.plot(
        series.index,
        series.rolling(3, min_periods=1).mean(),
        color="steelblue",
        linewidth=2,
        label="3-Month Trend",
    )
    ax.set_xlabel("Month")
    ax.set_ylabel("Quantity")
    ax.legend()
    ax.set_title(f"{selected_category} — Demand Trend")
    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)
    col1.metric("Average monthly demand", f"{series.mean():.0f}")
    col2.metric("Peak demand", f"{series.max():.0f}")
    col3.metric("Missing months", int(series.isna().sum()))

# =========================================================================
# TAB 2 — Anomaly Detection
# =========================================================================
with tab2:
    st.subheader(f"{selected_category} — Flagged Anomalies")

    cat_anom = anomalies_df[anomalies_df["CategoryName"] == selected_category].copy()
    cat_anom = cat_anom.sort_values("OrderDate")

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(cat_anom["OrderDate"], cat_anom["Quantity"], color="steelblue", linewidth=1.5, label="Demand")

    flagged = cat_anom[cat_anom["Final_Anomaly"] == True]
    ax.scatter(
        flagged["OrderDate"], flagged["Quantity"],
        color="red", marker="x", s=90, zorder=5, label="Anomaly (Final)",
    )
    ax.set_xlabel("Month")
    ax.set_ylabel("Quantity")
    ax.legend()
    ax.set_title(f"{selected_category} — Anomaly Overlay")
    st.pyplot(fig)

    st.markdown("**Detection method agreement** (Z-Score / IQR / Isolation Forest):")
    method_counts = cat_anom["Anomaly_Method_Count"].value_counts().sort_index()
    st.bar_chart(method_counts)

    with st.expander("View flagged anomaly rows"):
        st.dataframe(
            flagged[["OrderDate", "Quantity", "ZScore", "IQR_Anomaly", "IF_Anomaly", "Anomaly_Method_Count"]],
            use_container_width=True,
        )

# =========================================================================
# TAB 3 — Model Comparison
# =========================================================================
with tab3:
    st.subheader(f"{selected_category} — Forecasting Model Comparison")

    cat_models = model_comparison_df[model_comparison_df["CategoryName"] == selected_category]
    best_row = best_model_df[best_model_df["CategoryName"] == selected_category]

    if not best_row.empty:
        st.success(
            f"**Best model for {selected_category}: {best_row.iloc[0]['Model']}** "
            f"(RMSE = {best_row.iloc[0]['RMSE']:.1f})"
        )

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(cat_models["Model"], cat_models["RMSE"], color="darkorange")
    ax.set_ylabel("RMSE (lower is better)")
    ax.set_title(f"{selected_category} — Model RMSE Comparison")
    st.pyplot(fig)

    st.caption(
        "⚠️ MAPE is not shown for model selection — several test-period months have zero actual "
        "demand, which makes MAPE mathematically unstable (division by zero). RMSE is used as "
        "the reliable comparison metric instead, consistent with `best_model_per_category.csv`."
    )

    with st.expander("View raw comparison table"):
        st.dataframe(cat_models.reset_index(drop=True), use_container_width=True)

# =========================================================================
# TAB 4 — Future Forecast (with adjustable confidence interval slider)
# =========================================================================
with tab4:
    st.subheader(f"{selected_category} — Future Demand Forecast")

    confidence = st.slider(
        "Forecast confidence interval (%)",
        min_value=50, max_value=99, value=95, step=1,
        help="Adjusts the width of the shaded uncertainty band around the forecast.",
    )

    cat_future = future_df[future_df["CategoryName"] == selected_category].copy()
    cat_future = cat_future.sort_values("OrderDate")

    # The source file only stores a fixed 95% CI. To let the slider adjust the
    # band width without re-fitting the model here, we back out the implied
    # standard error from the stored 95% interval, then rescale it for the
    # user-selected confidence level using the normal-distribution z-score.
    z_95 = norm.ppf(0.975)
    implied_se = (cat_future["Upper_CI"] - cat_future["Forecast"]) / z_95

    z_selected = norm.ppf(0.5 + confidence / 200)
    lower_adj = cat_future["Forecast"] - z_selected * implied_se
    upper_adj = cat_future["Forecast"] + z_selected * implied_se

    # Demand cannot be negative — clip for display only, and warn if we had to.
    lower_display = lower_adj.clip(lower=0)
    clipped = (lower_adj < 0).any()

    fig, ax = plt.subplots(figsize=(10, 4.5))
    hist_series = historical_df[selected_category]
    ax.plot(hist_series.index, hist_series.values, color="steelblue", label="Historical")
    ax.plot(cat_future["OrderDate"], cat_future["Forecast"], color="crimson", marker="o", label="Forecast")
    ax.fill_between(
        cat_future["OrderDate"], lower_display, upper_adj,
        color="crimson", alpha=0.2, label=f"{confidence}% Confidence Interval",
    )
    ax.set_xlabel("Month")
    ax.set_ylabel("Quantity")
    ax.legend()
    ax.set_title(f"{selected_category} — Forecast with {confidence}% Confidence Interval")
    st.pyplot(fig)

    if clipped:
        st.warning(
            "The lower confidence bound was clipped at 0 for display (demand can't be negative). "
            "This category's forecast model shows high uncertainty — treat the point forecast "
            "as directional, not a precise commitment."
        )

    # Flag categories where the model output looks numerically unstable
    if (cat_future["Upper_CI"] - cat_future["Lower_CI"]).max() > 10 * hist_series.max():
        st.error(
            f"⚠️ Data quality note: {selected_category}'s forecast confidence interval is "
            "extremely wide relative to historical demand, suggesting the underlying model did "
            "not converge well for this category. Recommend re-fitting before using this forecast "
            "for business decisions."
        )

    with st.expander("View raw forecast table"):
        st.dataframe(cat_future.reset_index(drop=True), use_container_width=True)
