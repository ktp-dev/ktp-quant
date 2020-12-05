import pandas as pd
from papertrading.get_account_data import place_order

class MeanReversion:
    def __init__(self, ticker):
        self.yesterday_30_day = 0
        self.yesterday_90_day = 0
        self.today_30_day = 0
        self.today_90_day = 0
        #self.place_order = place_order
        self.ticker = ticker
        

    def handler(self, new_data):
        if (self.today_30_day > self.today_90_day and self.yesterday_30_day < self.yesterday_90_day):
            print('trigger sell')
            #place_order(self.ticker, 1, 'sell')
        elif (self.today_30_day < self.today_90_day and self.yesterday_30_day > self.yesterday_90_day):
            print('trigger buy')
            #place_order(self.ticker, 1, 'buy')
        else:
            print('do nothing')
            #do nothing
        

    def get_new_data(self):
        filename = "../../data/historical_data/" + self.ticker + ".csv"
        #print(filename)

        #calculate 90 day average today
        df = pd.read_csv(filename, nrows=90)
        for close in df['Close']:
            self.today_90_day += close
        self.today_90_day /= 90

        #calculate 90 day average yesterday
        df = pd.read_csv(filename,skiprows=[1] ,nrows=90)
        for close in df['Close']:
            self.yesterday_90_day += close
        self.yesterday_90_day /= 90

        #calculate 30 day average today
        df = pd.read_csv(filename, nrows=30)
        for close in df['Close']:
            self.today_30_day += close
        self.today_30_day /= 30

        #calculate 30 day average yesterday
        df = pd.read_csv(filename,skiprows=[1] ,nrows=30)
        for close in df['Close']:
            self.yesterday_30_day += close
        self.yesterday_30_day /= 30

        results = {'t90': self.today_90_day, 't30': self.today_30_day, 'y90': self.yesterday_90_day, 'y30': self.yesterday_30_day}

        return results


if __name__ == "__main__":
    meanreversion = MeanReversion('AAPL')
    print(meanreversion.get_new_data())

#Questions:
#   1. If we calcualte the 90 day averages with the close, then we wont be able to trigger a buy/sell until the next day
#       a. do we calculate with opens or just hope that it goes through the next day?