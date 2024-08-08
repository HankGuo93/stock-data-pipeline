import pandas as pd
from alpha_vantage.timeseries import TimeSeries

def fetch_data(api_key, output_path):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, _ = ts.get_intraday(symbol='GOOGL', interval='1min', outputsize='full')
    data.to_csv(output_path)
    return output_path