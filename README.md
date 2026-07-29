# 2ndproject
## Supply Chain Analytics - Demand Forecasting & Anomaly Detection

# 📦 Week 1 – Repository & Environment Setup

## 🚀 Project Title

**Supply Chain Analytics – Demand Forecasting & Anomaly Detection**

---

## 📅 Duration

**Week 1:** July 10 – July 17

---

# 📖 Objective

The objective of this week's work was to establish a standardized development environment for the entire team. This included creating the project repository, organizing the folder structure, configuring GitHub collaboration, managing project dependencies, and preparing the repository for future development.

---

# ✅ Tasks Completed

## 1. GitHub Repository Setup

- Created the project repository.
- Initialized the repository with a README file.
- Added a Python `.gitignore` file.
- Organized the project structure.

---

## 2. Project Folder Structure

Created the following directory structure:

```text
Supply-Chain-Analytics/
│
├── app/
├── data/
│   └── raw/
├── notebooks/
├── src/
├── docs/
├── images/
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 3. Dataset Management

- Added the raw supply chain dataset.
- Stored all CSV files inside the `data/raw` folder.
- Verified that the dataset files were correctly organized.

---

## 4. Python Environment Setup

Prepared the project environment by installing the required Python libraries.

Main libraries used:

- Pandas
- NumPy
- Matplotlib
- Seaborn
- Statsmodels
- Scikit-learn
- Prophet
- Streamlit
- Plotly

Generated the `requirements.txt` file to ensure every team member can install the same dependencies.

---

## 5. Git Configuration

Configured the repository with:

- Python `.gitignore`
- Standard project structure
- Clean repository organization

Ignored files include:

```text
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.DS_Store
```

---

## 6. Team Collaboration

- Invited all team members to the repository.
- Shared the repository for collaborative development.
- Defined the branch-based workflow.

Development workflow:

```text
Main Branch
      │
      ├── Week1 Branch
      ├── Week2 Branch
      ├── Week3 Branch
      └── Week4 Branch
