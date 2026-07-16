# 2ndproject
## Supply Chain Analytics - Demand Forecasting & Anomaly Detection
Week: 1
Phase: Time-Series Preprocessing & Decomposition
Tools Used: Python, Pandas, NumPy, Matplotlib, Jupyter Notebook, Git, GitHub

📖 Project Overview

This project focuses on building a Supply Chain Analytics pipeline that predicts future product demand and detects unusual supply chain behavior using historical order data.

The primary objective is to prepare a clean and structured time-series dataset that can be used for anomaly detection, demand forecasting, and an interactive Streamlit dashboard.

Week 1 establishes the foundation by collecting, cleaning, transforming, and preparing historical demand data.

🎯 Week 1 Objective

The main objective of Week 1 was to prepare a reliable monthly demand dataset for future analytics.

The work completed includes:

Understanding the dataset structure
Data quality assessment
Data cleaning
Merging related datasets
Monthly demand aggregation
Missing value handling
Time-series decomposition
Exporting cleaned datasets
📂 Dataset Used

The project uses seven CSV files.

Dataset	Purpose
Orders.csv	Stores order dates and customer IDs
OrderDetails.csv	Stores ordered quantities, prices, and order status
Product.csv	Contains product and category information
Customer.csv	Customer information for business analysis
Employee.csv	Employee and warehouse mapping
Warehouse.csv	Warehouse information
Region.csv	Regional information
📊 Business Problem

Supply chain organizations often struggle to maintain optimal inventory levels.

Problems include:

Overstock increases warehouse and storage costs.
Understock results in stockouts and lost sales.
Demand fluctuations are difficult to predict.
Manual inventory planning leads to inefficient procurement.

This project helps solve these problems using historical sales data and predictive analytics.

⚙️ Week 1 Workflow
Step 1 – Data Loading

Loaded all seven datasets into Jupyter Notebook using Pandas.

Step 2 – Data Understanding

Reviewed:

Dataset structure
Column names
Data types
Number of rows and columns
Missing values
Duplicate records
Step 3 – Data Cleaning

Performed:

Converted OrderDate to datetime format.
Verified primary keys.
Checked for duplicate records.
Validated missing values.
Step 4 – Data Integration

Merged:

Orders.csv
OrderDetails.csv
Product.csv

Created one unified dataset for analysis.

Step 5 – Revenue Calculation

Created a new feature:

Revenue = OrderItemQuantity × PerUnitPrice

This feature will support future business analysis.

Step 6 – Shipped Order Filtering

Only Shipped orders were selected.

Reason:

Pending and Cancelled orders do not represent actual fulfilled customer demand and would reduce forecasting accuracy.

Step 7 – Monthly Time-Series Creation

Converted daily transactions into monthly demand using:

OrderDate
CategoryName
OrderItemQuantity

This produced a monthly demand dataset for every product category.

Step 8 – Missing Value Handling

Created a complete monthly timeline.

Internal missing months were filled using Linear Interpolation while preserving leading and trailing missing values.

Step 9 – Time-Series Decomposition

Applied Seasonal Decomposition to separate:

Trend
Seasonality
Residual Noise

This helps understand historical demand behavior before forecasting.

Step 10 – Export Clean Data

Generated the following files:

monthly_demand_clean.csv
monthly_demand_clean_long.csv

These datasets will be used in Week 2 and Week 3.

📁 Files Generated
merged_supply_chain.csv

monthly_demand_clean.csv

monthly_demand_clean_long.csv

01_TimeSeries_Preprocessing.ipynb
📈 Technologies Used
Python
Pandas
NumPy
Matplotlib
Statsmodels
Jupyter Notebook
Git
GitHub
✅ Week 1 Deliverables

Completed:

Imported all datasets
Verified dataset quality
Cleaned data
Merged datasets
Converted dates
Created revenue column
Filtered shipped orders
Generated monthly demand dataset
Filled internal missing values
Performed seasonal decomposition
Exported clean datasets
📌 Business Outcome

At the end of Week 1, a clean and structured monthly demand dataset was successfully created.

This dataset provides the foundation for:

Detecting abnormal supply chain behavior (Week 2)
Building demand forecasting models (Week 3)
Deploying an interactive Streamlit dashboard (Week 4)

The preprocessing completed in Week 1 improves data quality, ensures consistent time-series analysis, and supports more accurate business decision-making.

🚀 Next Phase (Week 2)

The cleaned dataset created in Week 1 will be used to implement statistical anomaly detection techniques such as:

Z-Score
Interquartile Range (IQR)
Isolation Forest

These methods will identify unusual demand patterns and operational anomalies that may impact supply chain performance.
