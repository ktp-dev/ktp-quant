import pandas as pd

class MeanReversion:
    def __init__(self, ticker):
        self.yesterday_30_day = 0
        self.yesterday_90_day = 0
        self.today_30_day = 0
        self.today_90_day = 0
        #self.place_order = place_order
        #self.get_data = get_data
        self.ticker = ticker
        

    def handler(self, new_data):
        #RUN THE LOGIC HANDLER HERE
        pass

    def get_new_data(self):
        filename = "../../data/historical_data/" + self.ticker + ".csv"
        #print(filename)
        df = pd.read_csv(filename, nrows=90)
        print(df)
        print(df['Close'])
        pass
        #return self.get_data([self.ticker], ["Close"])
        for close in df['Close']:

        for index,row in df.iterrows():
            row['Close']


if __name__ == "__main__":
    meanreversion = MeanReversion('AAPL')
    #backtester.get_new_data()
    print(meanreversion.get_new_data())