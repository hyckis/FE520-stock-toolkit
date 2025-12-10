import unittest

import pandas as pd

from stocktoolkit.data import (
    download_price_data,
    download_multiple_price_data,
    get_close_price,
    resample_price,
)
from stocktoolkit.validation import validate_price_dataframe


class TestDataModule(unittest.TestCase):
    # ---------- download_price_data ----------

    def test_download_price_data_valid(self):
        df = download_price_data("AAPL", "2024-01-01", "2024-01-31")
        # Should return non-empty DataFrame with a DateTimeIndex
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertTrue(isinstance(df.index, pd.DatetimeIndex))

    def test_download_price_data_invalid_date(self):
        # Incorrect date format should raise ValueError (from validation)
        with self.assertRaises(ValueError):
            download_price_data("AAPL", "2024-13-01", "2024-01-31")

    def test_download_price_data_invalid_range(self):
        # End date before start date usually returns empty df -> validate_price_dataframe fails
        with self.assertRaises(ValueError):
            download_price_data("AAPL", "2024-02-01", "2024-01-01")

    # ---------- download_multiple_price_data ----------

    def test_download_multiple_price_data_valid(self):
        symbols = ["aapl", " msft "]
        data_dict = download_multiple_price_data(symbols, "2024-01-01", "2024-01-31")
        # Should have keys for both symbols, normalized to upper-case
        self.assertIn("AAPL", data_dict)
        self.assertIn("MSFT", data_dict)
        self.assertIsInstance(data_dict["AAPL"], pd.DataFrame)
        self.assertFalse(data_dict["AAPL"].empty)

    def test_download_multiple_price_data_invalid_dates(self):
        with self.assertRaises(ValueError):
            download_multiple_price_data(["AAPL", "MSFT"], "2024-13-01", "2024-01-31")

    # ---------- get_close_price ----------

    def test_get_close_price_prefers_adj_close(self):
        # Construct a small fake DataFrame with both 'Adj Close' and 'Close'
        idx = pd.date_range("2024-01-01", periods=3, freq="D")
        df = pd.DataFrame(
            {
                "Adj Close": [10.0, 10.5, 11.0],
                "Close": [9.0, 9.5, 10.0],
            },
            index=idx,
        )
        series = get_close_price(df, use_adjusted=True)
        self.assertTrue((series.values == [10.0, 10.5, 11.0]).all())
        self.assertEqual(series.name, "Close")

    def test_get_close_price_uses_close_if_no_adj(self):
        idx = pd.date_range("2024-01-01", periods=3, freq="D")
        df = pd.DataFrame(
            {
                "Close": [9.0, 9.5, 10.0],
            },
            index=idx,
        )
        series = get_close_price(df, use_adjusted=True)
        self.assertTrue((series.values == [9.0, 9.5, 10.0]).all())

    def test_get_close_price_raises_if_no_close_cols(self):
        idx = pd.date_range("2024-01-01", periods=3, freq="D")
        df = pd.DataFrame(
            {
                "Open": [9.0, 9.5, 10.0],
            },
            index=idx,
        )
        with self.assertRaises(ValueError):
            get_close_price(df, use_adjusted=True)

    # ---------- resample_price ----------

    def test_resample_price_last(self):
        idx = pd.date_range("2024-01-01", periods=5, freq="D")
        df = pd.DataFrame({"Close": [1, 2, 3, 4, 5]}, index=idx)

        weekly = resample_price(df, freq="W", how="last")
        self.assertIsInstance(weekly, pd.DataFrame)
        self.assertFalse(weekly.empty)

    def test_resample_price_first(self):
        idx = pd.date_range("2024-01-01", periods=5, freq="D")
        df = pd.DataFrame({"Close": [1, 2, 3, 4, 5]}, index=idx)

        weekly = resample_price(df, freq="W", how="FIRST")  # case-insensitive
        self.assertIsInstance(weekly, pd.DataFrame)
        self.assertFalse(weekly.empty)

    def test_resample_price_mean(self):
        idx = pd.date_range("2024-01-01", periods=5, freq="D")
        df = pd.DataFrame({"Close": [1, 2, 3, 4, 5]}, index=idx)

        weekly = resample_price(df, freq="W", how="mean")
        self.assertIsInstance(weekly, pd.DataFrame)
        self.assertFalse(weekly.empty)

    def test_resample_price_invalid_how(self):
        idx = pd.date_range("2024-01-01", periods=5, freq="D")
        df = pd.DataFrame({"Close": [1, 2, 3, 4, 5]}, index=idx)

        with self.assertRaises(ValueError):
            resample_price(df, freq="W", how="median")


if __name__ == "__main__":
    unittest.main()
