import pandas as pd
import numpy as np
import yfinance as yf


class RiskMetrics:

    @staticmethod
    def calculate_sharpe_ratio(df: pd.DataFrame, risk_free_rate=0.02) -> float:
        """
        Calculate annualized Sharpe Ratio.
        """
        daily_return = df["Daily_Return"].dropna()
        excess_return = daily_return - (risk_free_rate / 252)

        sharpe_ratio = np.sqrt(252) * (excess_return.mean() / excess_return.std())
        return round(sharpe_ratio, 4)

    @staticmethod
    def calculate_max_drawdown(df: pd.DataFrame) -> float:
        """
        Calculate Maximum Drawdown.
        """
        cumulative_returns = (1 + df["Daily_Return"].fillna(0)).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak

        max_drawdown = drawdown.min()
        return round(max_drawdown, 4)

    @staticmethod
    def calculate_beta(df: pd.DataFrame, ticker: str) -> float:
        """
        Calculate Beta against S&P 500 (^GSPC).
        """
        market = yf.Ticker("^GSPC")
        market_data = market.history(period="10y")

        market_data["Market_Return"] = market_data["Close"].pct_change()

        merged = pd.merge(
            df[["Date", "Daily_Return"]],
            market_data[["Market_Return"]],
            left_on="Date",
            right_index=True,
            how="inner"
        )
        clean = merged[["Daily_Return", "Market_Return"]].dropna()
        covariance = np.cov(clean["Daily_Return"], clean["Market_Return"])[0][1]
        
        market_variance = np.var(merged["Market_Return"].dropna())

        beta = covariance / market_variance
        return round(beta, 4)