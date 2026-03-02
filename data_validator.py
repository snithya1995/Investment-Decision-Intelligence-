import pandas as pd

class DataValidator:

    @staticmethod
    def check_missing_values(df: pd.DataFrame) -> bool:
        """
        Check if dataframe contains missing values.
        """
        missing = df.isnull().sum().sum()
        if missing > 0:
            print(f"Warning: Dataset contains {missing} missing values.")
            return False
        return True

    @staticmethod
    def check_date_continuity(df: pd.DataFrame) -> bool:
        """
        Ensure date column is continuous (no large gaps).
        """
        if "Date" not in df.columns:
            raise ValueError("Date column not found.")

        df_sorted = df.sort_values("Date")
        date_diff = df_sorted["Date"].diff().dt.days

        # Allow weekends (max 3 days gap)
        if date_diff.max() > 5:
            print("Warning: Large gaps detected in date continuity.")
            return False

        return True

    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> bool:
        """
        Run all validation checks.
        """
        checks = [
            DataValidator.check_missing_values(df),
            DataValidator.check_date_continuity(df)
        ]

        return all(checks)