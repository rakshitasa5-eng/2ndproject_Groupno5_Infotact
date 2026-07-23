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

# Week 2 – Statistical Anomaly Detection

## Project 3: Supply Chain Analytics – Demand Forecasting & Anomaly Detection

**Duration:** 17 July 2026 – 24 July 2026  
**Role:** Team Lead  
**Environment:** Jupyter Notebook  
**Language:** Python  

---

## 1. Overview

The main objective of my Week 2 work was to develop an anomaly detection pipeline for identifying unusual demand patterns in historical supply chain data.

I used the cleaned monthly demand dataset prepared during Week 1 and implemented three anomaly detection techniques:

- Z-Score
- Interquartile Range (IQR)
- Isolation Forest

The results from all three methods were compared to identify unusual demand observations and create a final anomaly dataset for further forecasting and dashboard development.

---

## 2. Business Problem

Unexpected changes in product demand can negatively affect supply chain operations.

Unusually high demand may contribute to:

- Stock shortages
- Emergency procurement
- Lost sales
- Delayed order fulfillment

Unusually low demand may contribute to:

- Overstocking
- Increased storage costs
- Tied-up working capital
- Inventory inefficiency

The purpose of this analysis was to automatically identify unusual demand patterns so that supply chain and operations teams can focus on observations that require further investigation.

---

## 3. Objective of My Work

My main objectives during Week 2 were:

- Load and inspect the cleaned monthly demand dataset.
- Validate data types and missing values.
- Analyze demand trends across product categories.
- Implement Z-Score anomaly detection.
- Implement IQR anomaly detection.
- Implement Isolation Forest anomaly detection.
- Compare all three anomaly detection methods.
- Create a multi-method anomaly agreement rule.
- Prepare the final anomaly dataset.
- Generate anomaly summary files.
- Validate the complete anomaly detection pipeline.
- Export final CSV files for future project phases.

---

## 4. Input Dataset

The main dataset used for my Week 2 analysis was:

`monthly_demand_clean_long.csv`

This dataset was prepared during Week 1 after cleaning, monthly aggregation, missing-period handling, and time-series preprocessing.

The main columns used were:

| Column | Description |
|---|---|
| OrderDate | Month associated with demand |
| CategoryName | Product category |
| Quantity | Monthly demand quantity |

The analysis covered five product categories:

- CPU
- Mother Board
- RAM
- Storage
- Video Card

---

## 5. My Week 2 Workflow

The workflow followed during my analysis was:

Clean Monthly Demand Dataset  
↓  
Dataset Inspection and Validation  
↓  
Demand Trend Analysis  
↓  
Z-Score Anomaly Detection  
↓  
IQR Anomaly Detection  
↓  
Isolation Forest  
↓  
Comparison of Three Methods  
↓  
Multi-Method Agreement  
↓  
Final Anomaly Flag  
↓  
Final Anomaly Dataset  
↓  
CSV Export and Validation

---

## 6. Dataset Inspection and Demand Analysis

I started Week 2 by loading `monthly_demand_clean_long.csv` into Jupyter Notebook.

I performed the following checks:

- Inspected the first rows of the dataset.
- Checked dataset shape.
- Checked column names.
- Verified data types.
- Checked missing values.
- Reviewed product categories.
- Analyzed demand quantities.
- Plotted historical demand trends by category.

### Outcome

The dataset was inspected and prepared for anomaly detection.

The demand trend analysis provided an initial understanding of how monthly demand changed across the five product categories.

---

## 7. Z-Score Anomaly Detection

The first anomaly detection technique I implemented was Z-Score.

Z-Score measures how far a demand observation is from the average demand relative to the standard deviation.

The method was applied category-wise because each product category has a different demand pattern.

A threshold was used to classify observations as normal or anomalous.

A new column was created:

`ZScore_Anomaly`

### Interpretation

- `False` – Observation was not detected as an anomaly.
- `True` – Observation exceeded the selected Z-Score threshold.

### Outcome

Z-Score provided the first statistical method for detecting extreme demand observations.

---

## 8. IQR Anomaly Detection

The second technique I implemented was Interquartile Range (IQR).

For each product category, I calculated:

