import pandas_gbq

# Configuration from your project
project_id = "ghost-demand-hackathon" 
dataset_id = "supply_chain_data"

# Uploading the winning results
print("Uploading results to BigQuery...")
pandas_gbq.to_gbq(
    ghost_df, 
    f"{dataset_id}.ghost_demand_alerts", 
    project_id=project_id, 
    if_exists='replace'
)

print("Data is live. You can now refresh Looker Studio.")