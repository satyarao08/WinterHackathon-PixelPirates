import pandas as pd

# This is the "Relative Path"
# It looks for the file inside your currently opened VS Code folder
path = "Amazon Sale Report.csv"

df = pd.read_csv(path, low_memory=False)

print(f"Successfully loaded {len(df)} rows from the project folder.")
#Checking the data
df.head()
# Keep only required columns
df = df[['Date', 'SKU', 'Qty', 'Status']]
df
valid_status = ['Shipped', 'Delivered']

df = df[df['Status'].isin(valid_status)]
df
df['Date'].head(10)
# IMPORTANT: ensure df is a copy (after filtering)
df = df.copy()

# Convert Date safely with explicit format
df.loc[:, 'Date'] = pd.to_datetime(
    df['Date'],
    format='%Y-%m-%d',
    errors='coerce'
)
df['Date'].dtype
df['Date'].isna().sum()
# Filter valid rows and force a copy
valid_status = ['Shipped', 'Delivered']
df = df[df['Status'].isin(valid_status)].copy()

# Convert Date safely
df.loc[:, 'Date'] = pd.to_datetime(
    df['Date'],
    format='%d-%m-%Y',   # adjust if needed
    errors='coerce'
)
#Sorting the data
daily_df = daily_df.sort_values(['SKU', 'Date'])
daily_df['rolling_mean_7'] = (
    daily_df
    .groupby('SKU')['daily_sales']
    .transform(lambda x: x.rolling(7, min_periods=1).mean())
)
daily_df['rolling_std_7'] = (
    daily_df
    .groupby('SKU')['daily_sales']
    .transform(lambda x: x.rolling(7, min_periods=1).std())
    .fillna(0)
)
daily_df['forecast_error'] = (
    daily_df['rolling_mean_7'] - daily_df['daily_sales']
)
daily_df['demand_change'] = (
    daily_df
    .groupby('SKU')['daily_sales']
    .pct_change()
    .fillna(0)
)

daily_df['volatility_ratio'] = (
    daily_df['rolling_std_7'] / (daily_df['rolling_mean_7'] + 1e-6)
)
daily_df[['daily_sales', 'rolling_mean_7', 'forecast_error']].describe()
