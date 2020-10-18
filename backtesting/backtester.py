import sys
sys.path.append("testing_algos")
import pandas as pd 

####
from aapl_algo import AAPLAlgo

#path: ./data/historical_data/AAPL.csv 

class Backtester():
	def __init__(self):
		self.portfolio = {"cash": 50000.0}
		self.current_price = {"cash": 1.0}
		self.algo = AAPLAlgo(self.place_order, self.get_data)

	def calculate_portfolio_value(self):
		portfolio_value = 0.0
		for ticker in self.portfolio:
			portfolio_value += self.portfolio[ticker] * self.current_price[ticker]
		return portfolio_value

	def get_data():
		#TODO
		pass


	def place_order(self, symbol, qty, side):
		if symbol in portfolio:
			if side == "buy":
				portfolio[symbol] += qty
				portfolio["cash"] -= qty * current_price[symbol]
			else:
				portfolio[symbol] -= qty
				portfolio["cash"] += qty * current_price[symbol]
		else:
			portfolio[symbol] = qty
			portfolio["cash"] -= qty * current_price[symbol]


	def main(self):
		#TODO
		pass


if __name__ == "__main__":
	backtester = Backtester()
	backtester.main()
