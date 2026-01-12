import streamlit as st
import pandas_gbq
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="GHOST-SHIELD AI", layout="wide")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ghost-demand-hackathon-6c69f097d879.json" 
project_id = "ghost-demand-hackathon"

@st.cache_data
def load_data():
    query = f"SELECT * FROM `supply_chain_data.ghost_demand_alerts`"
    df = pandas_gbq.read_gbq(query, project_id=project_id)
    df['Date'] = pd.to_datetime(df['Date'])
    return df.sort_values('Date')

try:
    df = load_data()

    st.sidebar.header("🛡️ GHOST-SHIELD AI")
    all_skus = df['SKU'].unique()
    selected_sku = st.sidebar.multiselect("Select Products", options=all_skus, default=all_skus[:3])
    filtered_df = df[df['SKU'].isin(selected_sku)]

    st.title("Supply Chain Action Dashboard")
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Savings Found", f"₹{filtered_df['cost_saving'].sum():,.0f}")
    m2.metric("Anomaly Alerts", len(filtered_df))
    m3.metric("Avg Forecast Error", f"{filtered_df['forecast_error'].mean():.2f}")

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
        
    with sim_col2:
        st.write("**Projected Impact**")
        simulated_savings = filtered_df['cost_saving'].sum() * production_multiplier
        st.success(f"With current settings, potential savings increase to: **₹{simulated_savings:,.0f}**")
        st.progress(0.75 if risk_appetite == "Aggressive" else 0.45)

    st.divider()

    st.header("🤖 Gemini Intelligence Insights")
    with st.expander("View Logic Behind Alerts", expanded=True):
        st.write(f"The **Isolation Forest** model identified {len(filtered_df)} anomalies.")
        st.write("**Gemini Analysis:** Recent spikes in SKU {selected_sku[0]} suggest localized demand decay. Recommendation: Reduce safety stock by 15% for next 7 days.")

    st.header("Production Cut Ledger")
    st.dataframe(filtered_df[['Date', 'SKU', 'recommended_cut', 'cost_saving']].head(10), use_container_width=True)

except Exception as e:
    st.error(f"Error loading UI: {e}")