import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the updated list of assets (tickers)
assets = [
    'AAPL', 'MSFT', 'GOOGL', 'JNJ', 'PFE', 'JPM', 'BAC', 'KO', 'PEP', 'XOM', 'CVX', 'GLD', 'USO', 'SLV', 
    'BTC-USD', 'ETH-USD', 'VNQ', '^TNX', 'LQD', 'AMZN', 'META', 'TSLA', 'BRK-B', 'V', 'WMT', 'PG', 'DIS', 
    'MA', 'NVDA', 'HD', 'PYPL', 'UNH', 'VZ', 'ADBE', 'NFLX', 'CMCSA', 'INTC', 'PFE', 'MRK', 'ABT', 'ABBV', 
    'T', 'PEP', 'KO', 'CSCO', 'XOM', 'CVX', 'NKE', 'MCD', 'MDT', 'HON', 'AMGN', 'BA', 'SBUX', 'CAT', 
    'IBM', 'MMM', 'GE', 'RTX', 'GS', 'USB', 'BLK', 'BK', 'SCHW', 'C', 'MS', 'BAC', 'WFC', 'AXP', 'SPGI', 
    'ADP', 'MSCI', 'ICE', 'TROW', 'COF', 'AFL', 'MET', 'PRU', 'LNC', 'VOO', 'IVV', 'SPY', 'IWM', 'VUG', 
    'VTV', 'QQQ', 'DIA', 'VOE', 'VBR', 'VB', 'MTUM', 'QUAL', 'VLUE', 'EFG', 'EFV', 'IEFA', 'IEMG', 'EEM', 
    'SPYX', 'ICLN', 'COST', 'ORCL', 'ACN', 'CRM', 'TXN', 'AVGO', 'QCOM'
]

# Define asset classes
asset_classes = {
    'Stocks': ['AAPL', 'MSFT', 'GOOGL', 'JNJ', 'PFE', 'JPM', 'BAC', 'KO', 'PEP', 'XOM', 'CVX', 'AMZN', 'META', 
               'TSLA', 'BRK-B', 'V', 'WMT', 'PG', 'DIS', 'MA', 'NVDA', 'HD', 'PYPL', 'UNH', 'VZ', 'ADBE', 
               'NFLX', 'CMCSA', 'INTC', 'MRK', 'ABT', 'ABBV', 'T', 'CSCO', 'NKE', 'MCD', 'MDT', 'HON', 
               'AMGN', 'BA', 'SBUX', 'CAT', 'IBM', 'MMM', 'GE', 'RTX', 'GS', 'USB', 'BLK', 'BK', 'SCHW', 
               'C', 'MS', 'WFC', 'AXP', 'SPGI', 'ADP', 'MSCI', 'ICE', 'TROW', 'COF', 'AFL', 'MET', 'PRU', 
               'LNC', 'COST', 'ORCL', 'ACN', 'CRM', 'TXN', 'AVGO', 'QCOM'],
    'ETFs': ['VOO', 'IVV', 'SPY', 'IWM', 'VUG', 'VTV', 'QQQ', 'DIA', 'VOE', 'VBR', 'VB', 'MTUM', 'QUAL', 'VLUE', 
             'EFG', 'EFV', 'IEFA', 'IEMG', 'EEM', 'SPYX', 'ICLN'],
    'Commodities': ['GLD', 'USO', 'SLV'],
    'Cryptocurrencies': ['BTC-USD', 'ETH-USD'],
    'Bonds': ['LQD'],
    'Indices': ['^TNX'],
    'Real Estate': ['VNQ']
}

# Define the time period
start_date = '2015-01-01'
end_date = '2023-12-31'

# Create an empty dictionary to store the data
price_data = {}

# Fetch historical price data for each asset
for asset in assets:
    ticker = yf.Ticker(asset)
    try:
        price_data[asset] = ticker.history(start=start_date, end=end_date)['Close']
    except Exception as e:
        print(f"Could not retrieve data for {asset}: {e}")

# Convert the dictionary to a DataFrame
price_df = pd.DataFrame(price_data)

# Save the DataFrame to a CSV file
price_df.to_csv('historical_prices2.csv')

# Create a color mapping for the asset classes
colors = {
    'Stocks': 'blue',
    'ETFs': 'green',
    'Commodities': 'orange',
    'Cryptocurrencies': 'red',
    'Bonds': 'purple',
    'Indices': 'brown',
    'Real Estate': 'pink'
}

# Plot the data
plt.figure(figsize=(14, 10))

for asset, data in price_data.items():
    for asset_class, assets_list in asset_classes.items():
        if asset in assets_list:
            plt.plot(data.index, data, label=asset, color=colors[asset_class], alpha=0.6)
            break

plt.legend()
plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Historical Prices of Assets')
plt.show()
