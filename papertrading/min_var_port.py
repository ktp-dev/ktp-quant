import yfinance as yf
import numpy as np
from get_account_data import Account
import math

def get_tickers():
	with open("./supported_tickers.txt") as f:
		lines = f.read().splitlines()
	return lines


def get_last_10_days(ticker):
	ticker_df = yf.download(ticker, progress=False)
	ticker_df['Change'] = ticker_df['Close'] - ticker_df['Open']
	ticker_df['% Return'] = ticker_df['Change'] / ticker_df['Open']
	#should be [-10:]
	#print(ticker_df[-11:-1])
	return ticker_df['% Return'].iloc[-10:].tolist()


def get_means(returns_dict):
	means = []
	for ticker in returns_dict.keys():
		means.append(np.mean(returns_dict[ticker]))
	return means

def get_std_dev(returns_dict):
	std_dev = []
	for ticker in returns_dict.keys():
		std_dev.append(np.std(returns_dict[ticker]))
	return std_dev

def get_covariance_matrix(returns_dict):
	values = []
	for ticker in returns_dict.keys():
		values.append(returns_dict[ticker]) #10 days of returns (10x100)
	return np.cov(values) #(100x100 matrix)


def calculate_weights(m, cov):
	u = np.ones(len(m))

	inv_cov = np.linalg.inv(cov)

	u_C = np.dot(u, inv_cov)

	w = u_C / (np.dot(u_C, u.transpose()))

	return w

if __name__ == "__main__":
	np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
	
	#Gathers ticker data
	tickers = get_tickers()
	returns_dict = {}
	
	for ticker in tickers:
		x = get_last_10_days(ticker)
		returns_dict[ticker] = x
	

	print("Finished gathering ticker data")


	#calculate mean return, standard deviation, and covariance matrix
	means = get_means(returns_dict)
	std_dev = get_std_dev(returns_dict)
	c = get_covariance_matrix(returns_dict)
	
	#calculate weights
	weights = calculate_weights(means, c)
	
	account1 = Account('PKZGH5RC8V75XJAUR8DF','mzAaDSHaEhlTOMZ7jArrvSz4OKpkB1QEa5JEsXSb','https://paper-api.alpaca.markets')
	account_data = account1.get_account_data()
	
	valued_weights = account_data['current_equity'] * weights

	#print(account1.get_last_price("AAPL"))
	desired_port = {}
	for i in range(len(tickers)):		
		print(tickers[i])
		shares_to_get = math.floor(valued_weights[i] / account1.get_last_price(tickers[i]))
		desired_port[tickers[i]] = shares_to_get
		print(shares_to_get)

	current_port = account_data["current_portfolio"]

	desired_port_tickers = list(desired_port.keys())
	current_port_tickers = list(current_port.keys())

	first_time_buys = []
	for item in desired_port_tickers:
		if item not in current_port_tickers:
			first_time_buys.append(item)
			desired_port_tickers.remove(item)
	sell_all = []
	for item in current_port_tickers:
		if item not in desired_port_tickers:
			sell_all.append(item)
			current_port_tickers.remove(item)


	before_list = []
	after_list = []
 	
	for ticker in desired_port_tickers:
		if abs(desired_port[ticker]) < abs(int(current_port[ticker])):
			before_list.append(ticker)
		else:
			after_list.append(ticker)


	"""
	FROM HERE UNTIL LINE 136 IS HOW YOU MAKE SELL AND BUY ORDERS TO ALPACA
	account1 is defined in line 74, you need to do that too
	

	also pls excuse the messy code, i was trying to fix the buying power
	issue and not really worrying about style
	"""

	for ticker in before_list:
		print(ticker)
		if ticker in current_port:
			#find out current value and buy/sell based on that
			if int(current_port[ticker]) > desired_port[ticker]:
				# sell current - desired
				account1.place_order(ticker, int(current_port[ticker]) - desired_port[ticker], "sell")
			elif desired_port[ticker] > int(current_port[ticker]):
				account1.place_order(ticker, desired_port[ticker] - int(current_port[ticker]), "buy")
		else:
			# buy/sell
			side = "sell" if desired_port[ticker] < 0 else "buy"
			account1.place_order(ticker, abs(desired_port[ticker]), side)



	for ticker in after_list:
		print(ticker)

		if ticker in current_port:
			#find out current value and buy/sell based on that
			if int(current_port[ticker]) > desired_port[ticker]:
				# sell current - desired
				account1.place_order(ticker, int(current_port[ticker]) - desired_port[ticker], "sell")
			elif desired_port[ticker] > int(current_port[ticker]):
				account1.place_order(ticker, desired_port[ticker] - int(current_port[ticker]), "buy")
		else:
			# buy/sell
			side = "sell" if desired_port[ticker] < 0 else "buy"
			account1.place_order(ticker, abs(desired_port[ticker]), side)

	for ticker in sell_all:
		if current_port[ticker] > 0:
			account1.place_order(ticker, int(current_port[ticker]), "sell")
		else:
			account1.place_order(ticker, int(current_port[ticker]), "buy")

	for ticker in first_time_buys:
		if desired_port[ticker] > 0:
			account1.place_order(ticker, int(desired_port[ticker]), "buy")
		else:
			account1.place_order(ticker, int(desired_port[ticker]), "sell")

	