- Q1 – 25th percentile
- Q3 – 75th percentile
- IQR = Q3 - Q1
- Lower boundary
- Upper boundary

The standard 1.5 × IQR rule was used to identify potential anomalies.

The following columns were created:

- `IQR_Lower`
- `IQR_Upper`
- `IQR_Anomaly`

### Interpretation

- `False` – Demand was within the expected IQR range.
- `True` – Demand was outside the calculated IQR boundaries.

### Outcome

IQR provided a second statistical approach that is less influenced by extreme values than methods based only on mean and standard deviation.

The IQR results were then compared with Z-Score results.

---

## 9. Isolation Forest Anomaly Detection

The third method I implemented was Isolation Forest using Scikit-learn.

Isolation Forest is a machine-learning-based anomaly detection algorithm.

Unlike Z-Score and IQR, it identifies unusual observations by learning how easily individual data points can be isolated from the rest of the data.

The model was applied separately to each product category.

The following result column was created:

`IF_Anomaly`

### Model Configuration

- Algorithm: Isolation Forest
- Analysis: Category-wise
- Random state: 42
- Contamination parameter used to control expected anomaly proportion

### Outcome

Isolation Forest added a machine-learning-based anomaly detection approach to complement the two statistical methods.

---

## 10. Comparison of Three Methods

After implementing all three techniques, I compared:

| Method | Technique |
|---|---|
| Z-Score | Mean and standard deviation based |
| IQR | Quartile-based statistical method |
| Isolation Forest | Machine-learning-based method |

Each observation could be detected by:

- No methods
- One method
- Two methods
- All three methods

I created:

`Anomaly_Method_Count`

This column records how many anomaly detection methods flagged each observation.

### Interpretation

- `0` – No method detected an anomaly.
- `1` – One method detected the observation.
- `2` – Two methods detected the observation.
- `3` – All three methods detected the observation.

---

## 11. Final Anomaly Rule

To prioritize stronger anomaly candidates, I created the final anomaly flag:

`Final_Anomaly`

The project rule used was:

**Final Anomaly = Observation detected by at least two anomaly detection methods.**

This means:

- Method Count 0 → Normal
- Method Count 1 → Possible anomaly
- Method Count 2 → Higher-confidence anomaly candidate
- Method Count 3 → Strong anomaly candidate

### Reason for Multi-Method Comparison

The project requires anomaly detection without creating excessive alerts.

Using agreement between multiple methods provides a practical way to prioritize unusual observations rather than treating every single-method detection as an equally important alert.

This rule prioritizes anomaly candidates for investigation but does not automatically prove the business cause of an anomaly.

---

## 12. Final Anomaly Dataset

After comparing all three methods, I prepared:

`final_anomaly_dataset.csv`

The final dataset contains:

- OrderDate
- CategoryName
- Quantity
- ZScore
- ZScore_Anomaly
- IQR_Lower
- IQR_Upper
- IQR_Anomaly
- IF_Anomaly
- Anomaly_Method_Count
- Final_Anomaly

This dataset contains the complete anomaly detection results and can be used in later stages of the project.

---

## 13. Anomaly Summary

I created:

`anomaly_summary.csv`

The summary contains category-wise information including:

- Total records
- Average demand
- Maximum demand
- Z-Score anomaly count
- IQR anomaly count
- Isolation Forest anomaly count
- Final anomaly count

This summary makes it easier to compare anomaly behavior across product categories.

---

## 14. Final Output Files

The important files generated from my Week 2 work include:

### Notebook

`02_Anomaly_Detection.ipynb`

### CSV Files

- `final_anomaly_dataset.csv`
- `final_detected_anomalies.csv`
- `anomaly_summary.csv`
- `anomaly_method_summary.csv`

### Visualizations

- Z-Score anomaly visualization
- IQR anomaly visualization
- Isolation Forest anomaly visualization
- Final anomaly visualization

---

## 15. Final Validation and Testing

Before completing Week 2, I performed final quality checks on the complete notebook.

The validation included:

