import pandas as pd

def load_and_prepare_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    df['Date'] = pd.to_datetime(
        df['Date'].astype(str).str.strip(),
        format='%m-%d-%y',
        errors='raise'
    )

    valid_status = ['Shipped', 'Delivered']
    df = df[df['Status'].isin(valid_status)].copy()

    daily_df = (
        df
        .groupby(['Date', 'SKU'], as_index=False)
        .agg(daily_sales=('Qty', 'sum'))
        .sort_values(['SKU', 'Date'])
    )

    return daily_df
