import unittest
import os
from src.download_tickers import get_sp500_tickers, get_dax_tickers, save_tickers

class TestDownloadTickers(unittest.TestCase):

    def test_get_sp500_tickers(self):
        tickers = get_sp500_tickers()
        self.assertGreater(len(tickers), 500)
        self.assertIn("AAPL", tickers)
        self.assertIn("MSFT", tickers)
        # Check for correct replacement of '.'
        self.assertIn("BRK-B", tickers)

    def test_get_dax_tickers(self):
        tickers = get_dax_tickers()
        self.assertGreaterEqual(len(tickers), 40)
        self.assertIn("ADS.DE", tickers)
        self.assertIn("VOW3.DE", tickers)

    def test_save_tickers(self):
        tickers = ["TEST1", "TEST2", "TEST3"]
        directory = "test_tickers"
        filename = "test.txt"
        filepath = os.path.join(directory, filename)

        save_tickers(tickers, filename, directory=directory)

        self.assertTrue(os.path.exists(filepath))

        with open(filepath, 'r') as f:
            saved_tickers = [line.strip() for line in f]

        self.assertEqual(tickers, saved_tickers)

        # Clean up
        os.remove(filepath)
        os.rmdir(directory)

if __name__ == '__main__':
    unittest.main()