import pandas as pd 
import numpy as np

def get_data():
    tickers = pd.read_csv('supported_tickers.txt', header=None)
    tickers.columns = ['Tickers']

    df = pd.DataFrame() # each column is one stock
    for ticker in tickers['Tickers']:
        data = pd.read_csv('historical_data/{}.csv'.format(ticker))
        df[ticker] = data['Close']
    
    return df

def get_highest_correlated(df):
    # generate correlation matrix
    matrix = df.corr()
    
    # convert correlation matrix to pairwise readable format
    matrix =  matrix.rename_axis(None).rename_axis(None, axis=1)
    pairs = matrix.stack().reset_index()
    pairs.columns = ['Ticker 1', 'Ticker 2', 'Correlation']

    # strip pairs correlating with themselves and duplicate correlations
    masked_dups = (pairs[['Ticker 1', 'Ticker 2']].apply(frozenset, axis=1).duplicated()) | (pairs['Ticker 1'] == pairs['Ticker 2'])
    pairs = pairs[~masked_dups]

    # sort by highest correlation
    pairs = pairs.sort_values('Correlation', ascending=False)

    return matrix, pairs

if __name__ == "__main__":
    df = get_data()
    matrix, pairs = get_highest_correlated(df)
    
    matrix.to_csv('matrix_correlation.csv')
    pairs.to_csv('pairs_correlation.csv')
