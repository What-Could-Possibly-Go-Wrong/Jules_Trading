import yfinance as yf
import os
import pandas as pd
import argparse
import time
from datetime import datetime, date

def read_tickers(filename):
    """Reads tickers from a file."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def download_data(ticker, start_date="2000-01-01", end_date=None, directory="Kurse"):
    """Downloads historical data for a single ticker and saves it as a CSV."""
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, f"{ticker}.csv")

    today = date.today()

    if os.path.exists(filepath):
        existing_data = pd.read_csv(filepath, index_col='Date')
        existing_data.index = pd.to_datetime(existing_data.index, format='%Y%m%d').date
        last_date = existing_data.index.max()

        if last_date >= today - pd.Timedelta(days=1):
            print(f"Data for {ticker} is already up to date.")
            return True

        start_date_dt = last_date + pd.Timedelta(days=1)
        start_date_str = start_date_dt.strftime('%Y-%m-%d')

        print(f"Updating data for {ticker} from {start_date_str}")

        try:
            new_data = yf.download(ticker, start=start_date_str, end=end_date, progress=False, auto_adjust=True)
            if not new_data.empty:
                new_data.index = new_data.index.strftime('%Y%m%d')
                new_data.to_csv(filepath, mode='a', header=False)
                print(f"Updated data for {ticker}")
        except Exception as e:
            print(f"Could not update data for {ticker}: {e}")
            return False
    else:
        print(f"Downloading data for {ticker} from {start_date}")
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
            if not data.empty:
                data.index.name = 'Date'
                data.index = data.index.strftime('%Y%m%d')
                data.to_csv(filepath)
                print(f"Saved data for {ticker}")
            else:
                print(f"No data found for {ticker}")
                return False
        except Exception as e:
            print(f"Could not download data for {ticker}: {e}")
            return False

    return True

def main():
    parser = argparse.ArgumentParser(description="Download historical stock data.")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging.')
    args = parser.parse_args()

    if args.debug:
        print("Debug mode enabled.")

    ticker_files = ["Ticker/sp500.txt", "Ticker/dax.txt"]
    all_tickers = []
    for ticker_file in ticker_files:
        tickers = read_tickers(ticker_file)
        all_tickers.extend(tickers[:5]) # Limit to 5 tickers per file

    failed_tickers = []

    end_date = datetime.now().strftime('%Y-%m-%d')

    for ticker in all_tickers:
        if not download_data(ticker, end_date=end_date):
            failed_tickers.append(ticker)
            if args.debug:
                with open("debug.txt", "a") as f:
                    f.write(f"Failed to download or update data for {ticker}\n")
        time.sleep(1)

    if failed_tickers:
        print("\nFailed to download data for the following tickers:")
        for ticker in failed_tickers:
            print(ticker)

if __name__ == "__main__":
    main()