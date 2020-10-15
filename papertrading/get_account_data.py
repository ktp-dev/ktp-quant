import alpaca_trade_api as tradeapi

def get_account_data():
	# First, open the API connection
    api = tradeapi.REST(
    	'sample_API_key',
    	'sample_API_key',
    	'https://paper-api.alpaca.markets'
    )

    # Get account info
    account = api.get_account()

    # Check if our account is restricted from trading.
    if account.trading_blocked:
    	print('Account is currently restricted from trading.')

    # Check our current balance
    equity = float(account.equity)
    #print(f'Today\'s portfolio balance: ${equity}')


    # Check our current balance
    buying_power = float(account.buying_power)
    #print(f'Today\'s portfolio buying power: ${buying_power}')

    # Get a list of all of our positions.
    portfolio = api.list_positions()
    portfolio_dict = {}

    # Current positions
    for position in portfolio:
        #print("{} shares of {}".format(position.qty, position.symbol))
        portfolio_dict[position.symbol] = position.qty

    return {'current_equity': equity, 'current_buying_power': buying_power, 'current_portfolio': portfolio_dict}

if __name__ == '__main__':
    """
    With the Alpaca API, you can check on your daily profit or loss by
    comparing your current balance to yesterday's balance.
    """
    get_account_data()

    

