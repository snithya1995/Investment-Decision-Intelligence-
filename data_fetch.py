# Import necessary libraries
import nt

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from data_validator import DataValidator
from technical_indicators import TechnicalIndicators
from risk_metrics import RiskMetrics

# Define a class to fetch stock data and company information
class StockDataFetcher:
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()

# Method to fetch historical stock data for a given number of years
    def fetch_historical_data(self, years: int = 10) -> pd.DataFrame:
        """
        Fetch historical stock data for given number of years.
        """
        end_date = datetime.today()
        start_date = end_date - timedelta(days=years * 365)

# Fetch historical data using yfinance
        stock = yf.Ticker(self.ticker)
        df = stock.history(start=start_date, end=end_date)

# Check if data is empty and raise an error if so
        if df.empty:
            raise ValueError(f"No data found for ticker {self.ticker}")

        df.reset_index(inplace=True)
        # Validate data
        if not DataValidator.validate_dataframe(df):
            print("Data validation warnings detected.")
        return df

# method to fetch company metadata
    def fetch_company_info(self) -> dict:
        """
        Fetch company metadata.
        """
        stock = yf.Ticker(self.ticker)
        return stock.info

# Call the main function to execute the code
if __name__ == "__main__":
    ticker = input("Enter ticker symbol: ")
    fetcher = StockDataFetcher(ticker)

    data = fetcher.fetch_historical_data()
    print(data.head())

    info = fetcher.fetch_company_info()
    print(f"\nCompany Name: {info.get('longName', 'N/A')}")

# Caluclate the technical indicators and print the results of CAGR
    data = TechnicalIndicators.add_daily_returns(data)
    data = TechnicalIndicators.add_moving_averages(data)
    data = TechnicalIndicators.add_rolling_volatility(data)

    cagr = TechnicalIndicators.calculate_cagr(data)
    print(f"\n10-Year CAGR: {cagr * 100:.2f}%")

    print(data.tail())

# Calculate risk metrics and print the results
sharpe = RiskMetrics.calculate_sharpe_ratio(data)
max_dd = RiskMetrics.calculate_max_drawdown(data)
beta = RiskMetrics.calculate_beta(data, ticker)

print(f"Sharpe Ratio: {sharpe}")
print(f"Max Drawdown: {max_dd * 100:.2f}%")
print(f"Beta vs S&P 500: {beta}")