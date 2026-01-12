daily_df['ghost_demand'].value_counts()
total_rows = len(daily_df)
ghost_rows = daily_df['ghost_demand'].sum()

ghost_pct = (ghost_rows / total_rows) * 100

print(f"Total SKU-days analysed: {total_rows}")
print(f"Ghost demand cases detected: {ghost_rows}")
print(f"Ghost demand rate: {ghost_pct:.2f}%")
daily_df[daily_df['ghost_demand'] == 1] \
    .sort_values('forecast_error', ascending=False) \
    .head(10)[[
        'Date',
        'SKU',
        'daily_sales',
        'rolling_mean_7',
        'forecast_error'
    ]]
sku_impact = (
    daily_df[daily_df['ghost_demand'] == 1]
    .groupby('SKU')
    .agg(
        ghost_days=('ghost_demand', 'count'),
        avg_forecast_gap=('forecast_error', 'mean'),
        max_forecast_gap=('forecast_error', 'max')
    )
    .sort_values('ghost_days', ascending=False)
)

sku_impact.head(10)
