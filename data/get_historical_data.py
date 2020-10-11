import yfinance as yf
import pandas as pd

df = pd.read_csv('supported_tickers.txt', header=None)
df.columns = ['Tickers']

for ticker in df['Tickers']:
    ticker_df = yf.download(ticker, start="2015-01-02").iloc[::-1]
    ticker_df.drop('Adj Close', axis=1)
    ticker_df['Change'] = ticker_df['Close'] - ticker_df['Open']
    ticker_df['% Return'] = ticker_df['Change'] / ticker_df['Close'] * 100
    ticker_df.to_csv('{}.csv'.format(ticker))