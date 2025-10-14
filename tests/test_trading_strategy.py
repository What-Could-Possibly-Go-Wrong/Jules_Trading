import unittest
import os
import pandas as pd
from src.trading_strategy import run_gld_20_100_strategy

class TestTradingStrategy(unittest.TestCase):

    def setUp(self):
        self.test_kurse_dir = "test_kurse"
        self.test_ind_dir = "test_indikatoren"
        self.test_trading_dir = "test_trading"
        self.ticker = "TEST"
        self.kurse_filepath = os.path.join(self.test_kurse_dir, f"{self.ticker}.csv")
        self.ind_filepath = os.path.join(self.test_ind_dir, f"{self.ticker}.csv")
        self.tradelog_filepath = os.path.join(self.test_trading_dir, f"{self.ticker}_tradelog.txt")
        self.kpi_filepath = os.path.join(self.test_trading_dir, f"{self.ticker}_kpis.txt")

        for d in [self.test_kurse_dir, self.test_ind_dir, self.test_trading_dir]:
            if not os.path.exists(d):
                os.makedirs(d)

        # Create dummy data files with a crossover event
        dates = pd.to_datetime(pd.date_range(start='2023-01-01', periods=120)).strftime('%Y%m%d')
        kurse_data = {
            'Date': dates,
            'Open': [100 + i for i in range(120)],
            'High': [102 + i for i in range(120)],
            'Low': [98 + i for i in range(120)],
            'Close': [101 + i for i in range(120)],
            'Volume': [1000] * 120
        }
        pd.DataFrame(kurse_data).to_csv(self.kurse_filepath, index=False)

        ma20 = [80 + i for i in range(60)] + [140 - i for i in range(60)]
        ma100 = [90 for i in range(120)]
        indikatoren_data = {
            'Date': dates,
            'MA20': ma20,
            'MA100': ma100
        }
        pd.DataFrame(indikatoren_data).to_csv(self.ind_filepath, index=False)


    def tearDown(self):
        for f in [self.kurse_filepath, self.ind_filepath, self.tradelog_filepath, self.kpi_filepath]:
            if os.path.exists(f):
                os.remove(f)
        for d in [self.test_kurse_dir, self.test_ind_dir, self.test_trading_dir]:
            if os.path.exists(d) and not os.listdir(d):
                os.rmdir(d)

    def test_run_gld_20_100_strategy(self):
        run_gld_20_100_strategy(self.ticker, kurse_dir=self.test_kurse_dir, indikatoren_dir=self.test_ind_dir, trading_dir=self.test_trading_dir)
        self.assertTrue(os.path.exists(self.tradelog_filepath))
        self.assertTrue(os.path.exists(self.kpi_filepath))

        with open(self.tradelog_filepath, 'r') as f:
            log = f.read()
            self.assertIn("BUY", log)
            self.assertIn("SELL", log)

if __name__ == '__main__':
    unittest.main()