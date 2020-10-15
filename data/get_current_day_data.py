import yfinance as yf
import pandas as pd

def get_current_day(ticker):
    #get data for current day
    ticker_df = yf.download(ticker).iloc[[-1]]
    ticker_df.drop('Adj Close', axis=1)
    ticker_df['Change'] = ticker_df['Close'] - ticker_df['Open']
    ticker_df['% Return'] = ticker_df['Change'] / ticker_df['Open'] * 100
    ticker_df = ticker_df.reset_index()
    ticker_df['Date'] = ticker_df['Date'].astype(str)

    #append to previous historical data
    old_df = pd.read_csv('historical_data/{}.csv'.format(ticker)).iloc[::-1]
    df = old_df.append(ticker_df).iloc[::-1].drop_duplicates()
    df.to_csv('historical_data/{}.csv'.format(ticker), index=False)

def get_current_day_all_tickers():
    f = open("supported_tickers.txt", "r")
    for x in f:
        get_current_day(x)

if __name__ == '__main__':
    get_current_day_all_tickers()
    