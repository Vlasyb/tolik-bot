import os
from binance.client import Client
import pandas as pd
import binance
import mplfinance as mpf
import matplotlib.pyplot as plt


# replace YOUR_API_KEY and YOUR_SECRET_KEY with your own keys
api_key = 'YZcPGzrU0KH6vSSmFXsf9utujHWl7YBm2i4trYynDo1kFPrI9PeYzXAzZHvMTfgq'
api_secret = '0eSdyRpYw3yMg6TszataVnvYH8w3IZ78p6EicZMufgIefytMHgL22hdtfQe7XupI'

# create a Binance client object
client = Client(api_key, api_secret)

# Get klines (candlestick) data for the past day
klines = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_4HOUR, "25 March, 2023", "29 March, 2023")
print(klines)

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
mpf.plot(df, type='candle', title='BTCUSDT Price', ylabel='Price', volume=True)

# Plot the graph
# df['close'].plot(figsize=(10, 6), title='BTCUSDT Price')
# plt.plot(df.index, df['close'])
# plt.gcf().autofmt_xdate()
# plt.title('BTCUSDT Price')
# plt.xlabel('Date')
# plt.ylabel('Price')
# plt.show()


# symbol = 'BTCUSDT'
# amount = 0.01

# buy_order = client.create_order(
#     symbol=symbol,
#     side=Client.SIDE_BUY,
#     type=Client.ORDER_TYPE_MARKET,
#     quantity=amount)


# ticker = client.get_symbol_ticker(symbol=symbol)
# price = float(ticker['price'])

# sell_amount = amount * price

# sell_order = client.create_order(
#     symbol=symbol,
#     side=Client.SIDE_SELL,
#     type=Client.ORDER_TYPE_MARKET,
#     quoteOrderQty=sell_amount)

# print the details of the sell order
