import csv
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

# url = "https://finance.yahoo.com/quote/SPY/options?p=SPY"

class Option_Snatcher:

    def __init__(self, url_in):

        self.url = url_in

        self.date_dict = {}

        self.options = []

    def get_date_list(self):

        resp = requests.get(self.url)

        soup = bs(resp.text, "html.parser")

        options = soup.find_all('option')

        for option in options:

            self.date_dict[option.string] = option['value']
        
        

    def get_options(self):

        first_date = self.url[self.url.find("date=") + 5: self.url.find("date=") + 15].strip()

        old_date = first_date
        
        for date in self.date_dict:

            print("new_date = ", self.date_dict[date])

            self.url = self.url.replace(old_date, self.date_dict[date])

            old_date = self.date_dict[date]

            self.get_call_options(date)

        

    def get_call_options(self, date):

        resp = requests.get(self.url)

        soup = bs(resp.text, "html.parser")

        self.call_table = soup.find('table')

        # for each row in the table
        for tr in self.call_table.find_all('tr')[1:]:
            
            data_cells = tr.find_all('td')

            data_list = ["call", date] + [item.string.strip('\n') for item in data_cells]

            self.options.append(data_list)
    
    
    def get_put_options(self, date):

        self.put_table = self.call_table.find_next('table')

         # for each row in the table
        for tr in self.put_table.find_all('tr')[1:]:
            
            data_cells = tr.find_all('td')

            data_list = ["put", date] + [item.string.strip('\n') for item in data_cells]

            self.options.append(data_list)

    def write_file(self):

        with open("spy_history.tsv", 'w') as outfile:
            
            outfileWriter = csv.writer(outfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            outfileWriter.writerow(["Contract_Type", "Contract_Date", "Contract_Name", "Last_Trade_Date", "Strike", "Last_Price", "Bid", "Ask", "Change", "%_Change", "Volume", "Open_Interest", "Implied_Volatility"])

            for data_list in self.options:

                outfileWriter.writerow(data_list)



def main():

    snatcher = Option_Snatcher("https://finance.yahoo.com/quote/SPY/options?date=1613433600&p=SPY")

    snatcher.get_date_list()

    snatcher.get_options()
    
    snatcher.write_file()

main()











            # contract_name = data_cells[0].string

            # last_trade_date = data_cells[1].string

            # strike = data_cells[2].string
            
            # last_price = data_cells[3].string

            # bid = data_cells[4].string
            
            # ask = data_cells[5].string

            # change = data_cells[6].string

            # percent_change = data_cells[7].string

            # volume = data_cells[8].string

            # open_interest = data_cells[9].string

            # implied_volatility = data_cells[10].string
            
            # print("contract_name = ", contract_name, '\n')
            # print("last_trade_date = ", last_trade_date, '\n')
            # print("strike = ", strike, '\n')
            # print("last_price = ", last_price, '\n')
            # print("bid = ", bid, '\n')
            # print("ask = ", ask, '\n')
            # print("change = ", change, '\n')
            # print("percent_change = ", percent_change, '\n')
            # print("volume = ", volume, '\n')
            # print("open_interest = ", open_interest, '\n')
            # print("implied_volatility = ", implied_volatility, '\n')

            # print('\n\n')