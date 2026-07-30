import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Supply Chain Analytics Dashboard",
    layout="wide"
)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("📦 Supply Chain Analytics Dashboard")

st.markdown("""
### 👩‍💻 Developed by: **Rakshita SA**

**Project:** Supply Chain Analytics – Demand Forecasting & Anomaly Detection

**Week 4:** Streamlit Deployment and Final Polish
""")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
from pathlib import Path

BASE_DIR = Path(__file__).parent

st.write("Current folder:", BASE_DIR)
st.write("Files found:", [f.name for f in BASE_DIR.iterdir()])

try:
    forecast = pd.read_csv("forecasting_ready_data.csv")
    future = pd.read_csv("future_demand_forecast.csv")
    anomaly = pd.read_csv("anomaly_summary.csv")

except Exception as e:
    st.error(f"Actual Error: {e}")
    st.stop()
# Convert date column
forecast["OrderDate"] = pd.to_datetime(forecast["OrderDate"])

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.header("Dashboard Filters")

product = st.sidebar.selectbox(
    "Select Product",
    sorted(forecast["CategoryName"].unique())
)

confidence = st.sidebar.slider(
    "Forecast Confidence (%)",
    min_value=80,
    max_value=99,
    value=95
)

st.sidebar.write(f"Selected Confidence: {confidence}%")
st.sidebar.markdown("## 👩‍💻 Developer")
st.sidebar.write("Rakshita SA")

# -------------------------------------------------
# Filter Dataset
# -------------------------------------------------
filtered = forecast[forecast["CategoryName"] == product]

# -------------------------------------------------
# Dataset Preview
# -------------------------------------------------
st.subheader("Dataset Preview")
st.dataframe(filtered)

# -------------------------------------------------
# Demand Trend
# -------------------------------------------------
st.subheader("Demand Trend")

fig, ax = plt.subplots(figsize=(10,4))

ax.plot(
    filtered["OrderDate"],
    filtered["Quantity"],
    marker="o"
)

ax.set_title(f"Demand Trend - {product}")
ax.set_xlabel("Order Date")
ax.set_ylabel("Quantity")
plt.xticks(rotation=45)

st.pyplot(fig)

# -------------------------------------------------
# Forecast Table
# -------------------------------------------------
st.subheader("Future Demand Forecast")

if "CategoryName" in future.columns:
    future_filtered = future[
        future["CategoryName"] == product
    ]
else:
    future_filtered = future

st.dataframe(future_filtered)

# -------------------------------------------------
# Anomaly Table
# -------------------------------------------------
st.subheader("Anomaly Detection")

if "CategoryName" in anomaly.columns:
    anomaly_filtered = anomaly[
        anomaly["CategoryName"] == product
    ]
else:
    anomaly_filtered = anomaly

st.dataframe(anomaly_filtered)

# -------------------------------------------------
# Business Insights
# -------------------------------------------------
st.subheader("Business Insights")

st.success("""
• Forecasting helps improve inventory planning.

• Demand trends help identify seasonal patterns.

• Anomaly detection highlights unusual sales behavior.

• Product-wise analysis supports better stock allocation.

• Interactive dashboard enables faster business decisions.
""")

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("""
### 👩‍💻 Developed by: **Rakshita SA**

📧 Email: your_email@example.com

🔗 GitHub: https://github.com/rakshitasa5-eng

💼 LinkedIn: https://linkedin.com/in/rakshita-sa-98a749256
""")