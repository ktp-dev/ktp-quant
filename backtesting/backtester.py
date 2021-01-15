import sys
sys.path.append("testing_algos")
import pandas as pd 
import matplotlib.pyplot as plt
from statistics_calc import *
####
from aapl_algo import AAPLAlgo



class Backtester():
	def __init__(self):
		self.portfolio = {"cash": 50000.0}
		self.current_price = {"cash": 1.0}
		self.algo = AAPLAlgo(self.place_order, self.get_data)

		self.data = self.load_data(["AAPL"], ["Close"])
		self.data_queue = self.load_data(["AAPL"], ["Close"])


	def calculate_portfolio_value(self):
		portfolio_value = 0.0
		for ticker in self.portfolio:
			portfolio_value += self.portfolio[ticker] * self.current_price[ticker]
		return portfolio_value

	def get_data(self, tickers, data):
		self.current_price["AAPL"] = self.data_queue[0]
		return self.data_queue.pop(0)


	def load_data(self, tickers, data):
		file_path = "../data/historical_data/" + "AAPL" + ".csv"
		df = pd.read_csv(file_path, header=None)
		close_prices_floats = df[4].to_list()
		close_prices_floats.pop(0)
		close_prices = [float(value) for value in close_prices_floats]
		close_prices.reverse()
		return close_prices

	def place_order(self, symbol, qty, side):
		if symbol in self.portfolio:
			if side == "buy":
				self.portfolio[symbol] += qty
				self.portfolio["cash"] -= qty * self.current_price[symbol]
			else:
				self.portfolio[symbol] -= qty
				self.portfolio["cash"] += qty * self.current_price[symbol]
		else:
			self.portfolio[symbol] = qty
			self.portfolio["cash"] -= qty * self.current_price[symbol]


	def main(self):
		portfolio_values = []
		for i in range(len(self.data)):
			#iterate through everyday
			self.algo.handler()
			newest_value = self.calculate_portfolio_value()
			portfolio_values.append(newest_value)
		er_aapl, std_aapl = calculate_statistics(portfolio_values, prices = True)
		er_stock, std_stock = calculate_statistics(self.data, prices = True)

		


		print("strategy return: " + str(er_aapl))
		print("strategy std: " + str(std_aapl))
		print("stock return: " + str(er_stock))
		print("stock std:" + str(std_stock))
		return portfolio_values
if __name__ == "__main__":
	backtester = Backtester()
	backtester.main()
