import ccxt
import pandas as pd
import datetime
from ta.momentum import RSIIndicator
from binance.client import Client
import mplfinance as mpf
import ta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import find_pivots


# -------------------------------------- Initialize connection to binance ------------------------------------------
# replace YOUR_API_KEY and YOUR_SECRET_KEY with your own keys
api_key = 'YZcPGzrU0KH6vSSmFXsf9utujHWl7YBm2i4trYynDo1kFPrI9PeYzXAzZHvMTfgq'
api_secret = '0eSdyRpYw3yMg6TszataVnvYH8w3IZ78p6EicZMufgIefytMHgL22hdtfQe7XupI'

# create a Binance client object
client = Client(api_key, api_secret)

# Get klines (candlestick) data for the past day
klines = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_4HOUR, "25 March, 2023", "29 March, 2023")

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                  'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

# Convert the timestamp to a human-readable format
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

df.close = df.close.astype(float)
df.high = df.high.astype(float)
df.low = df.low.astype(float)
df.volume = df.volume.astype(float)
df.open = df.open.astype(float)

# Set the timestamp as the index of the DataFrame
df.set_index('timestamp', inplace=True)

# Initialize Binance API
binance = ccxt.binance({
    'rateLimit': 1200,
    'enableRateLimit': True,
})

# Get historical price data (OHLCV) for Bitcoin
timeframe = '4h'
symbol = 'BTC/USDT'
since = binance.parse8601((datetime.datetime.now(
) - datetime.timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ'))

ohlcv = binance.fetch_ohlcv(symbol, timeframe, since)

# Convert data to pandas DataFrame
df = pd.DataFrame(
    ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

df.close = df.close.astype(float)
df.high = df.high.astype(float)
df.low = df.low.astype(float)
df.volume = df.volume.astype(float)
df.open = df.open.astype(float)


# Set the timestamp as the index of the DataFrame
df.set_index('timestamp', inplace=True)

# -------------------------------------- Initialize connection to binance ------------------------------------------


# -------------------------------------- Finding and adding pivots to graph ------------------------------------------
pivot_points_low = find_pivots.minPivotPoints(df['low'])
pivot_points_high = find_pivots.highPivotPoints(df['high'])

df['pivot_point_low'] = False
df['pivot_point_low'].iloc[pivot_points_low] = True

df['pivot_point_high'] = False
df['pivot_point_high'].iloc[pivot_points_high] = True

# Plot the DataFrame with pivot points marked as red dots
ap = [mpf.make_addplot(df['pivot_point_low'], type='bar',
                       markersize=10, marker=',', alpha=0.1, color='red'),
      mpf.make_addplot(df['pivot_point_high'], type='bar',
                       markersize=10, marker=',', alpha=0.1, color='green')]

# adding indexes to df
df_to_plot = df
df = df.reset_index()
# plotting the pivots


def plot_pivots():
    mpf.plot(df_to_plot, type='candle', title='BTCUSDT Price',
             addplot=ap, ylabel='Price')


# print(df['low'].values)
# -------------------------------------- Finding and adding pivots to graph ------------------------------------------


print("------------------------------")
low_pivots = find_pivots.get_low_pivot_row_and_price(df)
# some_pivot[0] = index of the pivot , some_pivot[1] price to buy at
some_pivot = low_pivots[0]

# Find loss or win pivot=[index,price]


print(find_pivots.low_pivot_win_loss(df, some_pivot))
plot_pivots()
