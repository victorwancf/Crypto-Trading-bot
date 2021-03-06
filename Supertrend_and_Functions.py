#Store all technical indicators

def tr(df):
    #ATR indicator: https://www.investopedia.com/terms/a/atr.asp
    df['previous_close'] = df['close'].shift(1)
    df['high-low'] = df['high']-df['low']
    df['high-pc'] = abs(df['high']-df['previous_close'])
    df['low-pc'] = abs(df['low']-df['previous_close'])
    tr = df[['high-low', 'high-pc', 'low-pc']].max(axis=1)
    return tr

def atr(df, period=14):
    df['tr'] = tr(df)
    the_atr = df['tr'].rolling(period).mean()
    return the_atr

def supertrend_st(df, period=7, multiplier=3):
    #Supertrend indicator: https://www.tradingfuel.com/supertrend-indicator-formula-and-calculation/
    df['atr'] = atr(df, period=period)
    hl2 = (df['high'] + df['low']) / 2

    df['upperband'] = hl2 + (multiplier * df['atr'])
    df['lowerband'] = hl2 - (multiplier * df['atr'])
    df['in_uptrend'] = True
    for current in range(1, len(df.index)):
        previous = current - 1

        if df['close'].iloc[current] > df['upperband'].iloc[previous]:
            df['in_uptrend'][current] = True
        elif df['close'].iloc[current] < df['lowerband'].iloc[previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'].iloc[current] = df['in_uptrend'].iloc[previous]

            if df['in_uptrend'].iloc[current] and df['lowerband'].iloc[current] < df['lowerband'].iloc[previous]:
                df['lowerband'].iloc[current] = df['lowerband'].iloc[previous]   #If the previous is higher, keep the previous lowerband

            if not df['in_uptrend'].iloc[current] and df['upperband'].iloc[current] > df['upperband'].iloc[previous]:
                df['upperband'].iloc[current] = df['upperband'].iloc[previous] #If the previous is lower, keep the previous lowerband
    return df