# https://www.barchart.com/etfs-funds/quotes/AAPL/volatility-greeks?moneyness=allRows
import os
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.webdriver.common.keys import Keys
import random
from datetime import date as d
import csv

# Path to each file
# ~/options_data/[Ticker]/[Current Date]_[Expiration].csv
# e.g. ~/options_data/SPY/02_17_2021_02_19_2021.csv

class Option_Snatcher:

    def __init__(self):

        # get the tickers we are tracking
        self.tickers = self.getTickers()

        # only needed to run this function once
        # self.createTickerDirectories()

        # set up the chrome driver
        ChromeOptions = webdriver.ChromeOptions()
        ChromeOptions.add_argument('--disable-browser-side-navigation')

        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"

        self.driver = webdriver.Chrome(executable_path=os.path.dirname(os.path.realpath(__file__)) + '/chromedriver', chrome_options=ChromeOptions, desired_capabilities=capa)

        # self.loginBarChart()
    
    def quitDriver(self):
        self.driver.quit()
    
    
    def getTickers(self):
        # get the path to the file with all of the tickers
        path = os.path.dirname(os.path.realpath(__file__)).replace("/option_data", '') + '/supported_tickers.txt'

        with open(path, 'r') as ticker_file:

            tickers = [ticker.strip() for ticker in ticker_file.readlines()]

            return tickers
        
    def createTickerDirectories(self):

        # get the current_directories

        for ticker in self.tickers:
            try:

                path = os.path.join(os.path.dirname(os.path.realpath(__file__)), ticker) 
                os.mkdir(path)
            except:
                continue

    

    def loginBarChart(self):

        email = "cgoldman1026@gmail.com"
        password = "KTPQUANT"

        self.driver.get("https://www.barchart.com/login")

        self.driver.implicitly_wait(10)

        email_field = self.driver.find_element(By.NAME, "email")

        email_field.send_keys(email)

        self.driver.implicitly_wait(10)

        password_field = self.driver.find_element(By.NAME, "password")

        password_field.send_keys(password)

        self.driver.implicitly_wait(10)

        login_button = self.driver.find_element_by_tag_name('button')

        login_button.click()



    def scrapeAllTickers(self):

        for ticker in self.tickers:

            self.scrapeTicker(ticker)
    
    
    def parseCallTable(self, ticker):

        overall_data = []

        time.sleep(random.random() * 6)

        soup = bs(self.driver.page_source, 'html.parser')

        table = soup.find("div", {'class', 'bc-datatable'})
        
        cells = table.find_all('td')

        row_data = ["Call"]

        # for each piece of data in the table except for the last row (there are 15 cells in each row)
        for i, cell in enumerate(cells[:-15]):
            # there are fourteen columns in each row
            # we only care about the first 10 columns (0 - 9 index)
            if i % 15 > 9:
                # skip this and move onto the next iteration
                if row_data != ["Call"]:
                    overall_data.append(row_data)
                
                row_data = ["Call"]
                continue

             
            data = cell.find('span', {'data-ng-bind':'cell'})  

            if i % 15 < 10:
                row_data.append(data.string)
    
        return overall_data
    
    def parsePutTable(self, ticker):

        overall_data = []

        time.sleep(random.random() * 6)
        
        soup = bs(self.driver.page_source, 'html.parser')

        table = soup.find_all("div", {'class', 'bc-datatable'})[1]
        
        cells = table.find_all('td')

        row_data = ["Put"]

        # for each piece of data in the table except for the last row (there are 15 cells in each row)
        for i, cell in enumerate(cells[:-15]):
            # there are fifteen cells in each row
            # we only care about the first 10 columns (0 - 9 index)
            if i % 15 > 9:
                # skip this and move onto the next iteration
                if row_data != ["Put"]:
                    overall_data.append(row_data)
                row_data = ["Put"]
                continue

             
            data = cell.find('span', {'data-ng-bind':'cell'})  

            if i % 15 < 10:
                row_data.append(data.string)

        return overall_data
        
    def getExpirationDates(self):

        soup = bs(self.driver.page_source, 'html.parser')

        # the date dropdown is the third dropdown menu on the page
        dates = soup.find_all("select")[2]

        options = dates.find_all('option')

        date_list = []

        for option in options:

            date_value = option["value"].strip()

            if len(date_value.split('-')) < 3:
                continue
            else:
                date_list.append(date_value)
        
        return date_list
    
    def scrapeTicker(self, ticker):

        today = d.today()

        today_date_string = "{}_{}_{}".format(today.month, today.day, today.year)

        # format the barchart url for this ticker
        url = "https://www.barchart.com/etfs-funds/quotes/{}/volatility-greeks?moneyness=allRows".format(ticker)

        # send the driver to the proper location
        self.driver.get(url)

        # wait for the page to load
        time.sleep(random.random() * 10)

        # get all the expiration dates which we have data for
        expirationDates = self.getExpirationDates()

        for date in expirationDates:

            split_date = date.split('-')

            option_date_string = "{}_{}_{}".format(split_date[1], split_date[2], split_date[0])

            url = "https://www.barchart.com/etfs-funds/quotes/{}/volatility-greeks?moneyness=allRows&expiration={}".format(ticker, date)

            # send the driver to the proper location
            self.driver.get(url)

            # wait for the page to load
            time.sleep(random.random() * 10)
            
            # parse the call table
            call_options = self.parseCallTable(ticker)

            print("Just scraped all call options for {} on {}! {} options in total.\n".format(ticker, option_date_string, len(call_options)))

            # parse the put table
            put_options = self.parsePutTable(ticker)

            print("Just scraped all put options for {} on {}! {} options in total.\n".format(ticker, option_date_string, len(put_options)))

            # open the file and write the data to it
            file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), ticker, "{}_{}.csv".format(today_date_string, option_date_string))
            
            with open(file_path, 'w') as outfile:
                # set up the CSV writer
                outfileWriter = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                outfileWriter.writerow(["Call/Put", "Strike", "Last", "Theoretical", "IV", "Delta", "Gamma", "Rho", "Theta", "Vega", "Volume"])
                
                # write all of the call options to the file
                for option in call_options:

                    outfileWriter.writerow(option)
                
                # write all of the put options to the file
                for option in put_options:

                    outfileWriter.writerow(option)
            
def main():

    snatcher = Option_Snatcher()

    snatcher.scrapeAllTickers()

    snatcher.quitDriver()

main()