- Checking required columns.
- Checking missing values.
- Checking duplicate month-category records.
- Checking quantity values.
- Verifying all five product categories.
- Validating Z-Score anomaly results.
- Validating IQR anomaly results.
- Validating Isolation Forest results.
- Verifying the multi-method anomaly count.
- Checking the final anomaly rule.
- Reopening exported CSV files to confirm successful export.

The complete Jupyter Notebook was also tested from a fresh kernel to confirm that the workflow could run from beginning to end.

---

## 16. Business Understanding

The anomaly detection pipeline helps identify unusual historical demand patterns automatically.

Instead of manually reviewing every demand observation, an Operations Analyst can focus on observations flagged by the anomaly detection methods.

The detected patterns may indicate periods requiring investigation for possible:

- Demand spikes
- Demand drops
- Inventory issues
- Promotional effects
- Seasonal changes
- Operational disruptions

However, anomaly detection identifies unusual behavior only.

Additional business information is required before concluding that an anomaly was specifically caused by a stockout, supplier delay, holiday, promotion, or another operational event.

---

## 17. Business Outcome

My Week 2 work produced a complete anomaly detection pipeline using three different techniques.

The key outcomes were:

- Automated detection of unusual demand patterns.
- Category-wise anomaly analysis.
- Comparison of statistical and machine-learning methods.
- Identification of higher-confidence anomaly candidates using multi-method agreement.
- Creation of a final anomaly dataset.
- Creation of category-wise anomaly summaries.
- Preparation of outputs for future forecasting and dashboard development.

The multi-method approach supports the project's objective of identifying important irregularities while reducing unnecessary alerts.

---

## 18. Week 2 Daily Work Summary

| Date | Work Completed |
|---|---|
| 17 Jul | Loaded and inspected the cleaned monthly dataset, checked data types and missing values, and analyzed demand trends by category. |
| 18 Jul | Implemented category-wise Z-Score anomaly detection and visualized detected anomalies. |
| 19 Jul | Implemented IQR anomaly detection and compared IQR results with Z-Score. |
| 20 Jul | Implemented Isolation Forest and compared all three anomaly detection methods. |
| 21 Jul | Prepared the final anomaly dataset, created anomaly summaries, and integrated final outputs. |
| 22 Jul | Reviewed integrated work, improved code comments, validated datasets, and checked anomaly outputs. |
| 23 Jul | Performed final notebook testing and exported validated CSV files. |
| 24 Jul | Finalized Week 2 documentation, GitHub submission, and prepared the work for presentation. |

---

## 19. Challenges and Solutions

### Challenge 1 – Different Results Across Methods

Z-Score, IQR, and Isolation Forest did not necessarily detect the same observations.

**Solution:**  
Instead of forcing the methods to produce identical results, I compared their outputs and created `Anomaly_Method_Count` to measure method agreement.

### Challenge 2 – Pandas GroupBy Warning During IQR

The initial IQR implementation using `groupby().apply()` generated a FutureWarning.

**Solution:**  
The IQR calculation was revised to process each product category separately without relying on the deprecated GroupBy behavior.

### Challenge 3 – Avoiding Excessive Anomaly Alerts

A single method may identify observations that another method considers normal.

**Solution:**  
A multi-method rule was used to prioritize observations detected by at least two methods as higher-confidence anomaly candidates.

---

## 20. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Jupyter Notebook
- Git
- GitHub

---

## 21. Connection to Week 3

Week 2 completes the anomaly detection component of the project.

The next phase is:

### Week 3 – Demand Forecasting

The next work will focus on:

- Creating a baseline forecasting model.
- Performing chronological train/test splitting.
- Implementing a forecasting model such as ARIMA or Prophet.
- Forecasting future product demand.
- Evaluating model performance using MAPE and/or RMSE.
- Preparing a future demand forecast for Streamlit integration.

---

## 22. Conclusion

During Week 2, I developed and validated the anomaly detection component of the Supply Chain Analytics project.

I implemented Z-Score, IQR, and Isolation Forest to identify unusual demand patterns across product categories.

The results from all three methods were compared, and a multi-method agreement strategy was used to prioritize higher-confidence anomaly candidates.

The final datasets and summaries are now prepared to support the next stages of the project: demand forecasting in Week 3 and Streamlit application development in Week 4.
