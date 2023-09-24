import os
from binance.client import Client
import pandas as pd
import ccxt
import datetime
import binance
import mplfinance as mpf
import matplotlib.pyplot as plt


# replace YOUR_API_KEY and YOUR_SECRET_KEY with your own keys
api_key = 'YZcPGzrU0KH6vSSmFXsf9utujHWl7YBm2i4trYynDo1kFPrI9PeYzXAzZHvMTfgq'
api_secret = '0eSdyRpYw3yMg6TszataVnvYH8w3IZ78p6EicZMufgIefytMHgL22hdtfQe7XupI'

# create a Binance client object
client = Client(api_key, api_secret)


def find_local_minimum(prices):
    local_min = prices[0]
    local_min_index = 0
    for i in range(1, len(prices) - 1):
        if prices[i - 1] > prices[i] < prices[i + 1]:
            if prices[i] < local_min:
                local_min = prices[i]
                local_min_index = i
    return local_min_index, local_min


# Initialize Binance API
binance = ccxt.binance({
    'rateLimit': 1200,
    'enableRateLimit': True,
})

# Get historical price data (OHLCV) for Bitcoin
timeframe = '1d'
symbol = 'BTC/USDT'
since = binance.parse8601((datetime.datetime.now(
) - datetime.timedelta(days=60)).strftime('%Y-%m-%dT%H:%M:%SZ'))

ohlcv = binance.fetch_ohlcv(symbol, timeframe, since)

# Convert data to pandas DataFrame
df = pd.DataFrame(
    ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Find the local minimum
min_index, local_min = find_local_minimum(df['low'])

# Print the result
print(
    f"Local minimum found at {df['timestamp'][min_index]} with a price of {local_min:.2f} USDT")


# Get klines (candlestick) data for the past day
# klines = client.get_historical_klines(
#     "BTCUSDT", Client.KLINE_INTERVAL_4HOUR, "20 February, 2023", "12 April, 2023")

df.close = df.close.astype(float)
df.high = df.high.astype(float)
df.low = df.low.astype(float)
df.volume = df.volume.astype(float)
df.open = df.open.astype(float)

# Set the timestamp as the index of the DataFrame
df.set_index('timestamp', inplace=True)
mpf.plot(df, type='candle', title='BTCUSDT Price', ylabel='Price', volume=True)
