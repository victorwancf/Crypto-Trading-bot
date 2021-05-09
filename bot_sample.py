#CCXT Github: https://github.com/ccxt/ccxt
#CCXT Doc: https://ccxt.readthedocs.io/en/latest/
#Pivot Point Supertrend: https://www.tradingview.com/script/L0AIiLvH-Pivot-Point-Supertrend/
#Supertrend with EMA: https://in.tradingview.com/script/xEtpZd0t/
#Technical Analysis Library in Python: https://technical-analysis-library-in-python.readthedocs.io/en/latest/
#Technical Analysis Library in Python Github: https://github.com/bukosabino/ta


import ccxt
import config
import ta
import schedule
from ta.volatility import BollingerBands, AverageTrueRange
import pandas as pd

exchange = ccxt.binance({
    'apiKey': config.BINANCE_API_KEY,
    'secret': config.BINANCE_SECRET_KEY,
    'options': {'adjustForTimeDifference': True} #CCXT may have bugs on sending milisecond to binance, need to adjust the time
})

balance = exchange.fetch_balance()
print(balance['total']['DOGE'])

bars = exchange.fetch_ohlcv('ETH/USDT', limit=21)

# for bar in bars:
#     print(bar)

df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']) #Filter out the last, unfinished candle

atr_indicator = AverageTrueRange(df['high'], df['low'], df['close'])
df['atr'] = atr_indicator.average_true_range()
print(df)