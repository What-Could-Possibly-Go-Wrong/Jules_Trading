import unittest
import os
import pandas as pd
from src.calculate_indicators import calculate_moving_averages

class TestCalculateIndicators(unittest.TestCase):

    def setUp(self):
        self.test_norm_dir = "test_normierte_kurse"
        self.test_ind_dir = "test_indikatoren"
        self.ticker = "TEST"
        self.norm_filepath = os.path.join(self.test_norm_dir, f"{self.ticker}.csv")
        self.ind_filepath = os.path.join(self.test_ind_dir, f"{self.ticker}.csv")

        if not os.path.exists(self.test_norm_dir):
            os.makedirs(self.test_norm_dir)

        # Create a dummy normalized data file
        dates = pd.to_datetime(pd.date_range(start='2023-01-01', periods=120)).strftime('%Y%m%d')
        data = {
            'Date': dates,
            'Normalized Close': [100 + i for i in range(120)],
        }
        df = pd.DataFrame(data)
        df.to_csv(self.norm_filepath, index=False)

    def tearDown(self):
        if os.path.exists(self.norm_filepath):
            os.remove(self.norm_filepath)
        if os.path.exists(self.ind_filepath):
            os.remove(self.ind_filepath)
        if os.path.exists(self.test_norm_dir):
            os.rmdir(self.test_norm_dir)
        if os.path.exists(self.test_ind_dir):
            os.rmdir(self.test_ind_dir)

    def test_calculate_moving_averages(self):
        calculate_moving_averages(directory=self.test_norm_dir, output_directory=self.test_ind_dir)
        self.assertTrue(os.path.exists(self.ind_filepath))

        df = pd.read_csv(self.ind_filepath, index_col='Date')

        # Check that the first 19 values of MA20 are NaN
        self.assertTrue(df['MA20'].iloc[:19].isnull().all())
        # Check a calculated value for MA20
        self.assertAlmostEqual(df['MA20'].iloc[19], 109.5)

        # Check that the first 99 values of MA100 are NaN
        self.assertTrue(df['MA100'].iloc[:99].isnull().all())
        # Check a calculated value for MA100
        self.assertAlmostEqual(df['MA100'].iloc[99], 149.5)


if __name__ == '__main__':
    unittest.main()