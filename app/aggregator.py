from datetime import date, timedelta
import pandas as pd

def build_day_series(df, start_date=None, end_date=None):
    """
    Build a continuous daily time series with:
    - 'day'
    - 'total_qty'
    Missing dates are filled with 0 qty.
    """
    df = df.copy()
    df['day'] = pd.to_datetime(df['day'])

    # Determine start and end range
    if start_date is None:
        start_date = df['day'].min()
    if end_date is None:
        end_date = df['day'].max()

    # Create full date index
    full_idx = pd.date_range(start=start_date, end=end_date, freq='D')

    # Reindex and fill missing values
    df = (df.set_index('day')
            .reindex(full_idx)
            .rename_axis('day')
            .fillna({'total_qty': 0})
            .reset_index())

    return df
