from sklearn.ensemble import IsolationForest

def detect_ghost_demand(df):

    features = [
        "daily_sales",
        "rolling_mean_7",
        "rolling_std_7",
        "forecast_error",
        "demand_change",
        "volatility_ratio"
    ]

    df = df.dropna(subset=features).copy()
    X = df[features]

    iso_model = IsolationForest(
        n_estimators=300,
        max_samples=256,
        max_features=0.8,
        contamination=0.02,
        random_state=42
    )

    iso_model.fit(X)

    df["ghost_flag"] = iso_model.predict(X)
    df["ghost_demand"] = (df["ghost_flag"] == -1).astype(int)

    return df
