import pandas as pd
import numpy as np

def build_features(daily_df: pd.DataFrame) -> pd.DataFrame:
    df = daily_df.copy()

    df['rolling_mean_7'] = (
        df.groupby('SKU')['daily_sales']
        .transform(lambda x: x.rolling(7, min_periods=3).mean())
    )

    df['rolling_std_7'] = (
        df.groupby('SKU')['daily_sales']
        .transform(lambda x: x.rolling(7, min_periods=3).std())
    )

    df['forecast_error'] = df['rolling_mean_7'] - df['daily_sales']
    df['demand_change'] = df.groupby('SKU')['daily_sales'].diff()
    df['volatility_ratio'] = df['rolling_std_7'] / (df['rolling_mean_7'] + 1e-6)

    df = df.dropna().reset_index(drop=True)
    return df
