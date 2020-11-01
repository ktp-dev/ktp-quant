from algorithm_template import Algorithm
import math

class AAPLAlgo(Algorithm):
	def __init__(self, place_order, get_data):
		self.sliding_prices = [0,0,0]
		self.portfolio_size = 50000 
		self.holding_period = 0
		self.held_shares = 0
		self.place_order = place_order
		self.get_data = get_data

	def handler(self):
		new_tick = self.get_new_data()
		self.sliding_prices.append(new_tick)
		del self.sliding_prices[0]

		if self.holding_period != 0:
			self.holding_period -= 1
			return 

		if self.held_shares != 0 and new_tick > self.sliding_prices[2]:
			return

		if self.held_shares != 0 and new_tick < self.sliding_prices[1]:
			self.place_order(symbol = "AAPL", qty = self.held_shares, side = "sell")
			self.portfolio_size += self.held_shares * new_tick
			self.held_shares = 0

		if self.sliding_prices[1] < self.sliding_prices[0] and self.sliding_prices[2] < self.sliding_prices[1]:
			self.held_shares = math.floor(self.portfolio_size/new_tick)
			self.place_order(symbol = "AAPL", qty = self.held_shares, side = "buy")
			self.portfolio_size -= self.held_shares * new_tick
			self.holding_period = 2

	def get_new_data(self):
		 
		return self.get_data(["AAPL"], ["Close"])

if __name__ == "__main__":
	new_instance = AAPLAlgo()	
