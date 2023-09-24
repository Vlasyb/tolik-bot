import ccxt
import pandas as pd
import datetime
from ta.momentum import RSIIndicator
from binance.client import Client
import mplfinance as mpf


# replace YOUR_API_KEY and YOUR_SECRET_KEY with your own keys
api_key = 'YZcPGzrU0KH6vSSmFXsf9utujHWl7YBm2i4trYynDo1kFPrI9PeYzXAzZHvMTfgq'
api_secret = '0eSdyRpYw3yMg6TszataVnvYH8w3IZ78p6EicZMufgIefytMHgL22hdtfQe7XupI'

# create a Binance client object
client = Client(api_key, api_secret)


def min_candle(prev, curr, next):
    if prev > curr and curr < next:
        return True
    return False


# prices[100] -> rsi_values[86]
def rsi_divergence(prices, rsi_values, rsi_period=14):
    divergences = []
    for i in range(rsi_period + 1, len(prices) - 2 - rsi_period):
        if min_candle(prices[rsi_period + i - 1], prices[rsi_period + i], prices[rsi_period + i + 1]) and min_candle(rsi_values[i - 1], rsi_values[i], rsi_values[i + 1]):
            for j in range(i + rsi_period + 1, len(prices) - 2 - rsi_period):
                if min_candle(prices[rsi_period + j - 1], prices[rsi_period + j], prices[rsi_period + j + 1]) and min_candle(rsi_values[j - 1], rsi_values[j], rsi_values[j + 1]):
                    if prices[rsi_period + i] < prices[rsi_period + j] and rsi_values[i] > rsi_values[j]:
                        # if i == 76-rsi_period and j == 168-rsi_period:
                        #     print("rsi_values[i]:")
                        #     print(rsi_values[i])
                        #     print("\n")
                        #     print("rsi_values[j]:")
                        #     print(rsi_values[j])
                        divergences.append((rsi_period + i, rsi_period + j))
    return divergences


def convert_to_time(point, df):
    dates = []
    dates.append(df['timestamp'][point[0]])
    dates.append(df['timestamp'][point[1]])
    return dates


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

# Calculate RSI
rsi_period = 14
rsi_indicator = RSIIndicator(df['low'], rsi_period)
df['rsi'] = rsi_indicator.rsi()

# Find RSI divergences
divergences = rsi_divergence(df['low'], df['rsi'], rsi_period)
print(divergences)
print(convert_to_time((76, 168), df))

df.close = df.close.astype(float)
df.high = df.high.astype(float)
df.low = df.low.astype(float)
df.volume = df.volume.astype(float)
df.open = df.open.astype(float)

ap0 = [
    mpf.make_addplot(df['rsi'], color='#ffa500', panel=0, title="RSI"),
]

# Set the timestamp as the index of the DataFrame
df.set_index('timestamp', inplace=True)
# mpf.make_addplot(df['rsi'], color='#ffa500', panel=0, title="RSI")
mpf.plot(df, type='candle', title='BTCUSDT Price', addplot=ap0,
         ylabel='Price')
