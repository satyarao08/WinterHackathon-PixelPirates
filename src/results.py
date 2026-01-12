import pandas as pd


def compute_kpis(daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute global Ghost Demand KPIs for dashboards.
    Returns a single-row DataFrame for Looker scorecards.
    """

    total_rows = len(daily_df)
    ghost_rows = int(daily_df["ghost_demand"].sum())

    ghost_rate = ghost_rows / total_rows if total_rows > 0 else 0.0

    kpi_df = pd.DataFrame([{
        "total_sku_days": total_rows,
        "ghost_cases": ghost_rows,
        "ghost_rate": ghost_rate
    }])

    return kpi_df


def compute_sku_impact(daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute SKU-level ghost demand impact table for Looker charts.
    """

    sku_df = (
        daily_df[daily_df["ghost_demand"] == 1]
        .groupby("SKU")
        .agg(
            ghost_days=("ghost_demand", "count"),
            avg_forecast_gap=("forecast_error", "mean"),
            max_forecast_gap=("forecast_error", "max"),
        )
        .reset_index()
        .sort_values("ghost_days", ascending=False)
    )

    return sku_df


def compute_top_ghost_events(daily_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Top ghost-demand SKU-days (largest forecast gap).
    Used for tables in Looker.
    """

    top_df = (
        daily_df[daily_df["ghost_demand"] == 1]
        .sort_values("forecast_error", ascending=False)
        .head(n)[
            ["Date", "SKU", "daily_sales", "rolling_mean_7", "forecast_error"]
        ]
    )

    return top_df
