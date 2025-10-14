import unittest
import os
import pandas as pd
from src.download_data import download_data, read_tickers
from datetime import datetime

class TestDownloadData(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_data"
        self.ticker = "AAPL" # Use a real ticker for testing download
        self.filepath = os.path.join(self.test_dir, f"{self.ticker}.csv")

        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_download_data_new(self):
        # Test downloading data for a new ticker
        self.assertTrue(download_data(self.ticker, directory=self.test_dir, end_date="2023-01-05"))
        self.assertTrue(os.path.exists(self.filepath))
        df = pd.read_csv(self.filepath)
        self.assertGreater(len(df), 0)

    def test_download_data_update(self):
        # Test updating existing data
        # Create a dummy file
        initial_data = {
            'Date': ['20221230'],
            'Open': [100],
            'High': [101],
            'Low': [99],
            'Close': [100.5],
            'Volume': [1000]
        }
        initial_df = pd.DataFrame(initial_data)
        initial_df.to_csv(self.filepath, index=False)

        self.assertTrue(download_data(self.ticker, directory=self.test_dir, end_date="2023-01-05"))

        df = pd.read_csv(self.filepath)
        self.assertGreater(len(df), 1)
        self.assertEqual(df.iloc[0]['Date'], 20221230)

    def test_read_tickers(self):
        # Test reading tickers from a file
        ticker_file = "test_tickers.txt"
        tickers = ["T1", "T2", "T3"]
        with open(ticker_file, 'w') as f:
            for t in tickers:
                f.write(f"{t}\n")

        read_tickers_list = read_tickers(ticker_file)
        self.assertEqual(tickers, read_tickers_list)
        os.remove(ticker_file)

if __name__ == '__main__':
    unittest.main()