```

---

# 📁 Files Added

```text
README.md
requirements.txt
.gitignore
data/raw/
app/
docs/
images/
notebooks/
src/
```

---

# 🛠 Technologies Used

- Git
- GitHub
- Python
- Jupyter Notebook
- Command Prompt

---

# 📌 Deliverables

- GitHub repository created
- Standard project folder structure
- Raw dataset uploaded
- Project dependencies documented
- Git ignore configuration completed
- Team collaboration workflow established

---

# 🎯 Outcome

The repository and development environment were successfully prepared for the project. The standardized structure and dependency management enable all team members to work consistently throughout the remaining project phases.

---

# Week 2 – Statistical Anomaly Detection

## Project: Supply Chain Analytics – Demand Forecasting & Anomaly Detection

**Duration:** 17 July 2026 – 24 July 2026  
**Phase:** Statistical Anomaly Detection  
**Environment:** Jupyter Notebook  
**Language:** Python  

---

## 1. Week 2 Overview

Week 2 focused on identifying unusual demand patterns in the cleaned monthly supply chain data prepared during Week 1.

Three anomaly detection techniques were implemented and compared:

1. Z-Score
2. Interquartile Range (IQR)
3. Isolation Forest

The methods were applied category-wise so that unusual demand could be evaluated relative to the normal demand behavior of each product category.

The outputs from all three methods were compared, and observations detected by multiple methods were prioritized as higher-confidence anomaly candidates.

---

## 2. Business Problem

Unexpected changes in product demand can create major supply chain challenges.

Sudden demand increases may contribute to:

- Stock shortages
- Emergency procurement
- Delayed order fulfillment
- Lost sales opportunities

Unexpected demand decreases may contribute to:

- Overstocking
- Increased warehouse costs
- Tied-up working capital
- Inventory inefficiency

Manually reviewing every monthly demand observation is inefficient.

Therefore, the objective of Week 2 was to develop an automated anomaly detection pipeline capable of identifying unusual demand patterns that require further business investigation.

---

## 3. Week 2 Objectives

The main objectives were:

- Load and validate the cleaned monthly demand dataset from Week 1.
- Analyze category-wise historical demand patterns.
- Implement Z-Score anomaly detection.
- Implement IQR anomaly detection.
- Implement Isolation Forest anomaly detection.
- Compare the results of all three techniques.
- Identify higher-confidence anomaly candidates using multi-method agreement.
- Reduce unnecessary alerts and support the project's goal of avoiding alert fatigue.
- Export final anomaly datasets for future forecasting and dashboard development.

---

## 4. Input Dataset

The primary input used for Week 2 was:

`monthly_demand_clean_long.csv`

This dataset was generated during Week 1 after:

- Data cleaning
- Dataset integration
- Datetime conversion
- Monthly demand aggregation
- Missing-period handling
- Linear interpolation
- Time-series preprocessing

The main fields used for anomaly detection were:

| Column | Description |
|---|---|
| OrderDate | Monthly time-series date |
| CategoryName | Product category |
| Quantity | Monthly demand quantity |

The product categories analyzed were:

- CPU
- Mother Board
- RAM
- Storage
- Video Card

---

## 5. Week 2 Workflow

The overall anomaly detection workflow was:

Raw Supply Chain Data  
↓  
Week 1 Data Cleaning & Preprocessing  
↓  
Clean Monthly Demand Dataset  
↓  
Data Validation & Demand Trend Analysis  
↓  
Z-Score Detection  
↓  
IQR Detection  
↓  
Isolation Forest  
↓  
Three-Method Comparison  
↓  
Multi-Method Agreement  
↓  
Final Anomaly Dataset  
↓  
Week 3 Forecasting & Week 4 Streamlit Integration

---

## 6. Day 1 – Dataset Loading and Exploration

The cleaned monthly demand dataset generated during Week 1 was loaded into Jupyter Notebook.

The following checks were performed:

- Dataset dimensions
- Column names
- Data types
- Missing values
- Descriptive statistics
- Product categories
- Category-wise demand trends

Monthly demand was visualized to understand historical behavior and identify possible spikes or drops before applying anomaly detection algorithms.

### Outcome

The dataset structure and quality were verified and prepared for statistical anomaly detection.

---

## 7. Z-Score Anomaly Detection

Z-Score was implemented as the first statistical anomaly detection technique.

The method measures how far an observation deviates from the mean relative to the standard deviation.

Z-Scores were calculated separately for each product category because normal demand levels differ across categories.

A strict threshold based on the absolute Z-Score was used to identify extreme demand observations.

### Interpretation

- A Z-Score close to zero indicates demand near the category average.
- A large positive Z-Score indicates unusually high demand.
- A large negative Z-Score indicates unusually low demand.
- Observations exceeding the selected threshold were flagged as potential anomalies.

### Outcome

Category-wise statistical anomalies were identified and visualized against historical monthly demand.

---

## 8. Interquartile Range (IQR) Anomaly Detection

The second method implemented was the Interquartile Range technique.

For each product category, the following values were calculated:

- Q1 – 25th percentile
- Q3 – 75th percentile
- IQR – difference between Q3 and Q1

The lower and upper anomaly boundaries were calculated using the standard 1.5 × IQR rule.

Demand observations outside these boundaries were classified as potential anomalies.

### Why IQR Was Used

IQR provides a robust anomaly detection technique because it is less influenced by extreme observations than methods based entirely on the mean and standard deviation.

### Outcome

IQR anomalies were identified category-wise and compared with the Z-Score results.

---

## 9. Isolation Forest Anomaly Detection

Isolation Forest was implemented as the third anomaly detection method.

Unlike Z-Score and IQR, Isolation Forest is a machine-learning-based anomaly detection algorithm.

The model attempts to isolate observations through random partitioning. Unusual observations are generally easier to isolate than normal observations.

Isolation Forest was applied separately to each product category.

A fixed random state was used to support reproducible results.

### Outcome

Machine-learning-based anomaly candidates were identified and compared with the statistical detection methods.

---

## 10. Comparison of All Three Methods

The outputs of the three methods were compared:

| Method | Approach |
|---|---|
| Z-Score | Mean and standard deviation |
| IQR | Quartile-based statistical boundaries |
| Isolation Forest | Machine-learning-based isolation |

The methods were not expected to identify exactly the same number of anomalies because they use different detection principles.

An observation could therefore be:

- Not detected by any method
- Detected by one method
- Detected by two methods
- Detected by all three methods

This comparison provides a broader assessment than relying on a single anomaly detection technique.

---

## 11. Multi-Method Anomaly Agreement

A method-count feature was created to record how many anomaly detection techniques flagged each observation.

The interpretation was:

- 0 methods → Normal observation
- 1 method → Possible anomaly
- 2 methods → Higher-confidence anomaly candidate
- 3 methods → Strong anomaly candidate

For the final project alerting rule, observations detected by at least two methods were prioritized as higher-confidence anomaly candidates.

### Why This Rule Was Used

The original project objective requires anomaly detection without generating excessive false alerts or "alert fatigue."

Using agreement between multiple methods helps prioritize observations that receive support from more than one detection technique.

This rule is a project-level alerting strategy and does not automatically prove that every flagged observation represents a real supply chain failure.

---

## 12. Final Anomaly Results

The final anomaly counts obtained from the analysis were:

| Detection Method | Number of Anomalies |
|---|---:|
| Z-Score | [ADD ACTUAL RESULT] |
| IQR | [ADD ACTUAL RESULT] |
| Isolation Forest | [ADD ACTUAL RESULT] |
| Final Multi-Method Anomalies | [ADD ACTUAL RESULT] |

These values should be updated using the actual output generated by the final Jupyter Notebook.

---

## 13. Category-Wise Analysis

Anomaly results were summarized for each product category:

- CPU
- Mother Board
- RAM
- Storage
- Video Card

The summary includes:

- Total observations
- Average demand
- Maximum demand
- Z-Score anomaly count
- IQR anomaly count
- Isolation Forest anomaly count
- Final higher-confidence anomaly count

This allows stakeholders to identify which product categories experienced more unusual historical demand behavior.

---

## 14. Data Validation

Before finalizing Week 2, the anomaly dataset was validated for:

- Missing values
- Duplicate month-category records
- Invalid quantities
- Required anomaly columns
- Product category consistency
- Anomaly method outputs
- Final anomaly rule consistency

The complete notebook was executed from a fresh Jupyter kernel to verify that the workflow runs reproducibly from data loading through final result export.

---

## 15. Team Integration

Week 2 work was divided across three team members.

### Team Lead

Responsible for:

- Main anomaly detection pipeline
- Z-Score implementation
- IQR implementation
- Isolation Forest implementation
- Three-method comparison
- Multi-method anomaly logic
- Final dataset integration
- Final validation and exports

### Team Member 2

Responsible for:

- Data validation
- Missing-value verification
- Duplicate checks
- Invalid quantity checks
- Anomaly validation
- Business interpretation support

### Team Member 3

Responsible for:

- Demand trend visualizations
- Anomaly visualizations
- Category-wise charts
- Dashboard-ready visual preparation
- README visualization support

The team outputs were reviewed and integrated before finalizing the Week 2 deliverables.

---

## 16. Final Deliverables

The main Week 2 deliverables include:

### Jupyter Notebooks

- `02_Anomaly_Detection.ipynb`
- `03_Data_Validation.ipynb`
- `04_Visualization.ipynb`

### Final Data Files

- `final_anomaly_dataset.csv`
- `final_detected_anomalies.csv`
- `anomaly_summary.csv`
- `anomaly_method_summary.csv`

### Visualizations

- Z-Score anomaly visualization
- IQR anomaly visualization
- Isolation Forest anomaly visualization
- Final higher-confidence anomaly visualization

---

## 17. Output File Descriptions

### `final_anomaly_dataset.csv`

Contains the complete monthly demand dataset along with anomaly detection outputs from all three methods and the final anomaly flag.

Important fields include:

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

### `final_detected_anomalies.csv`

Contains only observations classified as higher-confidence anomalies according to the final multi-method rule.

### `anomaly_summary.csv`

Contains category-wise summary information including demand statistics and anomaly counts.

### `anomaly_method_summary.csv`

Provides an overall comparison of the number of anomalies detected by Z-Score, IQR, Isolation Forest, and the final multi-method rule.

---

## 18. Business Understanding

The anomaly detection pipeline helps transform historical supply chain data into actionable monitoring information.

Instead of manually reviewing every monthly demand observation, operations teams can focus on unusual demand periods identified by the analytical pipeline.

Potential anomalies may represent situations that require investigation, such as:

- Unexpected demand spikes
- Sudden demand drops
- Unusual purchasing behavior
- Inventory-related disruptions
- Seasonal or promotional effects
- Operational irregularities

However, anomaly detection identifies unusual patterns rather than automatically determining their root cause.

Additional business context is required before attributing an anomaly to a specific event such as a stockout, promotion, holiday, or supplier delay.

---

## 19. Business Outcome

By completing Week 2, the project established an automated anomaly detection layer using both statistical and machine-learning techniques.

The main business benefits are:

- Early identification of unusual demand behavior
- Category-wise monitoring of demand irregularities
- Reduced dependence on manual data inspection
- Multi-method comparison for more reliable anomaly prioritization
- Support for reducing unnecessary operational alerts
- Preparation of anomaly indicators for future dashboard visualization

The final anomaly results can help Operations Analysts prioritize unusual periods for further investigation.

---

## 20. Connection to the Overall Project

Week 1 established the data foundation through:

- Data cleaning
- Monthly aggregation
- Missing-value handling
- Time-series preprocessing
- Seasonal decomposition

Week 2 added:

- Z-Score anomaly detection
- IQR anomaly detection
- Isolation Forest
- Multi-method comparison
- Final anomaly prioritization

The next phases are:

# Week 3 – Demand Forecasting

## Objective

The objective of Week 3 was to build the demand forecasting pipeline using historical demand data, evaluate forecasting performance, and prepare forecasting outputs for the final dashboard.

---

# Team Contributions

## Member 1 – Team Leader

### Responsibilities

- Dataset validation
- Forecast dataset preparation
- Train-test split
- Moving Average baseline
- Forecast evaluation
- Documentation
- GitHub integration

### Deliverables

- forecasting_ready_data.csv
- train-test datasets
- Moving Average results
- README updates

---

## Member 2

### Responsibilities

- Stationarity testing
- ADF Test
- ARIMA model implementation
- Model training
- Forecast generation

### Deliverables

- ARIMA model
- Future demand forecast
- ARIMA prediction outputs

---

## Member 3

### Responsibilities

- Visualization
- Forecast comparison charts
- Business interpretation
- Dashboard support

### Deliverables

- Trend charts
- Forecast plots
- Business insights

---

# Overall Workflow

1. Prepared forecasting dataset.
2. Validated dataset quality.
3. Created chronological train-test split.
4. Implemented Moving Average baseline.
5. Performed stationarity testing.
6. Developed ARIMA forecasting model.
7. Generated future demand forecasts.
8. Evaluated forecasting accuracy.
9. Created visualization dashboards.
10. Documented business recommendations.

---

# Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Statsmodels
- GitHub
- Jupyter Notebook

---

# Deliverables

## Dataset

- forecasting_ready_data.csv

## Forecasting

- train_data.csv
- test_data.csv
- moving_average_results.csv
- arima_predictions.csv
- future_demand_forecast.csv

## Evaluation

- MAE
- RMSE
- MAPE

## Visualizations

- Demand Trend
- Actual vs Forecast
- Future Demand Forecast

---

# Business Insights

- Forecasting improves inventory planning.
- Demand trends help optimize stock levels.
- Seasonal demand can be anticipated.
- Baseline forecasting provides a benchmark.
- Advanced forecasting improves operational decision-making.

---

# Week 3 Outcome

Successfully developed the demand forecasting workflow, generated baseline and advanced forecasts, evaluated model performance, and prepared outputs for the final Streamlit dashboard.

### Week 4 – Streamlit Deployment

The final application will allow stakeholders to:

- Select product categories
- View historical demand
- Identify historical anomalies
- View future demand forecasts
- Interact with forecast settings
- Support inventory and procurement decision-making

