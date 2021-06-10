# Crypto-Trading-bot

Welcome to the Crypto-Trading-bot repository!

The repository consist of two main parts, an algo trading bot and a backtesting system.

## Trading Bot

The trading bot is written in python(supertrend_CCXT_Bot.py). The whole framework is based on the CCXT library. It connects to the binance api to execute cryptocurrency trades. Currently, it is using the supertrend strategy to execute trades. The bot is traded on minute timeframe. It updates the cryptocurrency price for every 20 second. When the preset criteria is fulfilled, trades will be executed.

## Backtesting system

The backtesting system is also written in python (Bactesting_crypto.py). The backtesting.py libray is used. The dataset is downloaded from https://www.cryptodatadownload.com/data/binance/. The current backtesting strategy is the supertrend strategy. As the hourly and daily timeframe is backtested and the performance is quite poor, the strategy is now focused on minute timeframe.

Futher improvement for the current strategy could be:
1. Parameters tunning
2. replacing the first part of the supertrend indicator from (high - low )/2 to moving average
3. Adding other technical indicators 
