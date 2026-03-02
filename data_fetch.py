# Import necessary libraries
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

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