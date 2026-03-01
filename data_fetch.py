import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class StockDataFetcher:
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()

    def fetch_historical_data(self, years: int = 10) -> pd.DataFrame:
        """
        Fetch historical stock data for given number of years.
        """
        end_date = datetime.today()
        start_date = end_date - timedelta(days=years * 365)

        stock = yf.Ticker(self.ticker)
        df = stock.history(start=start_date, end=end_date)

        if df.empty:
            raise ValueError(f"No data found for ticker {self.ticker}")

        df.reset_index(inplace=True)
        return df

    def fetch_company_info(self) -> dict:
        """
        Fetch company metadata.
        """
        stock = yf.Ticker(self.ticker)
        return stock.info


if __name__ == "__main__":
    ticker = input("Enter ticker symbol: ")
    fetcher = StockDataFetcher(ticker)

    data = fetcher.fetch_historical_data()
    print(data.head())

    info = fetcher.fetch_company_info()
    print(f"\nCompany Name: {info.get('longName', 'N/A')}")