import alpaca_trade_api as tradeapi

class Account:
    def __init__ (self, apikey, secret, endpoint) :
        self.api = tradeapi.REST(
    	    apikey,
    	    secret,
    	    endpoint
        )
        self.account = self.api.get_account()

    def trade_api_call(self, apikey, secret, endpoint) :
        self.api = tradeapi.REST(
    	    apikey,
    	    secret,
    	    endpoint
        )
        self.account = self.api.get_account()
    
    def get_account_data(self):
        # Check if our account is restricted from trading.
        if self.account.trading_blocked:
    	    print('Account is currently restricted from trading.')

        # Check our current balance
        equity = float(self.account.equity)
        #print(f'Today\'s portfolio balance: ${equity}')

        # Check our current balance
        buying_power = float(self.account.buying_power)
        #print(f'Today\'s portfolio buying power: ${buying_power}')

        # Get a list of all of our positions.
        portfolio = self.api.list_positions()
        portfolio_dict = {}

        # Current positions
        for position in portfolio:
            #print("{} shares of {}".format(position.qty, position.symbol))
            portfolio_dict[position.symbol] = position.qty

        return {'current_equity': equity, 'current_buying_power': buying_power, 'current_portfolio': portfolio_dict}
    
    def get_day_portfolio_value(self):
        # Check if our account is restricted from trading.
        if self.account.trading_blocked:
    	    print('Account is currently restricted from trading.')

        # get portfolio information for one day, collected every hour
        entity = self.api.get_portfolio_history(period='1D', timeframe='1H')

        equity_dict = entity['equity']
        return equity_dict

    def get_week_portfolio_value(self):
        # Check if our account is restricted from trading.
        if self.account.trading_blocked:
    	    print('Account is currently restricted from trading.')

        # get portfolio information for one week, collected every day
        entity = self.api.get_portfolio_history(period='1W', timeframe='1D')

        equity_dict = entity['equity']
        return equity_dict

    def get_month_portfolio_value(self):
        # Check if our account is restricted from trading.
        if self.account.trading_blocked:
    	    print('Account is currently restricted from trading.')

        # get portfolio information for one month, collected every day
        entity = self.api.get_portfolio_history(period='1M', timeframe='1D')

        equity_dict = entity['equity']
        return equity_dict

    def get_current_portfolio_value(self):
        # Check if our account is restricted from trading.
        if self.account.trading_blocked:
    	    print('Account is currently restricted from trading.')

        # get current portfolio information
        entity = get_account_data()
        
        portfolio_dict = entity['current_portfolio']
        equity = entity['current_equity']

        return {equity, portfolio_dict}

    def place_order(self, symbol, qty, side):
        try :
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type='market',
                time_in_force='gtc'
            )
            return order.status
        except:
            return 'Order failed :('
    

if __name__ == '__main__':
    """
    With the Alpaca API, you can check on your daily profit or loss by
    comparing your current balance to yesterday's balance.
    """
    account1 = Account('PKWF08ICZ03US484CPSY','k6cdNDXVzslHxjXeRW1dKLuP3QzaiytVgdrstOFq','https://paper-api.alpaca.markets')
    print(account1.get_account_data())
    print(account1.place_order('AAPL', 1, 'buy'))
    print(account1.place_order('APL', 1, 'buy'))
    
    

    

