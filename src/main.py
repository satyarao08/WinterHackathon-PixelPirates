import os
from dotenv import load_dotenv
load_dotenv()

from src.data_cleaning import load_and_prepare_data
from src.feature_engineering import build_features
from src.ml_model import detect_ghost_demand
from src.optimization import optimize_production
from src.results import (
    compute_kpis,
    compute_sku_impact,
    compute_top_ghost_events,
)

from infra.bigquery import upload_dataframe


def main():
    # Ensure output folder exists (for debugging / local runs)
    os.makedirs("outputs", exist_ok=True)

    # 1. Load data
    daily_df = load_and_prepare_data("Data/Amazon Sale Report.csv")

    # 2. Feature engineering
    daily_df = build_features(daily_df)

    # 3. Ghost demand detection (ML)
    daily_df = detect_ghost_demand(daily_df)

    # 4. Optimization (OR)
    daily_df = optimize_production(daily_df)

    # 5. Business KPIs
    kpis = compute_kpis(daily_df)
    sku_impact = compute_sku_impact(daily_df)
    top_events = compute_top_ghost_events(daily_df)

    # 6. Save locally (optional, for inspection)
    daily_df.to_csv("outputs/final_results.csv", index=False)
    kpis.to_csv("outputs/kpis.csv", index=False)
    sku_impact.to_csv("outputs/sku_impact.csv", index=False)
    top_events.to_csv("outputs/top_events.csv", index=False)

    # 7. Push to BigQuery for Looker Studio
    upload_dataframe(daily_df, "final_results")
    upload_dataframe(kpis, "ghost_kpis")
    upload_dataframe(sku_impact, "ghost_sku_impact")
    upload_dataframe(top_events, "ghost_top_events")


if __name__ == "__main__":
    main()
