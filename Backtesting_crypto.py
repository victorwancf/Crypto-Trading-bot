#Other backtesting framework: https://github.com/kernc/backtesting.py/blob/master/doc/alternatives.md
#Cryto data and analytics (The dataset): https://www.cryptodatadownload.com/data/binance/

import pandas as pd
import numpy as np
import time
from Supertrend_and_Functions import atr, tr, supertrend_st
from backtesting import Strategy
from backtesting import Backtest
pd.options.mode.chained_assignment = None  # default='warn'
pd.set_option('display.max_rows', None)

Coin = "ETC/USDT"
start_date = "2021-04-01 00:00:00" #YYYY-MM-DD HH:MM:SS

start_read = time.time()
print("Reading Data and setting index...")

data_1m = pd.read_csv('Backtest_data\Binance_ETCUSDT_minute.csv', usecols=['date', 'open', 'high', 'low', 'close', 'Volume USDT'])
data_1m['date'] = pd.to_datetime(data_1m['date'], format='%d/%m/%Y %H:%M')
data_1m = data_1m.set_index('date')
data_1m = data_1m.sort_index(ascending=True)

end_read = time.time()
print(f"Readning data and setting index is ended, it took {end_read - start_read} second.\n")

end_date = data_1m.index[-1]
print("Backtesting starts date is {}".format(start_date))
print("Backtesting end date is {}\n".format(end_date))

def bar_aggregate(df, n):
    method = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'Volume USDT': 'sum'
    }

    df_arg = df.resample(f'{n}T', closed='left').agg(method).dropna()
    return df_arg

def change_to_timestamp(df):
    df['timestamp'] = df.index.view('int64') / 1000000  # Convert to timestamp
    df['timestamp'] = df['timestamp'].values.astype('datetime64[ms]')  # Convert to correct type
    df = df.sort_values(by='timestamp', ascending=True)
    df_tiemstamp = df.set_index('timestamp')
    return df_tiemstamp

def rename_cols(df):
    renamed_df = df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'Volume USDT': 'Volume'})
    return renamed_df

def start_at(df, start_date=start_date):
    data_start_index = df.index.get_loc(start_date)  #Getting the row index of the start date
    start_df = df[data_start_index:]
    return start_df

def set_data_param(df=data_1m, n=5, start_date=start_date):
    if n == 1:
        pass
    else:
        df = bar_aggregate(df, n)

    df_start = start_at(df, start_date)
    supertrend_df = supertrend_st(df_start)
    supertrend_df = rename_cols(supertrend_df)
    return supertrend_df

start_param = time.time()
print("Setting data param...")

supertrend_1m = set_data_param(data_1m, 1, start_date)
supertrend_5m = set_data_param(data_1m, 5, start_date)
supertrend_15m = set_data_param(data_1m, 15, start_date)
supertrend_30m = set_data_param(data_1m, 30, "2021-01-01 00:00:00")

end_read = time.time()
print(f"Data params is set, it took {end_read - start_param} second.")

class supertrend_signal(Strategy):
    buy_side_list = []
    sell_side_list = []

    def init(self):
        super().init()
        period = 7
        mutiplier = 3

    def next(self):
        super().next()
        supertrend_previous = self.data.in_uptrend[-2]
        supertrend_lastest = self.data.in_uptrend[-1]

        if not supertrend_previous and supertrend_lastest:
            self.buy()

        elif supertrend_previous and not supertrend_lastest:
            self.sell()

def backtest_(df):
    bt = Backtest(df, supertrend_signal, cash=1000000, commission=.001, exclusive_orders=True) #The backtest won't trade a fraction of the coin
    stats = bt.run()
    bt.plot()
    return stats

start_backtest = time.time()
print("Backtesting the data...")

stats_1m = pd.DataFrame(backtest_(supertrend_1m))
stats_5m = pd.DataFrame(backtest_(supertrend_5m))
stats_15m = pd.DataFrame(backtest_(supertrend_15m))
stats_30m = pd.DataFrame(backtest_(supertrend_30m))

end_backtest = time.time()
print(f"Data params is set, it took {end_backtest - start_backtest} second.")

# Put all stat into one DataFrame
stat = stats_1m.rename(columns={0: '1m'})
stat['5m'] = stats_5m
stat['15m'] = stats_15m
stat['30m'] = stats_30m
print("Finished backtesting! Outputing {} backtest data to csv.".format(Coin))

stat.to_csv(r'C:\Users\q3604\Desktop\Algo Trading\CCXT_BOT\Backtest_stats\{}_stat.csv'.format(Coin.replace("/", "_")))

#Backtesting Objective:
# 1. Maximise sharpe ratio, sortino ratio
# 2. Reduce maximum drawdown
# 3. Able to have similar performance on different Altcoin
# 4. Smooth the equity curve
