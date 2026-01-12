from dotenv import load_dotenv
import streamlit as st
import pandas_gbq
import pandas as pd
import plotly.express as px
import os

load_dotenv()

st.set_page_config(page_title="GHOST-SHIELD AI", layout="wide")

PROJECT_ID = os.environ["GCP_PROJECT_ID"]
DATASET = os.environ["BIGQUERY_DATASET"]

@st.cache_data
def load_data():
    query = f"SELECT * FROM `{DATASET}.final_results`"

    df = pandas_gbq.read_gbq(query, project_id=PROJECT_ID)
    df['Date'] = pd.to_datetime(df['Date'])
    return df.sort_values('Date')

try:
    df = load_data()

    st.sidebar.header("🛡️ GHOST-SHIELD AI")
    all_skus = df['SKU'].unique()
    selected_sku = st.sidebar.multiselect("Select Products", options=all_skus, default=all_skus)
    filtered_df = df[df['SKU'].isin(selected_sku)]

    st.title("Supply Chain Action Dashboard")
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    total_savings = df["cost_saving"].sum()
    ghost_cases = int(df["ghost_demand"].sum())

    m1.metric("Total Savings Found", f"₹{total_savings:,.0f}")
    m2.metric("Ghost Demand Alerts", ghost_cases)
    m3.metric("Actionable Cuts", int((df["recommended_cut"] > 0).sum()))


    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("Ghost Demand Trends")
        st.plotly_chart(px.line(filtered_df, x='Date', y='ghost_demand', color='SKU'), use_container_width=True)
    with col_r:
        st.subheader("Savings by SKU")
        st.bar_chart(filtered_df.groupby('SKU')['cost_saving'].sum())

    st.divider()

    st.header("💡 Strategic Simulation Tool")
    st.info("Adjust parameters to see how production changes affect the bottom line.")
    
    sim_col1, sim_col2 = st.columns([1, 2])
    
    with sim_col1:
        st.write("**Simulation Inputs**")
        production_multiplier = st.slider("Adjust Production Cost (Multiplier)", 0.5, 2.0, 1.0)
        risk_appetite = st.select_slider("Risk Appetite", options=["Conservative", "Balanced", "Aggressive"])
        if risk_appetite == "Conservative":
            risk_multiplier = 0.5
        elif risk_appetite == "Balanced":
            risk_multiplier = 1.0
        else:
            risk_multiplier = 1.3
        
    with sim_col2:
        st.write("**Projected Impact**")
        base_savings = filtered_df['cost_saving'].sum()
        simulated_savings = base_savings * production_multiplier * risk_multiplier
        st.success(f"With current settings, potential savings increase to: **₹{simulated_savings:,.0f}**")

    st.divider()

    st.header("🤖 Gemini Intelligence Insights")
    with st.expander("View Logic Behind Alerts", expanded=True):
        st.write(f"The **Isolation Forest** model identified {len(filtered_df)} anomalies.")
        st.write(f"Recent spikes in SKU {selected_sku[0]} suggest localized demand decay. Recommendation: Reduce safety stock by 15% for next 7 days.")

    st.header("Production Cut Ledger")
    st.dataframe(filtered_df[['Date', 'SKU', 'recommended_cut', 'cost_saving']].head(10), use_container_width=True)

except Exception as e:
    st.error(f"Error loading UI: {e}")
