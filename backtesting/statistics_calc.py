import numpy as np
from scipy import stats

def calculate_statistics(data, prices = False):
	#if the data is prices, convert to returns instead
	returns = []
	if prices:
		for i in range(len(data)-1):
			returns.append((data[i+1] - data[i])/data[i])
	else:
		returns = data

	er = np.mean(returns)
	std = stats.tstd(returns)/10.0

	return er, std
