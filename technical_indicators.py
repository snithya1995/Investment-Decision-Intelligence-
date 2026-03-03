import pandas as pd
import numpy as np


class TechnicalIndicators:

    @staticmethod
    def add_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
        df["Daily_Return"] = df["Close"].pct_change()
        return df

    @staticmethod
    def add_moving_averages(df: pd.DataFrame, short_window=50, long_window=200) -> pd.DataFrame:
        df[f"MA_{short_window}"] = df["Close"].rolling(window=short_window).mean()
        df[f"MA_{long_window}"] = df["Close"].rolling(window=long_window).mean()
        return df

    @staticmethod
    def add_rolling_volatility(df: pd.DataFrame, window=30) -> pd.DataFrame:
        df["Rolling_Volatility"] = df["Daily_Return"].rolling(window=window).std() * np.sqrt(252)
        return df

    @staticmethod
    def calculate_cagr(df: pd.DataFrame) -> float:
        """
        Calculate Compound Annual Growth Rate (CAGR)
        """
        start_price = df["Close"].iloc[0]
        end_price = df["Close"].iloc[-1]
        years = (df["Date"].iloc[-1] - df["Date"].iloc[0]).days / 365.25

        cagr = (end_price / start_price) ** (1 / years) - 1
        return round(cagr, 4)