import ccxt
import pandas as pd
from datetime import datetime
import schedule
import time
import config
from Supertrend_and_Functions import tr,atr,supertrend_st
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'

exchange = ccxt.binance({
    'apiKey': config.BINANCE_API_KEY,
    'secret': config.BINANCE_SECRET_KEY,
    'options': {'adjustForTimeDifference': True} #CCXT may have bugs on sending milisecond to binance, need to adjust the time
})

#print(exchange.fetch_balance())

Coin = 'ETC/BTC'

in_position = True

def check_buy_sell_singals(df):
    global in_position

    print("Checking for buys and sell")
    print(df.tail(5))
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1
    if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
        print('Changed to uptrend, Buy!')
        if not in_position:
            order = exchange.create_market_buy_order(Coin, coin_to_buy*0.98)
            print(order)
            in_position = True
        else:
            print("Already in_position, nothing to do")

    if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
        print('Changed to downtrend, Sell!')
        if in_position:
            order = exchange.create_market_sell_order(Coin, in_position_coin)
            print(order)
            in_position = False
        else:
            print("Aren't in_position, nothing to sell")

def run_bot():
    global coin_to_buy
    global in_position_coin

    print(f'Fetching new bars for {datetime.now().isoformat()}')
    bars = exchange.fetch_ohlcv(Coin, timeframe='1m', limit=100)
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close',
                                          'volume'])  # Filter out the last, unfinished candle
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    coin_price = df['close'][len(df) - 1]
    print(f"The current market price of {Coin} is :", coin_price)

    balance_json = exchange.fetch_balance()
    assets = balance_json['info']['balances']
    target_asset = next(item for item in assets if item["asset"] == Coin[:3])
    btc_balance = next(item for item in assets if item["asset"] == "BTC")
    in_position_coin = target_asset['free']
    print("You have ", in_position_coin, f"of {Coin[:3]} in position.")
    print("You have ", btc_balance['free'], f"of BTC in position.")

    coin_to_buy = float(btc_balance['free'])/float(coin_price)
    print(f"You can buy {coin_to_buy} of {Coin}")

    supertrend_data = supertrend_st(df)
    check_buy_sell_singals(supertrend_data)
    #print(supertrend_data)


schedule.every(20).seconds.do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(1)
#implement backtrader etc. to plot graph