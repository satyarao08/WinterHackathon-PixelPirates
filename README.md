# 🛡️ Ghost-Shield AI

## Description

Ghost-Shield AI is a decision-support system built to detect and mitigate **Ghost Demand** in retail and e-commerce supply chains.

Ghost Demand refers to demand signals that are **real in data but false in intent**. These spikes often occur during flash sales, influencer-driven trends, or promotional campaigns. Traditional forecasting systems treat these spikes as long-term demand, causing businesses to overproduce.

The result:
- Excess inventory
- Heavy discounting
- Warehousing costs
- Product waste
- Capital lock-up

Ghost-Shield AI identifies such misleading demand patterns early and converts them into **actionable production recommendations**, helping organizations reduce costs and waste while improving operational efficiency.

---


## Features

- Detects abnormal demand spikes using unsupervised machine learning  
- Identifies ghost demand at SKU–day level granularity  
- Recommends optimal production cuts using mathematical optimization  
- Estimates production cost savings and waste reduction  
- Provides business-ready dashboards for decision makers  

---

## Tech Stack

- Python  
- Pandas & NumPy  
- Scikit-learn (Isolation Forest)  
- Google OR-Tools  
- Google BigQuery  
- Looker Studio  
- Streamlit (internal exploratory UI)  

---

## Google Technologies Used

### Tools Used
- Google BigQuery
- Looker Studio
- Google OR-Tools
- Antigravity IDE
- Gemini API

### Why We Chose These Google Technologies

- **Google BigQuery**  
  Used as the central analytics warehouse to store processed demand data, ghost demand alerts, and optimization outputs.  
  BigQuery allows fast, scalable SQL-based analysis over large datasets and serves as the backend for dashboards without requiring additional infrastructure.

- **Looker Studio**  
  Used to build interactive dashboards directly connected to BigQuery.  
  This enables judges and stakeholders to explore ghost demand cases, SKU-level savings, and overall business impact in real time without running code.

- **Google OR-Tools**  
  Used to solve constrained optimization problems that convert ML-detected ghost demand into optimal production cut recommendations.  
  This ensures the solution goes beyond detection and delivers actionable, cost-minimizing decisions.

- **Antigravity IDE**  
  Used to write and run the code.  
  This ensures the solution goes beyond detection and delivers actionable, cost-minimizing decisions.

- **Gemini API**  
  To explain the final output of the code.
  
---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/satyarao08/WinterHackathon-PixelPirates
cd WinterHackathon-PixelPirates
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Google Cloud Credentials

- Create a service account in Google Cloud Console with access to BigQuery.
- Download the service account key JSON file.
- Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of the JSON file.

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
```

### 4. Run the Application

```bash
cd src
python main.py
```

```bash
cd ..
streamlit run app.py
```

---

## How it Works

1. **Data Ingestion**: Sales and forecast data are pulled from BigQuery.
2. **Feature Engineering**: The system calculates rolling means, standard deviations, and volatility ratios to capture the "rhythm" of demand.
3. **Detection**: The `ml_model` identifies records where the forecast deviates significantly from historical patterns without corresponding sales support.
4. **Optimization**: For every "Ghost" case, the `optimization` engine calculates the most cost-effective production reduction.
5. **Visualization**: All metrics are aggregated into the dashboard for executive and operational review.

---

## Team Members
- Satyashree G Rao
- Ashutosh Shenoy
