daily_df['anomaly_score'] = iso_model.decision_function(X)
daily_df['anomaly_flag'] = iso_model.predict(X)

daily_df['ghost_demand'] = (
    (daily_df['anomaly_flag'] == -1) &
    (daily_df['forecast_error'] > 0)
).astype(int)