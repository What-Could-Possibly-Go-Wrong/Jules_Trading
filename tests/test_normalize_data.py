import unittest
import os
import pandas as pd
from src.normalize_data import normalize_data

class TestNormalizeData(unittest.TestCase):

    def setUp(self):
        self.test_kurse_dir = "test_kurse"
        self.test_norm_dir = "test_normierte_kurse"
        self.ticker = "TEST"
        self.kurse_filepath = os.path.join(self.test_kurse_dir, f"{self.ticker}.csv")
        self.norm_filepath = os.path.join(self.test_norm_dir, f"{self.ticker}.csv")

        if not os.path.exists(self.test_kurse_dir):
            os.makedirs(self.test_kurse_dir)

        # Create a dummy data file
        data = {
            'Date': ['19991231', '20000103', '20000104'],
            'Open': [10, 20, 22],
            'High': [11, 21, 23],
            'Low': [9, 19, 21],
            'Close': [10, 20, 22],
            'Volume': [1000, 2000, 1500]
        }
        df = pd.DataFrame(data)
        df.to_csv(self.kurse_filepath, index=False)

    def tearDown(self):
        if os.path.exists(self.kurse_filepath):
            os.remove(self.kurse_filepath)
        if os.path.exists(self.norm_filepath):
            os.remove(self.norm_filepath)
        if os.path.exists(self.test_kurse_dir):
            os.rmdir(self.test_kurse_dir)
        if os.path.exists(self.test_norm_dir):
            os.rmdir(self.test_norm_dir)

    def test_normalize_data(self):
        normalize_data(directory=self.test_kurse_dir, output_directory=self.test_norm_dir)
        self.assertTrue(os.path.exists(self.norm_filepath))

        df = pd.read_csv(self.norm_filepath, index_col='Date')
        self.assertAlmostEqual(df.loc[20000103, 'Normalized Close'], 100.0)
        self.assertAlmostEqual(df.loc[20000104, 'Normalized Close'], 110.0)

if __name__ == '__main__':
    unittest.main()