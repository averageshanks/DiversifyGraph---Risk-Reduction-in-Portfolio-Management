import yfinance as yf
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Define the list of assets (tickers)
assets = [
    'AAPL', 'MSFT', 'GOOGL', 'JNJ', 'PFE', 'JPM', 'BAC', 'KO', 'PEP', 'XOM', 'CVX', 'GLD', 'USO', 'SLV', 
    'BTC-USD', 'ETH-USD', 'VNQ', '^TNX', 'LQD', 'AMZN', 'META', 'TSLA', 'BRK-B', 'V', 'WMT', 'PG', 'DIS', 
    'MA', 'NVDA', 'HD', 'PYPL', 'UNH', 'VZ', 'ADBE', 'NFLX', 'CMCSA', 'INTC', 'MRK', 'ABT', 'ABBV', 
    'T', 'CSCO', 'NKE', 'MCD', 'MDT', 'HON', 'AMGN', 'BA', 'SBUX', 'CAT', 'IBM', 'MMM', 'GE', 'RTX', 
    'GS', 'USB', 'BLK', 'BK', 'SCHW', 'C', 'MS', 'WFC', 'AXP', 'SPGI', 'ADP', 'MSCI', 'ICE', 'TROW', 
    'COF', 'AFL', 'MET', 'PRU', 'LNC', 'COST', 'ORCL', 'ACN', 'CRM', 'TXN', 'AVGO', 'QCOM'
]

# Create an empty list to store the fundamental data
fundamental_data = []

# Fetch fundamental data for each asset
for asset in assets:
    try:
        ticker = yf.Ticker(asset)
        info = ticker.info
        data = {
            'symbol': asset,
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
            'dividend_yield': info.get('dividendYield'),
            'enterprise_value': info.get('enterpriseValue'),
            'enterprise_to_revenue': info.get('enterpriseToRevenue'),
            'enterprise_to_ebitda': info.get('enterpriseToEbitda'),
            '52_week_high': info.get('fiftyTwoWeekHigh'),
            '52_week_low': info.get('fiftyTwoWeekLow'),
            'profit_margin': info.get('profitMargins'),
            'operating_margin': info.get('operatingMargins'),
            'return_on_assets': info.get('returnOnAssets'),
            'return_on_equity': info.get('returnOnEquity'),
            'revenue': info.get('totalRevenue'),
            'revenue_per_share': info.get('revenuePerShare'),
            'quarterly_revenue_growth': info.get('quarterlyRevenueGrowth'),
            'gross_profit': info.get('grossProfits'),
            'ebitda': info.get('ebitda'),
            'net_income_to_common': info.get('netIncomeToCommon'),
            'trailing_eps': info.get('trailingEps'),
            'forward_eps': info.get('forwardEps'),
            'peg_ratio': info.get('pegRatio'),
            'price_to_sales': info.get('priceToSalesTrailing12Months'),
            'price_to_book': info.get('priceToBook'),
            'forward_pe': info.get('forwardPE'),
            'beta': info.get('beta'),
            'book_value': info.get('bookValue'),
            'shares_outstanding': info.get('sharesOutstanding'),
            'float_shares': info.get('floatShares'),
            'shares_short': info.get('sharesShort'),
            'short_ratio': info.get('shortRatio'),
            'short_percent_of_float': info.get('shortPercentOfFloat'),
            'held_by_insiders': info.get('heldPercentInsiders'),
            'held_by_institutions': info.get('heldPercentInstitutions'),
            'short_percent_of_shares_outstanding': info.get('shortPercentOfSharesOutstanding'),
            'shares_short_prior_month': info.get('sharesShortPriorMonth'),
            'forward_annual_dividend_rate': info.get('dividendRate'),
            'forward_annual_dividend_yield': info.get('dividendYield'),
            'payout_ratio': info.get('payoutRatio'),
            'dividend_growth': info.get('dividendGrowth'),
            'five_year_avg_dividend_yield': info.get('fiveYearAvgDividendYield'),
            'beta3_year': info.get('beta3Year'),
            'total_cash': info.get('totalCash'),
            'total_cash_per_share': info.get('totalCashPerShare'),
            'total_debt': info.get('totalDebt'),
            'total_debt_to_equity': info.get('debtToEquity'),
            'current_ratio': info.get('currentRatio'),
            'quick_ratio': info.get('quickRatio'),
            'operating_cash_flow': info.get('operatingCashflow'),
            'levered_free_cash_flow': info.get('leveredFreeCashflow')
        }
        fundamental_data.append(data)
    except Exception as e:
        print(f"Could not retrieve data for {asset}: {e}")

# Convert the list to a DataFrame
fundamental_df = pd.DataFrame(fundamental_data)

# Save the raw fundamental data to a CSV file
fundamental_df.to_csv('raw_fundamental_data1.csv', index=False)

# Normalize the numerical columns
numeric_columns = fundamental_df.select_dtypes(include=['float64', 'int64']).columns
scaler = StandardScaler()
fundamental_df[numeric_columns] = scaler.fit_transform(fundamental_df[numeric_columns])

# Save the normalized data to a CSV file
fundamental_df.to_csv('normalized_fundamental_data1.csv', index=False)

print("Fundamental data has been saved to 'normalized_fundamental_data.csv'")
